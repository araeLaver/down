"""
Qhyx Inc. 사업성 검토 회의 진행 및 DB 기록
"""

from database_setup import Session, BusinessMeeting, BusinessPlan, ActivityLog, CompanyMilestone
from datetime import datetime, timedelta
import json

def conduct_business_review_meeting():
    """사업성 검토 회의 진행 및 DB 저장"""
    session = Session()
    
    try:
        # 회의 기록 생성
        meeting = BusinessMeeting(
            meeting_type='사업성검토',
            title='Qhyx Inc. 초기 사업 모델 및 성장 전략 검토',
            agenda='1) Qhyx 회사 비전 재확인 2) 핵심 사업 영역 정의 3) 수익 모델 설계 4) 시장 진입 전략 5) 1년간 성장 계획',
            participants=[
                {'name': '김창의', 'role': 'CCO (Chief Creative Officer)', 'department': 'Innovation'},
                {'name': '박실용', 'role': 'CPO (Chief Practical Officer)', 'department': 'Operations'},
                {'name': '이글로벌', 'role': 'CGO (Chief Global Officer)', 'department': 'Global Expansion'},
                {'name': '정브랜드', 'role': 'CBO (Chief Branding Officer)', 'department': 'Marketing'},
                {'name': '최검증', 'role': 'CVO (Chief Validation Officer)', 'department': 'Quality Assurance'},
                {'name': '신재무', 'role': 'CFO (Chief Financial Officer)', 'department': 'Finance'},
                {'name': '한전략', 'role': 'CSO (Chief Strategy Officer)', 'department': 'Strategy'}
            ],
            status='ongoing'
        )
        session.add(meeting)
        session.commit()
        
        print("🏢 Qhyx Inc. 사업성 검토 회의 시작!")
        print("=" * 60)
        
        # 회의 진행
        meeting_notes = conduct_meeting_discussion()
        
        # 비즈니스 플랜들 생성
        business_plans = create_business_plans(session)
        
        # 회의 완료 업데이트
        meeting.status = 'completed'
        meeting.meeting_notes = meeting_notes
        meeting.key_decisions = [
            "Qhyx는 AI 기반 예측불가능한 솔루션을 제공하는 회사로 포지셔닝",
            "1차 제품: Qhyx Bot (대화형 AI 어시스턴트)",
            "2차 제품: Qhyx Labs (창의적 실험 플랫폼)",
            "3차 제품: Qhyx Studio (맞춤형 AI 솔루션)",
            "목표: 1년 내 월 1억원 매출 달성",
            "투자 유치 목표: 10억원 (Series A)"
        ]
        meeting.action_items = [
            "Qhyx Bot MVP 개발 시작 (2주 내)",
            "브랜딩 가이드라인 완성 (1주 내)", 
            "투자 유치 피칭덱 제작 (3주 내)",
            "파일럿 고객 10명 확보 (1개월 내)",
            "지적재산권 출원 준비 (2개월 내)"
        ]
        meeting.follow_up_date = datetime.now() + timedelta(days=7)
        
        session.commit()
        
        # 마일스톤 추가
        milestone = CompanyMilestone(
            milestone_type='business',
            title='Qhyx Inc. 사업성 검토 회의 완료',
            description='초기 사업 모델, 수익 구조, 성장 전략 수립 완료',
            impact_score=9.0,
            details={
                'total_business_plans': len(business_plans),
                'revenue_target_12m': 1200000000,  # 12억 (월 1억 x 12개월)
                'investment_target': 1000000000,   # 10억
                'key_products': ['Qhyx Bot', 'Qhyx Labs', 'Qhyx Studio']
            }
        )
        session.add(milestone)
        session.commit()
        
        print(f"\n[OK] 회의 기록이 데이터베이스에 저장되었습니다. (Meeting ID: {meeting.id})")
        print(f"[DATA] {len(business_plans)}개의 사업 계획이 생성되었습니다.")
        
        return meeting.id, business_plans
        
    finally:
        session.close()

