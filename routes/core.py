from flask import Blueprint, render_template, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import text, func

from services.db import Session
from services.git_utils import parse_sync_log, get_git_stats, get_sync_status
from database_setup import (
    ActivityLog, SyncLog, CompanyMetric, CompanyMilestone,
    Employee, Task, BusinessMeeting, BusinessPlan, SCHEMA_NAME
)
from config import MarketConfig

core_bp = Blueprint('core', __name__)


@core_bp.route('/')
def index():
    """Qhyx Inc. 메인 홈페이지"""
    return render_template('index.html')


@core_bp.route('/dashboard')
def dashboard():
    """실시간 비즈니스 모니터링 대시보드"""
    return render_template('business_dashboard.html')


@core_bp.route('/business-plan')
def business_plan():
    """TravelMate 사업계획서"""
    return render_template('business_plan.html')


@core_bp.route('/monitor')
def monitor():
    """기존 시스템 모니터링 (호환성)"""
    return render_template('dashboard.html')


@core_bp.route('/api/stats')
def api_stats():
    """통계 API"""
    parse_sync_log()

    session = Session()
    try:
        recent_activities = session.query(ActivityLog).order_by(
            ActivityLog.timestamp.desc()
        ).limit(10).all()

        today = datetime.utcnow().date()
        sync_count = session.query(SyncLog).filter(
            text(f"DATE({SCHEMA_NAME}.sync_logs.timestamp) = :today")
        ).params(today=today).count()

        git_stats = get_git_stats()
        sync_status = get_sync_status()
        milestone_count = session.query(CompanyMilestone).count()
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


@core_bp.route('/api/logs')
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


@core_bp.route('/api/status')
def api_status():
    """시스템 상태 API (메인 웹사이트용)"""
    session = Session()
    try:
        sync_status = get_sync_status()

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


@core_bp.route('/api/dashboard-data')
def api_dashboard_data():
    """비즈니스 대시보드 데이터 API"""
    session = Session()
    try:
        today = datetime.utcnow().date()

        today_meetings = session.query(BusinessMeeting).filter(
            BusinessMeeting.meeting_date >= today
        ).count()

        active_tasks = session.query(Task).filter(
            Task.status.in_(['pending', 'in_progress'])
        ).count()

        today_metrics = session.query(CompanyMetric).filter(
            CompanyMetric.date >= today
        ).count()

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


@core_bp.route('/api/market-config')
def api_market_config():
    """시장 분석 설정 상태 API"""
    config_status = MarketConfig.get_status()
    return jsonify({
        'success': True,
        'config': config_status,
        'message': '환경변수 MARKET_ANALYSIS_MODE=full 설정 시 전체 모드 활성화'
    })
