"""
즉시 실행 계획 자동 생성
- 4주 단위 구체적 실행 계획
- 필요 리소스 자동 산출
- 체크리스트 생성
- 기술 스택 추천
"""

from datetime import datetime, timedelta
import json

class ActionPlanGenerator:
    def __init__(self):
        self.tech_stacks = {
            'nocode': {
                'tools': ['Bubble.io', 'Webflow', 'Airtable', 'Zapier'],
                'cost': 100000,  # 월
                'development_time': '1-2주',
                'skill_required': '초급',
                'suitable_for': ['MVP', '간단한 도구', '랜딩페이지']
            },
            'lowcode': {
                'tools': ['Next.js + Supabase', 'Firebase', 'Vercel'],
                'cost': 50000,  # 월
                'development_time': '2-4주',
                'skill_required': '중급',
                'suitable_for': ['웹앱', '간단한 SaaS', '관리 도구']
            },
            'fullstack': {
                'tools': ['React + Node.js + PostgreSQL', 'AWS/Azure'],
                'cost': 200000,  # 월
                'development_time': '2-3개월',
                'skill_required': '고급',
                'suitable_for': ['복잡한 플랫폼', '대규모 SaaS', '마켓플레이스']
            }
        }

    def recommend_tech_stack(self, business_type, budget, timeline_weeks):
        """기술 스택 추천"""
        if budget < 1000000 or timeline_weeks <= 2:
            return self.tech_stacks['nocode']
        elif budget < 5000000 or timeline_weeks <= 8:
            return self.tech_stacks['lowcode']
        else:
            return self.tech_stacks['fullstack']

    def generate_week1_plan(self, business_config):
        """1주차: MVP 개발 계획"""
        tech_stack = business_config.get('tech_stack', {})

        tasks = [
            {
                'day': '1일차',
                'title': '핵심 기능 정의 및 우선순위',
                'tasks': [
                    '사용자 스토리 작성 (최소 10개)',
                    '필수 기능 vs 부가 기능 분류',
                    'MVP 범위 확정 (1-3개 핵심 기능만)',
                    '경쟁사 벤치마킹 (5개 이상)'
                ],
                'deliverable': 'MVP 기획서 (1페이지)',
                'time_required': '4-6시간'
            },
            {
                'day': '2일차',
                'title': '랜딩페이지 제작',
                'tasks': [
                    '도메인 구매 및 설정',
                    'Webflow/Notion으로 랜딩페이지 제작',
                    '가치 제안 명확화 (헤드라인 + 서브라인)',
                    'CTA 버튼 및 이메일 수집 폼 추가',
                    'Google Analytics 설치'
                ],
                'deliverable': '작동하는 랜딩페이지 URL',
                'tools': ['Webflow (무료 플랜)', 'Google Analytics'],
                'time_required': '6-8시간'
            },
            {
                'day': '3일차',
                'title': '핵심 기능 프로토타입',
                'tasks': [
                    f"{tech_stack.get('tools', ['Bubble.io'])[0]}로 기본 UI 제작",
                    '사용자 등록/로그인 구현',
                    '핵심 기능 1개 구현 (80% 완성도)',
                    '간단한 데이터베이스 설계'
                ],
                'deliverable': '클릭 가능한 프로토타입',
                'time_required': '8-10시간'
            },
            {
                'day': '4일차',
                'title': '결제 시스템 연동',
                'tasks': [
                    'Stripe/Toss Payments 계정 생성',
                    '결제 페이지 디자인',
                    '테스트 결제 연동',
                    '영수증 이메일 자동 발송 설정'
                ],
                'deliverable': '결제 가능한 시스템',
                'tools': ['Stripe', 'Gmail SMTP'],
                'time_required': '4-6시간'
            },
            {
                'day': '5일차',
                'title': '베타 테스터 모집',
                'tasks': [
                    '지인/커뮤니티에 베타 공지 (10-20명 목표)',
                    '페이스북/인스타 그룹에 포스팅',
                    '무료 또는 50% 할인 쿠폰 제공',
                    '피드백 수집 구글폼 생성'
                ],
                'deliverable': '베타 테스터 10명 확보',
                'budget': '0원 (무료 채널 활용)',
                'time_required': '2-3시간'
            }
        ]

        return {
            'week': 1,
            'goal': 'MVP 개발 및 초기 고객 확보',
            'tasks': tasks,
            'total_time': '24-33시간',
            'budget': 100000,
            'success_criteria': ['작동하는 MVP', '베타 테스터 10명', '첫 피드백 수집']
        }

    def generate_week2_plan(self, business_config):
        """2주차: 시장 검증"""
        tasks = [
            {
                'day': '6-7일차',
                'title': '유료 광고 테스트',
                'tasks': [
                    '페이스북 광고 계정 생성',
                    '타겟 오디언스 설정 (인구통계/관심사)',
                    '광고 크리에이티브 3종 제작',
                    '일 예산 1만원으로 광고 시작',
                    '랜딩페이지 전환율 측정'
                ],
                'deliverable': '광고 성과 리포트',
                'budget': 100000,
                'kpis': ['CPC < 500원', 'CTR > 1%', '전환율 > 2%']
            },
            {
                'day': '8-9일차',
                'title': '고객 인터뷰',
                'tasks': [
                    '베타 테스터 5명과 1:1 인터뷰 (각 30분)',
                    '사용성 테스트 진행',
                    '지불 의향 조사 (가격 민감도 분석)',
                    '개선점 우선순위 도출'
                ],
                'deliverable': '고객 인터뷰 요약 리포트',
                'questions': [
                    '어떤 문제를 해결하고 싶었나요?',
                    '이 제품이 그 문제를 해결했나요?',
                    '얼마까지 지불할 의향이 있나요?',
                    '가장 불편했던 점은?',
                    '친구에게 추천하시겠습니까?'
                ]
            },
            {
                'day': '10-11일차',
                'title': '제품 개선',
                'tasks': [
                    '피드백 기반 우선순위 결정',
                    'Critical 버그 수정',
                    'UI/UX 개선 (상위 3개)',
                    '신규 기능 1개 추가 (요청 많은 것)'
                ],
                'deliverable': '개선된 버전 2.0',
                'time_required': '16-20시간'
            },
            {
                'day': '12일차',
                'title': '첫 유료 고객 확보',
                'tasks': [
                    '베타 테스터에게 유료 전환 제안',
                    '얼리버드 할인 50% 제공',
                    '첫 결제 완료',
                    '고객 온보딩 프로세스 테스트'
                ],
                'deliverable': '첫 유료 매출 달성',
                'target': '최소 1명, 목표 3-5명'
            }
        ]

        return {
            'week': 2,
            'goal': '시장 검증 및 첫 매출',
            'tasks': tasks,
            'budget': 150000,
            'success_criteria': ['첫 유료 고객 확보', '전환율 2% 이상', '고객 만족도 7/10 이상']
        }

    def generate_week3_plan(self, business_config):
        """3주차: 확장 준비"""
        tasks = [
            {
                'day': '13-15일차',
                'title': '마케팅 채널 다각화',
                'tasks': [
                    '블로그 콘텐츠 3개 작성 (SEO 최적화)',
                    '유튜브 소개 영상 제작 (3분 이내)',
                    '인스타그램/틱톡 릴스 5개',
                    '온라인 커뮤니티 (Reddit, 네이버카페) 진출'
                ],
                'deliverable': '다채널 콘텐츠 발행',
                'budget': 50000
            },
            {
                'day': '16-17일차',
                'title': '자동화 시스템 구축',
                'tasks': [
                    '이메일 마케팅 자동화 (Mailchimp)',
                    '신규 가입 환영 이메일 시퀀스',
                    '유저 행동 기반 리텐션 이메일',
                    '결제 실패 시 자동 알림'
                ],
                'deliverable': '자동화 워크플로우 가동',
                'tools': ['Mailchimp (무료 2000명)', 'Zapier']
            },
            {
                'day': '18-19일차',
                'title': '레퍼럴 프로그램',
                'tasks': [
                    '추천인 제도 설계 (추천인/가입자 모두 혜택)',
                    '추천 링크 자동 생성 시스템',
                    '대시보드에 추천 현황 표시',
                    '바이럴 요소 강화 (공유 버튼)'
                ],
                'deliverable': '작동하는 레퍼럴 시스템',
                'expected_effect': '고객 획득 비용 50% 감소'
            }
        ]

        return {
            'week': 3,
            'goal': '성장 엔진 구축',
            'tasks': tasks,
            'budget': 100000,
            'success_criteria': ['주간 신규 가입 20명', '레퍼럴 비율 10%', 'CAC 30% 감소']
        }

    def generate_week4_plan(self, business_config):
        """4주차: 스케일업"""
        tasks = [
            {
                'day': '20-22일차',
                'title': '광고 최적화',
                'tasks': [
                    'A/B 테스트: 광고 크리에이티브 10종',
                    '타겟 오디언스 세분화 (5개 이상)',
                    '성과 좋은 광고에 예산 집중',
                    '리타게팅 광고 시작'
                ],
                'deliverable': 'CAC 30% 감소',
                'budget': 300000
            },
            {
                'day': '23-24일차',
                'title': '고객 성공 사례',
                'tasks': [
                    '만족 고객 3명 인터뷰',
                    '성공 사례 콘텐츠 제작 (Before/After)',
                    '동영상 후기 촬영',
                    '웹사이트에 증거 자료 추가'
                ],
                'deliverable': '신뢰성 강화 콘텐츠',
                'expected_effect': '전환율 20% 향상'
            },
            {
                'day': '25-26일차',
                'title': '데이터 분석 및 개선',
                'tasks': [
                    'Google Analytics 데이터 분석',
                    '이탈률 높은 페이지 개선',
                    '전환 퍼널 최적화',
                    '주요 KPI 대시보드 구축'
                ],
                'deliverable': '데이터 기반 개선 실행'
            }
        ]

        return {
            'week': 4,
            'goal': '스케일업 및 최적화',
            'tasks': tasks,
            'budget': 400000,
            'success_criteria': ['주간 신규 고객 50명', '월 매출 300만원', 'LTV/CAC > 3']
        }

    def generate_comprehensive_plan(self, business_config):
        """4주 종합 실행 계획"""
        print(f"\n{'='*80}")
        print(f"📋 4주 실행 계획: {business_config['name']}")
        print(f"{'='*80}\n")

        # 기술 스택 추천
        tech_stack = self.recommend_tech_stack(
            business_config['type'],
            business_config.get('budget', 3000000),
            business_config.get('timeline_weeks', 4)
        )
        business_config['tech_stack'] = tech_stack

        print(f"🛠️  추천 기술 스택: {tech_stack['tools'][0]}")
        print(f"   개발 시간: {tech_stack['development_time']}")
        print(f"   필요 스킬: {tech_stack['skill_required']}")
        print(f"   월 비용: {tech_stack['cost']:,}원\n")

        # 주차별 계획
        week1 = self.generate_week1_plan(business_config)
        week2 = self.generate_week2_plan(business_config)
        week3 = self.generate_week3_plan(business_config)
        week4 = self.generate_week4_plan(business_config)

        weeks = [week1, week2, week3, week4]

        for week_plan in weeks:
            print(f"\n{'='*80}")
            print(f"📅 {week_plan['week']}주차: {week_plan['goal']}")
            print(f"{'='*80}\n")

            for task_group in week_plan['tasks']:
                print(f"▶ {task_group['day']}: {task_group['title']}")

                for task in task_group['tasks']:
                    print(f"  □ {task}")

                print(f"\n  ✅ 산출물: {task_group['deliverable']}")

                if 'budget' in task_group:
                    print(f"  💰 예산: {task_group['budget']:,}원")

                if 'time_required' in task_group:
                    print(f"  ⏱️  소요 시간: {task_group['time_required']}")

                if 'tools' in task_group:
                    print(f"  🛠️  도구: {', '.join(task_group['tools'])}")

                print()

            print(f"✓ 성공 기준: {', '.join(week_plan['success_criteria'])}")
            print(f"💰 주간 예산: {week_plan['budget']:,}원\n")

        # 종합 요약
        total_budget = sum(w['budget'] for w in weeks)

        print(f"\n{'='*80}")
        print(f"📊 종합 요약")
        print(f"{'='*80}\n")
        print(f"총 기간: 4주")
        print(f"총 예산: {total_budget:,}원")
        print(f"기술 스택: {tech_stack['tools'][0]}")
        print(f"\n주요 마일스톤:")
        print(f"  • 1주차: MVP 완성 + 베타 테스터 10명")
        print(f"  • 2주차: 첫 유료 고객 확보")
        print(f"  • 3주차: 자동화 시스템 구축")
        print(f"  • 4주차: 주간 50명 고객 확보")
        print(f"\n예상 결과:")
        print(f"  • 총 고객: 80-150명")
        print(f"  • 월 매출: 300-800만원")
        print(f"  • 손익분기: 2-3개월")

        return {
            'business_name': business_config['name'],
            'tech_stack': tech_stack,
            'weeks': weeks,
            'total_budget': total_budget,
            'generated_at': datetime.now().isoformat()
        }

    def generate_checklist(self, plan):
        """체크리스트 생성"""
        checklist = []

        for week in plan['weeks']:
            for task_group in week['tasks']:
                for task in task_group['tasks']:
                    checklist.append({
                        'week': week['week'],
                        'day': task_group['day'],
                        'task': task,
                        'completed': False,
                        'notes': ''
                    })

        return checklist

    def save_plan(self, plan, filename='action_plan.json'):
        """실행 계획 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 실행 계획 저장됨: {filename}")


# 사용 예시
if __name__ == "__main__":
    generator = ActionPlanGenerator()

    # IT 사업 예시
    business_configs = [
        {
            'name': 'AI 이력서 작성 도구',
            'type': 'saas',
            'budget': 2000000,
            'timeline_weeks': 4
        },
        {
            'name': '로컬 프리랜서 마켓플레이스',
            'type': 'marketplace',
            'budget': 5000000,
            'timeline_weeks': 8
        },
        {
            'name': 'SEO 컨설팅 에이전시',
            'type': 'agency',
            'budget': 1000000,
            'timeline_weeks': 2
        }
    ]

    for config in business_configs:
        plan = generator.generate_comprehensive_plan(config)
        generator.save_plan(plan, f"plan_{config['name'].replace(' ', '_')}.json")

        # 체크리스트 생성
        checklist = generator.generate_checklist(plan)
        print(f"\n총 {len(checklist)}개 작업 항목 생성됨")
        print("-" * 80)