def conduct_meeting_discussion():
    """회의 토론 내용"""
    print("\n[LIST] 회의 진행")
    print("-" * 40)
    
    discussion = """
    [TARGET] Qhyx Inc. 사업성 검토 회의 결과
    
    1. 회사 비전 및 미션
    - 비전: "예측할 수 없는 혁신으로 세상을 변화시킨다"
    - 미션: "AI 기술로 기존 패러다임을 뒤흔드는 솔루션 제공"
    - 핵심 가치: Quantum(양자적), Hope(희망), Youth(젊음), eXcellence(우수성)
    
    2. 핵심 사업 영역
    - AI 챗봇 및 어시스턴트 솔루션
    - 창의적 실험 및 R&D 플랫폼  
    - 맞춤형 AI 컨설팅 서비스
    - B2B SaaS 솔루션
    
    3. 수익 모델
    - 구독형 SaaS (월 10만원~100만원)
    - 컨설팅 서비스 (프로젝트당 500만원~5,000만원)
    - API 사용료 (호출당 과금)
    - 라이선스 수수료 (매출의 10-20%)
    
    4. 시장 진입 전략
    - 1단계: 스타트업 대상 MVP 출시
    - 2단계: 중소기업 확장
    - 3단계: 대기업 진출
    - 4단계: 글로벌 확장
    
    5. 경쟁 우위
    - "예측불가능성"을 핵심으로 한 독특한 포지셔닝
    - 완전히 검증된 유일한 브랜드명 "Qhyx"
    - AI 기반 창의적 솔루션 특화
    - 빠른 실험과 검증 문화
    """
    
    print(discussion)
    return discussion

def create_business_plans(session):
    """사업 계획들 생성"""
    plans = []
    
    # 1. Qhyx Bot
    plan1 = BusinessPlan(
        plan_name='Qhyx Bot - AI 대화 어시스턴트',
        plan_type='product',
        description='예측불가능한 대화와 창의적 아이디어를 제공하는 AI 챗봇 서비스',
        target_market='스타트업, 개발자, 창작자 (약 50만 잠재고객)',
        revenue_model='월 구독료 10만원, 프리미엄 50만원',
        projected_revenue_12m=600000000,  # 6억 (월 5천만원 x 12개월)
        investment_required=200000000,    # 2억
        risk_level='medium',
        feasibility_score=8.5,
        priority='high',
        status='approved',
        created_by='전체 임원진',
        details={
            'development_time': '3개월',
            'team_size': 5,
            'key_features': ['창의적 대화', '맞춤형 추천', 'API 연동', '다국어 지원'],
            'launch_date': '2025년 1분기'
        }
    )
    
    # 2. Qhyx Labs
    plan2 = BusinessPlan(
        plan_name='Qhyx Labs - 창의 실험 플랫폼',
        plan_type='service',
        description='기업 고객을 위한 AI 기반 창의적 실험 및 혁신 지원 플랫폼',
        target_market='중소기업, 대기업 R&D 부서 (약 1만 기업)',
        revenue_model='프로젝트별 컨설팅 500만원~5000만원',
        projected_revenue_12m=480000000,  # 4.8억 (월 4천만원 x 12개월)
        investment_required=300000000,    # 3억
        risk_level='medium',
        feasibility_score=7.5,
        priority='high',
        status='approved',
        created_by='전체 임원진',
        details={
            'development_time': '4개월',
            'team_size': 8,
            'key_services': ['혁신 워크샵', 'AI 실험', '데이터 분석', '전략 컨설팅'],
            'launch_date': '2025년 2분기'
        }
    )
    
    # 3. Qhyx Studio
    plan3 = BusinessPlan(
        plan_name='Qhyx Studio - 맞춤형 AI 솔루션',
        plan_type='service',
        description='고객별 맞춤형 AI 솔루션 개발 및 운영 서비스',
        target_market='대기업, 정부기관 (약 500개 기관)',
        revenue_model='프로젝트당 1억~10억원, 운영 수수료 월 1천만원',
        projected_revenue_12m=1200000000, # 12억 (대형 프로젝트 위주)
        investment_required=500000000,    # 5억
        risk_level='high',
        feasibility_score=6.5,
        priority='medium',
        status='draft',
        created_by='전체 임원진',
        details={
            'development_time': '6개월',
            'team_size': 12,
            'key_deliverables': ['맞춤형 AI 모델', '시스템 통합', '운영 지원', '교육 서비스'],
            'launch_date': '2025년 3분기'
        }
    )
    
    plans = [plan1, plan2, plan3]
    
    for plan in plans:
        session.add(plan)
        print(f"[LIST] 사업 계획 생성: {plan.plan_name}")
        print(f"   - 예상 매출: {plan.projected_revenue_12m:,}원")
        print(f"   - 투자 필요: {plan.investment_required:,}원")
        print(f"   - 실현성: {plan.feasibility_score}/10")
        print()
    
    session.commit()
    return plans

if __name__ == "__main__":
    meeting_id, plans = conduct_business_review_meeting()
    
    print("\n🎉 Qhyx Inc. 사업성 검토 완료!")
    print(f"💼 회의 ID: {meeting_id}")
    print(f"[DATA] 총 {len(plans)}개 사업 계획 수립")
    print(f"[TARGET] 1년 매출 목표: 12억원")
    print(f"[MONEY] 투자 유치 목표: 10억원")