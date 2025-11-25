"""
Qhyx Inc. 비즈니스 모니터링 및 상태 확인
현재 진행중인 모든 비즈니스 활동을 확인하고 리포트 생성
"""

from database_setup import Session, BusinessMeeting, BusinessPlan, ActivityLog, CompanyMilestone, CompanyMetric, Employee, Task
from datetime import datetime, timedelta
import json

class QhyxBusinessMonitor:
    def __init__(self):
        self.session = Session()
    
    def get_current_status(self):
        """현재 Qhyx Inc. 상태 종합 리포트"""
        today = datetime.now().date()
        
        # 오늘의 활동
        today_meetings = self.session.query(BusinessMeeting).filter(
            BusinessMeeting.meeting_date >= today
        ).count()
        
        today_tasks = self.session.query(Task).filter(
            Task.created_at >= today
        ).count()
        
        today_metrics = self.session.query(CompanyMetric).filter(
            CompanyMetric.date >= today
        ).count()
        
        # 진행중인 업무
        active_tasks = self.session.query(Task).filter(
            Task.status.in_(['pending', 'in_progress'])
        ).count()
        
        completed_tasks = self.session.query(Task).filter(
            Task.status == 'completed'
        ).count()
        
        # AI 직원 현황
        active_employees = self.session.query(Employee).filter(
            Employee.status == 'active'
        ).count()
        
        # 사업 계획 현황
        approved_plans = self.session.query(BusinessPlan).filter(
            BusinessPlan.status == 'approved'
        ).count()
        
        in_progress_plans = self.session.query(BusinessPlan).filter(
            BusinessPlan.status == 'in_progress'
        ).count()
        
        # 최근 마일스톤
        recent_milestones = self.session.query(CompanyMilestone).order_by(
            CompanyMilestone.achieved_at.desc()
        ).limit(3).all()
        
        report = f"""
🏢 ===== Qhyx Inc. 실시간 비즈니스 현황 =====

[DATE] 오늘의 활동 [{today.strftime('%Y-%m-%d')}]:
  • 진행된 회의: {today_meetings}건
  • 생성된 업무: {today_tasks}건  
  • 업데이트된 지표: {today_metrics}건

💼 업무 현황:
  • 진행중/대기중 업무: {active_tasks}건
  • 완료된 업무: {completed_tasks}건
  • 업무 완료율: {completed_tasks/(active_tasks + completed_tasks)*100:.1f}% (전체 기준)

👥 조직 현황:
  • 활성 AI 직원: {active_employees}명
  • 승인된 사업 계획: {approved_plans}개
  • 진행중인 사업 계획: {in_progress_plans}개

[TOP] 최근 마일스톤:
        """
        
        for milestone in recent_milestones:
            report += f"  • {milestone.title} (영향도: {milestone.impact_score}/10)\n"
        
        report += f"""
⏰ 시스템 상태: 24/7 자동 운영 중
[REFRESH] 다음 스케줄:
  • 오전 9시: 일일 전략 회의
  • 오후 2시: 지표 업데이트
  • 오후 6시: 일일 리뷰
  • 매시 정각: 지표 모니터링

[IDEA] Qhyx Inc.는 잠들어 있는 동안에도 계속 성장합니다!
        """
        
        return report
    
    def get_recent_activities(self, hours=24):
        """최근 활동 내역"""
        since = datetime.now() - timedelta(hours=hours)
        
        # 최근 회의들
        meetings = self.session.query(BusinessMeeting).filter(
            BusinessMeeting.meeting_date >= since
        ).order_by(BusinessMeeting.meeting_date.desc()).all()
        
        # 최근 업무들
        tasks = self.session.query(Task).filter(
            Task.created_at >= since
        ).order_by(Task.created_at.desc()).limit(10).all()
        
        activities = f"""
[LIST] 최근 {hours}시간 활동 내역:

🏢 회의 활동:
        """
        
        for meeting in meetings:
            activities += f"  • [{meeting.meeting_date.strftime('%m/%d %H:%M')}] {meeting.title}\n"
            if meeting.key_decisions:
                activities += f"    주요 결정: {len(meeting.key_decisions)}건\n"
        
        activities += "\n💼 업무 활동:\n"
        for task in tasks:
            activities += f"  • [{task.created_at.strftime('%m/%d %H:%M')}] {task.title} ({task.status})\n"
        
        return activities
    
    def get_performance_metrics(self):
        """성과 지표 요약"""
        # 최근 일주일 지표
        week_ago = datetime.now() - timedelta(days=7)
        
        metrics = self.session.query(CompanyMetric).filter(
            CompanyMetric.date >= week_ago.date()
        ).all()
        
        if not metrics:
            return "[DATA] 성과 지표: 데이터 수집 중..."
        
        # 카테고리별 최근 평균
        categories = {}
        for metric in metrics:
            if metric.category not in categories:
                categories[metric.category] = []
            categories[metric.category].append(metric.value)
        
        performance = "[DATA] 주요 성과 지표 (최근 7일 평균):\n"
        
        for category, values in categories.items():
            avg_value = sum(values) / len(values)
            performance += f"  • {category}: {avg_value:.1f}\n"
        
        return performance
    
    def close(self):
        self.session.close()

def show_live_status():
    """실시간 상태 표시"""
    monitor = QhyxBusinessMonitor()
    
    try:
        print(monitor.get_current_status())
        print("\n" + "="*60)
        print(monitor.get_recent_activities())
        print("\n" + "="*60) 
        print(monitor.get_performance_metrics())
        
    finally:
        monitor.close()

if __name__ == "__main__":
    show_live_status()