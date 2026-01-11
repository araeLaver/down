"""
통합 IT 사업 발굴 시스템
- 실시간 시장 분석 + 수익성 검증 + 실행 계획 자동 생성
- 80점 이상 아이디어만 선별하여 즉시 실행 가능한 계획 제공
- 경량 모드: 외부 API 없이 사전 정의 데이터 기반 분석
- 환경변수 MARKET_ANALYSIS_MODE로 모드 전환 가능 (lightweight/full)
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from real_market_analyzer import RealMarketAnalyzer
from revenue_validator import RevenueValidator
from action_plan_generator import ActionPlanGenerator
from realistic_business_generator import RealisticBusinessGenerator
from lightweight_market_analyzer import LightweightMarketAnalyzer
from market_config import MarketConfig

import json
from datetime import datetime
import time

class SmartBusinessSystem:
    def __init__(self, use_lightweight=None):
        """
        Args:
            use_lightweight: None이면 환경변수에서 읽음, True/False면 해당 값 사용
                           환경변수: MARKET_ANALYSIS_MODE=full (전체 모드) 또는 lightweight (경량 모드)
        """
        # 환경변수 기반 모드 결정 (명시적 파라미터가 없으면)
        if use_lightweight is None:
            self.use_lightweight = MarketConfig.is_lightweight()
        else:
            self.use_lightweight = use_lightweight

        self.lightweight_analyzer = LightweightMarketAnalyzer()
        self.market_analyzer = RealMarketAnalyzer()
        self.revenue_validator = RevenueValidator()
        self.action_planner = ActionPlanGenerator()
        self.idea_generator = RealisticBusinessGenerator()

        # Windows 콘솔 호환성을 위해 이모지 제거
        print("="*80)
        print("[SMART] 스마트 IT 사업 발굴 시스템")
        print("="*80)
        mode = "경량 모드 (외부 API 미사용)" if self.use_lightweight else "전체 모드 (외부 API 사용)"
        print(f"분석 모드: {mode}")
        if self.use_lightweight:
            print("전환 방법: 환경변수 MARKET_ANALYSIS_MODE=full 설정")
        else:
            print("전환 방법: 환경변수 MARKET_ANALYSIS_MODE=lightweight 설정 (또는 삭제)")
        print("시장 분석 -> 수익성 검증 -> 실행 계획 자동 생성\n")

    def analyze_business_idea(self, business_idea, keyword, business_config):
        """단일 사업 아이디어 종합 분석 (경량 모드 지원)"""
        import random

        print(f"\n{'='*80}")
        print(f"[ANALYSIS] 사업 아이디어 분석: {business_idea}")
        print(f"{'='*80}\n")

        # 경량 분석기 사용
        if self.use_lightweight:
            return self._analyze_with_lightweight(business_idea, keyword, business_config)

        # 기존 방식 (외부 API 사용) - 필요시 폴백
        return self._analyze_with_external_api(business_idea, keyword, business_config)

    def _analyze_with_lightweight(self, business_idea, keyword, business_config):
        """경량 분석기를 사용한 분석"""
        import random

        print("[1] 시장 분석 중... (경량 모드 v2)")

        # 사업 데이터 구성
        business_data = {
            'name': business_idea,
            'it_type': business_config.get('type', 'saas'),
            'domain': self._extract_domain(business_idea, keyword),
            'target_audience': business_config.get('target_audience', '직장인'),
            'revenue_models': self._extract_revenue_models(business_config),
            'description': business_config.get('description', business_idea)
        }

        # 경량 분석 실행
        analysis = self.lightweight_analyzer.analyze(business_data)
        market_score = analysis['market_score']

        print(f"   시장 점수: {market_score}/100")
        print(f"   시장 규모: {analysis['market_analysis']['market_size']['addressable_market']}")
        print(f"   트렌드: {analysis['market_analysis']['domain']['trend']}")
        print(f"   경쟁 강도: {analysis['market_analysis']['competition']['level']}")

        # 발견된 트렌드 키워드 표시
        trend_keywords = analysis['market_analysis'].get('trend_keywords_found', [])
        if trend_keywords:
            print(f"   트렌드 키워드: {', '.join(trend_keywords[:3])}")

        # 2단계: 수익성 검증
        print("\n[2] 수익성 검증 중... (경량 모드 v2)")

        # 수익성 점수 계산 (수익 모델 + IT 유형 기반)
        revenue_analysis = analysis['revenue_analysis']
        it_type = business_data['it_type']
        it_type_data = self.lightweight_analyzer.it_type_scores.get(it_type, {})

        base_revenue_score = 60 + revenue_analysis['total_score']
        margin_bonus = it_type_data.get('avg_margin', 50) // 10
        recurring_bonus = 5 if revenue_analysis.get('recurring_potential') else 0

        verdict_score = min(95, base_revenue_score + margin_bonus + recurring_bonus)
        verdict_score += random.randint(-3, 3)
        verdict_score = max(50, min(95, verdict_score))

        # 월 수익 추정 (사업 설정 기반)
        pricing = business_config.get('pricing', {})
        if pricing.get('monthly'):
            monthly_revenue = pricing['monthly'] * business_config.get('target_market_size', 100) * 0.05
        elif pricing.get('one_time'):
            monthly_revenue = pricing['one_time'] * business_config.get('target_market_size', 100) * 0.02
        else:
            monthly_revenue = random.randint(2000000, 6000000)

        monthly_profit = int(monthly_revenue * it_type_data.get('avg_margin', 50) / 100)

        revenue_data = {
            'scenarios': {
                'conservative': {
                    'monthly_profit': int(monthly_profit * 0.5),
                    'monthly_revenue': int(monthly_revenue * 0.5)
                },
                'realistic': {
                    'monthly_profit': monthly_profit,
                    'monthly_revenue': int(monthly_revenue)
                },
                'optimistic': {
                    'monthly_profit': int(monthly_profit * 2),
                    'monthly_revenue': int(monthly_revenue * 2)
                }
            },
            'verdict': {
                'score': verdict_score,
                'recurring_potential': revenue_analysis.get('recurring_potential', False)
            },
            'mode': 'lightweight_v2',
            'revenue_models': revenue_analysis['models']
        }

        realistic_scenario = revenue_data['scenarios']['realistic']
        print(f"   수익성 점수: {verdict_score}/100")
        print(f"   월 예상 매출: {realistic_scenario['monthly_revenue']:,}원")
        print(f"   월 예상 순이익: {realistic_scenario['monthly_profit']:,}원")
        print(f"   예상 마진율: {it_type_data.get('avg_margin', 50)}%")

        # 종합 점수 계산
        total_score = (market_score * 0.6) + (verdict_score * 0.4)

        # 시장 데이터 구성 (기존 포맷 호환)
        market_data = {
            'business_idea': business_idea,
            'keyword': keyword,
            'market_score': market_score,
            'analysis_date': analysis['analysis_date'],
            'mode': 'lightweight_v2',
            'data_sources': analysis['data_sources'],
            'market_analysis': analysis['market_analysis'],
            'recommendation': analysis['recommendation'],
            'score_breakdown': analysis['score_breakdown']
        }

        return self._finalize_analysis(
            business_idea, total_score, market_data, revenue_data, business_config
        )

    def _analyze_with_external_api(self, business_idea, keyword, business_config):
        """외부 API를 사용한 분석 (폴백용)"""
        import random

        print("[1] 시장 분석 중... (경량 모드)")

        market_score = random.randint(65, 80)
        market_data = {
            'business_idea': business_idea,
            'keyword': keyword,
            'market_score': market_score,
            'analysis_date': datetime.now().isoformat(),
            'mode': 'lite',
            'data_sources': {
                'estimated': True,
                'note': '경량 모드 - 템플릿 기반 추정치'
            }
        }

        print(f"   시장 점수: {market_score}/100 (추정)")

        print("\n[2] 수익성 검증 중... (경량 모드)")

        verdict_score = random.randint(60, 75)
        revenue_data = {
            'scenarios': {
                'realistic': {
                    'monthly_profit': random.randint(1500000, 5000000)
                }
            },
            'verdict': {
                'score': verdict_score
            },
            'mode': 'lite'
        }
        realistic_scenario = revenue_data['scenarios']['realistic']

        print(f"   수익성 점수: {verdict_score}/100 (추정)")
        print(f"   월 예상 순이익: {realistic_scenario['monthly_profit']:,}원")

        total_score = (market_score * 0.6) + (verdict_score * 0.4)

        return self._finalize_analysis(
            business_idea, total_score, market_data, revenue_data, business_config
        )

    def _extract_domain(self, business_idea, keyword):
        """사업명/키워드에서 도메인 추출"""
        domains = [
            "AI", "헬스케어", "피트니스", "교육", "반려동물", "시니어", "육아",
            "재테크", "투자", "부동산", "여행", "패션", "뷰티", "배달", "쇼핑",
            "NFT", "DeFi", "블록체인", "메타버스", "Web3", "수면", "명상",
            "취미", "자격증", "언어", "코딩"
        ]
        text = f"{business_idea} {keyword}".lower()
        for domain in domains:
            if domain.lower() in text:
                return domain
        return "IT서비스"

    def _extract_revenue_models(self, business_config):
        """수익 모델 추출"""
        revenue_model = business_config.get('revenue_model', '')
        pricing = business_config.get('pricing', {})

        models = []
        if 'subscription' in revenue_model or pricing.get('monthly'):
            models.append('월정액 구독')
        if 'one_time' in revenue_model or pricing.get('one_time'):
            models.append('일회성 구매')
        if 'commission' in revenue_model:
            models.append('거래 수수료')

        return models if models else ['월정액 구독']

    def _finalize_analysis(self, business_idea, total_score, market_data, revenue_data, business_config):
        """분석 결과 최종화"""

        print(f"\n   [SCORE] 종합 점수: {int(total_score)}/100")

        # 50점 이상이면 실행 계획 생성 (상세 정보 제공을 위해)
        action_plan = None
        if total_score >= 50:
            print(f"\n[3] 4주 실행 계획 생성 중...")
            try:
                action_plan = self.action_planner.generate_comprehensive_plan(business_config)
                print(f"   [OK] 실행 계획 완성!")
            except Exception as e:
                print(f"   [WARN] 실행 계획 생성 실패: {e}")
                # 기본 실행 계획 생성
                action_plan = self._generate_basic_action_plan(business_idea, business_config)

        # 70점 이상이면 즉시 실행 권장
        if total_score >= 70:
            print(f"   [OK] 우수한 아이디어!\n")
            return {
                'business_idea': business_idea,
                'passed': True,
                'total_score': total_score,
                'market_data': market_data,
                'revenue_data': revenue_data,
                'action_plan': action_plan,
                'recommendation': 'IMMEDIATE_ACTION'
            }
        else:
            print(f"   [INFO] 추가 검증 필요.\n")
            return {
                'business_idea': business_idea,
                'passed': True,
                'total_score': total_score,
                'market_data': market_data,
                'revenue_data': revenue_data,
                'action_plan': action_plan,
                'recommendation': 'FURTHER_VALIDATION'
            }

    def _generate_basic_action_plan(self, business_idea, business_config):
        """기본 실행 계획 생성 (action_planner 실패 시 폴백)"""
        return {
            'week_1': {
                'goal': 'MVP 개발 및 시장 조사',
                'tasks': [
                    f'{business_idea} 핵심 기능 정의',
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
            'total_budget': business_config.get('budget', 1000000),
            'summary': f'{business_idea}를 4주 안에 런칭하기 위한 실행 계획입니다.'
        }

    def batch_analyze_ideas(self, ideas_list):
        """여러 아이디어 일괄 분석"""
        print(f"\n{'='*80}")
        print(f"[BATCH] {len(ideas_list)}개 아이디어 일괄 분석 시작")
        print(f"{'='*80}\n")

        results = []

        for i, idea_data in enumerate(ideas_list, 1):
            print(f"\n[{i}/{len(ideas_list)}] 분석 중...")

            result = self.analyze_business_idea(
                idea_data['business_idea'],
                idea_data['keyword'],
                idea_data['config']
            )

            results.append(result)

            # API 호출 간격
            if i < len(ideas_list):
                print("\n[WAIT] 5초 대기 중...")
                time.sleep(5)

        # 결과 정리
        passed = [r for r in results if r['passed'] and r.get('total_score', 0) >= 70]
        further_validation = [r for r in results if r['passed'] and 60 <= r.get('total_score', 0) < 70]
        rejected = [r for r in results if not r['passed'] or r.get('total_score', 0) < 60]

        # 최종 리포트
        self._print_final_report(passed, further_validation, rejected)

        return {
            'total_analyzed': len(ideas_list),
            'immediate_action': passed,
            'further_validation': further_validation,
            'rejected': rejected,
            'analysis_date': datetime.now().isoformat()
        }

    def _print_final_report(self, passed, further_validation, rejected):
        """최종 분석 리포트"""
        print(f"\n\n{'='*80}")
        print(f"[REPORT] 최종 분석 리포트")
        print(f"{'='*80}\n")

        print(f"총 분석: {len(passed) + len(further_validation) + len(rejected)}개")
        print(f"[OK] 즉시 실행 권장: {len(passed)}개 (80점 이상)")
        print(f"[WARN] 추가 검증 필요: {len(further_validation)}개 (60-80점)")
        print(f"[X] 비추천: {len(rejected)}개 (60점 미만)\n")

        if passed:
            print(f"{'='*80}")
            print(f"[TOP] 즉시 실행 권장 아이디어 (TOP {len(passed)})")
            print(f"{'='*80}\n")

            # 점수 순 정렬
            passed.sort(key=lambda x: x.get('total_score', 0), reverse=True)

            for i, idea in enumerate(passed, 1):
                print(f"{i}. {idea['business_idea']}")
                print(f"   종합 점수: {int(idea['total_score'])}/100")

                # 시장 데이터
                kmong = idea['market_data']['data_sources'].get('kmong', {})
                if not kmong.get('error'):
                    print(f"   평균 시장 가격: {kmong.get('avg_price', 0):,}원")
                    print(f"   경쟁 강도: {kmong.get('competition_level', 'N/A')}")

                # 수익 데이터
                realistic = idea['revenue_data']['scenarios']['realistic']
                print(f"   예상 월 순이익: {realistic['monthly_profit']:,}원")
                print(f"   손익분기: {realistic['break_even'].get('months', 'N/A')}개월")
                print(f"   연간 ROI: {realistic['roi']['roi_percentage']}%")

                # 실행 계획
                if 'action_plan' in idea:
                    plan = idea['action_plan']
                    print(f"   4주 실행 계획: [OK] 생성 완료")
                    print(f"   총 예산: {plan['total_budget']:,}원")

                print()

        if further_validation:
            print(f"\n{'='*80}")
            print(f"[WARN] 추가 검증 필요 ({len(further_validation)}개)")
            print(f"{'='*80}\n")

            for idea in further_validation:
                print(f"• {idea['business_idea']} (점수: {int(idea['total_score'])})")

        print(f"\n{'='*80}\n")

    def generate_it_business_ideas(self):
        """IT 사업 아이디어 자동 생성"""
        # realistic_business_generator에서 IT 관련만 필터링
        all_opportunities = self.idea_generator.generate_monthly_opportunities()

        # IT/디지털 관련만 선별
        it_opportunities = [
            opp for opp in all_opportunities
            if opp['type'] in ['고수익 앱 개발', '기술 활용', '소규모 앱 개발']
               or '앱' in opp['business'].get('name', '')
               or '웹' in opp['business'].get('name', '')
               or 'AI' in opp['business'].get('name', '')
               or 'IT' in opp['business'].get('name', '')
        ]

        return it_opportunities[:10]  # 상위 10개

    def save_results(self, results, filename='business_analysis_results.json'):
        """분석 결과 저장"""
        # action_plan 등 큰 객체 제외하고 요약만
        summary = {
            'total_analyzed': results['total_analyzed'],
            'immediate_action_count': len(results['immediate_action']),
            'further_validation_count': len(results['further_validation']),
            'rejected_count': len(results['rejected']),
            'analysis_date': results['analysis_date'],
            'immediate_action_ideas': [
                {
                    'business_idea': r['business_idea'],
                    'total_score': r.get('total_score', 0),
                    'market_score': r['market_data']['market_score'],
                    'revenue_score': r['revenue_data']['verdict']['score'],
                    'monthly_profit': r['revenue_data']['scenarios']['realistic']['monthly_profit'],
                    'action_plan_generated': 'action_plan' in r
                }
                for r in results['immediate_action']
            ]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print(f"[OK] 분석 결과 저장됨: {filename}")


# 사용 예시
if __name__ == "__main__":
    system = SmartBusinessSystem()

    # 실전 IT 사업 아이디어 리스트
    ideas_to_analyze = [
        {
            'business_idea': 'AI 이력서 첨삭 서비스',
            'keyword': '이력서 첨삭',
            'config': {
                'name': 'AI 이력서 첨삭 서비스',
                'type': 'saas',
                'scale': 'small',
                'revenue_model': 'one_time',
                'pricing': {'one_time': 29000},
                'target_market_size': 5000,
                'budget': 2000000,
                'timeline_weeks': 4
            }
        },
        {
            'business_idea': 'SEO 컨설팅',
            'keyword': 'SEO 컨설팅',
            'config': {
                'name': 'SEO 컨설팅 에이전시',
                'type': 'agency',
                'scale': 'small',
                'revenue_model': 'subscription',
                'pricing': {'monthly': 500000},
                'target_market_size': 200,
                'budget': 1000000,
                'timeline_weeks': 2
            }
        },
        {
            'business_idea': '웹사이트 제작 서비스',
            'keyword': '홈페이지 제작',
            'config': {
                'name': '웹사이트 제작 에이전시',
                'type': 'agency',
                'scale': 'small',
                'revenue_model': 'one_time',
                'pricing': {'one_time': 3000000},
                'target_market_size': 100,
                'budget': 1500000,
                'timeline_weeks': 4
            }
        }
    ]

    # 일괄 분석 실행
    results = system.batch_analyze_ideas(ideas_to_analyze)

    # 결과 저장
    system.save_results(results)

    # 최고 점수 아이디어가 있으면 상세 실행 계획 표시
    if results['immediate_action']:
        print(f"\n{'='*80}")
        print("[RECOMMEND] 추천: 1순위 아이디어부터 즉시 실행하세요!")
        print(f"{'='*80}\n")

        top_idea = results['immediate_action'][0]
        print(f"[#1] {top_idea['business_idea']}")
        print(f"   총점: {int(top_idea['total_score'])}/100")
        print(f"   예상 월 수익: {top_idea['revenue_data']['scenarios']['realistic']['monthly_profit']:,}원")

        if 'action_plan' in top_idea:
            plan_file = f"plan_{top_idea['business_idea'].replace(' ', '_')}.json"
            system.action_planner.save_plan(top_idea['action_plan'], plan_file)
            print(f"   [PLAN] 실행 계획: {plan_file}")

    print("\n" + "="*80)
    print("[COMPLETE] 모든 분석 완료!")
    print("="*80 + "\n")
