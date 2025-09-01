"""
Qhyx Inc. MVP 제품 개발 계획
실제 시장에 출시 가능한 최소 기능 제품(MVP) 개발 로드맵
"""

from database_setup import Session, BusinessPlan, BusinessMeeting, CompanyMilestone, Task, Employee
from datetime import datetime, timedelta
import json

class QhyxMVPPlanner:
    def __init__(self):
        self.session = Session()
    
    def create_mvp_development_plan(self):
        """MVP 개발 계획 수립"""
        
        print("🚀 Qhyx Inc. MVP 제품 개발 계획 수립")
        print("=" * 60)
        
        # MVP 기획 회의 기록
        meeting = BusinessMeeting(
            meeting_type='MVP기획회의',
            title='Qhyx Inc. 시장 진입 MVP 제품 개발 계획',
            agenda=json.dumps([
                "1순위 MVP 제품 선정 및 기능 정의",
                "개발 일정 및 리소스 계획",
                "기술 스택 및 아키텍처 설계",
                "마케팅 및 고객 확보 전략",
                "수익 모델 및 가격 정책",
                "출시 후 성장 계획"
            ], ensure_ascii=False),
            participants=[
                {'name': '김창의', 'role': 'CCO', 'focus': '제품_비전_및_사용자경험'},
                {'name': '박실용', 'role': 'CPO', 'focus': '실현가능성_및_운영계획'},
                {'name': '테크노', 'role': 'CTO', 'focus': '기술구현_및_아키텍처'},
                {'name': '신재무', 'role': 'CFO', 'focus': '비용분석_및_수익모델'},
                {'name': '정브랜드', 'role': 'CBO', 'focus': '마케팅_및_브랜딩'},
                {'name': '한전략', 'role': 'CSO', 'focus': '시장진입전략'}
            ],
            status='ongoing'
        )
        self.session.add(meeting)
        self.session.commit()
        
        # MVP 제품들 분석 및 선정
        mvp_products = self.analyze_mvp_opportunities()
        selected_mvp = self.select_primary_mvp(mvp_products)
        
        # 개발 계획 수립
        development_plan = self.create_development_roadmap(selected_mvp)
        
        # 회의 완료 및 결과 기록
        meeting.status = 'completed'
        meeting.key_decisions = [
            f"1순위 MVP: {selected_mvp['name']} 선정",
            f"개발 기간: {selected_mvp['development_weeks']}주",
            f"출시 목표일: {selected_mvp['launch_date']}",
            f"초기 투자금: {selected_mvp['initial_investment']:,}원",
            f"첫 달 매출 목표: {selected_mvp['first_month_revenue']:,}원"
        ]
        meeting.action_items = development_plan['tasks']
        meeting.meeting_notes = self.generate_mvp_meeting_notes(selected_mvp, development_plan)
        
        self.session.commit()
        
        # 구체적 사업 계획 생성
        self.create_mvp_business_plan(selected_mvp)
        
        # 개발 업무들 생성
        self.create_development_tasks(development_plan['tasks'])
        
        print(f"✅ MVP 개발 계획 수립 완료: {selected_mvp['name']}")
        return meeting.id, selected_mvp, development_plan
    
    def analyze_mvp_opportunities(self):
        """MVP 제품 기회 분석"""
        
        mvp_candidates = {
            "qhyx_business_automation_bot": {
                "name": "Qhyx 비즈니스 자동화 봇",
                "description": "중소기업용 업무 자동화 챗봇 SaaS 서비스",
                "target_market": "월매출 1억 미만 중소기업 및 스타트업",
                "core_features": [
                    "고객 문의 자동응답",
                    "예약 및 일정 관리",
                    "기본적인 FAQ 처리",
                    "간단한 데이터 조회",
                    "이메일/SMS 자동 발송"
                ],
                "technical_complexity": 6,  # 1-10
                "market_readiness": 9,
                "development_weeks": 6,
                "initial_investment": 300000,  # 30만원
                "first_month_revenue": 1000000,  # 100만원
                "launch_date": "2025년 10월 15일",
                "pricing_model": {
                    "basic": "월 9만원 (기본 기능)",
                    "pro": "월 19만원 (고급 기능 + 커스터마이징)",
                    "enterprise": "월 39만원 (전용 지원 + 무제한 기능)"
                },
                "competitive_advantage": [
                    "Qhyx만의 '예측불가능한' 창의적 응답",
                    "매우 저렴한 가격",
                    "빠른 셋업 (30분 이내)",
                    "한국 중소기업 특화"
                ]
            },
            
            "qhyx_data_insight_dashboard": {
                "name": "Qhyx 데이터 인사이트 대시보드",
                "description": "기업 데이터를 쉽게 분석하고 시각화하는 노코드 대시보드",
                "target_market": "데이터 분석이 필요한 모든 기업",
                "core_features": [
                    "드래그앤드롭 대시보드 빌더",
                    "실시간 데이터 연동",
                    "AI 기반 인사이트 추천",
                    "자동 리포트 생성",
                    "모바일 최적화"
                ],
                "technical_complexity": 8,
                "market_readiness": 7,
                "development_weeks": 10,
                "initial_investment": 800000,
                "first_month_revenue": 2000000,
                "launch_date": "2025년 12월 1일",
                "pricing_model": {
                    "starter": "월 15만원",
                    "professional": "월 45만원", 
                    "enterprise": "월 99만원"
                }
            },
            
            "qhyx_smart_consulting_assistant": {
                "name": "Qhyx 스마트 컨설팅 어시스턴트",
                "description": "AI가 비즈니스 문제를 분석하고 솔루션을 제안하는 컨설팅 봇",
                "target_market": "컨설팅이 필요한 중소기업 CEO/임원",
                "core_features": [
                    "비즈니스 문제 분석",
                    "맞춤형 솔루션 제안",
                    "경쟁사 분석 리포트",
                    "성장 전략 수립 지원",
                    "실행 계획 템플릿 제공"
                ],
                "technical_complexity": 7,
                "market_readiness": 8,
                "development_weeks": 8,
                "initial_investment": 500000,
                "first_month_revenue": 1500000,
                "launch_date": "2025년 11월 15일",
                "pricing_model": {
                    "basic": "컨설팅 1회 10만원",
                    "monthly": "월 30만원 (무제한)",
                    "premium": "월 50만원 (1:1 전문가 지원)"
                }
            }
        }
        
        print("\n💡 MVP 후보 제품들 분석:")
        for key, product in mvp_candidates.items():
            print(f"\n🎯 {product['name']}")
            print(f"   기술복잡도: {product['technical_complexity']}/10")
            print(f"   시장준비도: {product['market_readiness']}/10")
            print(f"   개발기간: {product['development_weeks']}주")
            print(f"   첫달매출: {product['first_month_revenue']:,}원")
        
        return mvp_candidates
    
    def select_primary_mvp(self, candidates):
        """1순위 MVP 선정"""
        
        # 점수 계산 (시장준비도 + 낮은복잡도 + 빠른개발 + 높은수익)
        scored_candidates = []
        
        for key, candidate in candidates.items():
            score = (
                candidate['market_readiness'] * 3 +  # 시장준비도 가중치 높음
                (11 - candidate['technical_complexity']) * 2 +  # 복잡도는 낮을수록 좋음
                (15 - candidate['development_weeks']) * 1 +  # 개발기간은 짧을수록 좋음
                (candidate['first_month_revenue'] / 100000) * 1  # 수익성
            )
            scored_candidates.append((score, candidate))
        
        # 점수순 정렬
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        selected = scored_candidates[0][1]
        
        print(f"\n🏆 선정된 1순위 MVP: {selected['name']}")
        print(f"   📊 종합점수: {scored_candidates[0][0]:.1f}점")
        
        return selected
    
    def create_development_roadmap(self, mvp):
        """개발 로드맵 수립"""
        
        weeks = mvp['development_weeks']
        
        roadmap = {
            "phases": [
                {
                    "phase": "1단계: 기획 및 설계",
                    "duration": "1주",
                    "tasks": [
                        "상세 기능 명세서 작성",
                        "UI/UX 와이어프레임 설계",
                        "기술 아키텍처 설계",
                        "데이터베이스 스키마 설계"
                    ]
                },
                {
                    "phase": "2단계: 핵심 기능 개발",
                    "duration": f"{weeks-3}주",
                    "tasks": [
                        "백엔드 API 개발",
                        "프론트엔드 UI 개발", 
                        "AI 챗봇 엔진 구현",
                        "데이터베이스 연동",
                        "기본 기능 테스트"
                    ]
                },
                {
                    "phase": "3단계: 테스트 및 최적화",
                    "duration": "1주",
                    "tasks": [
                        "통합 테스트 진행",
                        "성능 최적화",
                        "보안 검증",
                        "사용자 피드백 반영"
                    ]
                },
                {
                    "phase": "4단계: 출시 준비",
                    "duration": "1주",
                    "tasks": [
                        "운영 서버 환경 구축",
                        "결제 시스템 연동",
                        "마케팅 자료 준비",
                        "고객 지원 체계 구축"
                    ]
                }
            ],
            "milestones": [
                {"week": 1, "milestone": "기획 완료"},
                {"week": 3, "milestone": "핵심 기능 프로토타입"},
                {"week": 5, "milestone": "베타 버전 완성"},
                {"week": 6, "milestone": "정식 출시"}
            ]
        }
        
        # 모든 태스크를 플랫 리스트로 변환
        all_tasks = []
        for phase in roadmap["phases"]:
            for task in phase["tasks"]:
                all_tasks.append(f"{phase['phase']}: {task}")
        
        roadmap["tasks"] = all_tasks
        
        return roadmap
    
    def generate_mvp_meeting_notes(self, mvp, roadmap):
        """MVP 회의록 생성"""
        
        notes = f"""
=== Qhyx Inc. MVP 제품 개발 계획 회의록 ===

📅 일시: {datetime.now().strftime('%Y-%m-%d %H:%M')}
🎯 목표: 시장 진입 가능한 MVP 제품 개발 계획 확정

🏆 선정된 MVP: {mvp['name']}

📋 제품 개요:
- 설명: {mvp['description']}
- 타겟시장: {mvp['target_market']}
- 핵심기능: {len(mvp['core_features'])}개

💰 비즈니스 모델:
- 초기투자: {mvp['initial_investment']:,}원
- 첫달매출목표: {mvp['first_month_revenue']:,}원
- 가격정책: {str(mvp['pricing_model'])}

⏰ 개발 일정:
- 총 개발기간: {mvp['development_weeks']}주
- 출시예정일: {mvp['launch_date']}
- 개발단계: {len(roadmap['phases'])}단계

🎯 경쟁우위:
        """
        
        for advantage in mvp['competitive_advantage']:
            notes += f"- {advantage}\n"
        
        notes += f"""
📊 성공지표:
- 출시 첫 달: 고객 50명 확보
- 출시 3개월: 월매출 500만원
- 출시 6개월: 월매출 1,000만원
- 고객만족도: 4.5/5.0 이상

🚀 다음단계:
- 즉시 개발팀 구성 및 역할 분담
- 기획 단계 착수 (1주 이내)
- 파일럿 고객 10명 사전 확보
- 마케팅 채널 구축 시작
        """
        
        return notes
    
    def create_mvp_business_plan(self, mvp):
        """MVP 비즈니스 계획 DB 저장"""
        
        # 기존 계획 확인
        existing = self.session.query(BusinessPlan).filter_by(
            plan_name=mvp['name']
        ).first()
        
        if not existing:
            plan = BusinessPlan(
                plan_name=mvp['name'],
                plan_type='product',
                description=mvp['description'],
                target_market=mvp['target_market'],
                revenue_model=f"SaaS 구독형: {str(mvp['pricing_model'])}",
                projected_revenue_12m=mvp['first_month_revenue'] * 12,  # 첫달 기준으로 연간 추정
                investment_required=mvp['initial_investment'],
                risk_level='medium',
                feasibility_score=mvp['market_readiness'],
                priority='high',
                status='approved',
                created_by='MVP 기획팀',
                approved_at=datetime.now(),
                details={
                    'development_weeks': mvp['development_weeks'],
                    'launch_date': mvp['launch_date'],
                    'core_features': mvp['core_features'],
                    'competitive_advantage': mvp['competitive_advantage'],
                    'pricing_model': mvp['pricing_model'],
                    'technical_complexity': mvp['technical_complexity'],
                    'market_readiness': mvp['market_readiness']
                }
            )
            
            self.session.add(plan)
            self.session.commit()
            
            print(f"📋 비즈니스 계획이 생성되었습니다: {mvp['name']}")
    
    def create_development_tasks(self, tasks):
        """개발 업무들 생성"""
        
        # AI 직원들 가져오기
        employees = self.session.query(Employee).filter_by(status='active').all()
        if not employees:
            print("⚠️  AI 직원이 없어서 업무 배정을 건너뜁니다.")
            return
        
        tasks_created = 0
        
        for i, task_desc in enumerate(tasks):
            # 담당자 배정 (순서대로 돌려가며)
            assignee = employees[i % len(employees)]
            
            # 우선순위 결정
            if '기획' in task_desc or '설계' in task_desc:
                priority = 'high'
            elif '테스트' in task_desc or '최적화' in task_desc:
                priority = 'medium'
            else:
                priority = 'high'  # 개발 업무는 높은 우선순위
            
            # 마감일 설정 (1-2주 후)
            due_days = 7 if priority == 'high' else 14
            
            task = Task(
                task_id=f"MVP_{datetime.now().strftime('%Y%m%d')}_{i+1:03d}",
                title=task_desc,
                description=f"MVP 개발을 위한 핵심 업무: {task_desc}",
                priority=priority,
                assigned_to=assignee.employee_id,
                due_date=datetime.now() + timedelta(days=due_days),
                status='pending'
            )
            
            self.session.add(task)
            tasks_created += 1
        
        self.session.commit()
        print(f"📋 {tasks_created}개의 개발 업무가 생성되었습니다.")
    
    def close(self):
        self.session.close()

