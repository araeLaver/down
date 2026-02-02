import subprocess
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import func

from services.db import Session
from services.git_utils import repo
from database_setup import (
    ActivityLog, SyncLog, CompanyMetric, SCHEMA_NAME
)
from sqlalchemy import text
from business_discovery_history import BusinessDiscoveryHistory, BusinessAnalysisSnapshot

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/api/sync/control', methods=['POST'])
def sync_control():
    """동기화 제어 API"""
    action = request.json.get('action')

    if action not in ['start', 'stop', 'restart', 'sync']:
        return jsonify({'error': 'Invalid action'}), 400

    session = Session()
    try:
        result = subprocess.run(['./sync-control.sh', action],
                              capture_output=True, text=True)

        activity = ActivityLog(
            activity_type='sync_control',
            description=f'Sync daemon {action}',
            details={'output': result.stdout},
            status='success' if result.returncode == 0 else 'error'
        )
        session.add(activity)
        session.commit()

        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@admin_bp.route('/api/metrics')
def api_metrics():
    """회사 성장 지표 API"""
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    session = Session()
    try:
        metrics = session.query(CompanyMetric).filter(
            CompanyMetric.date >= thirty_days_ago
        ).all()

        daily_commits = {}
        if repo:
            for commit in repo.iter_commits():
                date = datetime.fromtimestamp(commit.committed_date).date()
                if date >= thirty_days_ago.date():
                    date_str = date.isoformat()
                    daily_commits[date_str] = daily_commits.get(date_str, 0) + 1

        result = session.execute(text(f"""
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM {SCHEMA_NAME}.sync_logs
            WHERE timestamp >= :thirty_days_ago
            GROUP BY DATE(timestamp)
        """), {'thirty_days_ago': thirty_days_ago})

        daily_syncs = {}
        for row in result:
            daily_syncs[row.date.isoformat()] = row.count

        return jsonify({
            'daily_commits': daily_commits,
            'daily_syncs': daily_syncs,
            'custom_metrics': [
                {
                    'date': m.date.isoformat(),
                    'name': m.metric_name,
                    'value': m.value,
                    'unit': m.unit
                } for m in metrics
            ]
        })
    finally:
        session.close()


@admin_bp.route('/api/record', methods=['POST'])
def record_activity():
    """활동 기록 API"""
    data = request.json

    session = Session()
    try:
        activity = ActivityLog(
            activity_type=data.get('type', 'manual'),
            description=data.get('description'),
            details=data.get('details'),
            status=data.get('status', 'info')
        )

        session.add(activity)
        session.commit()

        return jsonify({'success': True, 'id': activity.id})
    finally:
        session.close()


@admin_bp.route('/api/cleanup/old-data', methods=['POST'])
def api_cleanup_old_data():
    """오래된 데이터 정리 (DB 비용 최적화)"""
    session = Session()
    try:
        cleanup_results = {}
        now = datetime.now()

        try:
            cutoff_30days = now - timedelta(days=30)
            deleted_activity = session.query(ActivityLog).filter(
                ActivityLog.timestamp < cutoff_30days
            ).delete(synchronize_session=False)
            cleanup_results['activity_logs'] = deleted_activity
        except Exception as e:
            cleanup_results['activity_logs'] = f'error: {str(e)}'

        try:
            deleted_sync = session.query(SyncLog).filter(
                SyncLog.timestamp < cutoff_30days
            ).delete(synchronize_session=False)
            cleanup_results['sync_logs'] = deleted_sync
        except Exception as e:
            cleanup_results['sync_logs'] = f'error: {str(e)}'

        try:
            cutoff_90days = now - timedelta(days=90)
            deleted_history = session.query(BusinessDiscoveryHistory).filter(
                BusinessDiscoveryHistory.discovered_at < cutoff_90days
            ).delete(synchronize_session=False)
            cleanup_results['discovery_history'] = deleted_history
        except Exception as e:
            cleanup_results['discovery_history'] = f'error: {str(e)}'

        try:
            deleted_snapshot = session.query(BusinessAnalysisSnapshot).filter(
                BusinessAnalysisSnapshot.created_at < cutoff_90days
            ).delete(synchronize_session=False)
            cleanup_results['analysis_snapshots'] = deleted_snapshot
        except Exception as e:
            cleanup_results['analysis_snapshots'] = f'error: {str(e)}'

        session.commit()

        total_deleted = sum(v for v in cleanup_results.values() if isinstance(v, int))
        return jsonify({
            'success': True,
            'message': f'총 {total_deleted}개 레코드 정리 완료',
            'details': cleanup_results,
            'cleanup_date': now.strftime('%Y-%m-%d %H:%M:%S')
        })

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@admin_bp.route('/api/cleanup/stats')
def api_cleanup_stats():
    """정리 대상 데이터 통계 조회"""
    session = Session()
    try:
        now = datetime.now()
        cutoff_30days = now - timedelta(days=30)
        cutoff_90days = now - timedelta(days=90)

        stats = {}

        try:
            stats['activity_logs_30d'] = session.query(func.count(ActivityLog.id)).filter(
                ActivityLog.timestamp < cutoff_30days
            ).scalar() or 0
        except:
            stats['activity_logs_30d'] = 'N/A'

        try:
            stats['sync_logs_30d'] = session.query(func.count(SyncLog.id)).filter(
                SyncLog.timestamp < cutoff_30days
            ).scalar() or 0
        except:
            stats['sync_logs_30d'] = 'N/A'

        try:
            stats['discovery_history_90d'] = session.query(func.count(BusinessDiscoveryHistory.id)).filter(
                BusinessDiscoveryHistory.discovered_at < cutoff_90days
            ).scalar() or 0
        except:
            stats['discovery_history_90d'] = 'N/A'

        try:
            stats['analysis_snapshots_90d'] = session.query(func.count(BusinessAnalysisSnapshot.id)).filter(
                BusinessAnalysisSnapshot.created_at < cutoff_90days
            ).scalar() or 0
        except:
            stats['analysis_snapshots_90d'] = 'N/A'

        total_cleanable = sum(v for v in stats.values() if isinstance(v, int))

        return jsonify({
            'cleanable_records': stats,
            'total_cleanable': total_cleanable,
            'note': '30일+ 로그, 90일+ 히스토리/스냅샷 정리 가능'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
