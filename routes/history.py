from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import func, cast, Date, Integer

from services.db import Session
from business_discovery_history import (
    BusinessDiscoveryHistory, BusinessAnalysisSnapshot,
    BusinessInsight, BusinessHistoryTracker, LowScoreBusiness
)

history_bp = Blueprint('history', __name__)


@history_bp.route('/api/business-history/stats')
def api_business_history_stats():
    """히스토리 통계 API"""
    session = Session()
    try:
        days = int(request.args.get('days', 7))
        tracker = BusinessHistoryTracker()
        stats = tracker.get_history_stats(days=days)
        return jsonify(stats)
    finally:
        session.close()


@history_bp.route('/api/business-history/list')
def api_business_history_list():
    """전체 히스토리 목록 API"""
    session = Session()
    try:
        period = request.args.get('period', '24h')
        score_filter = request.args.get('score', 'all')
        category_filter = request.args.get('category', 'all')
        search = request.args.get('search', '')
        limit = int(request.args.get('limit', 100))

        now = datetime.utcnow()
        if period == '24h':
            start_date = now - timedelta(hours=24)
        elif period == '7d':
            start_date = now - timedelta(days=7)
        elif period == '30d':
            start_date = now - timedelta(days=30)
        else:
            start_date = None

        query = session.query(BusinessDiscoveryHistory)

        if start_date:
            query = query.filter(BusinessDiscoveryHistory.discovered_at >= start_date)

        if score_filter == '90+':
            query = query.filter(BusinessDiscoveryHistory.total_score >= 90)
        elif score_filter == '80-89':
            query = query.filter(BusinessDiscoveryHistory.total_score >= 80, BusinessDiscoveryHistory.total_score < 90)
        elif score_filter == '70-79':
            query = query.filter(BusinessDiscoveryHistory.total_score >= 70, BusinessDiscoveryHistory.total_score < 80)
        elif score_filter == '60-79':
            query = query.filter(BusinessDiscoveryHistory.total_score >= 60, BusinessDiscoveryHistory.total_score < 80)
        elif score_filter == '60-69':
            query = query.filter(BusinessDiscoveryHistory.total_score >= 60, BusinessDiscoveryHistory.total_score < 70)
        elif score_filter == '0-59':
            query = query.filter(BusinessDiscoveryHistory.total_score < 60)
        elif score_filter == '60-':
            query = query.filter(BusinessDiscoveryHistory.total_score < 60)

        if category_filter != 'all':
            query = query.filter(BusinessDiscoveryHistory.category == category_filter)

        if search:
            query = query.filter(BusinessDiscoveryHistory.business_name.ilike(f'%{search}%'))

        histories = query.order_by(BusinessDiscoveryHistory.discovered_at.desc()).limit(limit).all()

        result = []
        for h in histories:
            result.append({
                'id': h.id,
                'discovered_at': h.discovered_at.isoformat() if h.discovered_at else None,
                'business_name': h.business_name,
                'business_type': h.business_type,
                'category': h.category,
                'keyword': h.keyword,
                'total_score': h.total_score or 0,
                'market_score': h.market_score or 0,
                'revenue_score': h.revenue_score or 0,
                'saved_to_db': h.saved_to_db,
                'discovery_batch': h.discovery_batch,
                'analysis_duration_ms': h.analysis_duration_ms
            })

        return jsonify(result)
    finally:
        session.close()


@history_bp.route('/api/business-history/insights')
def api_business_history_insights():
    """인사이트 목록 API"""
    session = Session()
    try:
        status = request.args.get('status', 'new')
        limit = int(request.args.get('limit', 20))

        query = session.query(BusinessInsight)

        if status != 'all':
            query = query.filter(BusinessInsight.status == status)

        insights = query.order_by(BusinessInsight.created_at.desc()).limit(limit).all()

        result = []
        for insight in insights:
            result.append({
                'id': insight.id,
                'created_at': insight.created_at.isoformat() if insight.created_at else None,
                'insight_type': insight.insight_type,
                'category': insight.category,
                'title': insight.title,
                'description': insight.description,
                'impact_level': insight.impact_level,
                'confidence_score': insight.confidence_score,
                'actionable': insight.actionable,
                'suggested_actions': insight.suggested_actions,
                'status': insight.status
            })

        return jsonify(result)
    finally:
        session.close()


@history_bp.route('/api/business-history/categories')
def api_business_history_categories():
    """카테고리별 분포 API"""
    session = Session()
    try:
        days = int(request.args.get('days', 7))
        start_date = datetime.utcnow() - timedelta(days=days)

        histories = session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.discovered_at >= start_date
        ).all()

        categories = {}
        for h in histories:
            cat = h.category or 'Unknown'
            categories[cat] = categories.get(cat, 0) + 1

        return jsonify(categories)
    finally:
        session.close()