def execute_mvp_planning():
    """MVP 개발 계획 실행"""
    planner = QhyxMVPPlanner()
    
    try:
        meeting_id, selected_mvp, roadmap = planner.create_mvp_development_plan()
        
        # 마일스톤 추가
        milestone = CompanyMilestone(
            milestone_type='product',
            title='MVP 제품 개발 계획 확정',
            description=f'{selected_mvp["name"]} MVP 개발 계획 수립 완료. {selected_mvp["development_weeks"]}주 개발 일정으로 {selected_mvp["launch_date"]} 출시 예정.',
            impact_score=10.0,
            details={
                'mvp_name': selected_mvp['name'],
                'development_weeks': selected_mvp['development_weeks'],
                'initial_investment': selected_mvp['initial_investment'],
                'first_month_revenue_target': selected_mvp['first_month_revenue'],
                'launch_date': selected_mvp['launch_date'],
                'total_development_phases': len(roadmap['phases'])
            }
        )
        
        planner.session.add(milestone)
        planner.session.commit()
        
        print("\n" + "="*60)
        print("🎉 MVP 개발 계획 수립 완료!")
        print(f"📋 회의 ID: {meeting_id}")
        print(f"🚀 선정 제품: {selected_mvp['name']}")
        print(f"⏰ 개발 기간: {selected_mvp['development_weeks']}주")
        print(f"🎯 출시일: {selected_mvp['launch_date']}")
        print(f"💰 초기 투자: {selected_mvp['initial_investment']:,}원")
        print(f"📈 첫달 매출 목표: {selected_mvp['first_month_revenue']:,}원")
        
        return selected_mvp
        
    finally:
        planner.close()

if __name__ == "__main__":
    mvp_plan = execute_mvp_planning()