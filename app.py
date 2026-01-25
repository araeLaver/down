from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import subprocess
import json
import os
import git
from threading import Thread
import time
from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker

# 통합 설정 모듈
from config import DatabaseConfig, DiscoveryConfig, APIConfig, NotificationConfig, LogConfig

# 통합 로깅 시스템
from logging_config import init_logging, get_app_logger, get_discovery_logger, LogContext

# 인증 모듈
from auth import require_api_key, optional_auth, create_auth_routes

# 로깅 초기화
app_logger = init_logging()
logger = get_app_logger()

from database_setup import (
    ActivityLog, SyncLog, CompanyMetric, GitCommit,
    Employee, Task, SystemHealth, CompanyMilestone,
    Revenue, BusinessMeeting, BusinessPlan, EmployeeSuggestion,
    SuggestionFeedback, SCHEMA_NAME, initialize_database
)
from business_monitor import QhyxBusinessMonitor
from continuous_business_discovery import ContinuousBusinessDiscovery
from business_discovery_history import (
    BusinessDiscoveryHistory, BusinessAnalysisSnapshot,
    BusinessInsight, BusinessHistoryTracker, initialize_history_tables,
    LowScoreBusiness
)
from startup_support_crawler import StartupSupportCrawler

app = Flask(__name__)
CORS(app, origins=["https://anonymous-kylen-untab-d30cd097.koyeb.app"])

# 환경변수 기반 PostgreSQL 연결 (보안 강화)
DATABASE_URL = DatabaseConfig.get_database_url()
engine = create_engine(DATABASE_URL, **DatabaseConfig.get_engine_options())
Session = sessionmaker(bind=engine)

def get_db_session():
    """안전한 DB 세션 생성 (재연결 포함)"""
    try:
        session = Session()
        # 연결 테스트
        session.execute(text("SELECT 1"))
        return session
    except Exception as e:
        print(f"[DB] Connection error, retrying: {e}")
        try:
            engine.dispose()  # 기존 연결 정리
            session = Session()
            return session
        except Exception as e2:
            print(f"[DB] Retry failed: {e2}")
            return None

