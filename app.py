from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
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

# Koyeb PostgreSQL 연결
connection_string = URL.create(
    'postgresql',
    username='unble',
    password='npg_1kjV0mhECxqs',
    host='ep-divine-bird-a1f4mly5.ap-southeast-1.pg.koyeb.app',
    database='unble',
)

engine = create_engine(
    connection_string,
    pool_pre_ping=True,
    pool_recycle=3600,  # 연결 1시간마다 재생성 (SSL 타임아웃 방지)
    pool_size=10,
    max_overflow=20
)
Session = sessionmaker(bind=engine)

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
        
        suggestion_list = []
        for suggestion in suggestions:
            # 직원 정보 가져오기
            employee = session.query(Employee).filter_by(employee_id=suggestion.employee_id).first()
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
        
        # AI 직원 현황
        employees = session.query(Employee).filter_by(status='active').all()
        employee_data = []
        for emp in employees:
            emp_tasks = session.query(Task).filter_by(assigned_to=emp.employee_id).count()
            employee_data.append({
                'name': emp.name,
                'role': emp.role,
                'status': emp.status,
                'tasks': emp_tasks
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

@app.route('/api/discovered-businesses')
def api_discovered_businesses():
    """자동 발굴된 사업 목록 API (60점 이상 모두 포함)"""
    session = Session()
    try:
        # BusinessDiscoveryHistory에서 60점 이상 사업 모두 조회
        histories = session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.total_score >= 60
        ).order_by(BusinessDiscoveryHistory.discovered_at.desc()).limit(100).all()

        business_list = []
        for biz in histories:
            # 월 매출 추정 (간단한 계산)
            monthly_revenue = biz.total_score * 100000  # 점수 * 10만원
            annual_revenue = monthly_revenue * 12
            investment = biz.total_score * 50000  # 점수 * 5만원

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
                'description': f"{biz.business_name} - 시장성 {biz.market_score:.1f}점, 수익성 {biz.revenue_score:.1f}점",
                'revenue_model': 'subscription',
                'details': {
                    'analysis_score': biz.total_score,
                    'market_score': biz.market_score,
                    'revenue_score': biz.revenue_score,
                    'category': biz.category,
                    'keyword': biz.keyword,
                    'market_analysis': biz.market_analysis,
                    'revenue_analysis': biz.revenue_analysis
                }
            })

        # 통계
        today = datetime.utcnow().date()
        today_count = session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.total_score >= 60,
            BusinessDiscoveryHistory.discovered_at >= today
        ).count()

        week_ago = datetime.utcnow() - timedelta(days=7)
        week_count = session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.total_score >= 60,
            BusinessDiscoveryHistory.discovered_at >= week_ago
        ).count()

        high_score_count = len([b for b in business_list if b['score'] >= 85])

        return jsonify({
            'businesses': business_list,
            'stats': {
                'total': len(business_list),
                'today': today_count,
                'this_week': week_count,
                'high_score': high_score_count
            }
        })
    finally:
        session.close()

@app.route('/api/trigger-discovery', methods=['GET', 'POST'])
def trigger_discovery():
    """수동으로 사업 발굴 트리거 (즉시 실행)"""
    try:
        from continuous_business_discovery import ContinuousBusinessDiscovery

        discovery = ContinuousBusinessDiscovery()
        results = discovery.run_once_now()

        return jsonify({
            'success': True,
            'message': '사업 발굴 실행 완료',
            'results': {
                'analyzed': results.get('analyzed', 0),
                'saved': results.get('saved', 0),
                'timestamp': results.get('timestamp')
            }
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

@app.route('/api/low-score-businesses/list')
def api_low_score_businesses():
    """낮은 점수 사업 목록 API (60점 미만)"""
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

    # 시작하자마자 한번 실행
    try:
        system.conduct_hourly_meeting()
    except Exception as e:
        logging.error(f"Initial meeting failed: {e}")
        print(f"Initial meeting failed: {e}")

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
    """백그라운드에서 지속적으로 사업 발굴"""
    import logging
    logging.info("[BACKGROUND] Starting continuous business discovery...")
    print("[BACKGROUND] Starting continuous business discovery...")

    discovery = ContinuousBusinessDiscovery()
    last_hour = -1

    while True:
        try:
            now = datetime.now()
            current_hour = now.hour
            current_minute = now.minute

            # 매시간 정각 근처(0~2분)에 실행, 중복 방지
            if current_minute <= 2 and current_hour != last_hour:
                logging.info(f"[DISCOVERY] Running hourly discovery at {now}")
                print(f"\n" + "="*80)
                print(f"[DISCOVERY] Running hourly discovery at {now.strftime('%Y-%m-%d %H:%M:%S')}")
                print("="*80)

                results = discovery.run_hourly_discovery()

                logging.info(f"[DISCOVERY] Results: analyzed={results.get('analyzed', 0)}, saved={results.get('saved', 0)}")
                print(f"\n[RESULTS] Analyzed: {results.get('analyzed', 0)}, Saved: {results.get('saved', 0)}")

                if results['saved'] > 0:
                    discovery.generate_discovery_meeting(results)

                last_hour = current_hour
                print(f"[NEXT] Next discovery at {(now + timedelta(hours=1)).strftime('%H:00')}")
                print("="*80 + "\n")

                time.sleep(180)  # 3분 대기 (정각 근처 중복 실행 방지)
            else:
                time.sleep(20)  # 20초마다 체크

        except Exception as e:
            logging.error(f"Discovery error: {e}")
            print(f"\n[ERROR] Discovery error: {e}\n")
            import traceback
            traceback.print_exc()
            time.sleep(60)


# 백그라운드 스레드 자동 시작 (Gunicorn에서도 작동)
def start_background_threads():
    """백그라운드 스레드 시작"""
    # Sync parser thread
    parser_thread = Thread(target=background_sync_parser, daemon=True)
    parser_thread.start()
    print("[STARTUP] Background sync parser started")

    # Meeting generator thread
    meeting_thread = Thread(target=background_meeting_generator, daemon=True)
    meeting_thread.start()
    print("[STARTUP] Background meeting generator started")

    # Business discovery thread - 재활성화
    discovery_thread = Thread(target=background_business_discovery, daemon=True)
    discovery_thread.start()
    print("[STARTUP] Background business discovery ENABLED - Running hourly")

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

# Production 환경 (Gunicorn)에서도 백그라운드 스레드 시작
start_background_threads()

# 백그라운드 스레드 시작
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)