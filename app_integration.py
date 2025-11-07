"""
Flask app에 통합할 코드

기존 app.py에 다음을 추가:
1. 백그라운드 사업 발굴 스레드
2. 발굴된 사업 조회 API
3. 대시보드 페이지
"""

# ==================== app.py 상단에 추가 ====================

from continuous_business_discovery import ContinuousBusinessDiscovery
import threading

# ==================== 백그라운드 함수 추가 ====================

def background_business_discovery():
    """백그라운드에서 지속적으로 사업 발굴"""
    import logging
    logging.info("[BACKGROUND] Starting continuous business discovery...")
    print("[BACKGROUND] Starting continuous business discovery...")

    discovery = ContinuousBusinessDiscovery()
    last_hour = -1

    while True:
        try:
            now = datetime.now()
            current_hour = now.hour
            current_minute = now.minute

            # 매시간 정각에 실행
            if current_minute == 0 and current_hour != last_hour:
                logging.info(f"[DISCOVERY] Running hourly discovery at {now}")
                print(f"[DISCOVERY] Running hourly discovery at {now}")

                results = discovery.run_hourly_discovery()

                if results['saved'] > 0:
                    discovery.generate_discovery_meeting(results)

                last_hour = current_hour
                time.sleep(60)
            else:
                time.sleep(30)

        except Exception as e:
            logging.error(f"Discovery error: {e}")
            print(f"Discovery error: {e}")
            time.sleep(60)


# ==================== API 엔드포인트 추가 ====================

@app.route('/api/discovered-businesses')
def api_discovered_businesses():
    """자동 발굴된 사업 목록 API"""
    session = Session()
    try:
        # 최근 발굴된 사업 (status='approved'이고 created_by='AI_Discovery_System')
        businesses = session.query(BusinessPlan).filter(
            BusinessPlan.created_by == 'AI_Discovery_System',
            BusinessPlan.status == 'approved'
        ).order_by(BusinessPlan.created_at.desc()).limit(50).all()

        business_list = []
        for biz in businesses:
            details = biz.details if isinstance(biz.details, dict) else {}

            business_list.append({
                'id': biz.id,
                'name': biz.plan_name,
                'type': biz.plan_type,
                'score': details.get('analysis_score', 0),
                'feasibility': biz.feasibility_score,
                'revenue_12m': biz.projected_revenue_12m,
                'investment': biz.investment_required,
                'risk': biz.risk_level,
                'priority': biz.priority,
                'created_at': biz.created_at.strftime('%Y-%m-%d %H:%M') if biz.created_at else None,
                'description': biz.description,
                'revenue_model': biz.revenue_model,
                'details': details
            })

        # 통계
        today = datetime.utcnow().date()
        today_count = session.query(BusinessPlan).filter(
            BusinessPlan.created_by == 'AI_Discovery_System',
            BusinessPlan.created_at >= today
        ).count()

        week_ago = datetime.utcnow() - timedelta(days=7)
        week_count = session.query(BusinessPlan).filter(
            BusinessPlan.created_by == 'AI_Discovery_System',
            BusinessPlan.created_at >= week_ago
        ).count()

        high_score_count = len([b for b in business_list if b['score'] >= 85])

        return jsonify({
            'businesses': business_list,
            'stats': {
                'total': len(business_list),
                'today': today_count,
                'this_week': week_count,
                'high_score': high_score_count
            }
        })
    finally:
        session.close()


@app.route('/api/business-stats')
def api_business_stats():
    """사업 발굴 통계 API"""
    session = Session()
    try:
        # 시간대별 발굴 현황 (최근 24시간)
        last_24h = datetime.utcnow() - timedelta(hours=24)

        hourly_discoveries = session.query(
            text(f"""
                SELECT DATE_TRUNC('hour', created_at) as hour,
                       COUNT(*) as count
                FROM {SCHEMA_NAME}.business_plans
                WHERE created_by = 'AI_Discovery_System'
                  AND created_at >= :last_24h
                GROUP BY DATE_TRUNC('hour', created_at)
                ORDER BY hour DESC
            """)
        ).params(last_24h=last_24h).all()

        hourly_data = {}
        for row in hourly_discoveries:
            hourly_data[row[0].strftime('%Y-%m-%d %H:00')] = row[1]

        # 점수 분포
        all_businesses = session.query(BusinessPlan).filter(
            BusinessPlan.created_by == 'AI_Discovery_System'
        ).all()

        score_distribution = {
            '90-100': 0,
            '85-89': 0,
            '80-84': 0,
            '75-79': 0,
            '70-74': 0
        }

        for biz in all_businesses:
            details = biz.details if isinstance(biz.details, dict) else {}
            score = details.get('analysis_score', 0)

            if score >= 90:
                score_distribution['90-100'] += 1
            elif score >= 85:
                score_distribution['85-89'] += 1
            elif score >= 80:
                score_distribution['80-84'] += 1
            elif score >= 75:
                score_distribution['75-79'] += 1
            elif score >= 70:
                score_distribution['70-74'] += 1

        return jsonify({
            'hourly_discoveries': hourly_data,
            'score_distribution': score_distribution,
            'total_discovered': len(all_businesses)
        })
    finally:
        session.close()


@app.route('/business-discovery')
def business_discovery():
    """사업 발굴 대시보드 페이지"""
    return render_template('business_discovery.html')


# ==================== app.py 하단 백그라운드 스레드 시작 부분에 추가 ====================

def start_background_threads():
    """백그라운드 스레드 시작"""
    # 기존 스레드들...

    # 사업 발굴 스레드 추가
    discovery_thread = Thread(target=background_business_discovery, daemon=True)
    discovery_thread.start()
    print("[STARTUP] Background business discovery started")


# 기존 start_background_threads() 호출 부분을 대체하거나
# Production 환경에서 start_background_threads() 실행
