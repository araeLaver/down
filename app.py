from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import subprocess
import json
import os
import git
from threading import Thread
import time
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from database_setup import (
    ActivityLog, SyncLog, CompanyMetric, GitCommit,
    Employee, Task, SystemHealth, CompanyMilestone,
    Revenue, SCHEMA_NAME, initialize_database
)

app = Flask(__name__)

# Koyeb PostgreSQL 연결
connection_string = URL.create(
    'postgresql',
    username='unble',
    password='npg_1kjV0mhECxqs',
    host='ep-divine-bird-a1f4mly5.ap-southeast-1.pg.koyeb.app',
    database='unble',
)

engine = create_engine(connection_string, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

# 데이터베이스 초기화
try:
    initialize_database()
except Exception as e:
    print(f"Database initialization warning: {e}")


# Git 저장소 객체
try:
    repo = git.Repo('.')
except:
    repo = None

def parse_sync_log():
    """sync.log 파일 파싱하여 데이터베이스에 저장"""
    session = Session()
    try:
        with open('sync.log', 'r') as f:
            lines = f.readlines()
            
        for line in lines:
            if line.strip():
                try:
                    # 로그 포맷: [YYYY-MM-DD HH:MM:SS] [TYPE] MESSAGE
                    parts = line.split(']', 2)
                    if len(parts) >= 3:
                        timestamp_str = parts[0].strip('[')
                        log_type = parts[1].strip(' [')
                        message = parts[2].strip()
                        
                        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        
                        # 중복 체크
                        existing = session.query(SyncLog).filter_by(
                            timestamp=timestamp,
                            action=log_type,
                            message=message
                        ).first()
                        
                        if not existing:
                            sync_log = SyncLog(
                                timestamp=timestamp,
                                action=log_type,
                                message=message,
                                status='success' if 'ERROR' not in message.upper() else 'error'
                            )
                            session.add(sync_log)
                except Exception as e:
                    print(f"Error parsing line: {e}")
                    
        session.commit()
    except FileNotFoundError:
        pass
    finally:
        session.close()

def get_git_stats():
    """Git 저장소 통계"""
    if not repo:
        return {}
    
    try:
        return {
            'current_branch': repo.active_branch.name,
            'total_commits': len(list(repo.iter_commits())),
            'uncommitted_changes': len(repo.index.diff(None)) + len(repo.untracked_files),
            'last_commit': {
                'hash': repo.head.commit.hexsha[:7],
                'message': repo.head.commit.message.strip(),
                'author': str(repo.head.commit.author),
                'date': datetime.fromtimestamp(repo.head.commit.committed_date).isoformat()
            }
        }
    except:
        return {}

def get_sync_status():
    """동기화 데몬 상태 확인"""
    try:
        result = subprocess.run(['./sync-control.sh', 'status'], 
                              capture_output=True, text=True)
        is_running = 'PID:' in result.stdout
        
        if is_running:
            pid_start = result.stdout.find('PID:') + 4
            pid_end = result.stdout.find(')', pid_start)
            pid = result.stdout[pid_start:pid_end].strip()
            return {'running': True, 'pid': pid}
        else:
            return {'running': False, 'pid': None}
    except:
        return {'running': False, 'pid': None}

@app.route('/')
def index():
    """메인 대시보드"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    """통계 API"""
    parse_sync_log()  # 최신 로그 파싱
    
    session = Session()
    try:
        # 최근 활동
        recent_activities = session.query(ActivityLog).order_by(
            ActivityLog.timestamp.desc()
        ).limit(10).all()
        
        # 오늘의 동기화 횟수
        today = datetime.utcnow().date()
        sync_count = session.query(SyncLog).filter(
            text(f"DATE({SCHEMA_NAME}.sync_logs.timestamp) = :today")
        ).params(today=today).count()
        
        # Git 통계
        git_stats = get_git_stats()
        
        # 동기화 상태
        sync_status = get_sync_status()
        
        # 마일스톤 수
        milestone_count = session.query(CompanyMilestone).count()
        
        # AI 직원 수
        employee_count = session.query(Employee).filter_by(status='active').count()
        
        return jsonify({
            'sync_status': sync_status,
            'git_stats': git_stats,
            'today_syncs': sync_count,
            'total_milestones': milestone_count,
            'active_employees': employee_count,
            'recent_activities': [
                {
                    'timestamp': a.timestamp.isoformat(),
                    'type': a.activity_type,
                    'description': a.description,
                    'status': a.status
                } for a in recent_activities
            ]
        })
    finally:
        session.close()

@app.route('/api/logs')
def api_logs():
    """로그 조회 API"""
    log_type = request.args.get('type', 'sync')
    limit = int(request.args.get('limit', 50))
    
    session = Session()
    try:
        if log_type == 'sync':
            logs = session.query(SyncLog).order_by(
                SyncLog.timestamp.desc()
            ).limit(limit).all()
            
            return jsonify([
                {
                    'timestamp': l.timestamp.isoformat(),
                    'action': l.action,
                    'message': l.message,
                    'status': l.status
                } for l in logs
            ])
        else:
            logs = session.query(ActivityLog).order_by(
                ActivityLog.timestamp.desc()
            ).limit(limit).all()
            
            return jsonify([
                {
                    'timestamp': l.timestamp.isoformat(),
                    'type': l.activity_type,
                    'description': l.description,
                    'details': l.details,
                    'status': l.status
                } for l in logs
            ])
    finally:
        session.close()

@app.route('/api/sync/control', methods=['POST'])
def sync_control():
    """동기화 제어 API"""
    action = request.json.get('action')
    
    if action not in ['start', 'stop', 'restart', 'sync']:
        return jsonify({'error': 'Invalid action'}), 400
    
    session = Session()
    try:
        result = subprocess.run(['./sync-control.sh', action], 
                              capture_output=True, text=True)
        
        # 활동 로그 기록
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

@app.route('/api/metrics')
def api_metrics():
    """회사 성장 지표 API"""
    # 최근 30일 지표
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    session = Session()
    try:
        metrics = session.query(CompanyMetric).filter(
            CompanyMetric.date >= thirty_days_ago
        ).all()
        
        # 일별 커밋 수
        daily_commits = {}
        if repo:
            for commit in repo.iter_commits():
                date = datetime.fromtimestamp(commit.committed_date).date()
                if date >= thirty_days_ago.date():
                    date_str = date.isoformat()
                    daily_commits[date_str] = daily_commits.get(date_str, 0) + 1
        
        # 일별 동기화 수 (원시 SQL 사용)
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

@app.route('/api/record', methods=['POST'])
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

# 백그라운드 작업
def background_sync_parser():
    """백그라운드에서 주기적으로 sync.log 파싱"""
    while True:
        try:
            parse_sync_log()
        except Exception as e:
            print(f"Background parser error: {e}")
        time.sleep(30)  # 30초마다 파싱


# 백그라운드 스레드 시작
if __name__ == '__main__':
    parser_thread = Thread(target=background_sync_parser, daemon=True)
    parser_thread.start()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)