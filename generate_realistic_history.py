"""
Qhyx Inc. 현실적인 사업 히스토리 데이터 생성기
- 다양한 사업 아이템 (10개 이상)
- 과거 6개월 히스토리
- 실제 스타트업처럼 보이는 데이터
"""

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from database_setup import (
    BusinessPlan, BusinessMeeting, Employee, Task,
    EmployeeSuggestion, Revenue, CompanyMetric,
    ActivityLog, CompanyMilestone, SCHEMA_NAME
)
import random
import json

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

# 다양한 사업 아이템들 (실제로 수익성이 있는 것들)
BUSINESS_PLANS = [
    {
        "name": "AI 챗봇 SaaS 플랫폼",
        "type": "product",
        "description": "중소기업을 위한 맞춤형 AI 고객상담 챗봇 서비스. 간단한 설정만으로 웹사이트에 통합 가능.",
        "target_market": "월 매출 1억-50억 중소기업, 온라인 쇼핑몰, 교육기관",
        "revenue_model": "SaaS 구독형 - Basic(월 9.9만원), Pro(월 29만원), Enterprise(월 89만원)",
        "projected_revenue": 180000000,  # 월 1500만원 x 12개월
        "investment": 45000000,
        "risk": "medium",
        "feasibility": 8.5,
        "status": "in_progress"
    },
    {
        "name": "기업 데이터 분석 자동화 툴",
        "type": "product",
        "description": "Excel/CSV 데이터를 AI가 자동 분석하여 인사이트 리포트 생성. 코딩 불필요.",
        "target_market": "데이터 분석팀이 없는 중소기업, 스타트업",
        "revenue_model": "사용량 기반 요금제 - 월 100건(5만원), 500건(20만원), 무제한(50만원)",
        "projected_revenue": 240000000,  # 월 2000만원 x 12개월
        "investment": 35000000,
        "risk": "medium",
        "feasibility": 8.0,
        "status": "approved"
    },
    {
        "name": "소상공인 마케팅 자동화 플랫폼",
        "type": "service",
        "description": "SNS 콘텐츠 자동 생성, 최적 시간 자동 포스팅, 고객 반응 분석 올인원 서비스.",
        "target_market": "카페, 음식점, 소규모 리테일 매장",
        "revenue_model": "월 구독 - 베이직(4.9만원), 프로(9.9만원), 콘텐츠 제작 대행(별도)",
        "projected_revenue": 156000000,
        "investment": 28000000,
        "risk": "low",
        "feasibility": 9.0,
        "status": "in_progress"
    },
    {
        "name": "개발자 코드 리뷰 AI 어시스턴트",
        "type": "product",
        "description": "GitHub/GitLab 연동 자동 코드 리뷰, 버그 탐지, 최적화 제안.",
        "target_market": "개발 팀이 있는 스타트업, 중견 IT기업",
        "revenue_model": "팀 단위 구독 - 5인(월 15만원), 20인(월 50만원), 엔터프라이즈(협의)",
        "projected_revenue": 300000000,
        "investment": 60000000,
        "risk": "medium",
        "feasibility": 7.5,
        "status": "approved"
    },
    {
        "name": "온라인 교육 콘텐츠 생성기",
        "type": "product",
        "description": "강의 스크립트 입력 시 AI가 슬라이드, 퀴즈, 요약본을 자동 생성.",
        "target_market": "온라인 강사, 기업 교육팀, 학원",
        "revenue_model": "크레딧 기반 - 100크레딧(3만원), 500크레딧(12만원), 무제한(월 30만원)",
        "projected_revenue": 144000000,
        "investment": 30000000,
        "risk": "medium",
        "feasibility": 8.5,
        "status": "in_progress"
    },
    {
        "name": "법률 문서 자동 작성 서비스",
        "type": "service",
        "description": "계약서, 내용증명, 합의서 등을 AI가 자동 생성. 변호사 검토 옵션 제공.",
        "target_market": "중소기업, 개인사업자, 프리랜서",
        "revenue_model": "문서당 과금 - 기본(2만원), 변호사 검토(+10만원), 월정액(월 20만원)",
        "projected_revenue": 216000000,
        "investment": 50000000,
        "risk": "high",
        "feasibility": 7.0,
        "status": "draft"
    },
    {
        "name": "부동산 시세 예측 AI 플랫폼",
        "type": "product",
        "description": "과거 데이터와 AI로 특정 지역 부동산 가격 변동 예측, 투자 인사이트 제공.",
        "target_market": "부동산 투자자, 중개업소, 일반인",
        "revenue_model": "구독형 - 개인(월 1.9만원), 프리미엄(월 4.9만원), 중개사(월 15만원)",
        "projected_revenue": 192000000,
        "investment": 55000000,
        "risk": "high",
        "feasibility": 6.5,
        "status": "draft"
    },
    {
        "name": "HR 채용 면접 자동화 도구",
        "type": "service",
        "description": "AI 화상 면접, 자동 평가, 역량 분석 리포트 제공.",
        "target_market": "중소기업 HR팀, 채용대행 업체",
        "revenue_model": "면접당 과금 - 기본(1만원/명), 심층(3만원/명), 무제한(월 50만원)",
        "projected_revenue": 276000000,
        "investment": 70000000,
        "risk": "medium",
        "feasibility": 7.5,
        "status": "approved"
    },
    {
        "name": "물류 최적화 AI 솔루션",
        "type": "product",
        "description": "배송 경로 최적화, 재고 예측, 물류 비용 절감 솔루션.",
        "target_market": "이커머스 업체, 물류 회사, 유통 기업",
        "revenue_model": "거래액 기반 - 월 거래액의 0.5%, 최소 월 30만원",
        "projected_revenue": 360000000,
        "investment": 90000000,
        "risk": "high",
        "feasibility": 6.0,
        "status": "draft"
    },
    {
        "name": "AI 기반 회계 자동화 앱",
        "type": "product",
        "description": "영수증 촬영만으로 자동 회계 처리, 세금 신고 도움, 재무제표 자동 생성.",
        "target_market": "1인 사업자, 프리랜서, 소규모 법인",
        "revenue_model": "월 구독 - 개인(월 9,900원), 사업자(월 29,000원), 법인(월 99,000원)",
        "projected_revenue": 168000000,
        "investment": 40000000,
        "risk": "medium",
        "feasibility": 8.0,
        "status": "in_progress"
    },
    {
        "name": "콘텐츠 저작권 모니터링 서비스",
        "type": "service",
        "description": "웹/SNS에서 무단 사용된 이미지/영상을 AI가 자동 탐지하여 알림.",
        "target_market": "크리에이터, 사진작가, 콘텐츠 제작사",
        "revenue_model": "월 구독 - 베이직(월 1.9만원), 프로(월 4.9만원), 에이전시(월 19만원)",
        "projected_revenue": 132000000,
        "investment": 35000000,
        "risk": "medium",
        "feasibility": 7.5,
        "status": "approved"
    },
    {
        "name": "스마트 미팅 노트 AI",
        "type": "product",
        "description": "회의 음성을 실시간 텍스트로 변환, 요약, 액션 아이템 자동 추출.",
        "target_market": "기업 전반, 컨설팅 회사, 프로젝트팀",
        "revenue_model": "사용 시간 기반 - 월 10시간(3만원), 50시간(12만원), 무제한(30만원)",
        "projected_revenue": 204000000,
        "investment": 45000000,
        "risk": "low",
        "feasibility": 8.5,
        "status": "in_progress"
    }
]

