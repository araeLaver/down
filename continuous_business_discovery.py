"""
지속적 사업 발굴 시스템
- 매시간 자동으로 새로운 IT 사업 아이디어 분석
- 80점 이상만 DB에 저장
- Flask 대시보드에서 실시간 확인 가능
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from smart_business_system import SmartBusinessSystem
from realistic_business_generator import RealisticBusinessGenerator
from trend_based_idea_generator import TrendBasedIdeaGenerator
from database_setup import Session, BusinessPlan, BusinessMeeting, Employee, get_kst_now
from business_discovery_history import BusinessHistoryTracker, initialize_history_tables, BusinessDiscoveryHistory
from datetime import datetime, timedelta
import time
import logging
import json
import random
import copy

# 로깅 설정
logging.basicConfig(
    filename='business_discovery.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

class ContinuousBusinessDiscovery:
    def __init__(self):
        self.smart_system = SmartBusinessSystem()
        self.idea_generator = RealisticBusinessGenerator()
        self.trend_generator = TrendBasedIdeaGenerator()  # 트렌드 기반 생성기 추가
        self.session = Session()
        self.history_tracker = BusinessHistoryTracker()

        # 히스토리 테이블 초기화
        try:
            initialize_history_tables()
        except Exception as e:
            print(f"History tables already exist: {e}")

        print("="*80)
        print("[DISCOVERY] 지속적 사업 발굴 시스템 시작 (히스토리 추적 활성화)")
        print("="*80)
        print("매시간 자동으로 IT 사업 아이디어 분석 및 DB 저장")
        print("70점 이상만 선별하여 실행 가능한 사업으로 등록")
        print("[OK] 모든 분석 결과를 히스토리에 기록하여 트렌드 분석 가능\n")

        logging.info("Continuous Business Discovery System Started with History Tracking")
    def create_variant_idea(self, original_opp, variant_type):
        """동일 사업아이템을 다른 방향으로 변형"""
        variant = copy.deepcopy(original_opp)
        business = variant.get('business', {})
        original_name = business.get('name', '')
        original_desc = business.get('description', '')

        variants = {
            'B2B': {'suffix': ' (B2B 기업용)', 'desc_add': ' 기업 고객 대상.', 'revenue_mult': 1.5},
            'Premium': {'suffix': ' (프리미엄)', 'desc_add': ' 고급 기능 포함.', 'revenue_mult': 2.0},
            'Global': {'suffix': ' (해외진출)', 'desc_add': ' 글로벌 시장 타겟.', 'revenue_mult': 1.8},
            'Niche': {'suffix': ' (특화버전)', 'desc_add': ' 특정 산업 맞춤.', 'revenue_mult': 1.3},
            'Subscription': {'suffix': ' (구독형)', 'desc_add': ' 월 정액 모델.', 'revenue_mult': 1.2}
        }

        v = variants.get(variant_type, variants['B2B'])
        business['name'] = original_name + v['suffix']
        business['description'] = (original_desc or '') + v['desc_add']
        variant['business'] = business
        variant['variant_type'] = variant_type
        return variant

    def get_it_business_ideas(self):
        """IT 사업 아이디어 생성 (템플릿 + 트렌드 혼합) - 중복 제거"""
        all_opportunities = []

        # 최근 24시간 이미 분석한 사업명 가져오기 (중복 방지) - 7일은 너무 길어서 1일로 변경
        from datetime import timedelta
        one_day_ago = get_kst_now() - timedelta(days=1)
        recent_businesses = self.session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.discovered_at >= one_day_ago
        ).all()
        recent_names = set([b.business_name for b in recent_businesses])

        print(f"   최근 24시간 분석된 사업: {len(recent_names)}개 (중복 방지)")

        # 1. 기존 템플릿 기반 아이디어 - 매번 다른 아이디어 생성
        # 여러 번 생성해서 더 많은 옵션 확보
        template_opportunities = []
        for _ in range(10):  # 10번 생성해서 더 다양한 아이디어 수집
            template_opportunities.extend(self.idea_generator.generate_monthly_opportunities())

        # IT/디지털/앱 관련만 필터 + 중복 제거
        it_opportunities = []
        for opp in template_opportunities:
            business = opp.get('business', {})
            name = business.get('name', '')

            # IT 관련 키워드 체크
            it_keywords = ['앱', '웹', 'AI', 'IT', '사이트', '플랫폼',
                          '자동화', 'SaaS', '소프트웨어', '디지털',
                          '온라인', '챗봇', 'API', '시스템']

            if any(keyword in name for keyword in it_keywords):
                # 이미 최근에 분석한 사업이면 다른 방향으로 변형
                if name in recent_names:
                    for vtype in ['B2B', 'Premium', 'Global', 'Niche', 'Subscription']:
                        variant = self.create_variant_idea(opp, vtype)
                        variant_name = variant['business']['name']
                        if variant_name not in recent_names:
                            it_opportunities.append(variant)
                            recent_names.add(variant_name)
                            print(f"   [VARIANT] {name} -> {variant_name}")
                            break
                else:
                    it_opportunities.append(opp)
                    recent_names.add(name)

        # 랜덤하게 섞어서 선택
        import random
import copy
        random.shuffle(it_opportunities)
        all_opportunities.extend(it_opportunities[:3])  # 3개 선택

        # 2. 실시간 트렌드 기반 아이디어 (4-5개) - 글로벌 트렌드 포함
        try:
            print("\n[TREND] 실시간 글로벌 트렌드 수집 중...")
            trend_ideas = self.trend_generator.generate_ideas_from_trends()

            # 중복 제거 후 트렌드 아이디어 필터링
            unique_trends = []
            for idea in trend_ideas:
                name = idea.get('business', {}).get('name', '')
                if name not in recent_names:
                    unique_trends.append(idea)
                    recent_names.add(name)
                else:
                    # 중복이면 변형 시도
                    for vtype in ['B2B', 'Premium', 'Global', 'Niche', 'Subscription']:
                        variant = self.create_variant_idea(idea, vtype)
                        variant_name = variant['business']['name']
                        if variant_name not in recent_names:
                            unique_trends.append(variant)
                            recent_names.add(variant_name)
                            print(f"   [VARIANT] {name} -> {variant_name}")
                            break

            # 트렌드 아이디어를 우선순위별로 정렬 (글로벌 트렌드 우선)
            sorted_trends = sorted(
                unique_trends,
                key=lambda x: (
                    x.get('business', {}).get('global_potential', False),
                    x.get('priority', '보통') == '높음'
                ),
                reverse=True
            )

            all_opportunities.extend(sorted_trends[:5])
            print(f"   트렌드 기반 아이디어 {len(sorted_trends[:5])}개 추가 (글로벌 포함, 중복 제거됨)")
        except Exception as e:
            print(f"   [WARNING] 트렌드 수집 실패: {e}")
            logging.warning(f"Trend collection failed: {e}")

        # 최종적으로 5-8개 반환 (더 다양한 아이디어)
        print(f"   최종 생성된 아이디어: {len(all_opportunities)}개 (모두 중복 제거됨)\n")
        return all_opportunities[:10]  # 최대 10개까지

    def generate_keyword(self, business_name):
        """사업 이름에서 검색 키워드 생성"""
        # 불필요한 단어 제거
        remove_words = ['앱', '서비스', '플랫폼', '시스템', '솔루션', '도구', '개발']
        keyword = business_name

        for word in remove_words:
            keyword = keyword.replace(word, '')

        keyword = keyword.strip()

        # 너무 짧으면 원본 사용
        if len(keyword) < 3:
            keyword = business_name

        return keyword

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

            print(f"   종합 점수: {int(total_score)}/100")
            print(f"   ㄴ 시장성: {int(market_score)}/100")
            print(f"   ㄴ 수익성: {int(revenue_score)}/100")

            # 분석 시간 계산
            analysis_duration_ms = int((time.time() - start_time) * 1000)

            # 실제 분석 데이터 사용
            market_analysis = market_data
            revenue_analysis = revenue_data

            # 실행 계획 추출 (있으면)
            action_plan = analysis_result.get('action_plan')

            saved_to_db = total_score >= 70  # 70점 이상으로 변경 (실제 AI 분석 결과가 보수적이므로)

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

            # 50점 미만이면 low_score_businesses 테이블에 저장
            if total_score < 60:
                # 실패 원인 판단
                if market_score < 60 and revenue_score < 60:
                    failure_reason = 'both'
                elif market_score < 60:
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

                print(f"   [LOW] 저점수 사업 (50점 미만). low_score_businesses 테이블에 저장 (개선 분석용)")
                logging.info(f"Saved to low_score_businesses: {name} (Score: {total_score}, Reason: {failure_reason})")

                return {
                    'saved': False,
                    'low_score_saved': True,
                    'name': name,
                    'score': total_score,
                    'market_score': market_score,
                    'revenue_score': revenue_score,
                    'failure_reason': failure_reason
                }

            # 50점 이상 business_plans 테이블에 저장 (50-69: 검토 대상, 70+: 우수)
            elif total_score >= 50:
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
                        risk_level='medium' if total_score > 75 else 'high',
                        feasibility_score=total_score / 10,
                        priority='high' if total_score >= 85 else 'medium',
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
                            'priority_reason': f"AI 분석 점수: {int(total_score)}점",
                            'ai_analysis': {
                                'market_analysis': market_analysis,
                                'revenue_analysis': revenue_analysis,
                                'action_plan': action_plan
                            }
                        }
                    )

                    self.session.add(business_plan)

                self.session.commit()
                print(f"   [OK] business_plans & history 테이블에 저장 완료!")
                logging.info(f"Saved business idea: {name} (Score: {total_score})")

                return {
                    'saved': True,
                    'name': name,
                    'score': total_score,
                    'market_score': market_score,
                    'revenue_score': revenue_score
                }

            else:
                print(f"   [SKIP] 점수 부족 (80점 미만). business_plans 건너뜀 (히스토리만 기록)")
                logging.info(f"Skipped business_plans but recorded in history: {name} (Score: {total_score})")

                return {
                    'saved': False,
                    'name': name,
                    'score': total_score,
                    'market_score': market_score,
                    'revenue_score': revenue_score
                }

        except Exception as e:
            print(f"   [ERROR] 오류 발생: {e}")
            logging.error(f"Error analyzing {name}: {e}")
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

        logging.info(f"Hourly discovery completed: {saved_count}/{len(it_ideas)} saved")

        return {
            'timestamp': now.isoformat(),
            'batch_id': discovery_batch,
            'analyzed': len(it_ideas),
            'saved': saved_count,
            'results': results
        }

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
            f"평균 점수: {int(sum(r['score'] for r in saved_ideas) / len(saved_ideas))}/100"
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
        self.session.commit()

        print(f"   [MEETING] 회의록 생성 완료!")
        logging.info(f"Meeting record created with {len(saved_ideas)} ideas")

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
                logging.info("System stopped by user")
                break
            except Exception as e:
                print(f"\n[ERROR] 오류 발생: {e}")
                logging.error(f"System error: {e}")
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
