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
    """Qhyx Inc. 메인 웹사이트"""
    return render_template('qhyx_main.html')

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

# 백그라운드 작업
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

# Production 환경 (Gunicorn)에서도 백그라운드 스레드 시작
start_background_threads()

# 백그라운드 스레드 시작
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)