"""
사업 발굴 히스토리 추적 시스템
- 모든 분석 결과를 상세하게 기록
- 시간대별, 카테고리별, 점수별 다양한 시각 제공
- 트렌드 분석 및 인사이트 도출
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Text, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from database_setup import Base, Session, SCHEMA_NAME, engine
import json

# 새로운 히스토리 테이블들
class BusinessDiscoveryHistory(Base):
    """사업 발굴 전체 히스토리 (모든 분석 결과 저장)"""
    __tablename__ = 'business_discovery_history'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    discovered_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # 사업 기본 정보
    business_name = Column(String(300), nullable=False, index=True)
    business_type = Column(String(100), index=True)
    category = Column(String(100), index=True)
    keyword = Column(String(200), index=True)

    # 점수 정보 (상세)
    total_score = Column(Float, index=True)
    market_score = Column(Float, index=True)
    revenue_score = Column(Float, index=True)

    # 시장 분석 상세
    market_analysis = Column(JSON)  # 네이버, 구글, 유튜브, Kmong 데이터

    # 수익 분석 상세
    revenue_analysis = Column(JSON)  # 3가지 시나리오, ROI, 손익분기점

    # 실행 계획 (80점 이상만)
    action_plan = Column(JSON)  # 4주 실행 계획

    # 메타 정보
    discovery_batch = Column(String(50), index=True)  # 발굴 배치 ID (예: 2025-01-09-14)
    saved_to_db = Column(Boolean, default=False, index=True)  # 80점 이상 여부
    analysis_duration_ms = Column(Integer)  # 분석 소요 시간

    # 전문 분석
    full_analysis = Column(JSON)  # 전체 분석 결과 원본

    # 인덱스
    __table_args__ = (
        Index('idx_discovery_date_score', 'discovered_at', 'total_score'),
        Index('idx_category_score', 'category', 'total_score'),
        Index('idx_batch_saved', 'discovery_batch', 'saved_to_db'),
        {'schema': SCHEMA_NAME, 'extend_existing': True}
    )


class BusinessAnalysisSnapshot(Base):
    """시간대별 분석 스냅샷"""
    __tablename__ = 'business_analysis_snapshots'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    snapshot_time = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    snapshot_type = Column(String(50), nullable=False, index=True)  # hourly, daily, weekly

    # 통계 정보
    total_analyzed = Column(Integer)
    total_saved = Column(Integer)  # 80점 이상
    avg_total_score = Column(Float)
    avg_market_score = Column(Float)
    avg_revenue_score = Column(Float)

    # 카테고리별 분포
    category_distribution = Column(JSON)

    # 점수대별 분포
    score_distribution = Column(JSON)  # 0-60, 60-70, 70-80, 80-90, 90-100

    # 상위 사업들
    top_businesses = Column(JSON)  # 상위 10개

    # 트렌드 정보
    trending_keywords = Column(JSON)
    trending_categories = Column(JSON)

    # 인사이트
    insights = Column(JSON)

    __table_args__ = (
        Index('idx_snapshot_time_type', 'snapshot_time', 'snapshot_type'),
        {'schema': SCHEMA_NAME, 'extend_existing': True}
    )


class BusinessInsight(Base):
    """발굴 과정에서 도출된 인사이트"""
    __tablename__ = 'business_insights'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    insight_type = Column(String(50), nullable=False, index=True)  # trend, opportunity, warning, recommendation
    category = Column(String(100), index=True)

    title = Column(String(300), nullable=False)
    description = Column(Text)

    # 근거 데이터
    evidence = Column(JSON)
    confidence_score = Column(Float)  # 0-1

    # 영향도
    impact_level = Column(String(20), index=True)  # low, medium, high, critical

    # 연관 사업들
    related_businesses = Column(JSON)

    # 실행 제안
    actionable = Column(Boolean, default=False, index=True)
    suggested_actions = Column(JSON)

    # 상태
    status = Column(String(20), default='new', index=True)  # new, reviewed, acted_on, dismissed
    reviewed_at = Column(DateTime)

    __table_args__ = (
        Index('idx_insight_type_status', 'insight_type', 'status'),
        Index('idx_impact_actionable', 'impact_level', 'actionable'),
        {'schema': SCHEMA_NAME, 'extend_existing': True}
    )


class BusinessComparisonLog(Base):
    """사업 비교 분석 로그"""
    __tablename__ = 'business_comparison_logs'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    compared_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    comparison_type = Column(String(50))  # category_comparison, score_comparison, trend_comparison

    # 비교 대상
    business_ids = Column(JSON)

    # 비교 결과
    comparison_result = Column(JSON)
    winner = Column(String(300))

    # 분석
    strengths = Column(JSON)
    weaknesses = Column(JSON)
    recommendations = Column(JSON)


class LowScoreBusiness(Base):
    """60점 미만 사업 아이디어 (학습 및 개선 목적)"""
    __tablename__ = 'low_score_businesses'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # 사업 기본 정보
    business_name = Column(String(300), nullable=False)
    business_type = Column(String(100), index=True)
    category = Column(String(100), index=True)
    keyword = Column(String(200), index=True)

    # 점수 정보
    total_score = Column(Float, index=True)
    market_score = Column(Float, index=True)
    revenue_score = Column(Float, index=True)

    # 실패 원인
    failure_reason = Column(String(100), index=True)  # 'low_market', 'low_revenue', 'both'

    # 시장/수익 분석 데이터
    market_analysis = Column(JSON)
    revenue_analysis = Column(JSON)

    # 개선 제안
    improvement_suggestions = Column(JSON)  # AI가 분석한 개선 방향

    # 메타 정보
    discovery_batch = Column(String(50), index=True)
    analysis_duration_ms = Column(Integer)

    # 원본 데이터
    full_data = Column(JSON)

    __table_args__ = (
        Index('idx_low_score_date', 'created_at'),
        Index('idx_low_score_reason', 'failure_reason'),
        Index('idx_low_score_category', 'category', 'total_score'),
        {'schema': SCHEMA_NAME, 'extend_existing': True}
    )


# 히스토리 관리 클래스
class BusinessHistoryTracker:
    def __init__(self):
        self.session = Session()

    def record_analysis(self, business_name, business_type, category, keyword,
                       total_score, market_score, revenue_score,
                       market_analysis, revenue_analysis, action_plan,
                       discovery_batch, saved_to_db, analysis_duration_ms,
                       full_analysis):
        """분석 결과를 히스토리에 기록"""

        history = BusinessDiscoveryHistory(
            business_name=business_name,
            business_type=business_type,
            category=category,
            keyword=keyword,
            total_score=total_score,
            market_score=market_score,
            revenue_score=revenue_score,
            market_analysis=market_analysis,
            revenue_analysis=revenue_analysis,
            action_plan=action_plan,
            discovery_batch=discovery_batch,
            saved_to_db=saved_to_db,
            analysis_duration_ms=analysis_duration_ms,
            full_analysis=full_analysis
        )

        self.session.add(history)
        self.session.commit()

        return history.id

    def create_snapshot(self, snapshot_type='hourly'):
        """현재 상황의 스냅샷 생성"""

        now = datetime.utcnow()

        # 시간 범위 설정
        if snapshot_type == 'hourly':
            time_range = now - timedelta(hours=1)
        elif snapshot_type == 'daily':
            time_range = now - timedelta(days=1)
        elif snapshot_type == 'weekly':
            time_range = now - timedelta(weeks=1)
        else:
            time_range = now - timedelta(hours=1)

        # 해당 기간 데이터 조회
        histories = self.session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.discovered_at >= time_range
        ).all()

        if not histories:
            return None

        # 통계 계산
        total_analyzed = len(histories)
        total_saved = sum(1 for h in histories if h.saved_to_db)

        total_scores = [h.total_score for h in histories if h.total_score]
        market_scores = [h.market_score for h in histories if h.market_score]
        revenue_scores = [h.revenue_score for h in histories if h.revenue_score]

        avg_total_score = sum(total_scores) / len(total_scores) if total_scores else 0
        avg_market_score = sum(market_scores) / len(market_scores) if market_scores else 0
        avg_revenue_score = sum(revenue_scores) / len(revenue_scores) if revenue_scores else 0

        # 카테고리별 분포
        category_dist = {}
        for h in histories:
            cat = h.category or 'Unknown'
            category_dist[cat] = category_dist.get(cat, 0) + 1

        # 점수대별 분포
        score_dist = {
            '0-60': 0,
            '60-70': 0,
            '70-80': 0,
            '80-90': 0,
            '90-100': 0
        }

        for h in histories:
            score = h.total_score or 0
            if score < 60:
                score_dist['0-60'] += 1
            elif score < 70:
                score_dist['60-70'] += 1
            elif score < 80:
                score_dist['70-80'] += 1
            elif score < 90:
                score_dist['80-90'] += 1
            else:
                score_dist['90-100'] += 1

        # 상위 사업들
        top_businesses = sorted(histories, key=lambda h: h.total_score or 0, reverse=True)[:10]
        top_biz_data = [
            {
                'name': b.business_name,
                'category': b.category,
                'score': b.total_score,
                'market_score': b.market_score,
                'revenue_score': b.revenue_score
            }
            for b in top_businesses
        ]

        # 트렌딩 키워드
        keyword_freq = {}
        for h in histories:
            if h.keyword:
                keyword_freq[h.keyword] = keyword_freq.get(h.keyword, 0) + 1

        trending_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:10]

        # 스냅샷 저장
        snapshot = BusinessAnalysisSnapshot(
            snapshot_type=snapshot_type,
            total_analyzed=total_analyzed,
            total_saved=total_saved,
            avg_total_score=round(avg_total_score, 2),
            avg_market_score=round(avg_market_score, 2),
            avg_revenue_score=round(avg_revenue_score, 2),
            category_distribution=category_dist,
            score_distribution=score_dist,
            top_businesses=top_biz_data,
            trending_keywords=[{'keyword': k, 'count': c} for k, c in trending_keywords],
            trending_categories=dict(sorted(category_dist.items(), key=lambda x: x[1], reverse=True)[:5])
        )

        self.session.add(snapshot)
        self.session.commit()

        return snapshot.id

    def generate_insights(self):
        """인사이트 자동 생성"""

        # 최근 24시간 데이터
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent = self.session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.discovered_at >= yesterday
        ).all()

        insights = []

        # 1. 고득점 트렌드 감지
        high_scorers = [h for h in recent if h.total_score and h.total_score >= 85]
        if len(high_scorers) >= 3:
            categories = {}
            for h in high_scorers:
                cat = h.category or 'Unknown'
                categories[cat] = categories.get(cat, 0) + 1

            top_category = max(categories.items(), key=lambda x: x[1])

            insight = BusinessInsight(
                insight_type='trend',
                category=top_category[0],
                title=f'고득점 사업 집중: {top_category[0]}',
                description=f'최근 24시간 동안 {top_category[0]} 카테고리에서 {top_category[1]}개의 85점 이상 사업이 발굴되었습니다.',
                evidence={'high_score_count': len(high_scorers), 'category': top_category[0]},
                confidence_score=0.9,
                impact_level='high',
                actionable=True,
                suggested_actions=[
                    f'{top_category[0]} 카테고리 심층 분석',
                    '유사 사업 추가 발굴',
                    '실행 우선순위 재검토'
                ]
            )
            insights.append(insight)

        # 2. 저조한 카테고리 경고
        low_scorers = [h for h in recent if h.total_score and h.total_score < 50]
        if len(low_scorers) >= 5:
            categories = {}
            for h in low_scorers:
                cat = h.category or 'Unknown'
                categories[cat] = categories.get(cat, 0) + 1

            if categories:
                worst_category = max(categories.items(), key=lambda x: x[1])

                insight = BusinessInsight(
                    insight_type='warning',
                    category=worst_category[0],
                    title=f'저조한 성과: {worst_category[0]}',
                    description=f'{worst_category[0]} 카테고리에서 지속적으로 낮은 점수가 나타나고 있습니다.',
                    evidence={'low_score_count': len(low_scorers), 'category': worst_category[0]},
                    confidence_score=0.8,
                    impact_level='medium',
                    actionable=True,
                    suggested_actions=[
                        f'{worst_category[0]} 카테고리 분석 기준 재검토',
                        '다른 카테고리로 리소스 재배분 고려'
                    ]
                )
                insights.append(insight)

        # 3. 새로운 기회 발견
        saved_count = len([h for h in recent if h.saved_to_db])
        if saved_count >= 10:
            insight = BusinessInsight(
                insight_type='opportunity',
                title='대량 기회 발견',
                description=f'최근 24시간 동안 {saved_count}개의 80점 이상 사업이 발굴되었습니다.',
                evidence={'saved_count': saved_count},
                confidence_score=0.95,
                impact_level='high',
                actionable=True,
                suggested_actions=[
                    '우선순위 기준 재정립',
                    '실행 팀 리소스 확대 검토',
                    '전략 회의 소집'
                ]
            )
            insights.append(insight)

        # 인사이트 저장
        for insight in insights:
            self.session.add(insight)

        if insights:
            self.session.commit()

        return len(insights)

    def save_low_score_business(self, business_name, business_type, category, keyword,
                                total_score, market_score, revenue_score,
                                failure_reason, market_analysis, revenue_analysis,
                                discovery_batch, analysis_duration_ms, full_data):
        """60점 미만 사업을 별도 테이블에 저장"""

        # AI 개선 제안 생성
        improvement_suggestions = self._generate_improvement_suggestions(
            failure_reason, market_score, revenue_score, category
        )

        low_score = LowScoreBusiness(
            business_name=business_name,
            business_type=business_type,
            category=category,
            keyword=keyword,
            total_score=total_score,
            market_score=market_score,
            revenue_score=revenue_score,
            failure_reason=failure_reason,
            market_analysis=market_analysis,
            revenue_analysis=revenue_analysis,
            improvement_suggestions=improvement_suggestions,
            discovery_batch=discovery_batch,
            analysis_duration_ms=analysis_duration_ms,
            full_data=full_data
        )

        self.session.add(low_score)
        self.session.commit()

        return low_score.id

    def _generate_improvement_suggestions(self, failure_reason, market_score, revenue_score, category):
        """개선 제안 생성"""
        suggestions = []

        if failure_reason in ['low_market', 'both']:
            if market_score < 30:
                suggestions.append({
                    'area': 'market',
                    'severity': 'critical',
                    'suggestion': '시장 수요가 매우 낮습니다. 타겟 고객층을 재정의하거나 다른 카테고리를 고려하세요.'
                })
            elif market_score < 45:
                suggestions.append({
                    'area': 'market',
                    'severity': 'high',
                    'suggestion': '경쟁이 치열하거나 시장이 작습니다. 니치 마켓을 찾거나 차별화 전략이 필요합니다.'
                })
            else:
                suggestions.append({
                    'area': 'market',
                    'severity': 'medium',
                    'suggestion': '시장성이 경계선입니다. 마케팅 전략을 강화하면 개선 가능합니다.'
                })

        if failure_reason in ['low_revenue', 'both']:
            if revenue_score < 30:
                suggestions.append({
                    'area': 'revenue',
                    'severity': 'critical',
                    'suggestion': '수익 모델이 약합니다. 가격 전략 재검토 또는 비용 구조 개선이 필요합니다.'
                })
            elif revenue_score < 45:
                suggestions.append({
                    'area': 'revenue',
                    'severity': 'high',
                    'suggestion': '초기 투자 대비 수익성이 낮습니다. ROI 개선 방안을 찾아야 합니다.'
                })
            else:
                suggestions.append({
                    'area': 'revenue',
                    'severity': 'medium',
                    'suggestion': '수익성이 경계선입니다. 운영 비용 최적화로 개선 가능합니다.'
                })

        # 카테고리별 추가 제안
        suggestions.append({
            'area': 'strategy',
            'severity': 'info',
            'suggestion': f'{category} 카테고리에서 성공한 유사 사업 모델을 벤치마킹하세요.'
        })

        return suggestions

    def get_history_stats(self, days=7):
        """히스토리 통계"""
        start_date = datetime.utcnow() - timedelta(days=days)

        histories = self.session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.discovered_at >= start_date
        ).all()

        return {
            'total_analyzed': len(histories),
            'total_saved': sum(1 for h in histories if h.saved_to_db),
            'avg_score': round(sum(h.total_score for h in histories if h.total_score) / len(histories), 2) if histories else 0,
            'categories': len(set(h.category for h in histories if h.category)),
            'date_range': {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': datetime.utcnow().strftime('%Y-%m-%d')
            }
        }

    def get_low_score_stats(self, days=7):
        """60점 미만 사업 통계"""
        start_date = datetime.utcnow() - timedelta(days=days)

        low_scores = self.session.query(LowScoreBusiness).filter(
            LowScoreBusiness.created_at >= start_date
        ).all()

        # 실패 원인별 분포
        failure_dist = {}
        for ls in low_scores:
            reason = ls.failure_reason or 'unknown'
            failure_dist[reason] = failure_dist.get(reason, 0) + 1

        # 카테고리별 실패율
        category_failures = {}
        for ls in low_scores:
            cat = ls.category or 'Unknown'
            category_failures[cat] = category_failures.get(cat, 0) + 1

        return {
            'total_low_score': len(low_scores),
            'avg_score': round(sum(ls.total_score for ls in low_scores if ls.total_score) / len(low_scores), 2) if low_scores else 0,
            'failure_distribution': failure_dist,
            'category_failures': dict(sorted(category_failures.items(), key=lambda x: x[1], reverse=True)[:5]),
            'improvement_rate': self._calculate_improvement_rate(low_scores)
        }

    def _calculate_improvement_rate(self, low_scores):
        """개선 가능성 비율 계산"""
        near_threshold = sum(1 for ls in low_scores if ls.total_score and ls.total_score >= 50)
        return round((near_threshold / len(low_scores) * 100), 1) if low_scores else 0


def initialize_history_tables():
    """히스토리 테이블 초기화"""
    Base.metadata.create_all(engine, checkfirst=True)
    print("비즈니스 히스토리 테이블 생성 완료")


if __name__ == "__main__":
    initialize_history_tables()
    print("Business Discovery History System Ready!")
