"""
비즈니스 관련 모듈 테스트
- revenue_validator.py
- business_meeting.py
- business_monitor.py
- business_discovery_history.py
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestRevenueValidator:
    """RevenueValidator 클래스 테스트"""

    def test_init_has_standard_costs(self):
        """초기화 시 표준 비용 존재"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()
        assert 'domain' in validator.standard_costs
        assert 'hosting' in validator.standard_costs
        assert 'tools' in validator.standard_costs
        assert 'marketing' in validator.standard_costs

    def test_calculate_startup_costs_saas_small(self):
        """SaaS 소규모 초기 비용 계산"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()
        costs = validator.calculate_startup_costs('saas', 'small')

        assert 'development' in costs
        assert 'infrastructure' in costs
        assert 'marketing' in costs
        assert 'operations' in costs
        assert 'total' in costs
        assert costs['total'] > 0
        assert costs['total'] == sum(v for k, v in costs.items() if k != 'total')

    def test_calculate_startup_costs_saas_medium(self):
        """SaaS 중규모 초기 비용 계산"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()
        costs_small = validator.calculate_startup_costs('saas', 'small')
        costs_medium = validator.calculate_startup_costs('saas', 'medium')

        # 중규모는 소규모보다 비용이 높아야 함
        assert costs_medium['total'] > costs_small['total']

    def test_calculate_startup_costs_agency(self):
        """에이전시 초기 비용 계산"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()
        costs = validator.calculate_startup_costs('agency', 'small')

        assert costs['total'] > 0
        assert costs['development'] > 0

    def test_calculate_startup_costs_marketplace(self):
        """마켓플레이스 초기 비용 계산"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()
        costs = validator.calculate_startup_costs('marketplace', 'small')

        assert costs['total'] > 0

    def test_calculate_startup_costs_tool(self):
        """도구 초기 비용 계산"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()
        costs = validator.calculate_startup_costs('tool', 'small')

        assert costs['total'] > 0

    def test_calculate_monthly_costs_low_customer(self):
        """고객 수 적을 때 월 운영 비용"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()
        costs = validator.calculate_monthly_costs('saas', 'small', customer_count=50)

        assert 'hosting' in costs
        assert 'tools' in costs
        assert 'marketing' in costs
        assert 'support' in costs
        assert 'total' in costs
        assert costs['hosting'] == validator.standard_costs['hosting']['cloud_small']

    def test_calculate_monthly_costs_medium_customer(self):
        """고객 수 중간일 때 월 운영 비용"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()
        costs = validator.calculate_monthly_costs('saas', 'small', customer_count=500)

        assert costs['hosting'] == validator.standard_costs['hosting']['cloud_medium']

    def test_calculate_monthly_costs_high_customer(self):
        """고객 수 많을 때 월 운영 비용"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()
        costs = validator.calculate_monthly_costs('saas', 'small', customer_count=2000)

        assert costs['hosting'] == validator.standard_costs['hosting']['cloud_large']

    def test_calculate_monthly_costs_support_scales(self):
        """고객 지원 비용 고객 수에 비례"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()
        costs_100 = validator.calculate_monthly_costs('saas', 'small', customer_count=100)
        costs_200 = validator.calculate_monthly_costs('saas', 'small', customer_count=200)

        assert costs_200['support'] == costs_100['support'] * 2

    def test_simulate_revenue_subscription(self):
        """구독형 매출 시뮬레이션"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        pricing = {'monthly': 30000}
        scenarios = validator.simulate_revenue('subscription', pricing, target_market_size=10000)

        assert 'conservative' in scenarios
        assert 'realistic' in scenarios
        assert 'optimistic' in scenarios

        for scenario in scenarios.values():
            assert 'monthly_customers' in scenario
            assert 'monthly_revenue' in scenario
            assert 'annual_revenue' in scenario
            assert 'customer_ltv' in scenario

    def test_simulate_revenue_one_time(self):
        """일회성 매출 시뮬레이션"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        pricing = {'one_time': 1000000}
        scenarios = validator.simulate_revenue('one_time', pricing, target_market_size=1000)

        assert scenarios['realistic']['monthly_revenue'] > 0

    def test_simulate_revenue_commission(self):
        """수수료 기반 매출 시뮬레이션"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        pricing = {
            'avg_transaction': 500000,
            'commission_rate': 0.1,
            'transactions_per_month': 3
        }
        scenarios = validator.simulate_revenue('commission', pricing, target_market_size=5000)

        assert scenarios['realistic']['monthly_revenue'] > 0

    def test_calculate_break_even_possible(self):
        """손익분기점 도달 가능"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        result = validator.calculate_break_even(
            startup_costs=5000000,
            monthly_costs=500000,
            monthly_revenue=1000000
        )

        assert result['break_even_possible'] is True
        assert 'months' in result
        assert result['months'] == 10.0  # 5M / 500K = 10 months

    def test_calculate_break_even_impossible(self):
        """손익분기점 도달 불가능"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        result = validator.calculate_break_even(
            startup_costs=5000000,
            monthly_costs=1000000,
            monthly_revenue=500000  # 비용보다 낮음
        )

        assert result['break_even_possible'] is False
        assert 'message' in result

    def test_calculate_roi(self):
        """ROI 계산"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        result = validator.calculate_roi(
            startup_costs=10000000,
            annual_revenue=30000000,
            annual_costs=10000000
        )

        assert 'annual_profit' in result
        assert 'roi_percentage' in result
        assert 'payback_period_years' in result
        assert 'rating' in result
        assert result['annual_profit'] == 20000000
        assert result['roi_percentage'] == 200.0

    def test_rate_roi_grades(self):
        """ROI 등급 평가"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        assert validator._rate_roi(250) == '매우 우수'
        assert validator._rate_roi(150) == '우수'
        assert validator._rate_roi(75) == '양호'
        assert validator._rate_roi(35) == '보통'
        assert validator._rate_roi(10) == '미흡'

    def test_generate_verdict_very_promising(self):
        """최종 판정 - 매우 유망"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        scenario = {
            'roi': {'roi_percentage': 150},
            'break_even': {'months': 8},
            'monthly_profit': 2000000
        }

        verdict = validator._generate_verdict(scenario)
        assert verdict['verdict'] == '매우 유망'
        assert verdict['score'] == 90

    def test_generate_verdict_promising(self):
        """최종 판정 - 유망"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        scenario = {
            'roi': {'roi_percentage': 70},
            'break_even': {'months': 15},
            'monthly_profit': 800000
        }

        verdict = validator._generate_verdict(scenario)
        assert verdict['verdict'] == '유망'
        assert verdict['score'] == 70

    def test_generate_verdict_not_recommended(self):
        """최종 판정 - 비추천"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        scenario = {
            'roi': {'roi_percentage': 10},
            'break_even': {'months': 36},
            'monthly_profit': 100000
        }

        verdict = validator._generate_verdict(scenario)
        assert verdict['verdict'] == '비추천'
        assert verdict['score'] == 30


class TestBusinessMeeting:
    """비즈니스 회의 모듈 테스트"""

    def test_conduct_meeting_discussion_returns_notes(self):
        """회의 토론 내용 반환"""
        from business_meeting import conduct_meeting_discussion

        notes = conduct_meeting_discussion()

        assert notes is not None
        assert len(notes) > 0
        assert 'Qhyx' in notes

    @pytest.mark.skip(reason="DB 의존성 - 통합 테스트로 분류")
    def test_conduct_business_review_meeting(self):
        """비즈니스 검토 회의 진행"""
        from business_meeting import conduct_business_review_meeting
        meeting_id, plans = conduct_business_review_meeting()
        assert meeting_id is not None
        assert len(plans) > 0

    def test_create_business_plans_structure(self):
        """비즈니스 플랜 생성 구조 검증"""
        mock_session = MagicMock()

        with patch('business_meeting.Session', return_value=mock_session):
            from business_meeting import create_business_plans
            plans = create_business_plans(mock_session)

            assert len(plans) == 3
            mock_session.add.assert_called()
            mock_session.commit.assert_called()


class TestQhyxBusinessMonitor:
    """QhyxBusinessMonitor 클래스 테스트"""

    def test_init_creates_session(self):
        """초기화 시 세션 생성"""
        with patch('business_monitor.Session') as mock_session:
            from business_monitor import QhyxBusinessMonitor
            monitor = QhyxBusinessMonitor()
            mock_session.assert_called_once()

    def test_get_current_status_returns_report(self):
        """현재 상태 리포트 반환"""
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value.count.return_value = 5
        mock_query.filter.return_value.order_by.return_value.limit.return_value.all.return_value = []
        mock_session.query.return_value = mock_query

        with patch('business_monitor.Session', return_value=mock_session):
            from business_monitor import QhyxBusinessMonitor
            monitor = QhyxBusinessMonitor()
            report = monitor.get_current_status()

            assert 'Qhyx Inc.' in report
            assert '비즈니스 현황' in report

    def test_get_recent_activities(self):
        """최근 활동 조회"""
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value.order_by.return_value.all.return_value = []
        mock_query.filter.return_value.order_by.return_value.limit.return_value.all.return_value = []
        mock_session.query.return_value = mock_query

        with patch('business_monitor.Session', return_value=mock_session):
            from business_monitor import QhyxBusinessMonitor
            monitor = QhyxBusinessMonitor()
            activities = monitor.get_recent_activities(hours=24)

            assert '활동 내역' in activities

    def test_get_performance_metrics_no_data(self):
        """성과 지표 - 데이터 없음"""
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value.all.return_value = []
        mock_session.query.return_value = mock_query

        with patch('business_monitor.Session', return_value=mock_session):
            from business_monitor import QhyxBusinessMonitor
            monitor = QhyxBusinessMonitor()
            metrics = monitor.get_performance_metrics()

            assert '데이터 수집 중' in metrics

    def test_close_session(self):
        """세션 종료"""
        mock_session = MagicMock()

        with patch('business_monitor.Session', return_value=mock_session):
            from business_monitor import QhyxBusinessMonitor
            monitor = QhyxBusinessMonitor()
            monitor.close()
            mock_session.close.assert_called_once()


class TestBusinessDiscoveryHistoryModels:
    """사업 발굴 히스토리 모델 테스트"""

    def test_business_discovery_history_has_fields(self):
        """BusinessDiscoveryHistory 필드 존재"""
        from business_discovery_history import BusinessDiscoveryHistory

        assert hasattr(BusinessDiscoveryHistory, 'id')
        assert hasattr(BusinessDiscoveryHistory, 'discovered_at')
        assert hasattr(BusinessDiscoveryHistory, 'business_name')
        assert hasattr(BusinessDiscoveryHistory, 'total_score')
        assert hasattr(BusinessDiscoveryHistory, 'market_score')
        assert hasattr(BusinessDiscoveryHistory, 'revenue_score')

    def test_business_analysis_snapshot_has_fields(self):
        """BusinessAnalysisSnapshot 필드 존재"""
        from business_discovery_history import BusinessAnalysisSnapshot

        assert hasattr(BusinessAnalysisSnapshot, 'id')
        assert hasattr(BusinessAnalysisSnapshot, 'snapshot_time')
        assert hasattr(BusinessAnalysisSnapshot, 'snapshot_type')
        assert hasattr(BusinessAnalysisSnapshot, 'total_analyzed')
        assert hasattr(BusinessAnalysisSnapshot, 'avg_total_score')

    def test_business_insight_has_fields(self):
        """BusinessInsight 필드 존재"""
        from business_discovery_history import BusinessInsight

        assert hasattr(BusinessInsight, 'id')
        assert hasattr(BusinessInsight, 'insight_type')
        assert hasattr(BusinessInsight, 'title')
        assert hasattr(BusinessInsight, 'confidence_score')
        assert hasattr(BusinessInsight, 'impact_level')

    def test_low_score_business_has_fields(self):
        """LowScoreBusiness 필드 존재"""
        from business_discovery_history import LowScoreBusiness

        assert hasattr(LowScoreBusiness, 'id')
        assert hasattr(LowScoreBusiness, 'business_name')
        assert hasattr(LowScoreBusiness, 'total_score')
        assert hasattr(LowScoreBusiness, 'failure_reason')
        assert hasattr(LowScoreBusiness, 'improvement_suggestions')


class TestBusinessHistoryTracker:
    """BusinessHistoryTracker 클래스 테스트"""

    def test_init_creates_session(self):
        """초기화 시 세션 생성"""
        with patch('business_discovery_history.Session') as mock_session:
            from business_discovery_history import BusinessHistoryTracker
            tracker = BusinessHistoryTracker()
            mock_session.assert_called_once()

    def test_refresh_session(self):
        """세션 새로고침"""
        mock_session = MagicMock()

        with patch('business_discovery_history.Session', return_value=mock_session):
            from business_discovery_history import BusinessHistoryTracker
            tracker = BusinessHistoryTracker()
            tracker.refresh_session()

            mock_session.rollback.assert_called()
            mock_session.close.assert_called()

    def test_safe_commit_success(self):
        """안전한 커밋 성공"""
        mock_session = MagicMock()

        with patch('business_discovery_history.Session', return_value=mock_session):
            from business_discovery_history import BusinessHistoryTracker
            tracker = BusinessHistoryTracker()
            result = tracker.safe_commit()

            assert result is True
            mock_session.commit.assert_called_once()

    def test_safe_commit_retry_on_failure(self):
        """커밋 실패 시 재시도"""
        mock_session = MagicMock()
        mock_session.commit.side_effect = [Exception("Error"), None]

        with patch('business_discovery_history.Session', return_value=mock_session):
            with patch('time.sleep'):
                from business_discovery_history import BusinessHistoryTracker
                tracker = BusinessHistoryTracker()
                result = tracker.safe_commit(max_retries=2)

                assert mock_session.commit.call_count == 2

    def test_generate_improvement_suggestions_low_market(self):
        """개선 제안 생성 - 낮은 시장성"""
        mock_session = MagicMock()

        with patch('business_discovery_history.Session', return_value=mock_session):
            from business_discovery_history import BusinessHistoryTracker
            tracker = BusinessHistoryTracker()

            suggestions = tracker._generate_improvement_suggestions(
                failure_reason='low_market',
                market_score=25,
                revenue_score=70,
                category='IT'
            )

            assert len(suggestions) >= 1
            market_suggestion = next(s for s in suggestions if s['area'] == 'market')
            assert market_suggestion['severity'] == 'critical'

    def test_generate_improvement_suggestions_low_revenue(self):
        """개선 제안 생성 - 낮은 수익성"""
        mock_session = MagicMock()

        with patch('business_discovery_history.Session', return_value=mock_session):
            from business_discovery_history import BusinessHistoryTracker
            tracker = BusinessHistoryTracker()

            suggestions = tracker._generate_improvement_suggestions(
                failure_reason='low_revenue',
                market_score=75,
                revenue_score=20,
                category='SaaS'
            )

            assert len(suggestions) >= 1
            revenue_suggestion = next(s for s in suggestions if s['area'] == 'revenue')
            assert revenue_suggestion['severity'] == 'critical'

    def test_generate_improvement_suggestions_both(self):
        """개선 제안 생성 - 둘 다 낮음"""
        mock_session = MagicMock()

        with patch('business_discovery_history.Session', return_value=mock_session):
            from business_discovery_history import BusinessHistoryTracker
            tracker = BusinessHistoryTracker()

            suggestions = tracker._generate_improvement_suggestions(
                failure_reason='both',
                market_score=35,
                revenue_score=40,
                category='마켓플레이스'
            )

            assert len(suggestions) >= 2
            areas = [s['area'] for s in suggestions]
            assert 'market' in areas
            assert 'revenue' in areas

    def test_calculate_improvement_rate(self):
        """개선 가능성 비율 계산"""
        mock_session = MagicMock()

        with patch('business_discovery_history.Session', return_value=mock_session):
            from business_discovery_history import BusinessHistoryTracker
            tracker = BusinessHistoryTracker()

            # Mock low score objects
            mock_low_scores = [
                MagicMock(total_score=55),  # 50 이상 - 개선 가능
                MagicMock(total_score=52),  # 50 이상 - 개선 가능
                MagicMock(total_score=45),  # 50 미만
                MagicMock(total_score=30),  # 50 미만
            ]

            rate = tracker._calculate_improvement_rate(mock_low_scores)
            assert rate == 50.0  # 2/4 = 50%

    def test_calculate_improvement_rate_empty(self):
        """개선 가능성 비율 - 빈 리스트"""
        mock_session = MagicMock()

        with patch('business_discovery_history.Session', return_value=mock_session):
            from business_discovery_history import BusinessHistoryTracker
            tracker = BusinessHistoryTracker()

            rate = tracker._calculate_improvement_rate([])
            assert rate == 0


class TestRevenueScenarios:
    """수익 시나리오별 테스트"""

    def test_conservative_has_lowest_conversion(self):
        """보수적 시나리오는 가장 낮은 전환율"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        pricing = {'monthly': 50000}
        scenarios = validator.simulate_revenue('subscription', pricing, target_market_size=10000)

        assert scenarios['conservative']['monthly_customers'] < scenarios['realistic']['monthly_customers']
        assert scenarios['realistic']['monthly_customers'] < scenarios['optimistic']['monthly_customers']

    def test_annual_revenue_is_12x_monthly(self):
        """연매출은 월매출의 12배"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        pricing = {'monthly': 30000}
        scenarios = validator.simulate_revenue('subscription', pricing, target_market_size=5000)

        for scenario in scenarios.values():
            assert scenario['annual_revenue'] == scenario['monthly_revenue'] * 12


class TestEdgeCases:
    """엣지 케이스 테스트"""

    def test_unknown_business_type_startup_costs(self):
        """알 수 없는 비즈니스 타입 초기 비용"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        costs = validator.calculate_startup_costs('unknown_type', 'small')

        # 알 수 없는 타입은 모든 비용이 0
        assert costs['total'] == 0

    def test_zero_target_market_revenue(self):
        """타겟 시장 0일 때 매출"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        pricing = {'monthly': 50000}
        scenarios = validator.simulate_revenue('subscription', pricing, target_market_size=0)

        for scenario in scenarios.values():
            assert scenario['monthly_customers'] == 0
            assert scenario['monthly_revenue'] == 0
            assert scenario['customer_ltv'] == 0  # 0으로 나누기 방지

    def test_negative_roi(self):
        """음수 ROI"""
        from revenue_validator import RevenueValidator
        validator = RevenueValidator()

        result = validator.calculate_roi(
            startup_costs=10000000,
            annual_revenue=5000000,
            annual_costs=10000000
        )

        assert result['annual_profit'] == -5000000
        assert result['roi_percentage'] == -50.0
        assert result['payback_period_years'] is None  # 음수 수익이면 None

