"""
지속적 사업 발굴 시스템
- 설정 기반 스케줄로 자동 IT 사업 아이디어 분석
- 설정된 점수 이상만 DB에 저장
- Flask 대시보드에서 실시간 확인 가능
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from smart_business_system import SmartBusinessSystem
from realistic_business_generator import RealisticBusinessGenerator
from database_setup import Session, BusinessPlan, BusinessMeeting, Employee, get_kst_now
from business_discovery_history import BusinessHistoryTracker, initialize_history_tables, BusinessDiscoveryHistory
from config import DiscoveryConfig
from utils import DatabaseManager, clean_keyword, get_next_scheduled_time
from notifications import notify_discovery_complete, notify_high_score_idea, notify_error
from logging_config import get_discovery_logger
from datetime import datetime, timedelta
import time
import json
import random

# 통합 로깅 시스템 사용
logger = get_discovery_logger()

class ContinuousBusinessDiscovery:
    def __init__(self):
        self.smart_system = SmartBusinessSystem()
        self.idea_generator = RealisticBusinessGenerator()
        self.session = Session()
        self.history_tracker = BusinessHistoryTracker()

        # 히스토리 테이블 초기화
        try:
            initialize_history_tables()
        except Exception as e:
            print(f"History tables already exist: {e}")

        # 설정 정보
        self.min_score = DiscoveryConfig.get_min_score()
        self.schedule_hours = DiscoveryConfig.get_schedule_hours()
        self.ideas_per_run = DiscoveryConfig.get_ideas_per_run()

        print("="*80)
        print("[DISCOVERY] 사업 발굴 시스템 시작 (경량 모드)")
        print("="*80)
        print(f"스케줄: {self.schedule_hours} (KST)")
        print(f"최소 저장 점수: {self.min_score}점")
        print(f"실행당 아이디어: {self.ideas_per_run}개")
        print("[OK] 템플릿 기반 아이디어 생성 (메모리 최적화)\n")

        logger.info(f"Discovery System Started - Schedule: {self.schedule_hours}, Min Score: {self.min_score}")

    def refresh_session(self):
        """DB 세션 새로고침 (연결 오류 복구용)"""
        try:
            self.session.rollback()
            self.session.close()
        except:
            pass
        self.session = Session()
        logger.info("Session refreshed due to connection error")

    def safe_commit(self, max_retries=3):
        """안전한 커밋 (재시도 로직 포함)"""
        for attempt in range(max_retries):
            try:
                self.session.commit()
                return True
            except Exception as e:
                logger.warning(f"Commit attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    self.refresh_session()
                    time.sleep(1)
                else:
                    print(f"   [ERROR] DB 커밋 실패 (재시도 {max_retries}회 후): {e}")
                    return False
        return False

    def get_it_business_ideas(self):
        """템플릿 기반 사업 아이디어 생성 (메모리 최적화 + 다양화)"""
        all_opportunities = []
        recent_names = set()

        # 최근 저장된 사업명 조회 (중복 방지)
        try:
            self.refresh_session()
            existing_plans = self.session.query(BusinessPlan.plan_name).limit(200).all()
            recent_names = set([plan[0] for plan in existing_plans])

            # 히스토리에서도 최근 이름 조회 (더 정확한 중복 방지, LIMIT 500으로 비용 최적화)
            recent_history = self.session.query(BusinessDiscoveryHistory.business_name).filter(
                BusinessDiscoveryHistory.discovered_at >= datetime.now() - timedelta(days=7)
            ).limit(500).all()
            recent_names.update([h[0] for h in recent_history])

            print(f"   중복 방지 대상: {len(recent_names)}개")
        except Exception as e:
            print(f"   [WARN] DB 조회 실패: {e}")

        print("\n[GENERATE] 다양한 아이디어 생성 중...")

        try:
            # 동적 조합 아이디어 우선 생성 (수천 가지 조합 가능)
            dynamic_ideas = self.idea_generator.generate_dynamic_combination_ideas(exclude_names=recent_names)
            random.shuffle(dynamic_ideas)

            # 템플릿 아이디어도 생성 (백업용)
            template_ideas = self.idea_generator.generate_monthly_opportunities()
            random.shuffle(template_ideas)

            # 동적 아이디어를 먼저 배치하여 우선 선택되게 함
            combined_ideas = dynamic_ideas + template_ideas

            # 설정된 개수만큼 중복되지 않은 아이디어 선택
            selected_count = 0
            max_select = self.ideas_per_run

            for opp in combined_ideas:
                if selected_count >= max_select:
                    break

                name = opp.get('business', {}).get('name', '')
                if name and name not in recent_names:
                    all_opportunities.append(opp)
                    recent_names.add(name)
                    selected_count += 1
                    print(f"   [OK] 선택 {selected_count}: {name}")

        except Exception as e:
            print(f"   [ERROR] 아이디어 생성 실패: {e}")
            import traceback
            traceback.print_exc()

        print(f"\n   최종 아이디어: {len(all_opportunities)}개\n")
        return all_opportunities

    def generate_keyword(self, business_name):
        """사업 이름에서 검색 키워드 생성 (utils.clean_keyword 사용)"""
        return clean_keyword(business_name)

    def create_business_config(self, opportunity):
        """기회를 분석 가능한 설정으로 변환"""
        business = opportunity['business']
        name = business.get('name', '')

        # 사업 타입 추정
        if '앱' in name or '플랫폼' in name or 'SaaS' in name:
            biz_type = 'saas'
            scale = 'small'
        elif '개발' in name or '제작' in name or '컨설팅' in name:
            biz_type = 'agency'
            scale = 'small'
        elif '매칭' in name or '마켓' in name:
            biz_type = 'marketplace'
            scale = 'small'
        else:
            biz_type = 'saas'
            scale = 'small'

        # 가격 추정
        startup_cost_str = business.get('startup_cost', '100만원')
        if isinstance(startup_cost_str, str):
            # "500만원" 또는 "100-300만원" 형식 처리
            cost_str = startup_cost_str.replace('만원', '').replace('이하', '')
            if '-' in cost_str:
                cost_str = cost_str.split('-')[0]  # 최소값 사용

            try:
                startup_cost = int(cost_str) * 10000
            except:
                startup_cost = 1000000
        else:
            startup_cost = 1000000

        # 매출 추정
        revenue_str = business.get('monthly_revenue',
                                   business.get('revenue_potential', '100-300만원'))
        if isinstance(revenue_str, str):
            revenue_str = revenue_str.replace('월 ', '').replace('만원', '')
            if '-' in revenue_str:
                # 중간값 사용
                parts = revenue_str.split('-')
                try:
                    avg_revenue = (int(parts[0]) + int(parts[1])) // 2
                    monthly_price = avg_revenue * 10000
                except:
                    monthly_price = 50000
            else:
                try:
                    monthly_price = int(revenue_str) * 10000
                except:
                    monthly_price = 50000
        else:
            monthly_price = 50000

        # 고객당 가격 추정 (월 매출 / 예상 고객 수)
        estimated_customers = 20
        price_per_customer = monthly_price // estimated_customers

        return {
            'name': name,
            'type': biz_type,
            'scale': scale,
            'revenue_model': 'subscription' if biz_type == 'saas' else 'one_time',
            'pricing': {
                'monthly': price_per_customer if biz_type == 'saas' else None,
                'one_time': price_per_customer * 10 if biz_type == 'agency' else None
            },
            'target_market_size': 5000,
            'budget': startup_cost,
            'timeline_weeks': 4
        }

    def analyze_and_save(self, opportunity, discovery_batch):
        """아이디어 분석 및 DB 저장 (히스토리 기록 포함)"""
        business = opportunity['business']
        name = business.get('name', '')

        start_time = time.time()

        print(f"\n{'='*80}")
        print(f"[ANALYSIS] {name}")
        print(f"{'='*80}")

        try:
            # 키워드 생성
            keyword = self.generate_keyword(name)

            # 설정 생성
            config = self.create_business_config(opportunity)

            # 실제 AI 분석 수행 (SmartBusinessSystem 사용)
            print("   [AI] 실제 AI 분석 시작...")
            analysis_result = self.smart_system.analyze_business_idea(name, keyword, config)

            # 분석 실패 시 처리
            if not analysis_result.get('passed'):
                print(f"   [FAIL] 분석 실패: {analysis_result.get('reason', 'Unknown')}")
                # 실패한 경우도 히스토리에 기록하고 종료
                market_score = analysis_result.get('market_score', 0)
                total_score = market_score
                revenue_score = 0

                self.history_tracker.record_analysis(
                    business_name=name,
                    business_type=config['type'],
                    category=opportunity.get('category', 'IT/디지털'),
                    keyword=keyword,
                    total_score=total_score,
                    market_score=market_score,
                    revenue_score=revenue_score,
                    saved_to_db=False,
                    discovery_batch=discovery_batch,
                    market_analysis=f"실패: {analysis_result.get('reason', 'Unknown')}",
                    revenue_analysis="N/A",
                    action_plan=None,
                    full_analysis=json.dumps(analysis_result, ensure_ascii=False),
                    analysis_duration_ms=int((time.time() - start_time) * 1000)
                )

                return {'saved': False, 'reason': analysis_result.get('reason')}

            # 분석 성공 - 점수 추출
            market_data = analysis_result.get('market_data', {})
            revenue_data = analysis_result.get('revenue_data', {})

            market_score = market_data.get('market_score', 0)
            revenue_score = revenue_data.get('verdict', {}).get('score', 0)
            total_score = analysis_result.get('total_score', 0)

            print(f"   종합 점수: {total_score:.1f}/100")
            print(f"   ㄴ 시장성: {market_score:.1f}/100")
            print(f"   ㄴ 수익성: {revenue_score:.1f}/100")

            # 분석 시간 계산
            analysis_duration_ms = int((time.time() - start_time) * 1000)

            # 실제 분석 데이터 사용
            market_analysis = market_data
            revenue_analysis = revenue_data

            # 실행 계획 추출 (있으면)
            action_plan = analysis_result.get('action_plan')

            saved_to_db = total_score >= self.min_score  # 설정 기반 최소 점수

            # [HISTORY] 히스토리에 기록 (모든 분석 결과 저장)
            self.history_tracker.record_analysis(
                business_name=name,
                business_type=config['type'],
                category=opportunity.get('category', 'IT/디지털'),
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
                full_analysis=opportunity
            )

            # 저점수 기준 (설정에서 가져옴)
            low_score_threshold = DiscoveryConfig.DEFAULT_LOW_SCORE_THRESHOLD

            # 저점수 사업은 low_score_businesses 테이블에 저장
            if total_score < low_score_threshold:
                # 실패 원인 판단
                if market_score < low_score_threshold and revenue_score < low_score_threshold:
                    failure_reason = 'both'
                elif market_score < low_score_threshold:
                    failure_reason = 'low_market'
                else:
                    failure_reason = 'low_revenue'

                self.history_tracker.save_low_score_business(
                    business_name=name,
                    business_type=config['type'],
                    category=opportunity.get('category', 'IT/디지털'),
                    keyword=keyword,
                    total_score=total_score,
                    market_score=market_score,
                    revenue_score=revenue_score,
                    failure_reason=failure_reason,
                    market_analysis=market_analysis,
                    revenue_analysis=revenue_analysis,
                    discovery_batch=discovery_batch,
                    analysis_duration_ms=analysis_duration_ms,
                    full_data=opportunity
                )

                print(f"   [LOW] 저점수 사업 ({low_score_threshold}점 미만). low_score_businesses 테이블에 저장")
                logger.info(f"Saved to low_score_businesses: {name} (Score: {total_score}, Reason: {failure_reason})")

                return {
                    'saved': False,
                    'low_score_saved': True,
                    'name': name,
                    'score': total_score,
                    'market_score': market_score,
                    'revenue_score': revenue_score,
                    'failure_reason': failure_reason
                }

            # 저점수 이상은 business_plans 테이블에 저장
            elif total_score >= low_score_threshold:
                print(f"   [SAVE] 우수한 아이디어! DB에 저장 중...")

                # 사업 계획으로 DB에 저장
                existing = self.session.query(BusinessPlan).filter_by(
                    plan_name=name
                ).first()

                if existing:
                    print(f"   [UPDATE] 이미 존재하는 사업. 점수 업데이트")
                    existing.feasibility_score = total_score / 10
                else:
                    # 실제 AI 분석 결과에서 매출 추정값 추출
                    realistic_scenario = revenue_data.get('scenarios', {}).get('realistic', {})
                    monthly_profit = realistic_scenario.get('monthly_profit', 0)
                    monthly_revenue_estimate = realistic_scenario.get('monthly_revenue', 0)
                    annual_revenue = monthly_revenue_estimate * 12 if monthly_revenue_estimate > 0 else config['pricing'].get('monthly', 50000) * 12 * 20

                    business_plan = BusinessPlan(
                        plan_name=name,
                        plan_type='IT Service',
                        description=business.get('description', f"{name} 사업"),
                        target_market=f"디지털 네이티브, IT 활용 고객",
                        revenue_model=config['revenue_model'],
                        projected_revenue_12m=annual_revenue,
                        investment_required=config['budget'],
                        risk_level=DiscoveryConfig.get_risk_level(total_score),
                        feasibility_score=total_score / 10,
                        priority=DiscoveryConfig.get_priority(total_score),
                        status='approved',
                        created_by='AI_Discovery_System',
                        details={
                            'discovery_date': get_kst_now().isoformat(),
                            'analysis_score': total_score,
                            'market_score': market_score,
                            'revenue_score': revenue_score,
                            'market_keyword': keyword,
                            'business_type': config['type'],
                            'startup_cost': config['budget'],
                            'estimated_monthly_revenue': monthly_revenue_estimate,
                            'estimated_monthly_profit': monthly_profit,
                            'opportunity_type': opportunity.get('type', 'AI_Discovery'),
                            'priority_reason': f"AI 분석 점수: {total_score:.1f}점",
                            'ai_analysis': {
                                'market_analysis': market_analysis,
                                'revenue_analysis': revenue_analysis,
                                'action_plan': action_plan
                            }
                        }
                    )

                    self.session.add(business_plan)

                if self.safe_commit():
                    print(f"   [OK] business_plans & history 테이블에 저장 완료!")
                else:
                    print(f"   [WARN] DB 저장 실패, 다음 아이디어로 진행")
                    return {
                        'saved': False,
                        'name': name,
                        'score': total_score,
                        'market_score': market_score,
                        'revenue_score': revenue_score,
                        'error': 'DB commit failed'
                    }
                logger.info(f"Saved business idea: {name} (Score: {total_score})")

                return {
                    'saved': True,
                    'name': name,
                    'score': total_score,
                    'market_score': market_score,
                    'revenue_score': revenue_score
                }

            else:
                print(f"   [SKIP] 점수 부족 ({self.min_score}점 미만). business_plans 건너뜀 (히스토리만 기록)")
                logger.info(f"Skipped business_plans but recorded in history: {name} (Score: {total_score})")

                return {
                    'saved': False,
                    'name': name,
                    'score': total_score,
                    'market_score': market_score,
                    'revenue_score': revenue_score
                }

        except Exception as e:
            print(f"   [ERROR] 오류 발생: {e}")
            logger.error(f"Error analyzing {name}: {e}")
            return {
                'saved': False,
                'name': name,
                'error': str(e)
            }

    def run_hourly_discovery(self):
        """매시간 사업 발굴 (히스토리 추적 및 인사이트 생성)"""
        now = get_kst_now()
        discovery_batch = now.strftime('%Y-%m-%d-%H')  # 배치 ID

        print(f"\n{'='*80}")
        print(f"[TIME] {now.strftime('%Y-%m-%d %H:%M:%S')} - 사업 발굴 시작")
        print(f"[BATCH] 배치 ID: {discovery_batch}")
        print(f"{'='*80}\n")

        # IT 사업 아이디어 생성
        it_ideas = self.get_it_business_ideas()
        print(f"[IDEAS] 이번 시간 분석 대상: {len(it_ideas)}개\n")

        results = []
        saved_count = 0

        for i, idea in enumerate(it_ideas, 1):
            print(f"\n[{i}/{len(it_ideas)}]")
            result = self.analyze_and_save(idea, discovery_batch)
            results.append(result)

            if result.get('saved'):
                saved_count += 1

            # API 요청 간격 (실제 웹 스크래핑 시)
            time.sleep(2)

        # 결과 요약
        print(f"\n{'='*80}")
        print(f"[RESULT] 이번 시간 결과")
        print(f"{'='*80}")
        print(f"분석: {len(it_ideas)}개")
        print(f"저장: {saved_count}개 (50점 이상)")
        print(f"제외: {len(it_ideas) - saved_count}개 (50점 미만)\n")

        # 시간별 스냅샷 생성
        print(f"[SNAPSHOT] 시간별 스냅샷 생성 중...")
        try:
            snapshot_id = self.history_tracker.create_snapshot(snapshot_type='hourly')
            if snapshot_id:
                print(f"   [OK] 스냅샷 생성 완료 (ID: {snapshot_id})")
        except Exception as e:
            print(f"   [WARNING] 스냅샷 생성 실패: {e}")

        # 인사이트 생성
        print(f"[INSIGHT] 인사이트 분석 중...")
        try:
            insight_count = self.history_tracker.generate_insights()
            if insight_count > 0:
                print(f"   [OK] {insight_count}개 인사이트 생성")
            else:
                print(f"   [INFO] 새로운 인사이트 없음")
        except Exception as e:
            print(f"   [WARNING] 인사이트 생성 실패: {e}")

        logger.info(f"Hourly discovery completed: {saved_count}/{len(it_ideas)} saved")

        # 결과 객체 생성
        discovery_results = {
            'timestamp': now.isoformat(),
            'batch_id': discovery_batch,
            'analyzed': len(it_ideas),
            'saved': saved_count,
            'results': results
        }

        # 알림 전송 (설정된 경우)
        try:
            notify_discovery_complete(discovery_results)

            # 고득점 아이디어 개별 알림
            for result in results:
                if result.get('saved') and result.get('score', 0) >= DiscoveryConfig.DEFAULT_HIGH_SCORE_THRESHOLD:
                    notify_high_score_idea(result)
        except Exception as e:
            logger.warning(f"Notification failed: {e}")

        return discovery_results

    def generate_discovery_meeting(self, results):
        """발굴 결과 회의록 생성"""
        now = get_kst_now()
        saved_ideas = [r for r in results['results'] if r.get('saved')]

        if not saved_ideas:
            print("   저장된 아이디어 없음. 회의록 생성 안 함.")
            return

        # 회의록 생성
        agenda = [
            "신규 IT 사업 기회 발굴 결과 검토",
            "고득점 아이디어 분석",
            "실행 우선순위 결정",
            "다음 단계 액션 아이템"
        ]

        key_decisions = [
            f"이번 시간 {results['saved']}개 유망 사업 발굴",
            f"평균 점수: {sum(r['score'] for r in saved_ideas) / len(saved_ideas):.1f}/100"
        ]

        for idea in saved_ideas:
            key_decisions.append(f"[OK] {idea['name']} (점수: {idea['score']})")

        action_items = [
            "상위 3개 아이디어 상세 시장 조사",
            "기술 스택 및 개발 리소스 검토",
            "ROI 시뮬레이션 실행",
            "파일럿 프로젝트 착수 검토"
        ]

        meeting = BusinessMeeting(
            meeting_type='사업 발굴 회의',
            title=f'자동 IT 사업 발굴 - {now.strftime("%Y-%m-%d %H시")}',
            agenda=json.dumps(agenda, ensure_ascii=False),
            participants=json.dumps(['AI Discovery System', 'Business Analyzer'], ensure_ascii=False),
            key_decisions=key_decisions,
            action_items=action_items,
            status='completed',
            meeting_notes=json.dumps({
                'type': 'automatic_discovery',
                'analyzed_count': results['analyzed'],
                'saved_count': results['saved'],
                'discovery_system': 'Continuous Business Discovery v1.0',
                'ideas': [{'name': r['name'], 'score': r['score']} for r in saved_ideas]
            }, ensure_ascii=False)
        )

        self.session.add(meeting)
        if self.safe_commit():
            print(f"   [MEETING] 회의록 생성 완료!")
        else:
            print(f"   [WARN] 회의록 저장 실패")
        logger.info(f"Meeting record created with {len(saved_ideas)} ideas")

    def run_continuous(self):
        """지속적 실행 (24/7)"""
        print("[CONTINUOUS] 24/7 지속 실행 모드 시작")
        print("매시간 정각에 자동 사업 발굴")
        print("Ctrl+C로 종료\n")

        last_hour = -1

        while True:
            try:
                now = get_kst_now()
                current_hour = now.hour
                current_minute = now.minute

                # 매시간 정각에 실행
                if current_minute == 0 and current_hour != last_hour:
                    results = self.run_hourly_discovery()

                    # 회의록 생성
                    if results['saved'] > 0:
                        self.generate_discovery_meeting(results)

                    last_hour = current_hour

                    # 다음 시간까지 대기
                    print(f"\n[NEXT] 다음 발굴: {(now + timedelta(hours=1)).strftime('%H:00')}")
                    print("="*80 + "\n")

                    time.sleep(60)  # 1분 대기
                else:
                    # 30초마다 체크
                    time.sleep(30)

            except KeyboardInterrupt:
                print("\n\n[STOP] 시스템 종료")
                logger.info("System stopped by user")
                break
            except Exception as e:
                print(f"\n[ERROR] 오류 발생: {e}")
                logger.error(f"System error: {e}")
                time.sleep(60)

    def run_once_now(self):
        """즉시 1회 실행 (테스트용)"""
        print("[RUN] 즉시 실행 모드\n")

        results = self.run_hourly_discovery()

        if results['saved'] > 0:
            self.generate_discovery_meeting(results)

        print("\n[DONE] 완료!")
        return results

    def close(self):
        """세션 정리"""
        self.session.close()


# 실행
if __name__ == "__main__":
    import sys

    discovery = ContinuousBusinessDiscovery()

    try:
        if len(sys.argv) > 1 and sys.argv[1] == '--once':
            # 1회만 실행
            discovery.run_once_now()
        else:
            # 지속 실행
            discovery.run_continuous()
    finally:
        discovery.close()