# AI 직원 프로필
AI_EMPLOYEES = [
    {"id": "EMP_001", "name": "김태윤", "role": "CEO / 전략기획", "department": "경영"},
    {"id": "EMP_002", "name": "이서연", "role": "CTO / 기술총괄", "department": "개발"},
    {"id": "EMP_003", "name": "박민준", "role": "백엔드 엔지니어", "department": "개발"},
    {"id": "EMP_004", "name": "최지우", "role": "AI 엔지니어", "department": "개발"},
    {"id": "EMP_005", "name": "정하늘", "role": "프론트엔드 엔지니어", "department": "개발"},
    {"id": "EMP_006", "name": "강민서", "role": "데이터 분석가", "department": "분석"},
    {"id": "EMP_007", "name": "윤재혁", "role": "제품 매니저", "department": "기획"},
    {"id": "EMP_008", "name": "임수빈", "role": "마케팅 매니저", "department": "마케팅"},
    {"id": "EMP_009", "name": "한지호", "role": "디자이너", "department": "디자인"},
    {"id": "EMP_010", "name": "오세영", "role": "고객성공 매니저", "department": "CS"}
]

def generate_historical_data():
    """6개월치 히스토리 데이터 생성"""
    session = Session()

    try:
        # 1. AI 직원 생성
        print("=== AI 직원 생성 중... ===")
        for emp_data in AI_EMPLOYEES:
            existing = session.query(Employee).filter_by(employee_id=emp_data['id']).first()
            if not existing:
                emp = Employee(
                    employee_id=emp_data['id'],
                    name=emp_data['name'],
                    role=emp_data['role'],
                    department=emp_data['department'],
                    status='active',
                    created_at=datetime.now() - timedelta(days=180),
                    performance_score=random.uniform(7.0, 9.5),
                    tasks_completed=random.randint(50, 200)
                )
                session.add(emp)
        session.commit()
        print(f"[OK] {len(AI_EMPLOYEES)}명의 AI 직원 생성 완료")

        # 2. 사업 계획 생성
        print("\n=== 사업 계획 생성 중... ===")
        plan_objects = []
        for idx, plan_data in enumerate(BUSINESS_PLANS):
            existing = session.query(BusinessPlan).filter_by(plan_name=plan_data['name']).first()
            if not existing:
                created_date = datetime.now() - timedelta(days=random.randint(30, 180))
                plan = BusinessPlan(
                    plan_name=plan_data['name'],
                    plan_type=plan_data['type'],
                    description=plan_data['description'],
                    target_market=plan_data['target_market'],
                    revenue_model=plan_data['revenue_model'],
                    projected_revenue_12m=plan_data['projected_revenue'],
                    investment_required=plan_data['investment'],
                    risk_level=plan_data['risk'],
                    feasibility_score=plan_data['feasibility'],
                    priority='high' if plan_data['feasibility'] >= 8.0 else 'medium',
                    status=plan_data['status'],
                    created_by='EMP_001',
                    created_at=created_date,
                    approved_at=created_date + timedelta(days=7) if plan_data['status'] != 'draft' else None,
                    details={
                        'market_size': '약 1000억원',
                        'competitors': 3,
                        'unique_value': 'AI 기반 자동화'
                    }
                )
                session.add(plan)
                plan_objects.append(plan)
        session.commit()
        print(f"[OK] {len(BUSINESS_PLANS)}개의 사업 계획 생성 완료")

        # 3. 과거 6개월 회의록 생성
        print("\n=== 과거 6개월 회의록 생성 중... ===")
        meeting_types = [
            "사업성 검토 회의",
            "주간 전략 회의",
            "제품 개발 회의",
            "고객 피드백 리뷰",
            "마케팅 전략 회의",
            "투자 유치 준비 회의",
            "기술 아키텍처 회의",
            "파트너십 논의"
        ]

        meeting_count = 0
        for days_ago in range(180, 0, -7):  # 6개월 전부터 매주
            for _ in range(random.randint(2, 5)):  # 주당 2-5개 회의
                meeting_date = datetime.now() - timedelta(days=days_ago, hours=random.randint(9, 17))
                meeting_type = random.choice(meeting_types)

                # 회의 주제는 사업 계획 중 하나
                plan = random.choice(BUSINESS_PLANS)

                participants = random.sample([emp['name'] for emp in AI_EMPLOYEES], k=random.randint(3, 6))

                key_decisions = [
                    f"{plan['name']} 우선순위 조정",
                    "다음 분기 로드맵 확정",
                    f"예산 {random.randint(500, 3000)}만원 승인"
                ]

                action_items = [
                    f"시장 조사 추가 분석 ({random.choice(participants)})",
                    f"프로토타입 개발 시작 ({random.choice(participants)})",
                    f"고객 인터뷰 10건 진행 ({random.choice(participants)})"
                ]

                meeting = BusinessMeeting(
                    meeting_type=meeting_type,
                    title=f"{plan['name']} - {meeting_type}",
                    agenda=json.dumps([
                        "지난 주 진행사항 리뷰",
                        f"{plan['name']} 현황 점검",
                        "주요 이슈 및 대응방안",
                        "다음 주 실행 계획"
                    ]),
                    participants=json.dumps(participants),
                    key_decisions=json.dumps(key_decisions[:random.randint(1, 3)]),
                    action_items=json.dumps(action_items[:random.randint(2, 3)]),
                    meeting_date=meeting_date,
                    status='completed',
                    meeting_notes=json.dumps({
                        "summary": f"{plan['name']}에 대한 {meeting_type} 진행. 전반적인 진행상황 양호.",
                        "challenges": "시장 경쟁 심화, 개발 리소스 부족",
                        "next_steps": "프로토타입 완성 및 베타 테스트 시작"
                    })
                )
                session.add(meeting)
                meeting_count += 1

        session.commit()
        print(f"[OK] {meeting_count}개의 회의록 생성 완료")

        # 4. 직원 건의사항 생성
        print("\n=== 직원 건의사항 생성 중... ===")
        suggestion_categories = ["efficiency", "resource", "process", "idea", "concern"]
        suggestion_count = 0

        for days_ago in range(150, 0, -10):  # 5개월 전부터 10일마다
            for _ in range(random.randint(1, 3)):
                emp = random.choice(AI_EMPLOYEES)
                plan = random.choice(BUSINESS_PLANS)

                suggestion_date = datetime.now() - timedelta(days=days_ago)
                suggestion_id = f"SUG_{suggestion_date.strftime('%Y%m%d')}_{suggestion_count+1:03d}"

                titles = [
                    f"{plan['name']} 개발 효율화 방안",
                    "팀 협업 도구 개선 필요",
                    f"{plan['name']} 마케팅 전략 제안",
                    "고객 지원 프로세스 간소화",
                    f"{plan['name']} 가격 정책 재검토"
                ]

                suggestion = EmployeeSuggestion(
                    suggestion_id=suggestion_id,
                    employee_id=emp['id'],
                    category=random.choice(suggestion_categories),
                    priority=random.choice(['low', 'medium', 'high']),
                    title=random.choice(titles),
                    description=f"{plan['name']} 관련하여 {random.choice(['효율성', '수익성', '사용자 경험'])} 개선을 위한 제안입니다.",
                    suggested_solution="구체적인 실행 방안 및 단계별 계획",
                    expected_benefit=f"예상 효과: {random.choice(['개발 시간 30% 단축', '비용 20% 절감', '고객 만족도 15% 향상'])}",
                    implementation_difficulty=random.choice(['easy', 'medium', 'hard']),
                    status=random.choice(['implemented', 'approved', 'reviewing', 'submitted']),
                    created_at=suggestion_date,
                    estimated_impact=random.uniform(5.0, 9.0),
                    tags=json.dumps([plan['type'], 'improvement', 'revenue'])
                )
                session.add(suggestion)
                suggestion_count += 1

        session.commit()
        print(f"[OK] {suggestion_count}개의 건의사항 생성 완료")

        # 5. 수익 데이터 생성 (진행중인 사업들)
        print("\n=== 수익 데이터 생성 중... ===")
        revenue_count = 0
        active_plans = [p for p in BUSINESS_PLANS if p['status'] == 'in_progress']

        for days_ago in range(120, 0, -1):  # 4개월 전부터 매일
            date = datetime.now() - timedelta(days=days_ago)

            # 일부 날짜에만 수익 발생
            if random.random() < 0.3:  # 30% 확률
                plan = random.choice(active_plans)
                daily_revenue = random.uniform(50000, 500000)  # 5만원 ~ 50만원

                revenue = Revenue(
                    date=date.date(),
                    source=plan['name'],
                    amount=daily_revenue,
                    currency='KRW',
                    category='subscription' if 'SaaS' in plan['name'] or '구독' in plan['revenue_model'] else 'one-time',
                    customer_id=f"CUST_{random.randint(1000, 9999)}",
                    notes=f"{plan['name']} 서비스 이용료"
                )
                session.add(revenue)
                revenue_count += 1

        session.commit()
        print(f"[OK] {revenue_count}건의 수익 데이터 생성 완료")

        # 6. 회사 지표 생성
        print("\n=== 회사 성장 지표 생성 중... ===")
        metrics = [
            ("active_users", "명", "growth"),
            ("mrr", "만원", "finance"),
            ("customer_satisfaction", "점", "growth"),
            ("code_commits", "건", "tech"),
            ("api_calls", "건", "tech")
        ]

        metric_count = 0
        for days_ago in range(180, 0, -7):  # 6개월 전부터 매주
            date = datetime.now() - timedelta(days=days_ago)

            for metric_name, unit, category in metrics:
                if metric_name == "active_users":
                    value = 100 + (180 - days_ago) * random.uniform(2, 5)  # 점진적 증가
                elif metric_name == "mrr":
                    value = 500 + (180 - days_ago) * random.uniform(5, 15)  # MRR 증가
                elif metric_name == "customer_satisfaction":
                    value = random.uniform(8.0, 9.5)
                elif metric_name == "code_commits":
                    value = random.randint(50, 150)
                else:
                    value = random.randint(10000, 50000)

                metric = CompanyMetric(
                    date=date.date(),
                    metric_name=metric_name,
                    value=value,
                    unit=unit,
                    category=category
                )
                session.add(metric)
                metric_count += 1

        session.commit()
        print(f"[OK] {metric_count}개의 지표 데이터 생성 완료")

        # 7. 마일스톤 생성
        print("\n=== 주요 마일스톤 생성 중... ===")
        milestones = [
            {
                "type": "business",
                "title": "첫 유료 고객 확보",
                "description": "AI 챗봇 SaaS 플랫폼 첫 유료 고객 3명 확보",
                "days_ago": 150,
                "impact": 9.0
            },
            {
                "type": "business",
                "title": "월 매출 1000만원 달성",
                "description": "3개 사업 합계 월 매출 1000만원 돌파",
                "days_ago": 100,
                "impact": 8.5
            },
            {
                "type": "technical",
                "title": "AI 엔진 v2.0 출시",
                "description": "성능 50% 향상된 AI 엔진 개발 완료",
                "days_ago": 120,
                "impact": 8.0
            },
            {
                "type": "team",
                "title": "AI 직원 10명 체제 구축",
                "description": "자율 운영 가능한 AI 팀 구성 완료",
                "days_ago": 160,
                "impact": 9.5
            },
            {
                "type": "business",
                "title": "누적 고객 100명 돌파",
                "description": "전체 서비스 합산 누적 고객 100명 달성",
                "days_ago": 80,
                "impact": 8.0
            },
            {
                "type": "technical",
                "title": "API 일일 호출 10만건 돌파",
                "description": "시스템 안정성 확보 및 스케일업 성공",
                "days_ago": 60,
                "impact": 7.5
            }
        ]

        for milestone_data in milestones:
            milestone_date = datetime.now() - timedelta(days=milestone_data['days_ago'])

            milestone = CompanyMilestone(
                milestone_type=milestone_data['type'],
                title=milestone_data['title'],
                description=milestone_data['description'],
                achieved_at=milestone_date,
                impact_score=milestone_data['impact'],
                details={"category": milestone_data['type']}
            )
            session.add(milestone)

        session.commit()
        print(f"[OK] {len(milestones)}개의 마일스톤 생성 완료")

        print("\n" + "="*60)
        print("[SUCCESS] 모든 히스토리 데이터 생성 완료!")
        print("="*60)
        print(f"[+] AI 직원: {len(AI_EMPLOYEES)}명")
        print(f"[+] 사업 계획: {len(BUSINESS_PLANS)}개")
        print(f"[+] 회의록: {meeting_count}건")
        print(f"[+] 건의사항: {suggestion_count}건")
        print(f"[+] 수익 데이터: {revenue_count}건")
        print(f"[+] 성장 지표: {metric_count}건")
        print(f"[+] 마일스톤: {len(milestones)}개")
        print("="*60)

    except Exception as e:
        session.rollback()
        print(f"[ERROR] 오류 발생: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    print("Qhyx Inc. 현실적인 히스토리 데이터 생성 시작...")
    print("기간: 과거 6개월 (180일)")
    print()
    generate_historical_data()
