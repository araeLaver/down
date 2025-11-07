"""
수익성 검증 모듈
- 실제 비용 계산
- 예상 매출 시뮬레이션
- 손익분기점 분석
- 시나리오별 ROI 계산
"""

from datetime import datetime, timedelta
import json

class RevenueValidator:
    def __init__(self):
        # IT 사업 표준 비용
        self.standard_costs = {
            'domain': 15000,  # 연간
            'hosting': {
                'shared': 10000,  # 월
                'vps': 30000,
                'cloud_small': 50000,
                'cloud_medium': 150000,
                'cloud_large': 500000
            },
            'ssl': 0,  # Let's Encrypt 무료
            'email': 5000,  # 월 (G Suite)
            'tools': {
                'design': 20000,  # Figma, Canva 등
                'development': 30000,  # 각종 개발 도구
                'marketing': 50000,  # 마케팅 툴
                'analytics': 10000,  # GA, Mixpanel 등
                'crm': 30000  # 고객 관리
            },
            'marketing': {
                'google_ads_cpc': 800,  # 클릭당
                'facebook_ads_cpm': 5000,  # 1000노출당
                'seo': 500000,  # 월 (대행사)
                'content_marketing': 300000  # 월
            },
            'outsourcing': {
                'designer': 50000,  # 일당
                'developer': 80000,  # 일당
                'marketer': 40000,  # 일당
                'writer': 30000  # 일당
            }
        }

    def calculate_startup_costs(self, business_type, scale='small'):
        """초기 투자 비용 계산"""
        costs = {
            'development': 0,
            'infrastructure': 0,
            'marketing': 0,
            'operations': 0,
            'total': 0
        }

        if business_type == 'saas':
            if scale == 'small':
                costs['development'] = 2000000  # 노코드 또는 간단한 개발
                costs['infrastructure'] = 100000  # 첫 달 서버
                costs['marketing'] = 500000  # 초기 광고
                costs['operations'] = 200000  # 기타
            elif scale == 'medium':
                costs['development'] = 5000000  # 외주 개발
                costs['infrastructure'] = 300000
                costs['marketing'] = 1500000
                costs['operations'] = 500000
            else:  # large
                costs['development'] = 15000000  # 풀스택 개발
                costs['infrastructure'] = 1000000
                costs['marketing'] = 5000000
                costs['operations'] = 2000000

        elif business_type == 'agency':
            if scale == 'small':
                costs['development'] = 500000  # 웹사이트 + 포트폴리오
                costs['infrastructure'] = 50000
                costs['marketing'] = 1000000  # 고객 확보
                costs['operations'] = 300000
            elif scale == 'medium':
                costs['development'] = 2000000
                costs['infrastructure'] = 200000
                costs['marketing'] = 3000000
                costs['operations'] = 1000000

        elif business_type == 'marketplace':
            if scale == 'small':
                costs['development'] = 3000000
                costs['infrastructure'] = 200000
                costs['marketing'] = 2000000  # 양쪽 확보
                costs['operations'] = 500000
            elif scale == 'medium':
                costs['development'] = 10000000
                costs['infrastructure'] = 1000000
                costs['marketing'] = 10000000
                costs['operations'] = 2000000

        elif business_type == 'tool':
            if scale == 'small':
                costs['development'] = 1000000  # 간단한 도구
                costs['infrastructure'] = 50000
                costs['marketing'] = 300000
                costs['operations'] = 100000

        costs['total'] = sum(costs.values())
        return costs

    def calculate_monthly_costs(self, business_type, scale='small', customer_count=0):
        """월 운영 비용 계산"""
        costs = {
            'hosting': 0,
            'tools': 0,
            'marketing': 0,
            'support': 0,
            'payment_fees': 0,
            'total': 0
        }

        # 호스팅 (고객 수에 따라 증가)
        if customer_count < 100:
            costs['hosting'] = self.standard_costs['hosting']['cloud_small']
        elif customer_count < 1000:
            costs['hosting'] = self.standard_costs['hosting']['cloud_medium']
        else:
            costs['hosting'] = self.standard_costs['hosting']['cloud_large']

        # SaaS 도구
        if scale == 'small':
            costs['tools'] = 50000
        elif scale == 'medium':
            costs['tools'] = 150000
        else:
            costs['tools'] = 500000

        # 마케팅
        if business_type == 'saas':
            costs['marketing'] = 500000 if scale == 'small' else 2000000
        elif business_type == 'agency':
            costs['marketing'] = 300000 if scale == 'small' else 1000000

        # 고객 지원
        costs['support'] = customer_count * 1000  # 고객당 월 1000원

        costs['total'] = sum(costs.values())
        return costs

    def simulate_revenue(self, business_model, pricing, target_market_size):
        """매출 시뮬레이션 (보수적/현실적/낙관적)"""
        scenarios = {
            'conservative': {},
            'realistic': {},
            'optimistic': {}
        }

        # 전환율 가정
        conversion_rates = {
            'conservative': 0.01,  # 1%
            'realistic': 0.03,     # 3%
            'optimistic': 0.05     # 5%
        }

        for scenario, conversion_rate in conversion_rates.items():
            monthly_customers = int(target_market_size * conversion_rate)

            if business_model == 'subscription':
                monthly_revenue = monthly_customers * pricing['monthly']
                annual_revenue = monthly_revenue * 12

            elif business_model == 'one_time':
                # 월 신규 고객 기준
                monthly_revenue = monthly_customers * pricing['one_time']
                annual_revenue = monthly_revenue * 12

            elif business_model == 'commission':
                # 거래액 기반
                avg_transaction = pricing['avg_transaction']
                commission_rate = pricing['commission_rate']
                transactions_per_customer = pricing.get('transactions_per_month', 5)

                monthly_revenue = monthly_customers * transactions_per_customer * avg_transaction * commission_rate
                annual_revenue = monthly_revenue * 12

            scenarios[scenario] = {
                'monthly_customers': monthly_customers,
                'monthly_revenue': int(monthly_revenue),
                'annual_revenue': int(annual_revenue),
                'customer_ltv': int(annual_revenue / monthly_customers) if monthly_customers > 0 else 0
            }

        return scenarios

    def calculate_break_even(self, startup_costs, monthly_costs, monthly_revenue):
        """손익분기점 계산"""
        if monthly_revenue <= monthly_costs:
            return {
                'break_even_possible': False,
                'message': '월 매출이 월 비용보다 낮음. 가격이나 고객 수 조정 필요'
            }

        monthly_profit = monthly_revenue - monthly_costs
        months_to_break_even = startup_costs / monthly_profit

        return {
            'break_even_possible': True,
            'months': round(months_to_break_even, 1),
            'date': (datetime.now() + timedelta(days=30 * months_to_break_even)).strftime('%Y-%m-%d'),
            'monthly_profit': int(monthly_profit),
            'annual_profit': int(monthly_profit * 12)
        }

    def calculate_roi(self, startup_costs, annual_revenue, annual_costs):
        """ROI 계산"""
        annual_profit = annual_revenue - annual_costs
        roi_percentage = (annual_profit / startup_costs) * 100

        return {
            'annual_profit': int(annual_profit),
            'roi_percentage': round(roi_percentage, 2),
            'payback_period_years': round(startup_costs / annual_profit, 2) if annual_profit > 0 else None,
            'rating': self._rate_roi(roi_percentage)
        }

    def _rate_roi(self, roi_percentage):
        """ROI 등급"""
        if roi_percentage >= 200:
            return '매우 우수'
        elif roi_percentage >= 100:
            return '우수'
        elif roi_percentage >= 50:
            return '양호'
        elif roi_percentage >= 20:
            return '보통'
        else:
            return '미흡'

    def comprehensive_validation(self, business_config):
        """종합 수익성 검증"""
        print(f"\n{'='*60}")
        print(f"수익성 검증: {business_config['name']}")
        print(f"{'='*60}\n")

        # 1. 초기 비용
        startup_costs_detail = self.calculate_startup_costs(
            business_config['type'],
            business_config.get('scale', 'small')
        )
        startup_costs = startup_costs_detail['total']

        print(f"1. 초기 투자 비용")
        for key, value in startup_costs_detail.items():
            if key != 'total':
                print(f"   {key}: {value:,}원")
        print(f"   총 투자: {startup_costs:,}원\n")

        # 2. 월 비용 (시나리오별)
        scenarios_costs = {}
        scenarios_revenue = self.simulate_revenue(
            business_config['revenue_model'],
            business_config['pricing'],
            business_config['target_market_size']
        )

        print(f"2. 시나리오별 예측\n")

        results = {}

        for scenario_name, scenario_data in scenarios_revenue.items():
            monthly_customers = scenario_data['monthly_customers']

            monthly_costs_detail = self.calculate_monthly_costs(
                business_config['type'],
                business_config.get('scale', 'small'),
                monthly_customers
            )
            monthly_costs = monthly_costs_detail['total']

            # 손익분기점
            break_even = self.calculate_break_even(
                startup_costs,
                monthly_costs,
                scenario_data['monthly_revenue']
            )

            # ROI
            annual_costs = monthly_costs * 12
            roi = self.calculate_roi(
                startup_costs,
                scenario_data['annual_revenue'],
                annual_costs
            )

            results[scenario_name] = {
                'customers': monthly_customers,
                'monthly_revenue': scenario_data['monthly_revenue'],
                'monthly_costs': monthly_costs,
                'monthly_profit': scenario_data['monthly_revenue'] - monthly_costs,
                'annual_revenue': scenario_data['annual_revenue'],
                'annual_costs': annual_costs,
                'break_even': break_even,
                'roi': roi
            }

            # 출력
            print(f"   [{scenario_name.upper()}]")
            print(f"   월 고객: {monthly_customers}명")
            print(f"   월 매출: {scenario_data['monthly_revenue']:,}원")
            print(f"   월 비용: {monthly_costs:,}원")
            print(f"   월 순이익: {scenario_data['monthly_revenue'] - monthly_costs:,}원")

            if break_even['break_even_possible']:
                print(f"   손익분기: {break_even['months']}개월")
            else:
                print(f"   손익분기: 불가 ({break_even['message']})")

            print(f"   연간 ROI: {roi['roi_percentage']}% ({roi['rating']})")
            print()

        # 3. 최종 판정
        realistic = results['realistic']
        verdict = self._generate_verdict(realistic)

        print(f"3. 최종 평가")
        print(f"   판정: {verdict['verdict']}")
        print(f"   신뢰도: {verdict['confidence']}")
        print(f"   권장사항: {verdict['recommendation']}")
        print(f"\n{'='*60}\n")

        return {
            'business_name': business_config['name'],
            'startup_costs': startup_costs_detail,
            'scenarios': results,
            'verdict': verdict,
            'analysis_date': datetime.now().isoformat()
        }

    def _generate_verdict(self, realistic_scenario):
        """최종 판정"""
        roi = realistic_scenario['roi']['roi_percentage']
        break_even_months = realistic_scenario['break_even'].get('months', 999)
        monthly_profit = realistic_scenario['monthly_profit']

        if roi >= 100 and break_even_months <= 12 and monthly_profit > 1000000:
            return {
                'verdict': '매우 유망',
                'confidence': '높음',
                'recommendation': '즉시 실행 권장',
                'score': 90
            }
        elif roi >= 50 and break_even_months <= 18 and monthly_profit > 500000:
            return {
                'verdict': '유망',
                'confidence': '중간',
                'recommendation': '추가 검증 후 진행',
                'score': 70
            }
        elif roi >= 20 and break_even_months <= 24:
            return {
                'verdict': '보통',
                'confidence': '낮음',
                'recommendation': '신중한 접근 필요',
                'score': 50
            }
        else:
            return {
                'verdict': '비추천',
                'confidence': '매우 낮음',
                'recommendation': '다른 아이템 검토 권장',
                'score': 30
            }

    def save_validation(self, results, filename='revenue_validation.json'):
        """검증 결과 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"수익성 검증 결과 저장됨: {filename}")


# 사용 예시
if __name__ == "__main__":
    validator = RevenueValidator()

    # 예시 1: SaaS 프로젝트 관리 도구
    saas_config = {
        'name': 'AI 프로젝트 관리 도구',
        'type': 'saas',
        'scale': 'small',
        'revenue_model': 'subscription',
        'pricing': {
            'monthly': 29000  # 월 구독료
        },
        'target_market_size': 10000  # 타겟 시장 크기 (월 방문자)
    }

    result1 = validator.comprehensive_validation(saas_config)

    # 예시 2: 웹 개발 에이전시
    agency_config = {
        'name': '웹 개발 에이전시',
        'type': 'agency',
        'scale': 'small',
        'revenue_model': 'one_time',
        'pricing': {
            'one_time': 3000000  # 프로젝트당 가격
        },
        'target_market_size': 100  # 월 리드
    }

    result2 = validator.comprehensive_validation(agency_config)

    # 예시 3: 프리랜서 마켓플레이스
    marketplace_config = {
        'name': '프리랜서 마켓플레이스',
        'type': 'marketplace',
        'scale': 'small',
        'revenue_model': 'commission',
        'pricing': {
            'avg_transaction': 500000,  # 평균 거래액
            'commission_rate': 0.15,    # 15% 수수료
            'transactions_per_month': 3  # 고객당 월 거래 횟수
        },
        'target_market_size': 5000  # 월 방문자
    }

    result3 = validator.comprehensive_validation(marketplace_config)

    # 종합 결과 비교
    print("\n" + "="*60)
    print("🏆 수익성 비교")
    print("="*60 + "\n")

    all_results = [
        ('SaaS', result1),
        ('Agency', result2),
        ('Marketplace', result3)
    ]

    for name, result in all_results:
        realistic = result['scenarios']['realistic']
        print(f"{name}:")
        print(f"  초기 투자: {result['startup_costs']['total']:,}원")
        print(f"  월 순이익: {realistic['monthly_profit']:,}원")
        print(f"  연간 ROI: {realistic['roi']['roi_percentage']}%")
        print(f"  손익분기: {realistic['break_even'].get('months', 'N/A')}개월")
        print(f"  판정: {result['verdict']['verdict']}")
        print()
