"""
데이터베이스 데이터 검증 스크립트
"""
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from database_setup import (
    BusinessPlan, BusinessMeeting, Employee, Task,
    EmployeeSuggestion, Revenue, CompanyMetric,
    CompanyMilestone, SCHEMA_NAME
)
from datetime import datetime, timedelta

# DB 연결
connection_string = URL.create(
    'postgresql',
    username='unble',
    password='npg_1kjV0mhECxqs',
    host='ep-divine-bird-a1f4mly5.ap-southeast-1.pg.koyeb.app',
    database='unble',
)

engine = create_engine(connection_string, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

def verify_data():
    session = Session()
    try:
        print("="*60)
        print("데이터베이스 검증 시작")
        print("="*60)

        # 1. AI 직원 수
        employee_count = session.query(Employee).count()
        print(f"\n[직원] 총 {employee_count}명")

        employees = session.query(Employee).limit(3).all()
        for emp in employees:
            print(f"  - {emp.name} ({emp.role})")

        # 2. 사업 계획
        plan_count = session.query(BusinessPlan).count()
        print(f"\n[사업 계획] 총 {plan_count}개")

        plans = session.query(BusinessPlan).all()
        for plan in plans:
            print(f"  - {plan.plan_name}")
            print(f"    상태: {plan.status}, 예상 수익: {plan.projected_revenue_12m:,}원")

        # 3. 회의록 (날짜별)
        meeting_count = session.query(BusinessMeeting).count()
        print(f"\n[회의록] 총 {meeting_count}건")

        # 최근 3개월 회의록
        three_months_ago = datetime.now() - timedelta(days=90)
        recent_meetings = session.query(BusinessMeeting).filter(
            BusinessMeeting.meeting_date >= three_months_ago
        ).order_by(BusinessMeeting.meeting_date.desc()).limit(5).all()

        print("  최근 회의:")
        for meeting in recent_meetings:
            print(f"  - {meeting.meeting_date.strftime('%Y-%m-%d')}: {meeting.title}")

        # 날짜 범위 확인
        oldest_meeting = session.query(BusinessMeeting).order_by(
            BusinessMeeting.meeting_date.asc()
        ).first()
        newest_meeting = session.query(BusinessMeeting).order_by(
            BusinessMeeting.meeting_date.desc()
        ).first()

        if oldest_meeting and newest_meeting:
            print(f"\n  회의 날짜 범위:")
            print(f"  - 가장 오래된 회의: {oldest_meeting.meeting_date.strftime('%Y-%m-%d')}")
            print(f"  - 가장 최근 회의: {newest_meeting.meeting_date.strftime('%Y-%m-%d')}")

        # 4. 건의사항
        suggestion_count = session.query(EmployeeSuggestion).count()
        print(f"\n[건의사항] 총 {suggestion_count}건")

        suggestions = session.query(EmployeeSuggestion).limit(3).all()
        for sug in suggestions:
            print(f"  - {sug.title} (상태: {sug.status})")

        # 5. 수익 데이터
        revenue_count = session.query(Revenue).count()
        total_revenue = session.query(Revenue).with_entities(
            Revenue.amount
        ).all()

        total = sum([r.amount for r in total_revenue])
        print(f"\n[수익] 총 {revenue_count}건, 누적: {total:,.0f}원")

        # 최근 수익
        recent_revenue = session.query(Revenue).order_by(
            Revenue.date.desc()
        ).limit(5).all()

        print("  최근 수익:")
        for rev in recent_revenue:
            print(f"  - {rev.date}: {rev.source} - {rev.amount:,.0f}원")

        # 6. 지표
        metric_count = session.query(CompanyMetric).count()
        print(f"\n[성장 지표] 총 {metric_count}건")

        # 7. 마일스톤
        milestone_count = session.query(CompanyMilestone).count()
        print(f"\n[마일스톤] 총 {milestone_count}개")

        milestones = session.query(CompanyMilestone).order_by(
            CompanyMilestone.achieved_at.desc()
        ).all()

        for ms in milestones:
            print(f"  - {ms.achieved_at.strftime('%Y-%m-%d')}: {ms.title}")

        print("\n" + "="*60)
        print("[결과] 데이터가 정상적으로 생성되었습니다!")
        print("="*60)

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    verify_data()
