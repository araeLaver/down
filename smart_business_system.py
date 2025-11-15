"""
통합 IT 사업 발굴 시스템
- 실시간 시장 분석 + 수익성 검증 + 실행 계획 자동 생성
- 80점 이상 아이디어만 선별하여 즉시 실행 가능한 계획 제공
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from real_market_analyzer import RealMarketAnalyzer
from revenue_validator import RevenueValidator
from action_plan_generator import ActionPlanGenerator
from realistic_business_generator import RealisticBusinessGenerator

import json
from datetime import datetime
import time

class SmartBusinessSystem:
    def __init__(self):
        self.market_analyzer = RealMarketAnalyzer()
        self.revenue_validator = RevenueValidator()
        self.action_planner = ActionPlanGenerator()
        self.idea_generator = RealisticBusinessGenerator()

        # Windows 콘솔 호환성을 위해 이모지 제거
        print("="*80)
        print("[SMART] 스마트 IT 사업 발굴 시스템")
        print("="*80)
        print("실시간 시장 분석 -> 수익성 검증 -> 실행 계획 자동 생성\n")

    def analyze_business_idea(self, business_idea, keyword, business_config):
        """단일 사업 아이디어 종합 분석"""
        print(f"\n{'='*80}")
        print(f"📊 사업 아이디어 분석: {business_idea}")
        print(f"{'='*80}\n")

        # 1단계: 시장 분석
        print("1️⃣  실시간 시장 분석 중...")
        market_data = self.market_analyzer.comprehensive_analysis(business_idea, keyword)
        market_score = market_data['market_score']

        print(f"   시장 점수: {market_score}/100")

        # 점수 낮으면 조기 종료
        if market_score < 60:
            print(f"   ❌ 시장 점수 부족 (60점 미만). 다른 아이디어 권장.\n")
            return {
                'business_idea': business_idea,
                'passed': False,
                'reason': '시장 점수 부족',
                'market_score': market_score
            }

        # 2단계: 수익성 검증
        print("\n2️⃣  수익성 검증 중...")
        revenue_data = self.revenue_validator.comprehensive_validation(business_config)
        realistic_scenario = revenue_data['scenarios']['realistic']
        verdict_score = revenue_data['verdict']['score']

        print(f"   수익성 점수: {verdict_score}/100")
        print(f"   월 예상 순이익: {realistic_scenario['monthly_profit']:,}원")

        # 수익성 낮으면 조기 종료
        if verdict_score < 60:
            print(f"   ❌ 수익성 부족. 다른 아이디어 권장.\n")
            return {
                'business_idea': business_idea,
                'passed': False,
                'reason': '수익성 부족',
                'market_score': market_score,
                'revenue_score': verdict_score
            }

        # 종합 점수 계산
        total_score = (market_score * 0.6) + (verdict_score * 0.4)

        print(f"\n   📈 종합 점수: {total_score:.1f}/100")

        # 70점 이상이면 실행 계획 생성
        if total_score >= 70:
            print(f"   ✅ 우수한 아이디어! 실행 계획 생성 중...\n")

            # 3단계: 실행 계획 자동 생성
            print("3️⃣  4주 실행 계획 생성 중...")
            action_plan = self.action_planner.generate_comprehensive_plan(business_config)

            print(f"\n   ✅ 실행 계획 완성!")

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
            print(f"   ⚠️  보통 수준. 추가 검증 필요.\n")
            return {
                'business_idea': business_idea,
                'passed': True,
                'total_score': total_score,
                'market_data': market_data,
                'revenue_data': revenue_data,
                'recommendation': 'FURTHER_VALIDATION'
            }

    def batch_analyze_ideas(self, ideas_list):
        """여러 아이디어 일괄 분석"""
        print(f"\n{'='*80}")
        print(f"🔍 {len(ideas_list)}개 아이디어 일괄 분석 시작")
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
                print("\n⏳ 5초 대기 중...")
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
        print(f"📊 최종 분석 리포트")
        print(f"{'='*80}\n")

        print(f"총 분석: {len(passed) + len(further_validation) + len(rejected)}개")
        print(f"✅ 즉시 실행 권장: {len(passed)}개 (80점 이상)")
        print(f"⚠️  추가 검증 필요: {len(further_validation)}개 (60-80점)")
        print(f"❌ 비추천: {len(rejected)}개 (60점 미만)\n")

        if passed:
            print(f"{'='*80}")
            print(f"🏆 즉시 실행 권장 아이디어 (TOP {len(passed)})")
            print(f"{'='*80}\n")

            # 점수 순 정렬
            passed.sort(key=lambda x: x.get('total_score', 0), reverse=True)

            for i, idea in enumerate(passed, 1):
                print(f"{i}. {idea['business_idea']}")
                print(f"   종합 점수: {idea['total_score']:.1f}/100")

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
                    print(f"   4주 실행 계획: ✅ 생성 완료")
                    print(f"   총 예산: {plan['total_budget']:,}원")

                print()

        if further_validation:
            print(f"\n{'='*80}")
            print(f"⚠️  추가 검증 필요 ({len(further_validation)}개)")
            print(f"{'='*80}\n")

            for idea in further_validation:
                print(f"• {idea['business_idea']} (점수: {idea['total_score']:.1f})")

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

        print(f"✅ 분석 결과 저장됨: {filename}")


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
        print("💡 추천: 1순위 아이디어부터 즉시 실행하세요!")
        print(f"{'='*80}\n")

        top_idea = results['immediate_action'][0]
        print(f"🥇 {top_idea['business_idea']}")
        print(f"   총점: {top_idea['total_score']:.1f}/100")
        print(f"   예상 월 수익: {top_idea['revenue_data']['scenarios']['realistic']['monthly_profit']:,}원")

        if 'action_plan' in top_idea:
            plan_file = f"plan_{top_idea['business_idea'].replace(' ', '_')}.json"
            system.action_planner.save_plan(top_idea['action_plan'], plan_file)
            print(f"   📋 실행 계획: {plan_file}")

    print("\n" + "="*80)
    print("✅ 모든 분석 완료!")
    print("="*80 + "\n")