# 데이터베이스 초기화
try:
    initialize_database()
    initialize_history_tables()
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
    """Qhyx Inc. 메인 홈페이지"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """실시간 비즈니스 모니터링 대시보드"""
    return render_template('business_dashboard.html')

@app.route('/startup-roadmap')
def startup_roadmap():
    """창업 로드맵 대시보드"""
    return render_template('startup_roadmap.html')

@app.route('/business-plan')
def business_plan():
    """TravelMate 사업계획서"""
    return render_template('business_plan.html')

@app.route('/monitor')
def monitor():
    """기존 시스템 모니터링 (호환성)"""
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

@app.route('/meetings')
def meetings():
    """회의 보고서 페이지"""
    return render_template('meetings.html')

@app.route('/suggestions')
def suggestions():
    """직원 건의사항 페이지"""
    return render_template('suggestions.html')

@app.route('/api/meetings')
def api_meetings():
    """회의 보고서 API"""
    session = Session()
    try:
        # 최근 회의 목록 조회
        meetings = session.query(BusinessMeeting).order_by(
            BusinessMeeting.meeting_date.desc()
        ).limit(10).all()
        
        meeting_list = []
        for meeting in meetings:
            # Safe JSON parsing for agenda
            agenda_data = []
            if meeting.agenda:
                try:
                    # Try to parse as JSON first
                    agenda_data = json.loads(meeting.agenda)
                except json.JSONDecodeError:
                    # If not JSON, split plain text by common delimiters
                    if ')' in meeting.agenda:
                        # Split by numbered items like "1) Item 2) Item"
                        agenda_data = [item.strip() for item in meeting.agenda.replace(') ', ')\n').split('\n') if item.strip()]
                    else:
                        # Just use as single item
                        agenda_data = [meeting.agenda]
            
            # Safe JSON parsing for participants
            participants_data = []
            if meeting.participants:
                if isinstance(meeting.participants, list):
                    # Already a list
                    participants_data = meeting.participants
                elif isinstance(meeting.participants, str):
                    try:
                        # Try to parse as JSON first
                        participants_data = json.loads(meeting.participants)
                    except json.JSONDecodeError:
                        # If not JSON, use as single item or split by comma
                        if ',' in meeting.participants:
                            participants_data = [p.strip() for p in meeting.participants.split(',')]
                        else:
                            participants_data = [meeting.participants]
            
            # Parse meeting_notes
            meeting_notes_data = {}
            if meeting.meeting_notes:
                try:
                    meeting_notes_data = json.loads(meeting.meeting_notes)
                except:
                    pass

            meeting_data = {
                'id': meeting.id,
                'title': meeting.title,
                'meeting_type': meeting.meeting_type,
                'date': meeting.meeting_date.strftime('%Y-%m-%d %H:%M') if meeting.meeting_date else None,
                'status': meeting.status,
                'agenda': agenda_data,
                'key_decisions': meeting.key_decisions if meeting.key_decisions else [],
                'action_items': meeting.action_items if meeting.action_items else [],
                'participants': participants_data,
                'meeting_notes': meeting_notes_data
            }
            meeting_list.append(meeting_data)
        
        return jsonify({
            'meetings': meeting_list,
            'total_count': len(meeting_list)
        })
    finally:
        session.close()

@app.route('/api/meetings/<int:meeting_id>')
def api_meeting_detail(meeting_id):
    """특정 회의 상세 정보 API"""
    session = Session()
    try:
        meeting = session.query(BusinessMeeting).filter_by(id=meeting_id).first()
        if not meeting:
            return jsonify({'error': 'Meeting not found'}), 404
        
        # 회의록 파싱
        meeting_notes = {}
        if meeting.meeting_notes:
            try:
                meeting_notes = json.loads(meeting.meeting_notes)
            except:
                pass
        
        # Safe JSON parsing for agenda
        agenda_data = []
        if meeting.agenda:
            try:
                # Try to parse as JSON first
                agenda_data = json.loads(meeting.agenda)
            except json.JSONDecodeError:
                # If not JSON, split plain text by common delimiters
                if ')' in meeting.agenda:
                    # Split by numbered items like "1) Item 2) Item"
                    agenda_data = [item.strip() for item in meeting.agenda.replace(') ', ')\n').split('\n') if item.strip()]
                else:
                    # Just use as single item
                    agenda_data = [meeting.agenda]
        
        # Safe JSON parsing for participants
        participants_data = []
        if meeting.participants:
            if isinstance(meeting.participants, list):
                # Already a list
                participants_data = meeting.participants
            elif isinstance(meeting.participants, str):
                try:
                    # Try to parse as JSON first
                    participants_data = json.loads(meeting.participants)
                except json.JSONDecodeError:
                    # If not JSON, use as single item or split by comma
                    if ',' in meeting.participants:
                        participants_data = [p.strip() for p in meeting.participants.split(',')]
                    else:
                        participants_data = [meeting.participants]
        
        meeting_detail = {
            'id': meeting.id,
            'title': meeting.title,
            'meeting_type': meeting.meeting_type,
            'date': meeting.meeting_date.strftime('%Y-%m-%d %H:%M') if meeting.meeting_date else None,
            'status': meeting.status,
            'agenda': agenda_data,
            'key_decisions': meeting.key_decisions if meeting.key_decisions else [],
            'action_items': meeting.action_items if meeting.action_items else [],
            'participants': participants_data,
            'meeting_notes': meeting_notes
        }
        
        return jsonify(meeting_detail)
    finally:
        session.close()

@app.route('/api/suggestions')
def api_suggestions():
    """건의사항 목록 API"""
    session = Session()
    try:
        # 최근 건의사항 목록 조회 (상태별로 정렬)
        suggestions = session.query(EmployeeSuggestion).order_by(
            EmployeeSuggestion.created_at.desc()
        ).limit(20).all()
        
        # 직원 정보 일괄 조회 (N+1 쿼리 제거)
        employee_ids = list(set(s.employee_id for s in suggestions))
        employees_dict = {e.employee_id: e for e in session.query(Employee).filter(
            Employee.employee_id.in_(employee_ids)
        ).all()} if employee_ids else {}

        suggestion_list = []
        for suggestion in suggestions:
            employee = employees_dict.get(suggestion.employee_id)
            employee_name = employee.name if employee else suggestion.employee_id
            
            suggestion_data = {
                'id': suggestion.id,
                'suggestion_id': suggestion.suggestion_id,
                'employee_id': suggestion.employee_id,
                'employee_name': employee_name,
                'category': suggestion.category,
                'priority': suggestion.priority,
                'title': suggestion.title,
                'description': suggestion.description,
                'suggested_solution': suggestion.suggested_solution,
                'expected_benefit': suggestion.expected_benefit,
                'implementation_difficulty': suggestion.implementation_difficulty,
                'status': suggestion.status,
                'created_at': suggestion.created_at.strftime('%Y-%m-%d %H:%M') if suggestion.created_at else None,
                'reviewed_at': suggestion.reviewed_at.strftime('%Y-%m-%d %H:%M') if suggestion.reviewed_at else None,
                'estimated_impact': suggestion.estimated_impact,
                'tags': suggestion.tags if suggestion.tags else []
            }
            suggestion_list.append(suggestion_data)
        
        # 상태별 통계
        stats = {
            'total': len(suggestion_list),
            'submitted': len([s for s in suggestion_list if s['status'] == 'submitted']),
            'reviewing': len([s for s in suggestion_list if s['status'] == 'reviewing']),
            'approved': len([s for s in suggestion_list if s['status'] == 'approved']),
            'implemented': len([s for s in suggestion_list if s['status'] == 'implemented'])
        }
        
        return jsonify({
            'suggestions': suggestion_list,
            'stats': stats
        })
    finally:
        session.close()

@app.route('/api/suggestions/<int:suggestion_id>')
def api_suggestion_detail(suggestion_id):
    """특정 건의사항 상세 정보 API"""
    session = Session()
    try:
        suggestion = session.query(EmployeeSuggestion).filter_by(id=suggestion_id).first()
        if not suggestion:
            return jsonify({'error': 'Suggestion not found'}), 404
        
        # 직원 정보
        employee = session.query(Employee).filter_by(employee_id=suggestion.employee_id).first()
        
        # 피드백 목록
        feedbacks = session.query(SuggestionFeedback).filter_by(
            suggestion_id=suggestion.suggestion_id
        ).order_by(SuggestionFeedback.created_at.desc()).all()
        
        feedback_list = []
        for feedback in feedbacks:
            feedback_list.append({
                'id': feedback.id,
                'feedback_type': feedback.feedback_type,
                'feedback_text': feedback.feedback_text,
                'created_by': feedback.created_by,
                'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M'),
                'is_internal': feedback.is_internal
            })
        
        suggestion_detail = {
            'id': suggestion.id,
            'suggestion_id': suggestion.suggestion_id,
            'employee_id': suggestion.employee_id,
            'employee_name': employee.name if employee else suggestion.employee_id,
            'employee_role': employee.role if employee else '',
            'category': suggestion.category,
            'priority': suggestion.priority,
            'title': suggestion.title,
            'description': suggestion.description,
            'suggested_solution': suggestion.suggested_solution,
            'expected_benefit': suggestion.expected_benefit,
            'implementation_difficulty': suggestion.implementation_difficulty,
            'status': suggestion.status,
            'created_at': suggestion.created_at.strftime('%Y-%m-%d %H:%M') if suggestion.created_at else None,
            'reviewed_at': suggestion.reviewed_at.strftime('%Y-%m-%d %H:%M') if suggestion.reviewed_at else None,
            'implemented_at': suggestion.implemented_at.strftime('%Y-%m-%d %H:%M') if suggestion.implemented_at else None,
            'reviewer_notes': suggestion.reviewer_notes,
            'implementation_cost': suggestion.implementation_cost,
            'estimated_impact': suggestion.estimated_impact,
            'tags': suggestion.tags if suggestion.tags else [],
            'feedbacks': feedback_list
        }
        
        return jsonify(suggestion_detail)
    finally:
        session.close()

@app.route('/api/suggestions', methods=['POST'])
def api_create_suggestion():
    """새 건의사항 생성 API"""
    data = request.json
    
    session = Session()
    try:
        # 건의사항 ID 생성
        from datetime import datetime
        today = datetime.now()
        suggestion_id = f"SUG_{today.strftime('%Y%m%d')}_{session.query(EmployeeSuggestion).count() + 1:03d}"
        
        suggestion = EmployeeSuggestion(
            suggestion_id=suggestion_id,
            employee_id=data.get('employee_id'),
            category=data.get('category'),
            priority=data.get('priority', 'medium'),
            title=data.get('title'),
            description=data.get('description'),
            suggested_solution=data.get('suggested_solution'),
            expected_benefit=data.get('expected_benefit'),
            implementation_difficulty=data.get('implementation_difficulty', 'medium'),
            estimated_impact=data.get('estimated_impact'),
            tags=data.get('tags', [])
        )
        
        session.add(suggestion)
        session.commit()
        
        return jsonify({
            'success': True, 
            'suggestion_id': suggestion_id,
            'id': suggestion.id
        })
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route('/api/suggestions/<int:suggestion_id>/feedback', methods=['POST'])
def api_add_suggestion_feedback(suggestion_id):
    """건의사항에 피드백 추가 API"""
    data = request.json
    
    session = Session()
    try:
        # 건의사항 존재 확인
        suggestion = session.query(EmployeeSuggestion).filter_by(id=suggestion_id).first()
        if not suggestion:
            return jsonify({'error': 'Suggestion not found'}), 404
        
        feedback = SuggestionFeedback(
            suggestion_id=suggestion.suggestion_id,
            feedback_type=data.get('feedback_type', 'comment'),
            feedback_text=data.get('feedback_text'),
            created_by=data.get('created_by', 'System'),
            is_internal=data.get('is_internal', False)
        )
        
        session.add(feedback)
        session.commit()
        
        return jsonify({'success': True, 'id': feedback.id})
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route('/api/suggestions/<int:suggestion_id>/status', methods=['PUT'])
def api_update_suggestion_status(suggestion_id):
    """건의사항 상태 업데이트 API"""
    data = request.json
    
    session = Session()
    try:
        suggestion = session.query(EmployeeSuggestion).filter_by(id=suggestion_id).first()
        if not suggestion:
            return jsonify({'error': 'Suggestion not found'}), 404
        
        old_status = suggestion.status
        suggestion.status = data.get('status')
        suggestion.reviewer_notes = data.get('reviewer_notes')
        
        # 상태에 따라 날짜 업데이트
        if suggestion.status in ['approved', 'rejected'] and old_status == 'submitted':
            suggestion.reviewed_at = datetime.utcnow()
        elif suggestion.status == 'implemented':
            suggestion.implemented_at = datetime.utcnow()
            suggestion.implementation_cost = data.get('implementation_cost')
        
        session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
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

@app.route('/api/dashboard-data')
def api_dashboard_data():
    """비즈니스 대시보드 데이터 API"""
    session = Session()
    try:
        today = datetime.utcnow().date()
        
        # 오늘의 회의 수
        today_meetings = session.query(BusinessMeeting).filter(
            BusinessMeeting.meeting_date >= today
        ).count()
        
        # 진행중인 업무 수
        active_tasks = session.query(Task).filter(
            Task.status.in_(['pending', 'in_progress'])
        ).count()
        
        # 오늘의 지표 업데이트 수
        today_metrics = session.query(CompanyMetric).filter(
            CompanyMetric.date >= today
        ).count()
        
        # 최근 활동들
        recent_activities = session.query(BusinessMeeting).order_by(
            BusinessMeeting.meeting_date.desc()
        ).limit(5).all()
        
        activities = []
        for meeting in recent_activities:
            activities.append({
                'time': meeting.meeting_date.strftime('%H:%M'),
                'type': 'meeting',
                'description': meeting.title,
                'status': meeting.status
            })
        
        # AI 직원 현황 (N+1 쿼리 제거: 단일 쿼리로 태스크 수 집계)
        task_counts = session.query(
            Task.assigned_to,
            func.count(Task.id).label('task_count')
        ).group_by(Task.assigned_to).subquery()

        employees_with_tasks = session.query(
            Employee,
            func.coalesce(task_counts.c.task_count, 0).label('task_count')
        ).outerjoin(
            task_counts,
            Employee.employee_id == task_counts.c.assigned_to
        ).filter(Employee.status == 'active').all()

        employee_data = []
        for emp, task_count in employees_with_tasks:
            employee_data.append({
                'name': emp.name,
                'role': emp.role,
                'status': emp.status,
                'tasks': task_count
            })
        
        # 사업 계획 현황
        business_plans = session.query(BusinessPlan).filter(
            BusinessPlan.status.in_(['approved', 'in_progress'])
        ).all()
        
        plan_data = []
        for plan in business_plans:
            monthly_revenue = int(plan.projected_revenue_12m / 12) if plan.projected_revenue_12m else 0
            plan_data.append({
                'name': plan.plan_name,
                'status': plan.status,
                'revenue': f'{monthly_revenue:,}원/월'
            })
        
        return jsonify({
            'meetings': today_meetings,
            'tasks': active_tasks,
            'metrics': today_metrics,
            'activities': activities,
            'employees': employee_data,
            'business_plans': plan_data
        })
    finally:
        session.close()

@app.route('/api/status')
def api_status():
    """시스템 상태 API (메인 웹사이트용)"""
    session = Session()
    try:
        # 시스템 상태 확인
        sync_status = get_sync_status()
        
        # 오늘의 활동 수
        today = datetime.utcnow().date()
        today_meetings = session.query(BusinessMeeting).filter(
            BusinessMeeting.meeting_date >= today
        ).count()
        
        active_employees = session.query(Employee).filter_by(status='active').count()
        
        return jsonify({
            'system_running': True,
            'autonomous_meetings': today_meetings,
            'active_employees': active_employees,
            'sync_daemon_running': sync_status['running'],
            'last_update': datetime.utcnow().isoformat()
        })
    finally:
        session.close()

@app.route('/api/market-config')
def api_market_config():
    """시장 분석 설정 상태 API

    유료 플랜 전환 후 환경변수 MARKET_ANALYSIS_MODE=full 설정하면
    실제 외부 API를 사용한 시장 분석이 활성화됨
    """
    config_status = MarketConfig.get_status()
    return jsonify({
        'success': True,
        'config': config_status,
        'message': '환경변수 MARKET_ANALYSIS_MODE=full 설정 시 전체 모드 활성화'
    })

@app.route('/business-discovery')
def business_discovery():
    """사업 발굴 대시보드 페이지"""
    return render_template('business_discovery.html')

@app.route('/business-history')
def business_history():
    """사업 발굴 히스토리 & 분석 대시보드"""
    return render_template('business_history.html')

@app.route('/business-review')
def business_review():
    """검토 필요 사업 (60-79점)"""
    return render_template('business_review.html')

@app.route('/business-rejected')
def business_rejected():
    """부적합 사업 (60점 미만)"""
    return render_template('business_rejected.html')

@app.route('/business')
def business_landing():
    """사업 분석 랜딩 페이지"""
    return render_template('business_landing.html')

@app.route('/trigger-discovery')
def trigger_discovery_page():
    """수동 사업 발굴 페이지"""
    return render_template('trigger_discovery.html')

def generate_default_action_plan(business_name, business_type):
    """기본 실행 계획 생성 (DB에 없는 경우)"""
    return {
        'week_1': {
            'goal': 'MVP 개발 및 시장 조사',
            'tasks': [
                f'{business_name} 핵심 기능 정의',
                '경쟁사 분석 및 차별화 포인트 도출',
                '랜딩페이지 제작 (Webflow/Notion)',
                '초기 고객 타겟 정의'
            ]
        },
        'week_2': {
            'goal': '프로토타입 및 검증',
            'tasks': [
                'MVP 프로토타입 제작',
                '베타 테스터 10명 모집',
                '사용자 피드백 수집',
                '가격 책정 테스트'
            ]
        },
        'week_3': {
            'goal': '마케팅 및 고객 확보',
            'tasks': [
                'SNS 마케팅 시작 (인스타/페이스북)',
                '소규모 유료 광고 테스트 (일 1만원)',
                '첫 유료 고객 확보',
                '고객 후기 수집'
            ]
        },
        'week_4': {
            'goal': '최적화 및 확장',
            'tasks': [
                '전환율 최적화',
                '자동화 시스템 구축',
                '추가 기능 개발',
                '월 목표 매출 달성'
            ]
        },
        'total_budget': 1000000,
        'summary': f'{business_name}를 4주 안에 런칭하기 위한 실행 계획입니다.'
    }

def generate_startup_guide(business_name, business_type, score):
    """상세 시작 가이드 생성"""

    # 사업 유형별 기술 스택 추천
    tech_stacks = {
        'saas': {
            'recommended': 'No-Code / Low-Code',
            'tools': ['Bubble.io', 'Webflow', 'Airtable', 'Zapier'],
            'cost': '월 5-10만원',
            'learning_time': '1-2주',
            'reason': 'SaaS는 빠른 MVP 검증이 중요. 코딩 없이 2주 내 런칭 가능'
        },
        'agency': {
            'recommended': '포트폴리오 + 프리랜서 플랫폼',
            'tools': ['Notion', 'Figma', '크몽', '숨고', 'LinkedIn'],
            'cost': '월 0-5만원',
            'learning_time': '즉시 시작 가능',
            'reason': '에이전시는 기술보다 영업력이 중요. 플랫폼 활용으로 즉시 시작'
        },
        'marketplace': {
            'recommended': 'No-Code 마켓플레이스 빌더',
            'tools': ['Sharetribe', 'Bubble.io', 'Webflow + Memberstack'],
            'cost': '월 10-30만원',
            'learning_time': '2-3주',
            'reason': '마켓플레이스는 양면 시장. 빠른 런칭 후 수요/공급 테스트 필요'
        }
    }

    tech = tech_stacks.get(business_type, tech_stacks['saas'])

    return {
        'day1_checklist': {
            'title': 'Day 1: 오늘 당장 시작하기',
            'tasks': [
                {
                    'task': '도메인 구매',
                    'detail': f'{business_name.replace(" ", "").lower()}.com 또는 .kr',
                    'tool': 'Namecheap, 가비아',
                    'cost': '1-2만원/년',
                    'time': '10분'
                },
                {
                    'task': '랜딩페이지 제작',
                    'detail': '서비스 소개 + 이메일 수집 폼',
                    'tool': 'Notion, Webflow (무료)',
                    'cost': '0원',
                    'time': '2-3시간'
                },
                {
                    'task': '경쟁사 5개 분석',
                    'detail': '가격, 기능, 리뷰 정리',
                    'tool': 'Google 스프레드시트',
                    'cost': '0원',
                    'time': '1-2시간'
                },
                {
                    'task': 'SNS 계정 생성',
                    'detail': '인스타그램 비즈니스 계정',
                    'tool': 'Instagram, 페이스북',
                    'cost': '0원',
                    'time': '30분'
                }
            ]
        },
        'tech_stack': tech,
        'marketing_channels': {
            'free': [
                {'channel': '인스타그램', 'strategy': '관련 해시태그로 일 1포스팅', 'expected': '월 100-500 팔로워'},
                {'channel': '블로그/브런치', 'strategy': '주 2회 전문 콘텐츠 발행', 'expected': '월 1000-5000 방문자'},
                {'channel': '커뮤니티', 'strategy': '네이버 카페, 오픈카톡 참여', 'expected': '초기 베타 테스터 확보'},
                {'channel': '지인 네트워크', 'strategy': '카톡/링크드인으로 런칭 알림', 'expected': '첫 10명 고객'}
            ],
            'paid': [
                {'channel': '페이스북/인스타 광고', 'budget': '일 1-3만원', 'expected': 'CPC 300-500원'},
                {'channel': '네이버 검색광고', 'budget': '일 1-2만원', 'expected': '타겟 키워드 노출'},
                {'channel': '인플루언서', 'budget': '건당 5-30만원', 'expected': '신뢰도 확보'}
            ]
        },
        'first_customer_strategy': {
            'title': '첫 10명 고객 확보 전략',
            'steps': [
                {
                    'step': 1,
                    'action': '무료/할인 제공',
                    'detail': '첫 달 무료 또는 50% 할인으로 진입 장벽 낮추기',
                    'target': '3명'
                },
                {
                    'step': 2,
                    'action': '지인 영업',
                    'detail': '카톡, 인스타 DM으로 직접 연락. 솔직하게 도움 요청',
                    'target': '3명'
                },
                {
                    'step': 3,
                    'action': '커뮤니티 활동',
                    'detail': '관련 오픈카톡, 페이스북 그룹에서 무료 상담 제공',
                    'target': '2명'
                },
                {
                    'step': 4,
                    'action': '콘텐츠 마케팅',
                    'detail': '블로그 글 하단에 CTA 삽입',
                    'target': '2명'
                }
            ]
        },
        'cost_breakdown': {
            'essential': [
                {'item': '도메인', 'cost': 15000, 'period': '년'},
                {'item': '호스팅/서버', 'cost': 0, 'period': '월', 'note': 'Vercel/Netlify 무료'},
                {'item': '이메일 서비스', 'cost': 0, 'period': '월', 'note': 'Mailchimp 무료 (500명까지)'}
            ],
            'recommended': [
                {'item': 'No-Code 툴', 'cost': 50000, 'period': '월'},
                {'item': '광고비', 'cost': 300000, 'period': '월'},
                {'item': '디자인 툴', 'cost': 15000, 'period': '월', 'note': 'Canva Pro'}
            ],
            'total_minimum': 15000,
            'total_recommended': 380000
        },
        'risk_management': [
            {
                'risk': '고객이 안 모임',
                'solution': '가격 낮추기, 무료 체험 연장, 타겟 재설정',
                'prevention': '런칭 전 최소 10명 사전 등록 확보'
            },
            {
                'risk': '경쟁사가 너무 강함',
                'solution': '니치 시장 집중, 특정 고객군 전문화',
                'prevention': '차별화 포인트 3개 이상 준비'
            },
            {
                'risk': '기술적 문제',
                'solution': 'No-Code로 우회, 외주 활용',
                'prevention': 'MVP는 최대한 단순하게'
            }
        ],
        'success_metrics': {
            'week1': {'goal': '랜딩페이지 완성 + 이메일 20개 수집', 'importance': '시장 관심도 검증'},
            'week2': {'goal': '베타 테스터 10명 + 피드백 수집', 'importance': '제품-시장 적합성 확인'},
            'week4': {'goal': '유료 고객 5명 + 월 50만원 매출', 'importance': '수익 모델 검증'},
            'month3': {'goal': '월 200만원 매출 + 고객 30명', 'importance': '지속 가능성 확인'}
        }
    }

def generate_default_market_analysis(business_name, keyword):
    """경량 시장 분석 생성 (도메인별 정적 데이터 기반)"""
    import hashlib

    # 도메인별 시장 데이터 정의
    domain_market_data = {
        'ai': {
            'market_size': '2조 5천억원',
            'growth_rate': 35,
            'competition_level': '높음',
            'entry_barrier': '중간',
            'trend': '급성장',
            'naver_search': 85000,
            'seasonality': '연중 꾸준',
            'target_size': '기업 고객 50만+',
            'keywords': ['AI', '인공지능', '머신러닝', 'GPT', '자동화', '챗봇']
        },
        'saas': {
            'market_size': '1조 8천억원',
            'growth_rate': 28,
            'competition_level': '중간',
            'entry_barrier': '낮음',
            'trend': '성장세',
            'naver_search': 45000,
            'seasonality': '연중 꾸준',
            'target_size': '중소기업 200만+',
            'keywords': ['구독', 'SaaS', '클라우드', '서비스', '플랫폼']
        },
        'ecommerce': {
            'market_size': '8조원',
            'growth_rate': 15,
            'competition_level': '매우 높음',
            'entry_barrier': '낮음',
            'trend': '안정적 성장',
            'naver_search': 120000,
            'seasonality': '연말 성수기',
            'target_size': '온라인 소비자 3천만+',
            'keywords': ['쇼핑', '판매', '커머스', '마켓', '스토어', '굿즈']
        },
        'education': {
            'market_size': '3조원',
            'growth_rate': 22,
            'competition_level': '중간',
            'entry_barrier': '중간',
            'trend': '성장세',
            'naver_search': 68000,
            'seasonality': '학기초 성수기',
            'target_size': '학습자 800만+',
            'keywords': ['교육', '강의', '학습', '코딩', '튜터', '멘토링']
        },
        'content': {
            'market_size': '1조 2천억원',
            'growth_rate': 25,
            'competition_level': '높음',
            'entry_barrier': '낮음',
            'trend': '성장세',
            'naver_search': 55000,
            'seasonality': '연중 꾸준',
            'target_size': '콘텐츠 소비자 2천만+',
            'keywords': ['콘텐츠', '블로그', '유튜브', '영상', '크리에이터']
        },
        'marketing': {
            'market_size': '2조원',
            'growth_rate': 18,
            'competition_level': '높음',
            'entry_barrier': '중간',
            'trend': '안정적',
            'naver_search': 72000,
            'seasonality': '연말 성수기',
            'target_size': '사업자 700만+',
            'keywords': ['마케팅', '광고', '홍보', 'SNS', '브랜딩']
        },
        'finance': {
            'market_size': '5조원',
            'growth_rate': 20,
            'competition_level': '매우 높음',
            'entry_barrier': '높음',
            'trend': '성장세',
            'naver_search': 95000,
            'seasonality': '연초/연말 성수기',
            'target_size': '금융 소비자 2천만+',
            'keywords': ['투자', '재테크', '주식', '금융', '핀테크']
        },
        'health': {
            'market_size': '4조원',
            'growth_rate': 30,
            'competition_level': '중간',
            'entry_barrier': '중간',
            'trend': '급성장',
            'naver_search': 88000,
            'seasonality': '연초 성수기',
            'target_size': '건강 관심층 1천만+',
            'keywords': ['건강', '헬스', '다이어트', '운동', '웰니스']
        },
        'default': {
            'market_size': '1조원',
            'growth_rate': 15,
            'competition_level': '중간',
            'entry_barrier': '중간',
            'trend': '안정적',
            'naver_search': 30000,
            'seasonality': '연중 꾸준',
            'target_size': '잠재 고객 100만+',
            'keywords': []
        }
    }

    # 키워드 기반 도메인 매칭
    def detect_domain(name, kw):
        text = f"{name} {kw}".lower()
        for domain, data in domain_market_data.items():
            if domain == 'default':
                continue
            for dk in data.get('keywords', []):
                if dk.lower() in text:
                    return domain
        return 'default'

    domain = detect_domain(business_name, keyword)
    market = domain_market_data[domain]

    # 해시 기반 변동값 생성 (동일 입력 = 동일 출력)
    hash_val = int(hashlib.md5(f"{business_name}{keyword}".encode()).hexdigest()[:8], 16)
    variation = (hash_val % 20 - 10) / 100  # -10% ~ +10% 변동

    search_count = int(market['naver_search'] * (1 + variation))
    global_interest = min(95, max(40, 60 + int(market['growth_rate'] * 0.8) + int(variation * 30)))

    # 경쟁도 점수 계산
    competition_scores = {'낮음': 30, '중간': 55, '높음': 75, '매우 높음': 90}
    competition_score = competition_scores.get(market['competition_level'], 55)

    # 진입 장벽 점수
    barrier_scores = {'낮음': 25, '중간': 50, '높음': 75}
    barrier_score = barrier_scores.get(market['entry_barrier'], 50)

    return {
        'naver': {
            'search_count': search_count,
            'competition': market['competition_level'],
            'competition_score': competition_score,
            'related_keywords': [keyword, f'{keyword} 추천', f'{keyword} 후기', f'{keyword} 비교']
        },
        'google_trends': {
            'global_interest': global_interest,
            'trend': market['trend'],
            'growth_rate': market['growth_rate']
        },
        'market_info': {
            'market_size': market['market_size'],
            'growth_rate': market['growth_rate'],
            'seasonality': market['seasonality'],
            'target_size': market['target_size'],
            'entry_barrier': market['entry_barrier'],
            'entry_barrier_score': barrier_score,
            'domain': domain
        },
        'market_summary': f"{business_name} 관련 시장 규모는 {market['market_size']}이며, 연 {market['growth_rate']}% 성장 중입니다. 경쟁 강도는 '{market['competition_level']}'이고, 진입 장벽은 '{market['entry_barrier']}' 수준입니다. {market['target_size']}의 잠재 고객이 있습니다."
    }

def generate_default_revenue_analysis(business_name, score):
    """기본 수익 분석 생성 (DB에 없는 경우)"""
    base_revenue = score * 50000
    return {
        'scenarios': {
            'conservative': {
                'monthly_revenue': int(base_revenue * 0.5),
                'monthly_profit': int(base_revenue * 0.3)
            },
            'realistic': {
                'monthly_revenue': base_revenue,
                'monthly_profit': int(base_revenue * 0.6),
                'break_even_months': 3
            },
            'optimistic': {
                'monthly_revenue': int(base_revenue * 2),
                'monthly_profit': int(base_revenue * 1.2)
            }
        },
        'startup_cost': int(score * 50000),
        'annual_roi': int((base_revenue * 12 - score * 50000) / (score * 50000) * 100),
        'revenue_model': 'subscription',
        'revenue_summary': f'{business_name}은 월 {int(base_revenue/10000)}만원 수익이 예상됩니다.'
    }

@app.route('/api/discovered-businesses')
def api_discovered_businesses():
    """자동 발굴된 사업 목록 API (전체 점수 포함, 서버 사이드 페이징)"""
    session = None
    try:
        session = get_db_session()

        # 페이징 파라미터
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        limit = min(limit, 100)  # 최대 100개
        offset = (page - 1) * limit

        # 전체 개수 조회
        total_count = session.query(func.count(BusinessDiscoveryHistory.id)).scalar()

        # 오늘/이번주 통계
        from datetime import datetime, timedelta
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = today - timedelta(days=7)

        today_count = session.query(func.count(BusinessDiscoveryHistory.id)).filter(
            BusinessDiscoveryHistory.discovered_at >= today
        ).scalar()

        week_count = session.query(func.count(BusinessDiscoveryHistory.id)).filter(
            BusinessDiscoveryHistory.discovered_at >= week_ago
        ).scalar()

        high_score_count = session.query(func.count(BusinessDiscoveryHistory.id)).filter(
            BusinessDiscoveryHistory.total_score >= 85
        ).scalar()

        # 페이징된 데이터 조회 (중복 제거 - 같은 이름은 가장 최근 것만)
        # 서브쿼리로 각 business_name의 최신 ID 선택
        from sqlalchemy import func as sqlfunc
        subquery = session.query(
            sqlfunc.max(BusinessDiscoveryHistory.id).label('max_id')
        ).group_by(BusinessDiscoveryHistory.business_name).subquery()

        histories = session.query(BusinessDiscoveryHistory).join(
            subquery, BusinessDiscoveryHistory.id == subquery.c.max_id
        ).order_by(
            BusinessDiscoveryHistory.discovered_at.desc()
        ).offset(offset).limit(limit).all()

        # 전체 개수도 중복 제거된 개수로 갱신
        total_count = session.query(sqlfunc.count(sqlfunc.distinct(BusinessDiscoveryHistory.business_name))).scalar()

        logger.info(f"[API] discovered-businesses: page={page}, limit={limit}, total={total_count}")

        business_list = []
        for biz in histories:
            # 월 매출 추정 (간단한 계산)
            monthly_revenue = biz.total_score * 100000  # 점수 * 10만원
            annual_revenue = monthly_revenue * 12
            investment = biz.total_score * 50000  # 점수 * 5만원

            # 시장 분석 데이터 파싱 (없거나 새 필드 없으면 기본값 생성)
            market_data = biz.market_analysis if isinstance(biz.market_analysis, dict) else {}
            if not market_data or not market_data.get('market_info'):
                # 기존 데이터가 없거나 새로운 market_info 필드가 없으면 경량 분석으로 대체
                default_market = generate_default_market_analysis(biz.business_name, biz.keyword or biz.business_name)
                # 기존 데이터가 있으면 병합, 없으면 기본값 사용
                if market_data:
                    default_market.update({k: v for k, v in market_data.items() if v})
                market_data = default_market

            # 수익 분석 데이터 파싱 (없으면 기본값 생성)
            revenue_data = biz.revenue_analysis if isinstance(biz.revenue_analysis, dict) else {}
            if not revenue_data:
                revenue_data = generate_default_revenue_analysis(biz.business_name, biz.total_score)

            # 실행 계획 데이터 파싱 (없으면 기본값 생성)
            action_plan_data = biz.action_plan if isinstance(biz.action_plan, dict) else {}
            if not action_plan_data:
                action_plan_data = generate_default_action_plan(biz.business_name, biz.business_type)

            # 시작 가이드 생성
            startup_guide = generate_startup_guide(biz.business_name, biz.business_type, biz.total_score)

            # full_analysis에서 사업 상세 정보 추출 또는 기본값 생성
            full_analysis_data = biz.full_analysis if isinstance(biz.full_analysis, dict) else {}
            business_info = full_analysis_data.get('business', {})

            # 새 필드가 없으면 기본값 생성
            if not business_info.get('it_type_label'):
                # IT 사업 유형 자동 분류
                biz_type_lower = (biz.business_type or '').lower()
                if any(x in biz_type_lower for x in ['플랫폼', '커뮤니티', '네트워크']):
                    it_type = 'platform'
                    it_label = '플랫폼'
                elif any(x in biz_type_lower for x in ['마켓', '매칭', '중개']):
                    it_type = 'marketplace'
                    it_label = '마켓플레이스'
                elif any(x in biz_type_lower for x in ['대행', '컨설팅', '에이전시']):
                    it_type = 'agency'
                    it_label = '에이전시'
                elif any(x in biz_type_lower for x in ['도구', '툴', '봇', '자동화']):
                    it_type = 'tools'
                    it_label = '생산성 도구'
                else:
                    it_type = 'saas'
                    it_label = 'SaaS'

                # 기본 핵심 기능
                default_features = {
                    'saas': ['데이터 관리', '알림 시스템', '분석 대시보드'],
                    'marketplace': ['실시간 매칭', '리뷰 시스템', '간편 결제'],
                    'agency': ['프로젝트 관리', '1:1 맞춤 서비스', '품질 보장'],
                    'tools': ['간편한 UX', '빠른 처리', '다중 플랫폼'],
                    'platform': ['커뮤니티 기능', '콘텐츠 큐레이션', '개인화']
                }

                # 기본 기술 스택
                default_tech = {
                    'saas': ['Bubble.io', 'Supabase'],
                    'marketplace': ['Sharetribe', 'Webflow'],
                    'agency': ['Notion', 'Figma'],
                    'tools': ['React', 'Chrome Extension'],
                    'platform': ['Firebase', 'Vercel']
                }

                # 기본 수익 모델
                default_revenue = {
                    'saas': ['월정액 구독', '프리미엄 요금제'],
                    'marketplace': ['거래 수수료', '프리미엄 리스팅'],
                    'agency': ['프로젝트 단가', '리테이너 계약'],
                    'tools': ['일회성 구매', '프리미엄 기능'],
                    'platform': ['멤버십', '광고']
                }

                business_info = {
                    'it_type': it_type,
                    'it_type_label': it_label,
                    'core_features': default_features.get(it_type, []),
                    'differentiator': f"기존 서비스 대비 50% 저렴한 가격",
                    'tech_stack': default_tech.get(it_type, []),
                    'revenue_models': default_revenue.get(it_type, []),
                    'target_audience': '직장인'
                }
                full_analysis_data['business'] = business_info

            # 실제 수익 데이터가 있으면 사용
            if revenue_data:
                scenarios = revenue_data.get('scenarios', {})
                realistic = scenarios.get('realistic', scenarios.get('현실적', {}))
                monthly_revenue = realistic.get('monthly_revenue', realistic.get('월_예상_수익', monthly_revenue))
                annual_revenue = monthly_revenue * 12
                investment = revenue_data.get('startup_cost', revenue_data.get('initial_investment', investment))

            # 경량 시장 분석 데이터 추출
            market_info = market_data.get('market_info', {})
            trend = market_info.get('trend', market_data.get('trend', '안정'))
            competition_level = market_info.get('competition_level', market_data.get('competition_level', 55))
            market_size_raw = market_info.get('market_size', market_data.get('market_size', '중형'))

            # 점수 상세 분석
            score_breakdown = market_data.get('score_breakdown', {})
            if not score_breakdown:
                # 기본 점수 분석 생성
                score_breakdown = {
                    'base_score': int(biz.total_score * 0.6),
                    'domain_bonus': int((biz.market_score or 0) * 0.2),
                    'trend_bonus': 5 if trend in ['급상승', '상승'] else 0,
                    'target_bonus': 3,
                    'revenue_bonus': int((biz.revenue_score or 0) * 0.15),
                    'competition_penalty': -5 if competition_level > 70 else 0
                }

            business_list.append({
                'id': biz.id,
                'name': biz.business_name,
                'type': biz.business_type,
                'score': biz.total_score,
                'feasibility': biz.total_score / 10,
                'revenue_12m': annual_revenue,
                'investment': investment,
                'risk': 'low' if biz.total_score >= 80 else 'medium' if biz.total_score >= 70 else 'high',
                'priority': 'high' if biz.total_score >= 80 else 'medium',
                'created_at': biz.discovered_at.strftime('%Y-%m-%d %H:%M') if biz.discovered_at else None,
                'description': f"{biz.business_name} - 시장성 {int(biz.market_score)}점, 수익성 {int(biz.revenue_score)}점",
                'revenue_model': revenue_data.get('revenue_model', 'subscription'),
                # 경량 시장 분석 필드 추가
                'trend': trend,
                'competition_level': competition_level,
                'market_size': market_size_raw,
                'score_breakdown': score_breakdown,
                'details': {
                    'analysis_score': biz.total_score,
                    'market_score': biz.market_score,
                    'revenue_score': biz.revenue_score,
                    'category': biz.category,
                    'keyword': biz.keyword,
                    'market_analysis': market_data,
                    'revenue_analysis': revenue_data,
                    'action_plan': action_plan_data,
                    'startup_guide': startup_guide,
                    'full_analysis': full_analysis_data
                }
            })

        # 통계
        # 페이지 정보 계산
        total_pages = (total_count + limit - 1) // limit

        return jsonify({
            'businesses': business_list,
            'stats': {
                'total': total_count,
                'today': today_count,
                'this_week': week_count,
                'high_score': high_score_count
            },
            'pagination': {
                'page': page,
                'limit': limit,
                'total_pages': total_pages,
                'total_items': total_count
            }
        })
    except Exception as e:
        logger.error(f"[API] discovered-businesses 오류: {e}")
        return jsonify({
            'businesses': [],
            'stats': {'total': 0, 'today': 0, 'this_week': 0, 'high_score': 0},
            'error': str(e)
        }), 200  # 에러여도 200 반환하여 프론트엔드에서 처리 가능
    finally:
        if session:
            session.close()

@app.route('/api/low-score-businesses')
def api_low_score_businesses():
    """저점수 사업 목록 API (50점 미만)"""
    session = Session()
    try:
        # low_score_businesses 테이블에서 50점 미만 사업 조회
        from sqlalchemy import text

        # 직접 SQL로 조회 (테이블이 존재한다면)
        result = session.execute(text(f"""
            SELECT id, business_name, business_type, total_score, market_score, revenue_score,
                   category, keyword, market_analysis, revenue_analysis, discovered_at
            FROM {SCHEMA_NAME}.low_score_businesses
            ORDER BY discovered_at DESC
            LIMIT 100
        """))

        business_list = []
        for row in result:
            # 월 매출 추정
            monthly_revenue = row.total_score * 100000
            annual_revenue = monthly_revenue * 12
            investment = row.total_score * 50000

            business_list.append({
                'id': row.id,
                'name': row.business_name,
                'type': row.business_type,
                'score': row.total_score,
                'feasibility': row.total_score / 10,
                'revenue_12m': annual_revenue,
                'investment': investment,
                'risk': 'high',
                'priority': 'low',
                'created_at': row.discovered_at.strftime('%Y-%m-%d %H:%M') if row.discovered_at else None,
                'description': f"{row.business_name} - 시장성 {int(row.market_score)}점, 수익성 {int(row.revenue_score)}점 (실험적 아이디어)",
                'revenue_model': 'experimental',
                'details': {
                    'analysis_score': row.total_score,
                    'market_score': row.market_score,
                    'revenue_score': row.revenue_score,
                    'category': row.category,
                    'keyword': row.keyword,
                    'market_analysis': row.market_analysis,
                    'revenue_analysis': row.revenue_analysis
                }
            })

        # 통계
        total_count = session.execute(text(f"""
            SELECT COUNT(*) FROM {SCHEMA_NAME}.low_score_businesses
        """)).scalar()

        today = datetime.utcnow().date()
        today_count = session.execute(text(f"""
            SELECT COUNT(*) FROM {SCHEMA_NAME}.low_score_businesses
            WHERE DATE(discovered_at) = :today
        """), {'today': today}).scalar()

        return jsonify({
            'businesses': business_list,
            'stats': {
                'total': total_count or 0,
                'today': today_count or 0,
                'this_week': 0,
                'high_score': 0
            }
        })
    except Exception as e:
        # 테이블이 없거나 에러가 발생하면 빈 목록 반환
        logging.error(f"Error fetching low score businesses: {e}")
        return jsonify({
            'businesses': [],
            'stats': {
                'total': 0,
                'today': 0,
                'this_week': 0,
                'high_score': 0
            }
        })
    finally:
        session.close()

@app.route('/api/trigger-discovery', methods=['GET', 'POST'])
def trigger_discovery():
    """수동으로 사업 발굴 트리거 (백그라운드에서 비동기 실행)"""
    try:
        from threading import Thread
        from continuous_business_discovery import ContinuousBusinessDiscovery

        def run_discovery_background():
            """백그라운드에서 발굴 실행"""
            try:
                discovery = ContinuousBusinessDiscovery()
                results = discovery.run_hourly_discovery()

                if results['saved'] > 0:
                    discovery.generate_discovery_meeting(results)

                logging.info(f"Discovery completed: analyzed={results.get('analyzed')}, saved={results.get('saved')}")
                print(f"[TRIGGER] Discovery completed: {results.get('analyzed')} analyzed, {results.get('saved')} saved")
            except Exception as e:
                logging.error(f"Background discovery error: {e}")
                print(f"[TRIGGER ERROR] {e}")

        # 백그라운드 스레드로 실행
        thread = Thread(target=run_discovery_background, daemon=True)
        thread.start()

        return jsonify({
            'success': True,
            'message': '사업 발굴이 백그라운드에서 시작되었습니다',
            'status': 'running',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/review-businesses')
def api_review_businesses():
    """검토 필요 사업 (60-79점) API"""
    session = Session()
    try:
        businesses = session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.total_score >= 60,
            BusinessDiscoveryHistory.total_score < 80
        ).order_by(BusinessDiscoveryHistory.discovered_at.desc()).limit(100).all()

        business_list = []
        for biz in businesses:
            business_list.append({
                'id': biz.id,
                'business_name': biz.business_name,
                'business_type': biz.business_type,
                'category': biz.category,
                'total_score': biz.total_score,
                'market_score': biz.market_score,
                'revenue_score': biz.revenue_score,
                'discovered_at': biz.discovered_at.strftime('%Y-%m-%d %H:%M') if biz.discovered_at else None,
                'market_analysis': biz.market_analysis,
                'revenue_analysis': biz.revenue_analysis
            })

        return jsonify({
            'businesses': business_list,
            'total': len(business_list)
        })
    finally:
        session.close()

@app.route('/api/rejected-businesses')
def api_rejected_businesses():
    """부적합 사업 (60점 미만) API"""
    session = Session()
    try:
        businesses = session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.total_score < 60
        ).order_by(BusinessDiscoveryHistory.discovered_at.desc()).limit(100).all()

        business_list = []
        for biz in businesses:
            business_list.append({
                'id': biz.id,
                'business_name': biz.business_name,
                'business_type': biz.business_type,
                'category': biz.category,
                'total_score': biz.total_score,
                'market_score': biz.market_score,
                'revenue_score': biz.revenue_score,
                'discovered_at': biz.discovered_at.strftime('%Y-%m-%d %H:%M') if biz.discovered_at else None,
                'market_analysis': biz.market_analysis,
                'revenue_analysis': biz.revenue_analysis,
                'full_analysis': biz.full_analysis
            })

        return jsonify({
            'businesses': business_list,
            'total': len(business_list)
        })
    finally:
        session.close()

@app.route('/api/low-score-businesses/list-old')
def api_low_score_businesses_old():
    """낮은 점수 사업 목록 API (60점 미만) - 구버전"""
    session = Session()
    try:
        days = int(request.args.get('days', 30))
        limit = int(request.args.get('limit', 200))

        from datetime import datetime, timedelta
        start_date = datetime.utcnow() - timedelta(days=days)

        # LowScoreBusiness 테이블에서 조회
        businesses = session.query(LowScoreBusiness).filter(
            LowScoreBusiness.created_at >= start_date
        ).order_by(LowScoreBusiness.created_at.desc()).limit(limit).all()

        business_list = []
        for biz in businesses:
            business_list.append({
                'id': biz.id,
                'business_name': biz.business_name,
                'business_type': biz.business_type,
                'category': biz.category,
                'keyword': biz.keyword,
                'total_score': biz.total_score,
                'market_score': biz.market_score,
                'revenue_score': biz.revenue_score,
                'failure_reason': biz.failure_reason,
                'created_at': biz.created_at.strftime('%Y-%m-%d %H:%M') if biz.created_at else None,
                'market_analysis': biz.market_analysis,
                'revenue_analysis': biz.revenue_analysis,
                'improvement_suggestions': biz.improvement_suggestions,
                'discovery_batch': biz.discovery_batch,
                'full_data': biz.full_data
            })

        # 통계
        total_count = len(business_list)
        avg_score = sum([b['total_score'] for b in business_list]) / total_count if total_count > 0 else 0

        # 실패 이유별 분포
        failure_reasons = {}
        for biz in business_list:
            reason = biz['failure_reason'] or 'unknown'
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1

        return jsonify({
            'businesses': business_list,
            'total': total_count,
            'stats': {
                'avg_score': round(avg_score, 1),
                'failure_reasons': failure_reasons
            }
        })
    finally:
        session.close()

# ==================== 사업 발굴 히스토리 API ====================

@app.route('/api/business-history/stats')
def api_business_history_stats():
    """히스토리 통계 API"""
    session = Session()
    try:
        days = int(request.args.get('days', 7))
        tracker = BusinessHistoryTracker()
        stats = tracker.get_history_stats(days=days)
        return jsonify(stats)
    finally:
        session.close()

@app.route('/api/business-history/list')
def api_business_history_list():
    """전체 히스토리 목록 API"""
    session = Session()
    try:
        # 필터 파라미터
        period = request.args.get('period', '24h')
        score_filter = request.args.get('score', 'all')
        category_filter = request.args.get('category', 'all')
        search = request.args.get('search', '')
        limit = int(request.args.get('limit', 100))

        # 기간 필터
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        if period == '24h':
            start_date = now - timedelta(hours=24)
        elif period == '7d':
            start_date = now - timedelta(days=7)
        elif period == '30d':
            start_date = now - timedelta(days=30)
        else:
            start_date = None

        # 쿼리 시작
        query = session.query(BusinessDiscoveryHistory)

        if start_date:
            query = query.filter(BusinessDiscoveryHistory.discovered_at >= start_date)

        # 점수 필터
        if score_filter == '90+':
            query = query.filter(BusinessDiscoveryHistory.total_score >= 90)
        elif score_filter == '80-89':
            query = query.filter(BusinessDiscoveryHistory.total_score >= 80, BusinessDiscoveryHistory.total_score < 90)
        elif score_filter == '70-79':
            query = query.filter(BusinessDiscoveryHistory.total_score >= 70, BusinessDiscoveryHistory.total_score < 80)
        elif score_filter == '60-79':
            query = query.filter(BusinessDiscoveryHistory.total_score >= 60, BusinessDiscoveryHistory.total_score < 80)
        elif score_filter == '60-69':
            query = query.filter(BusinessDiscoveryHistory.total_score >= 60, BusinessDiscoveryHistory.total_score < 70)
        elif score_filter == '0-59':
            query = query.filter(BusinessDiscoveryHistory.total_score < 60)
        elif score_filter == '60-':
            query = query.filter(BusinessDiscoveryHistory.total_score < 60)

        # 카테고리 필터
        if category_filter != 'all':
            query = query.filter(BusinessDiscoveryHistory.category == category_filter)

        # 검색
        if search:
            query = query.filter(BusinessDiscoveryHistory.business_name.ilike(f'%{search}%'))

        # 정렬 및 제한
        histories = query.order_by(BusinessDiscoveryHistory.discovered_at.desc()).limit(limit).all()

        # 결과 변환
        result = []
        for h in histories:
            result.append({
                'id': h.id,
                'discovered_at': h.discovered_at.isoformat() if h.discovered_at else None,
                'business_name': h.business_name,
                'business_type': h.business_type,
                'category': h.category,
                'keyword': h.keyword,
                'total_score': h.total_score or 0,
                'market_score': h.market_score or 0,
                'revenue_score': h.revenue_score or 0,
                'saved_to_db': h.saved_to_db,
                'discovery_batch': h.discovery_batch,
                'analysis_duration_ms': h.analysis_duration_ms
            })

        return jsonify(result)
    finally:
        session.close()

@app.route('/api/business-history/insights')
def api_business_history_insights():
    """인사이트 목록 API"""
    session = Session()
    try:
        status = request.args.get('status', 'new')
        limit = int(request.args.get('limit', 20))

        query = session.query(BusinessInsight)

        if status != 'all':
            query = query.filter(BusinessInsight.status == status)

        insights = query.order_by(BusinessInsight.created_at.desc()).limit(limit).all()

        result = []
        for insight in insights:
            result.append({
                'id': insight.id,
                'created_at': insight.created_at.isoformat() if insight.created_at else None,
                'insight_type': insight.insight_type,
                'category': insight.category,
                'title': insight.title,
                'description': insight.description,
                'impact_level': insight.impact_level,
                'confidence_score': insight.confidence_score,
                'actionable': insight.actionable,
                'suggested_actions': insight.suggested_actions,
                'status': insight.status
            })

        return jsonify(result)
    finally:
        session.close()

@app.route('/api/business-history/categories')
def api_business_history_categories():
    """카테고리별 분포 API"""
    session = Session()
    try:
        days = int(request.args.get('days', 7))
        start_date = datetime.utcnow() - timedelta(days=days)

        histories = session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.discovered_at >= start_date
        ).all()

        categories = {}
        for h in histories:
            cat = h.category or 'Unknown'
            categories[cat] = categories.get(cat, 0) + 1

        return jsonify(categories)
    finally:
        session.close()

@app.route('/api/business-history/snapshots')
def api_business_history_snapshots():
    """스냅샷 목록 API"""
    session = Session()
    try:
        snapshot_type = request.args.get('type', 'hourly')
        limit = int(request.args.get('limit', 24))

        snapshots = session.query(BusinessAnalysisSnapshot).filter(
            BusinessAnalysisSnapshot.snapshot_type == snapshot_type
        ).order_by(BusinessAnalysisSnapshot.snapshot_time.desc()).limit(limit).all()

        result = []
        for s in snapshots:
            result.append({
                'id': s.id,
                'snapshot_time': s.snapshot_time.isoformat() if s.snapshot_time else None,
                'snapshot_type': s.snapshot_type,
                'total_analyzed': s.total_analyzed,
                'total_saved': s.total_saved,
                'avg_total_score': s.avg_total_score,
                'avg_market_score': s.avg_market_score,
                'avg_revenue_score': s.avg_revenue_score,
                'category_distribution': s.category_distribution,
                'score_distribution': s.score_distribution,
                'top_businesses': s.top_businesses,
                'trending_keywords': s.trending_keywords
            })

        return jsonify(result)
    finally:
        session.close()

@app.route('/api/business-history/trends')
def api_business_history_trends():
    """트렌드 분석 API"""
    session = Session()
    try:
        days = int(request.args.get('days', 30))
        start_date = datetime.utcnow() - timedelta(days=days)

        # 일별 통계
        from sqlalchemy import func, cast, Date
        daily_stats = session.query(
            cast(BusinessDiscoveryHistory.discovered_at, Date).label('date'),
            func.count(BusinessDiscoveryHistory.id).label('total'),
            func.avg(BusinessDiscoveryHistory.total_score).label('avg_score'),
            func.sum(func.cast(BusinessDiscoveryHistory.saved_to_db, Integer)).label('saved_count')
        ).filter(
            BusinessDiscoveryHistory.discovered_at >= start_date
        ).group_by(
            cast(BusinessDiscoveryHistory.discovered_at, Date)
        ).order_by('date').all()

        result = []
        for stat in daily_stats:
            result.append({
                'date': stat.date.isoformat() if stat.date else None,
                'total': stat.total or 0,
                'avg_score': round(stat.avg_score, 2) if stat.avg_score else 0,
                'saved_count': stat.saved_count or 0
            })

        return jsonify(result)
    finally:
        session.close()


@app.route('/api/low-score-businesses/list')
def api_low_score_businesses_list():
    """60점 미만 사업 목록 API"""
    from business_discovery_history import LowScoreBusiness
    session = Session()
    try:
        # 필터 파라미터
        days = int(request.args.get('days', 7))
        failure_reason = request.args.get('failure_reason', 'all')
        category = request.args.get('category', 'all')
        limit = int(request.args.get('limit', 50))

        start_date = datetime.utcnow() - timedelta(days=days)

        query = session.query(LowScoreBusiness).filter(
            LowScoreBusiness.created_at >= start_date
        )

        if failure_reason != 'all':
            query = query.filter(LowScoreBusiness.failure_reason == failure_reason)

        if category != 'all':
            query = query.filter(LowScoreBusiness.category == category)

        businesses = query.order_by(
            LowScoreBusiness.created_at.desc()
        ).limit(limit).all()

        result = []
        for biz in businesses:
            result.append({
                'id': biz.id,
                'business_name': biz.business_name,
                'business_type': biz.business_type,
                'category': biz.category,
                'keyword': biz.keyword,
                'total_score': biz.total_score,
                'market_score': biz.market_score,
                'revenue_score': biz.revenue_score,
                'failure_reason': biz.failure_reason,
                'improvement_suggestions': biz.improvement_suggestions,
                'created_at': biz.created_at.isoformat() if biz.created_at else None,
                'discovery_batch': biz.discovery_batch,
                'analysis_duration_ms': biz.analysis_duration_ms
            })

        return jsonify({
            'total': len(result),
            'businesses': result
        })
    finally:
        session.close()


@app.route('/api/low-score-businesses/stats')
def api_low_score_businesses_stats():
    """60점 미만 사업 통계 API"""
    tracker = BusinessHistoryTracker()
    try:
        days = int(request.args.get('days', 7))
        stats = tracker.get_low_score_stats(days=days)
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/low-score-businesses/detail/<int:business_id>')
def api_low_score_business_detail(business_id):
    """60점 미만 사업 상세 정보 API"""
    from business_discovery_history import LowScoreBusiness
    session = Session()
    try:
        biz = session.query(LowScoreBusiness).filter_by(id=business_id).first()

        if not biz:
            return jsonify({'error': 'Business not found'}), 404

        return jsonify({
            'id': biz.id,
            'business_name': biz.business_name,
            'business_type': biz.business_type,
            'category': biz.category,
            'keyword': biz.keyword,
            'total_score': biz.total_score,
            'market_score': biz.market_score,
            'revenue_score': biz.revenue_score,
            'failure_reason': biz.failure_reason,
            'market_analysis': biz.market_analysis,
            'revenue_analysis': biz.revenue_analysis,
            'improvement_suggestions': biz.improvement_suggestions,
            'created_at': biz.created_at.isoformat() if biz.created_at else None,
            'discovery_batch': biz.discovery_batch,
            'analysis_duration_ms': biz.analysis_duration_ms,
            'full_data': biz.full_data
        })
    finally:
        session.close()

# ==================== 백그라운드 작업 ====================

def background_sync_parser():
    """백그라운드에서 주기적으로 sync.log 파싱"""
    while True:
        try:
            parse_sync_log()
        except Exception as e:
            print(f"Background parser error: {e}")
        time.sleep(30)  # 30초마다 파싱


def background_meeting_generator():
    """백그라운드에서 매시간 회의 생성"""
    from stable_hourly_meeting import StableHourlyMeeting
    import logging

    logging.info("[BACKGROUND] Starting hourly meeting generator...")
    print("[BACKGROUND] Starting hourly meeting generator...")

    system = StableHourlyMeeting()
    last_hour = -1


    while True:
        try:
            now = datetime.now()
            current_hour = now.hour
            current_minute = now.minute

            # 매시간 00분에 실행
            if current_minute == 0 and current_hour != last_hour:
                logging.info(f"[MEETING] Generating meeting at {now}")
                print(f"[MEETING] Generating meeting at {now}")
                system.conduct_hourly_meeting()
                last_hour = current_hour
                time.sleep(60)
            else:
                # 30초마다 체크
                time.sleep(30)
        except Exception as e:
            logging.error(f"Meeting generator error: {e}")
            print(f"Meeting generator error: {e}")
            time.sleep(60)


def background_business_discovery():
    """백그라운드에서 8시간마다 사업 발굴 (설정 기반 스케줄)"""
    import logging

    # 설정에서 스케줄 가져오기
    scheduled_hours = DiscoveryConfig.get_schedule_hours()

    logging.info(f"[BACKGROUND] Starting business discovery (schedule: {scheduled_hours})...")
    print(f"[BACKGROUND] Starting business discovery (schedule: {scheduled_hours})...")

    discovery = None
    last_run_hour = -1
    error_count = 0

    while True:
        try:
            now = datetime.now()
            current_hour = now.hour
            current_minute = now.minute

            # 지정된 시간 정각 근처(0~2분)에 실행, 중복 방지
            if current_hour in scheduled_hours and current_minute <= 2 and current_hour != last_run_hour:
                logging.info(f"[DISCOVERY] Running scheduled discovery at {now}")
                print(f"\n" + "="*80)
                print(f"[DISCOVERY] Running discovery at {now.strftime('%Y-%m-%d %H:%M:%S')}")
                print("="*80)

                # 매번 새로운 discovery 인스턴스 생성 (DB 연결 갱신)
                try:
                    discovery = ContinuousBusinessDiscovery()
                    results = discovery.run_hourly_discovery()

                    logging.info(f"[DISCOVERY] Results: analyzed={results.get('analyzed', 0)}, saved={results.get('saved', 0)}")
                    print(f"\n[RESULTS] Analyzed: {results.get('analyzed', 0)}, Saved: {results.get('saved', 0)}")

                    if results['saved'] > 0:
                        discovery.generate_discovery_meeting(results)

                    error_count = 0  # 성공 시 에러 카운트 리셋
                except Exception as inner_e:
                    print(f"[DISCOVERY] Inner error: {inner_e}")
                    error_count += 1
                    # DB 연결 정리
                    try:
                        engine.dispose()
                    except:
                        pass

                last_run_hour = current_hour

                # 다음 실행 시간 계산
                next_hours = [h for h in scheduled_hours if h > current_hour]
                next_hour = next_hours[0] if next_hours else scheduled_hours[0]
                print(f"[NEXT] Next discovery at {next_hour:02d}:00")
                print("="*80 + "\n")

                time.sleep(180)  # 3분 대기 (정각 근처 중복 실행 방지)
            else:
                time.sleep(30)  # 30초마다 체크

        except Exception as e:
            logging.error(f"Discovery error: {e}")
            print(f"\n[ERROR] Discovery error: {e}\n")
            error_count += 1
            # 연속 오류 시 더 오래 대기
            wait_time = min(300, 60 * error_count)  # 최대 5분
            print(f"[WAIT] Waiting {wait_time}s before retry (error count: {error_count})")
            time.sleep(wait_time)


# 백그라운드 스레드 자동 시작 (Gunicorn에서도 작동)
def start_background_threads():
    """백그라운드 스레드 시작"""
    print("[STARTUP] Waiting 30 seconds...")
    time.sleep(30)
    print("[STARTUP] Starting background threads now...")
    # Sync parser thread
    parser_thread = Thread(target=background_sync_parser, daemon=True)
    parser_thread.start()
    print("[STARTUP] Background sync parser started")

    # Meeting generator thread
    meeting_thread = Thread(target=background_meeting_generator, daemon=True)
    meeting_thread.start()
    print("[STARTUP] Background meeting generator started")

    # Business discovery thread - 설정 기반 스케줄
    discovery_thread = Thread(target=background_business_discovery, daemon=True)
    discovery_thread.start()
    schedule = DiscoveryConfig.get_schedule_hours()
    print(f"[STARTUP] Background business discovery ENABLED - Schedule: {schedule} (KST)")

# ============================================
# 창업 지원사업 관련 라우트
# ============================================

@app.route('/startup-support')
def startup_support():
    """1인 창업 지원사업 탐색 페이지"""
    return render_template('startup_support.html')

@app.route('/api/startup-support/programs')
def api_startup_support_programs():
    """모든 창업 지원사업 조회"""
    try:
        crawler = StartupSupportCrawler()
        programs = crawler.get_all_support_programs()
        return jsonify(programs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/startup-support/recommend', methods=['POST'])
def api_startup_support_recommend():
    """사용자 맞춤 지원사업 추천"""
    try:
        user_profile = request.json
        crawler = StartupSupportCrawler()
        recommendations = crawler.get_recommended_programs(user_profile)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/startup-support/search')
def api_startup_support_search():
    """지원사업 검색"""
    try:
        keyword = request.args.get('keyword')
        category = request.args.get('category')
        max_amount = request.args.get('max_amount')

        crawler = StartupSupportCrawler()
        results = crawler.search_programs(
            keyword=keyword,
            category=category,
            max_amount=max_amount
        )
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============= 창업 로드맵 API =============

@app.route('/api/startup-roadmap/phases')
def api_roadmap_phases():
    """창업 로드맵 단계 조회"""
    phases = [
        {
            'id': 1,
            'title': '아이디어 검증',
            'description': '시장 조사 및 아이디어 검증 단계',
            'status': 'completed',
            'progress': 100,
            'tasks': [
                {'id': 1, 'title': '시장 조사 및 경쟁 분석', 'done': True},
                {'id': 2, 'title': '타겟 고객 정의', 'done': True},
                {'id': 3, 'title': '문제점/솔루션 가설 수립', 'done': True},
                {'id': 4, 'title': 'AI 사업 아이디어 발굴', 'done': True}
            ]
        },
        {
            'id': 2,
            'title': '사업 계획 수립',
            'description': '비즈니스 모델 및 사업계획서 작성',
            'status': 'in_progress',
            'progress': 40,
            'tasks': [
                {'id': 5, 'title': '비즈니스 모델 캔버스 작성', 'done': True},
                {'id': 6, 'title': '수익 모델 설계', 'done': True},
                {'id': 7, 'title': '사업계획서 작성', 'done': False},
                {'id': 8, 'title': '재무 계획 수립', 'done': False},
                {'id': 9, 'title': '창업 지원사업 신청', 'done': False}
            ]
        },
        {
            'id': 3,
            'title': '법인 설립 & 준비',
            'description': '사업자 등록 및 법인 설립',
            'status': 'pending',
            'progress': 0,
            'tasks': [
                {'id': 10, 'title': '사업자 등록 (개인/법인)', 'done': False},
                {'id': 11, 'title': '사업장 확보', 'done': False},
                {'id': 12, 'title': '통장/카드 개설', 'done': False},
                {'id': 13, 'title': '필요 인허가 취득', 'done': False}
            ]
        },
        {
            'id': 4,
            'title': 'MVP 개발',
            'description': '최소 기능 제품 개발 및 테스트',
            'status': 'pending',
            'progress': 0,
            'tasks': [
                {'id': 14, 'title': '핵심 기능 정의', 'done': False},
                {'id': 15, 'title': '프로토타입 개발', 'done': False},
                {'id': 16, 'title': '베타 테스트', 'done': False},
                {'id': 17, 'title': '피드백 반영', 'done': False}
            ]
        },
        {
            'id': 5,
            'title': '런칭 & 성장',
            'description': '제품 출시 및 성장 전략 실행',
            'status': 'pending',
            'progress': 0,
            'tasks': [
                {'id': 18, 'title': '마케팅 전략 실행', 'done': False},
                {'id': 19, 'title': '첫 고객 확보', 'done': False},
                {'id': 20, 'title': '피드백 수집 및 개선', 'done': False},
                {'id': 21, 'title': '스케일업 준비', 'done': False}
            ]
        }
    ]
    return jsonify(phases)

@app.route('/api/startup-roadmap/stats')
def api_roadmap_stats():
    """창업 로드맵 통계"""
    stats = {
        'current_phase': 2,
        'current_phase_name': '사업 계획 수립',
        'completed_tasks': 6,
        'total_tasks': 21,
        'overall_progress': 29,
        'days_elapsed': 15,
        'next_milestone': '사업계획서 작성 완료'
    }
    return jsonify(stats)

@app.route('/api/startup-roadmap/weekly-tasks')
def api_roadmap_weekly_tasks():
    """이번 주 할 일 목록"""
    tasks = [
        {'id': 1, 'title': '사업계획서 초안 작성', 'priority': 'high', 'done': False},
        {'id': 2, 'title': '창업지원센터 상담 예약', 'priority': 'high', 'done': False},
        {'id': 3, 'title': '시장 규모 조사', 'priority': 'medium', 'done': True},
        {'id': 4, 'title': '경쟁사 분석 자료 정리', 'priority': 'medium', 'done': False},
        {'id': 5, 'title': '예비창업패키지 지원 조건 확인', 'priority': 'low', 'done': False}
    ]
    return jsonify(tasks)

@app.route('/api/startup-roadmap/task/<int:task_id>', methods=['PUT'])
def api_roadmap_update_task(task_id):
    """태스크 상태 업데이트"""
    data = request.get_json()
    done = data.get('done', False)
    # 실제로는 DB에 저장하지만 현재는 더미 응답
    return jsonify({
        'success': True,
        'task_id': task_id,
        'done': done
    })

# ============= 데이터 정리 API (DB 비용 최적화) =============

@app.route('/api/cleanup/old-data', methods=['POST'])
def api_cleanup_old_data():
    """오래된 데이터 정리 (DB 비용 최적화)

    정리 대상:
    - ActivityLog: 30일 이상 된 로그
    - SyncLog: 30일 이상 된 로그
    - BusinessDiscoveryHistory: 90일 이상 된 히스토리
    - BusinessAnalysisSnapshot: 90일 이상 된 스냅샷
    """
    session = Session()
    try:
        cleanup_results = {}
        now = datetime.now()

        # 1. ActivityLog 정리 (30일 이상)
        try:
            cutoff_30days = now - timedelta(days=30)
            deleted_activity = session.query(ActivityLog).filter(
                ActivityLog.timestamp < cutoff_30days
            ).delete(synchronize_session=False)
            cleanup_results['activity_logs'] = deleted_activity
        except Exception as e:
            cleanup_results['activity_logs'] = f'error: {str(e)}'

        # 2. SyncLog 정리 (30일 이상)
        try:
            deleted_sync = session.query(SyncLog).filter(
                SyncLog.timestamp < cutoff_30days
            ).delete(synchronize_session=False)
            cleanup_results['sync_logs'] = deleted_sync
        except Exception as e:
            cleanup_results['sync_logs'] = f'error: {str(e)}'

        # 3. BusinessDiscoveryHistory 정리 (90일 이상)
        try:
            cutoff_90days = now - timedelta(days=90)
            deleted_history = session.query(BusinessDiscoveryHistory).filter(
                BusinessDiscoveryHistory.discovered_at < cutoff_90days
            ).delete(synchronize_session=False)
            cleanup_results['discovery_history'] = deleted_history
        except Exception as e:
            cleanup_results['discovery_history'] = f'error: {str(e)}'

        # 4. BusinessAnalysisSnapshot 정리 (90일 이상)
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

@app.route('/api/cleanup/stats')
def api_cleanup_stats():
    """정리 대상 데이터 통계 조회"""
    session = Session()
    try:
        now = datetime.now()
        cutoff_30days = now - timedelta(days=30)
        cutoff_90days = now - timedelta(days=90)

        stats = {}

        # 정리 대상 레코드 수 조회
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

        # 총 정리 가능 레코드
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

# 인증 라우트 등록
create_auth_routes(app)
print("[STARTUP] Auth routes registered")

# Production 환경 (Gunicorn)에서도 백그라운드 스레드 시작
# 별도 스레드에서 실행하여 서버 시작을 블로킹하지 않도록 함
startup_thread = Thread(target=start_background_threads, daemon=True)
startup_thread.start()
print("[STARTUP] Background initialization thread started (non-blocking)")

# 백그라운드 스레드 시작
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)