import logging
from flask import Blueprint, render_template, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import func, text

from services.db import Session, get_db_session
from services.business_helpers import (
    generate_default_action_plan, generate_startup_guide,
    generate_default_market_analysis, generate_default_revenue_analysis
)
from database_setup import SCHEMA_NAME
from business_discovery_history import (
    BusinessDiscoveryHistory, LowScoreBusiness
)
from logging_config import get_app_logger

logger = get_app_logger()

discovery_bp = Blueprint('discovery', __name__)


@discovery_bp.route('/business-discovery')
def business_discovery():
    """사업 발굴 대시보드 페이지"""
    return render_template('business_discovery.html')


@discovery_bp.route('/business-history')
def business_history():
    """사업 발굴 히스토리 & 분석 대시보드"""
    return render_template('business_history.html')


@discovery_bp.route('/business-review')
def business_review():
    """검토 필요 사업 (60-79점)"""
    return render_template('business_review.html')


@discovery_bp.route('/business-rejected')
def business_rejected():
    """부적합 사업 (60점 미만)"""
    return render_template('business_rejected.html')


@discovery_bp.route('/business')
def business_landing():
    """사업 분석 랜딩 페이지"""
    return render_template('business_landing.html')


@discovery_bp.route('/trigger-discovery')
def trigger_discovery_page():
    """수동 사업 발굴 페이지"""
    return render_template('trigger_discovery.html')


