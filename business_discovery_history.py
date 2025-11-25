"""
    
-     
- , ,    
-     
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Text, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from database_setup import Base, Session, SCHEMA_NAME, engine, get_kst_now
import json

#   
class BusinessDiscoveryHistory(Base):
    """    (   )"""
    __tablename__ = 'business_discovery_history'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    discovered_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    #   
    business_name = Column(String(300), nullable=False, index=True)
    business_type = Column(String(100), index=True)
    category = Column(String(100), index=True)
    keyword = Column(String(200), index=True)

    #   ()
    total_score = Column(Float, index=True)
    market_score = Column(Float, index=True)
    revenue_score = Column(Float, index=True)

    #   
    market_analysis = Column(JSON)  # , , , Kmong 

    #   
    revenue_analysis = Column(JSON)  # 3 , ROI, 

    #   (80 )
    action_plan = Column(JSON)  # 4  

    #  
    discovery_batch = Column(String(50), index=True)  #   ID (: 2025-01-09-14)
    saved_to_db = Column(Boolean, default=False, index=True)  # 80  
    analysis_duration_ms = Column(Integer)  #   

    #  
    full_analysis = Column(JSON)  #    

    # 
    __table_args__ = (
        Index('idx_discovery_date_score', 'discovered_at', 'total_score'),
        Index('idx_category_score', 'category', 'total_score'),
        Index('idx_batch_saved', 'discovery_batch', 'saved_to_db'),
        {'schema': SCHEMA_NAME, 'extend_existing': True}
    )


class BusinessAnalysisSnapshot(Base):
    """  """
    __tablename__ = 'business_analysis_snapshots'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    snapshot_time = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    snapshot_type = Column(String(50), nullable=False, index=True)  # hourly, daily, weekly

    #  
    total_analyzed = Column(Integer)
    total_saved = Column(Integer)  # 80 
    avg_total_score = Column(Float)
    avg_market_score = Column(Float)
    avg_revenue_score = Column(Float)

    #  
    category_distribution = Column(JSON)

    #  
    score_distribution = Column(JSON)  # 0-60, 60-70, 70-80, 80-90, 90-100

    #  
    top_businesses = Column(JSON)  #  10

    #  
    trending_keywords = Column(JSON)
    trending_categories = Column(JSON)

    # 
    insights = Column(JSON)

    __table_args__ = (
        Index('idx_snapshot_time_type', 'snapshot_time', 'snapshot_type'),
        {'schema': SCHEMA_NAME, 'extend_existing': True}
    )


class BusinessInsight(Base):
    """   """
    __tablename__ = 'business_insights'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    insight_type = Column(String(50), nullable=False, index=True)  # trend, opportunity, warning, recommendation
    category = Column(String(100), index=True)

    title = Column(String(300), nullable=False)
    description = Column(Text)

    #  
    evidence = Column(JSON)
    confidence_score = Column(Float)  # 0-1

    # 
    impact_level = Column(String(20), index=True)  # low, medium, high, critical

    #  
    related_businesses = Column(JSON)

    #  
    actionable = Column(Boolean, default=False, index=True)
    suggested_actions = Column(JSON)

    # 
    status = Column(String(20), default='new', index=True)  # new, reviewed, acted_on, dismissed
    reviewed_at = Column(DateTime)

    __table_args__ = (
        Index('idx_insight_type_status', 'insight_type', 'status'),
        Index('idx_impact_actionable', 'impact_level', 'actionable'),
        {'schema': SCHEMA_NAME, 'extend_existing': True}
    )


class BusinessComparisonLog(Base):
    """   """
    __tablename__ = 'business_comparison_logs'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    compared_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    comparison_type = Column(String(50))  # category_comparison, score_comparison, trend_comparison

    #  
    business_ids = Column(JSON)

    #  
    comparison_result = Column(JSON)
    winner = Column(String(300))

    # 
    strengths = Column(JSON)
    weaknesses = Column(JSON)
    recommendations = Column(JSON)


class LowScoreBusiness(Base):
    """60    (   )"""
    __tablename__ = 'low_score_businesses'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    #   
    business_name = Column(String(300), nullable=False)
    business_type = Column(String(100), index=True)
    category = Column(String(100), index=True)
    keyword = Column(String(200), index=True)

    #  
    total_score = Column(Float, index=True)
    market_score = Column(Float, index=True)
    revenue_score = Column(Float, index=True)

    #  
    failure_reason = Column(String(100), index=True)  # 'low_market', 'low_revenue', 'both'

    # /  
    market_analysis = Column(JSON)
    revenue_analysis = Column(JSON)

    #  
    improvement_suggestions = Column(JSON)  # AI   

    #  
    discovery_batch = Column(String(50), index=True)
    analysis_duration_ms = Column(Integer)

    #  
    full_data = Column(JSON)

    __table_args__ = (
        Index('idx_low_score_date', 'created_at'),
        Index('idx_low_score_reason', 'failure_reason'),
        Index('idx_low_score_category', 'category', 'total_score'),
        {'schema': SCHEMA_NAME, 'extend_existing': True}
    )


#   
class BusinessHistoryTracker:
    def __init__(self):
        self.session = Session()

    def record_analysis(self, business_name, business_type, category, keyword,
                       total_score, market_score, revenue_score,
                       market_analysis, revenue_analysis, action_plan,
                       discovery_batch, saved_to_db, analysis_duration_ms,
                       full_analysis):
        """   """

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
        """   """

        now = get_kst_now()

        #   
        if snapshot_type == 'hourly':
            time_range = now - timedelta(hours=1)
        elif snapshot_type == 'daily':
            time_range = now - timedelta(days=1)
        elif snapshot_type == 'weekly':
            time_range = now - timedelta(weeks=1)
        else:
            time_range = now - timedelta(hours=1)

        #    
        histories = self.session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.discovered_at >= time_range
        ).all()

        if not histories:
            return None

        #  
        total_analyzed = len(histories)
        total_saved = sum(1 for h in histories if h.saved_to_db)

        total_scores = [h.total_score for h in histories if h.total_score]
        market_scores = [h.market_score for h in histories if h.market_score]
        revenue_scores = [h.revenue_score for h in histories if h.revenue_score]

        avg_total_score = sum(total_scores) / len(total_scores) if total_scores else 0
        avg_market_score = sum(market_scores) / len(market_scores) if market_scores else 0
        avg_revenue_score = sum(revenue_scores) / len(revenue_scores) if revenue_scores else 0

        #  
        category_dist = {}
        for h in histories:
            cat = h.category or 'Unknown'
            category_dist[cat] = category_dist.get(cat, 0) + 1

        #  
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

        #  
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

        #  
        keyword_freq = {}
        for h in histories:
            if h.keyword:
                keyword_freq[h.keyword] = keyword_freq.get(h.keyword, 0) + 1

        trending_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:10]

        #  
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
        """  """

        #  24 
        yesterday = get_kst_now() - timedelta(days=1)
        recent = self.session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.discovered_at >= yesterday
        ).all()

        insights = []

        # 1.   
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
                title=f'  : {top_category[0]}',
                description=f' 24  {top_category[0]}  {top_category[1]} 85   .',
                evidence={'high_score_count': len(high_scorers), 'category': top_category[0]},
                confidence_score=0.9,
                impact_level='high',
                actionable=True,
                suggested_actions=[
                    f'{top_category[0]}   ',
                    '   ',
                    '  '
                ]
            )
            insights.append(insight)

        # 2.   
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
                    title=f' : {worst_category[0]}',
                    description=f'{worst_category[0]}      .',
                    evidence={'low_score_count': len(low_scorers), 'category': worst_category[0]},
                    confidence_score=0.8,
                    impact_level='medium',
                    actionable=True,
                    suggested_actions=[
                        f'{worst_category[0]}    ',
                        '    '
                    ]
                )
                insights.append(insight)

        # 3.   
        saved_count = len([h for h in recent if h.saved_to_db])
        if saved_count >= 10:
            insight = BusinessInsight(
                insight_type='opportunity',
                title='  ',
                description=f' 24  {saved_count} 80   .',
                evidence={'saved_count': saved_count},
                confidence_score=0.95,
                impact_level='high',
                actionable=True,
                suggested_actions=[
                    '  ',
                    '    ',
                    '  '
                ]
            )
            insights.append(insight)

        #  
        for insight in insights:
            self.session.add(insight)

        if insights:
            self.session.commit()

        return len(insights)

    def save_low_score_business(self, business_name, business_type, category, keyword,
                                total_score, market_score, revenue_score,
                                failure_reason, market_analysis, revenue_analysis,
                                discovery_batch, analysis_duration_ms, full_data):
        """60     """

        # AI   
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
        """  """
        suggestions = []

        if failure_reason in ['low_market', 'both']:
            if market_score < 30:
                suggestions.append({
                    'area': 'market',
                    'severity': 'critical',
                    'suggestion': '   .      .'
                })
            elif market_score < 45:
                suggestions.append({
                    'area': 'market',
                    'severity': 'high',
                    'suggestion': '   .      .'
                })
            else:
                suggestions.append({
                    'area': 'market',
                    'severity': 'medium',
                    'suggestion': ' .     .'
                })

        if failure_reason in ['low_revenue', 'both']:
            if revenue_score < 30:
                suggestions.append({
                    'area': 'revenue',
                    'severity': 'critical',
                    'suggestion': '  .        .'
                })
            elif revenue_score < 45:
                suggestions.append({
                    'area': 'revenue',
                    'severity': 'high',
                    'suggestion': '    . ROI    .'
                })
            else:
                suggestions.append({
                    'area': 'revenue',
                    'severity': 'medium',
                    'suggestion': ' .     .'
                })

        #   
        suggestions.append({
            'area': 'strategy',
            'severity': 'info',
            'suggestion': f'{category}      .'
        })

        return suggestions

    def get_history_stats(self, days=7):
        """ """
        start_date = get_kst_now() - timedelta(days=days)

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
                'end': get_kst_now().strftime('%Y-%m-%d')
            }
        }

    def get_low_score_stats(self, days=7):
        """60   """
        start_date = get_kst_now() - timedelta(days=days)

        low_scores = self.session.query(LowScoreBusiness).filter(
            LowScoreBusiness.created_at >= start_date
        ).all()

        #   
        failure_dist = {}
        for ls in low_scores:
            reason = ls.failure_reason or 'unknown'
            failure_dist[reason] = failure_dist.get(reason, 0) + 1

        #  
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
        """   """
        near_threshold = sum(1 for ls in low_scores if ls.total_score and ls.total_score >= 50)
        return round((near_threshold / len(low_scores) * 100), 1) if low_scores else 0


def initialize_history_tables():
    """  """
    Base.metadata.create_all(engine, checkfirst=True)
    print("    ")


if __name__ == "__main__":
    initialize_history_tables()
    print("Business Discovery History System Ready!")