@history_bp.route('/api/business-history/snapshots')
def api_business_history_snapshots():
    """스냅샷 목록 API"""
    session = Session()
    try:
        snapshot_type = request.args.get('type', 'hourly')
        limit = int(request.args.get('limit', 24))

        snapshots = session.query(BusinessAnalysisSnapshot).filter(
            BusinessAnalysisSnapshot.snapshot_type == snapshot_type
        ).order_by(BusinessAnalysisSnapshot.snapshot_time.desc()).limit(limit).all()

        result = []
        for s in snapshots:
            result.append({
                'id': s.id,
                'snapshot_time': s.snapshot_time.isoformat() if s.snapshot_time else None,
                'snapshot_type': s.snapshot_type,
                'total_analyzed': s.total_analyzed,
                'total_saved': s.total_saved,
                'avg_total_score': s.avg_total_score,
                'avg_market_score': s.avg_market_score,
                'avg_revenue_score': s.avg_revenue_score,
                'category_distribution': s.category_distribution,
                'score_distribution': s.score_distribution,
                'top_businesses': s.top_businesses,
                'trending_keywords': s.trending_keywords
            })

        return jsonify(result)
    finally:
        session.close()


@history_bp.route('/api/business-history/trends')
def api_business_history_trends():
    """트렌드 분석 API"""
    session = Session()
    try:
        days = int(request.args.get('days', 30))
        start_date = datetime.utcnow() - timedelta(days=days)

        daily_stats = session.query(
            cast(BusinessDiscoveryHistory.discovered_at, Date).label('date'),
            func.count(BusinessDiscoveryHistory.id).label('total'),
            func.avg(BusinessDiscoveryHistory.total_score).label('avg_score'),
            func.sum(func.cast(BusinessDiscoveryHistory.saved_to_db, Integer)).label('saved_count')
        ).filter(
            BusinessDiscoveryHistory.discovered_at >= start_date
        ).group_by(
            cast(BusinessDiscoveryHistory.discovered_at, Date)
        ).order_by('date').all()

        result = []
        for stat in daily_stats:
            result.append({
                'date': stat.date.isoformat() if stat.date else None,
                'total': stat.total or 0,
                'avg_score': round(stat.avg_score, 2) if stat.avg_score else 0,
                'saved_count': stat.saved_count or 0
            })

        return jsonify(result)
    finally:
        session.close()


@history_bp.route('/api/low-score-businesses/list')
def api_low_score_businesses_list():
    """60점 미만 사업 목록 API"""
    session = Session()
    try:
        days = int(request.args.get('days', 7))
        failure_reason = request.args.get('failure_reason', 'all')
        category = request.args.get('category', 'all')
        limit = int(request.args.get('limit', 50))

        start_date = datetime.utcnow() - timedelta(days=days)

        query = session.query(LowScoreBusiness).filter(
            LowScoreBusiness.created_at >= start_date
        )

        if failure_reason != 'all':
            query = query.filter(LowScoreBusiness.failure_reason == failure_reason)

        if category != 'all':
            query = query.filter(LowScoreBusiness.category == category)

        businesses = query.order_by(
            LowScoreBusiness.created_at.desc()
        ).limit(limit).all()

        result = []
        for biz in businesses:
            result.append({
                'id': biz.id,
                'business_name': biz.business_name,
                'business_type': biz.business_type,
                'category': biz.category,
                'keyword': biz.keyword,
                'total_score': biz.total_score,
                'market_score': biz.market_score,
                'revenue_score': biz.revenue_score,
                'failure_reason': biz.failure_reason,
                'improvement_suggestions': biz.improvement_suggestions,
                'created_at': biz.created_at.isoformat() if biz.created_at else None,
                'discovery_batch': biz.discovery_batch,
                'analysis_duration_ms': biz.analysis_duration_ms
            })

        return jsonify({
            'total': len(result),
            'businesses': result
        })
    finally:
        session.close()


@history_bp.route('/api/low-score-businesses/stats')
def api_low_score_businesses_stats():
    """60점 미만 사업 통계 API"""
    tracker = BusinessHistoryTracker()
    try:
        days = int(request.args.get('days', 7))
        stats = tracker.get_low_score_stats(days=days)
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@history_bp.route('/api/low-score-businesses/detail/<int:business_id>')
def api_low_score_business_detail(business_id):
    """60점 미만 사업 상세 정보 API"""
    session = Session()
    try:
        biz = session.query(LowScoreBusiness).filter_by(id=business_id).first()

        if not biz:
            return jsonify({'error': 'Business not found'}), 404

        return jsonify({
            'id': biz.id,
            'business_name': biz.business_name,
            'business_type': biz.business_type,
            'category': biz.category,
            'keyword': biz.keyword,
            'total_score': biz.total_score,
            'market_score': biz.market_score,
            'revenue_score': biz.revenue_score,
            'failure_reason': biz.failure_reason,
            'market_analysis': biz.market_analysis,
            'revenue_analysis': biz.revenue_analysis,
            'improvement_suggestions': biz.improvement_suggestions,
            'created_at': biz.created_at.isoformat() if biz.created_at else None,
            'discovery_batch': biz.discovery_batch,
            'analysis_duration_ms': biz.analysis_duration_ms,
            'full_data': biz.full_data
        })
    finally:
        session.close()