@discovery_bp.route('/api/discovered-businesses')
def api_discovered_businesses():
    """자동 발굴된 사업 목록 API (전체 점수 포함, 서버 사이드 페이징)"""
    session = None
    try:
        session = get_db_session()

        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        limit = min(limit, 100)
        offset = (page - 1) * limit

        total_count = session.query(func.count(BusinessDiscoveryHistory.id)).scalar()

        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = today - timedelta(days=7)

        today_count = session.query(func.count(BusinessDiscoveryHistory.id)).filter(
            BusinessDiscoveryHistory.discovered_at >= today
        ).scalar()

        week_count = session.query(func.count(BusinessDiscoveryHistory.id)).filter(
            BusinessDiscoveryHistory.discovered_at >= week_ago
        ).scalar()

        high_score_count = session.query(func.count(BusinessDiscoveryHistory.id)).filter(
            BusinessDiscoveryHistory.total_score >= 85
        ).scalar()

        from sqlalchemy import func as sqlfunc
        subquery = session.query(
            sqlfunc.max(BusinessDiscoveryHistory.id).label('max_id')
        ).group_by(BusinessDiscoveryHistory.business_name).subquery()

        histories = session.query(BusinessDiscoveryHistory).join(
            subquery, BusinessDiscoveryHistory.id == subquery.c.max_id
        ).order_by(
            BusinessDiscoveryHistory.discovered_at.desc()
        ).offset(offset).limit(limit).all()

        total_count = session.query(sqlfunc.count(sqlfunc.distinct(BusinessDiscoveryHistory.business_name))).scalar()

        logger.info(f"[API] discovered-businesses: page={page}, limit={limit}, total={total_count}")

        business_list = []
        for biz in histories:
            monthly_revenue = biz.total_score * 100000
            annual_revenue = monthly_revenue * 12
            investment = biz.total_score * 50000

            market_data = biz.market_analysis if isinstance(biz.market_analysis, dict) else {}
            if not market_data or not market_data.get('market_info'):
                default_market = generate_default_market_analysis(biz.business_name, biz.keyword or biz.business_name)
                if market_data:
                    default_market.update({k: v for k, v in market_data.items() if v})
                market_data = default_market

            revenue_data = biz.revenue_analysis if isinstance(biz.revenue_analysis, dict) else {}
            if not revenue_data:
                revenue_data = generate_default_revenue_analysis(biz.business_name, biz.total_score)

            action_plan_data = biz.action_plan if isinstance(biz.action_plan, dict) else {}
            if not action_plan_data:
                action_plan_data = generate_default_action_plan(biz.business_name, biz.business_type)

            startup_guide = generate_startup_guide(biz.business_name, biz.business_type, biz.total_score)

            full_analysis_data = biz.full_analysis if isinstance(biz.full_analysis, dict) else {}
            business_info = full_analysis_data.get('business', {})

            if not business_info.get('it_type_label'):
                biz_type_lower = (biz.business_type or '').lower()
                if any(x in biz_type_lower for x in ['플랫폼', '커뮤니티', '네트워크']):
                    it_type = 'platform'
                    it_label = '플랫폼'
                elif any(x in biz_type_lower for x in ['마켓', '매칭', '중개']):
                    it_type = 'marketplace'
                    it_label = '마켓플레이스'
                elif any(x in biz_type_lower for x in ['대행', '컨설팅', '에이전시']):
                    it_type = 'agency'
                    it_label = '에이전시'
                elif any(x in biz_type_lower for x in ['도구', '툴', '봇', '자동화']):
                    it_type = 'tools'
                    it_label = '생산성 도구'
                else:
                    it_type = 'saas'
                    it_label = 'SaaS'

                default_features = {
                    'saas': ['데이터 관리', '알림 시스템', '분석 대시보드'],
                    'marketplace': ['실시간 매칭', '리뷰 시스템', '간편 결제'],
                    'agency': ['프로젝트 관리', '1:1 맞춤 서비스', '품질 보장'],
                    'tools': ['간편한 UX', '빠른 처리', '다중 플랫폼'],
                    'platform': ['커뮤니티 기능', '콘텐츠 큐레이션', '개인화']
                }

                default_tech = {
                    'saas': ['Bubble.io', 'Supabase'],
                    'marketplace': ['Sharetribe', 'Webflow'],
                    'agency': ['Notion', 'Figma'],
                    'tools': ['React', 'Chrome Extension'],
                    'platform': ['Firebase', 'Vercel']
                }

                default_revenue = {
                    'saas': ['월정액 구독', '프리미엄 요금제'],
                    'marketplace': ['거래 수수료', '프리미엄 리스팅'],
                    'agency': ['프로젝트 단가', '리테이너 계약'],
                    'tools': ['일회성 구매', '프리미엄 기능'],
                    'platform': ['멤버십', '광고']
                }

                business_info = {
                    'it_type': it_type,
                    'it_type_label': it_label,
                    'core_features': default_features.get(it_type, []),
                    'differentiator': f"기존 서비스 대비 50% 저렴한 가격",
                    'tech_stack': default_tech.get(it_type, []),
                    'revenue_models': default_revenue.get(it_type, []),
                    'target_audience': '직장인'
                }
                full_analysis_data['business'] = business_info

            if revenue_data:
                scenarios = revenue_data.get('scenarios', {})
                realistic = scenarios.get('realistic', scenarios.get('현실적', {}))
                monthly_revenue = realistic.get('monthly_revenue', realistic.get('월_예상_수익', monthly_revenue))
                annual_revenue = monthly_revenue * 12
                investment = revenue_data.get('startup_cost', revenue_data.get('initial_investment', investment))

            market_info = market_data.get('market_info', {})
            trend = market_info.get('trend', market_data.get('trend', '안정'))
            competition_level = market_info.get('competition_level', market_data.get('competition_level', 55))
            market_size_raw = market_info.get('market_size', market_data.get('market_size', '중형'))

            score_breakdown = market_data.get('score_breakdown', {})
            if not score_breakdown:
                score_breakdown = {
                    'base_score': int(biz.total_score * 0.6),
                    'domain_bonus': int((biz.market_score or 0) * 0.2),
                    'trend_bonus': 5 if trend in ['급상승', '상승'] else 0,
                    'target_bonus': 3,
                    'revenue_bonus': int((biz.revenue_score or 0) * 0.15),
                    'competition_penalty': -5 if competition_level > 70 else 0
                }

            business_list.append({
                'id': biz.id,
                'name': biz.business_name,
                'type': biz.business_type,
                'score': biz.total_score,
                'feasibility': biz.total_score / 10,
                'revenue_12m': annual_revenue,
                'investment': investment,
                'risk': 'low' if biz.total_score >= 80 else 'medium' if biz.total_score >= 70 else 'high',
                'priority': 'high' if biz.total_score >= 80 else 'medium',
                'created_at': biz.discovered_at.strftime('%Y-%m-%d %H:%M') if biz.discovered_at else None,
                'description': f"{biz.business_name} - 시장성 {int(biz.market_score)}점, 수익성 {int(biz.revenue_score)}점",
                'revenue_model': revenue_data.get('revenue_model', 'subscription'),
                'trend': trend,
                'competition_level': competition_level,
                'market_size': market_size_raw,
                'score_breakdown': score_breakdown,
                'details': {
                    'analysis_score': biz.total_score,
                    'market_score': biz.market_score,
                    'revenue_score': biz.revenue_score,
                    'category': biz.category,
                    'keyword': biz.keyword,
                    'market_analysis': market_data,
                    'revenue_analysis': revenue_data,
                    'action_plan': action_plan_data,
                    'startup_guide': startup_guide,
                    'full_analysis': full_analysis_data
                }
            })

        total_pages = (total_count + limit - 1) // limit

        return jsonify({
            'businesses': business_list,
            'stats': {
                'total': total_count,
                'today': today_count,
                'this_week': week_count,
                'high_score': high_score_count
            },
            'pagination': {
                'page': page,
                'limit': limit,
                'total_pages': total_pages,
                'total_items': total_count
            }
        })
    except Exception as e:
        logger.error(f"[API] discovered-businesses 오류: {e}")
        return jsonify({
            'businesses': [],
            'stats': {'total': 0, 'today': 0, 'this_week': 0, 'high_score': 0},
            'error': str(e)
        }), 200
    finally:
        if session:
            session.close()


@discovery_bp.route('/api/low-score-businesses')
def api_low_score_businesses():
    """저점수 사업 목록 API (50점 미만)"""
    session = Session()
    try:
        result = session.execute(text(f"""
            SELECT id, business_name, business_type, total_score, market_score, revenue_score,
                   category, keyword, market_analysis, revenue_analysis, discovered_at
            FROM {SCHEMA_NAME}.low_score_businesses
            ORDER BY discovered_at DESC
            LIMIT 100
        """))

        business_list = []
        for row in result:
            monthly_revenue = row.total_score * 100000
            annual_revenue = monthly_revenue * 12
            investment = row.total_score * 50000

            business_list.append({
                'id': row.id,
                'name': row.business_name,
                'type': row.business_type,
                'score': row.total_score,
                'feasibility': row.total_score / 10,
                'revenue_12m': annual_revenue,
                'investment': investment,
                'risk': 'high',
                'priority': 'low',
                'created_at': row.discovered_at.strftime('%Y-%m-%d %H:%M') if row.discovered_at else None,
                'description': f"{row.business_name} - 시장성 {int(row.market_score)}점, 수익성 {int(row.revenue_score)}점 (실험적 아이디어)",
                'revenue_model': 'experimental',
                'details': {
                    'analysis_score': row.total_score,
                    'market_score': row.market_score,
                    'revenue_score': row.revenue_score,
                    'category': row.category,
                    'keyword': row.keyword,
                    'market_analysis': row.market_analysis,
                    'revenue_analysis': row.revenue_analysis
                }
            })

        total_count = session.execute(text(f"""
            SELECT COUNT(*) FROM {SCHEMA_NAME}.low_score_businesses
        """)).scalar()

        today = datetime.utcnow().date()
        today_count = session.execute(text(f"""
            SELECT COUNT(*) FROM {SCHEMA_NAME}.low_score_businesses
            WHERE DATE(discovered_at) = :today
        """), {'today': today}).scalar()

        return jsonify({
            'businesses': business_list,
            'stats': {
                'total': total_count or 0,
                'today': today_count or 0,
                'this_week': 0,
                'high_score': 0
            }
        })
    except Exception as e:
        logging.error(f"Error fetching low score businesses: {e}")
        return jsonify({
            'businesses': [],
            'stats': {
                'total': 0,
                'today': 0,
                'this_week': 0,
                'high_score': 0
            }
        })
    finally:
        session.close()


@discovery_bp.route('/api/trigger-discovery', methods=['GET', 'POST'])
def trigger_discovery():
    """수동으로 사업 발굴 트리거 (백그라운드에서 비동기 실행)"""
    try:
        from threading import Thread
        from continuous_business_discovery import ContinuousBusinessDiscovery

        def run_discovery_background():
            """백그라운드에서 발굴 실행"""
            try:
                discovery = ContinuousBusinessDiscovery()
                results = discovery.run_hourly_discovery()

                if results['saved'] > 0:
                    discovery.generate_discovery_meeting(results)

                logging.info(f"Discovery completed: analyzed={results.get('analyzed')}, saved={results.get('saved')}")
                print(f"[TRIGGER] Discovery completed: {results.get('analyzed')} analyzed, {results.get('saved')} saved")
            except Exception as e:
                logging.error(f"Background discovery error: {e}")
                print(f"[TRIGGER ERROR] {e}")

        thread = Thread(target=run_discovery_background, daemon=True)
        thread.start()

        return jsonify({
            'success': True,
            'message': '사업 발굴이 백그라운드에서 시작되었습니다',
            'status': 'running',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@discovery_bp.route('/api/review-businesses')
def api_review_businesses():
    """검토 필요 사업 (60-79점) API"""
    session = Session()
    try:
        businesses = session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.total_score >= 60,
            BusinessDiscoveryHistory.total_score < 80
        ).order_by(BusinessDiscoveryHistory.discovered_at.desc()).limit(100).all()

        business_list = []
        for biz in businesses:
            business_list.append({
                'id': biz.id,
                'business_name': biz.business_name,
                'business_type': biz.business_type,
                'category': biz.category,
                'total_score': biz.total_score,
                'market_score': biz.market_score,
                'revenue_score': biz.revenue_score,
                'discovered_at': biz.discovered_at.strftime('%Y-%m-%d %H:%M') if biz.discovered_at else None,
                'market_analysis': biz.market_analysis,
                'revenue_analysis': biz.revenue_analysis
            })

        return jsonify({
            'businesses': business_list,
            'total': len(business_list)
        })
    finally:
        session.close()


@discovery_bp.route('/api/rejected-businesses')
def api_rejected_businesses():
    """부적합 사업 (60점 미만) API"""
    session = Session()
    try:
        businesses = session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.total_score < 60
        ).order_by(BusinessDiscoveryHistory.discovered_at.desc()).limit(100).all()

        business_list = []
        for biz in businesses:
            business_list.append({
                'id': biz.id,
                'business_name': biz.business_name,
                'business_type': biz.business_type,
                'category': biz.category,
                'total_score': biz.total_score,
                'market_score': biz.market_score,
                'revenue_score': biz.revenue_score,
                'discovered_at': biz.discovered_at.strftime('%Y-%m-%d %H:%M') if biz.discovered_at else None,
                'market_analysis': biz.market_analysis,
                'revenue_analysis': biz.revenue_analysis,
                'full_analysis': biz.full_analysis
            })

        return jsonify({
            'businesses': business_list,
            'total': len(business_list)
        })
    finally:
        session.close()


@discovery_bp.route('/api/low-score-businesses/list-old')
def api_low_score_businesses_old():
    """낮은 점수 사업 목록 API (60점 미만) - 구버전"""
    session = Session()
    try:
        days = int(request.args.get('days', 30))
        limit = int(request.args.get('limit', 200))

        start_date = datetime.utcnow() - timedelta(days=days)

        businesses = session.query(LowScoreBusiness).filter(
            LowScoreBusiness.created_at >= start_date
        ).order_by(LowScoreBusiness.created_at.desc()).limit(limit).all()

        business_list = []
        for biz in businesses:
            business_list.append({
                'id': biz.id,
                'business_name': biz.business_name,
                'business_type': biz.business_type,
                'category': biz.category,
                'keyword': biz.keyword,
                'total_score': biz.total_score,
                'market_score': biz.market_score,
                'revenue_score': biz.revenue_score,
                'failure_reason': biz.failure_reason,
                'created_at': biz.created_at.strftime('%Y-%m-%d %H:%M') if biz.created_at else None,
                'market_analysis': biz.market_analysis,
                'revenue_analysis': biz.revenue_analysis,
                'improvement_suggestions': biz.improvement_suggestions,
                'discovery_batch': biz.discovery_batch,
                'full_data': biz.full_data
            })

        total_count = len(business_list)
        avg_score = sum([b['total_score'] for b in business_list]) / total_count if total_count > 0 else 0

        failure_reasons = {}
        for biz in business_list:
            reason = biz['failure_reason'] or 'unknown'
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1

        return jsonify({
            'businesses': business_list,
            'total': total_count,
            'stats': {
                'avg_score': round(avg_score, 1),
                'failure_reasons': failure_reasons
            }
        })
    finally:
        session.close()
