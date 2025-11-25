"""
   
-    IT   
- 80  DB 
- Flask    
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

#  
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
        self.trend_generator = TrendBasedIdeaGenerator()  #    
        self.session = Session()
        self.history_tracker = BusinessHistoryTracker()

        #   
        try:
            initialize_history_tables()
        except Exception as e:
            print(f"History tables already exist: {e}")

        print("="*80)
        print("[DISCOVERY]      (  )")
        print("="*80)
        print("  IT     DB ")
        print("70      ")
        print("[OK]        \n")

        logging.info("Continuous Business Discovery System Started with History Tracking")
    def create_variant_idea(self, original_opp, variant_type):
        """    """
        variant = copy.deepcopy(original_opp)
        business = variant.get('business', {})
        original_name = business.get('name', '')
        original_desc = business.get('description', '')

        variants = {
            'B2B': {'suffix': ' (B2B )', 'desc_add': '   .', 'revenue_mult': 1.5},
            'Premium': {'suffix': ' ()', 'desc_add': '   .', 'revenue_mult': 2.0},
            'Global': {'suffix': ' ()', 'desc_add': '   .', 'revenue_mult': 1.8},
            'Niche': {'suffix': ' ()', 'desc_add': '   .', 'revenue_mult': 1.3},
            'Subscription': {'suffix': ' ()', 'desc_add': '   .', 'revenue_mult': 1.2}
        }

        v = variants.get(variant_type, variants['B2B'])
        business['name'] = original_name + v['suffix']
        business['description'] = (original_desc or '') + v['desc_add']
        variant['business'] = business
        variant['variant_type'] = variant_type
        return variant

    def get_it_business_ideas(self):
        """IT    ( +  ) -  """
        all_opportunities = []

        #  24     ( ) - 7   1 
        from datetime import timedelta
        one_day_ago = get_kst_now() - timedelta(days=1)
        recent_businesses = self.session.query(BusinessDiscoveryHistory).filter(
            BusinessDiscoveryHistory.discovered_at >= one_day_ago
        ).all()
        recent_names = set([b.business_name for b in recent_businesses])

        print(f"    24  : {len(recent_names)} ( )")

        # 1.     -    
        #       
        template_opportunities = []
        for _ in range(10):  # 10     
            template_opportunities.extend(self.idea_generator.generate_monthly_opportunities())

        # IT//   +  
        it_opportunities = []
        for opp in template_opportunities:
            business = opp.get('business', {})
            name = business.get('name', '')

            # IT   
            it_keywords = ['', '', 'AI', 'IT', '', '',
                          '', 'SaaS', '', '',
                          '', '', 'API', '']

            if any(keyword in name for keyword in it_keywords):
                #       
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

        #   
        import random
import copy
        random.shuffle(it_opportunities)
        all_opportunities.extend(it_opportunities[:3])  # 3 

        # 2.     (4-5) -   
        try:
            print("\n[TREND]     ...")
            trend_ideas = self.trend_generator.generate_ideas_from_trends()

            #      
            unique_trends = []
            for idea in trend_ideas:
                name = idea.get('business', {}).get('name', '')
                if name not in recent_names:
                    unique_trends.append(idea)
                    recent_names.add(name)
                else:
                    #   
                    for vtype in ['B2B', 'Premium', 'Global', 'Niche', 'Subscription']:
                        variant = self.create_variant_idea(idea, vtype)
                        variant_name = variant['business']['name']
                        if variant_name not in recent_names:
                            unique_trends.append(variant)
                            recent_names.add(variant_name)
                            print(f"   [VARIANT] {name} -> {variant_name}")
                            break

            #     (  )
            sorted_trends = sorted(
                unique_trends,
                key=lambda x: (
                    x.get('business', {}).get('global_potential', False),
                    x.get('priority', '') == ''
                ),
                reverse=True
            )

            all_opportunities.extend(sorted_trends[:5])
            print(f"      {len(sorted_trends[:5])}  ( ,  )")
        except Exception as e:
            print(f"   [WARNING]   : {e}")
            logging.warning(f"Trend collection failed: {e}")

        #  5-8  (  )
        print(f"     : {len(all_opportunities)} (  )\n")
        return all_opportunities[:10]  #  10

    def generate_keyword(self, business_name):
        """    """
        #   
        remove_words = ['', '', '', '', '', '', '']
        keyword = business_name

        for word in remove_words:
            keyword = keyword.replace(word, '')

        keyword = keyword.strip()

        #    
        if len(keyword) < 3:
            keyword = business_name

        return keyword

    def create_business_config(self, opportunity):
        """    """
        business = opportunity['business']
        name = business.get('name', '')

        #   
        if '' in name or '' in name or 'SaaS' in name:
            biz_type = 'saas'
            scale = 'small'
        elif '' in name or '' in name or '' in name:
            biz_type = 'agency'
            scale = 'small'
        elif '' in name or '' in name:
            biz_type = 'marketplace'
            scale = 'small'
        else:
            biz_type = 'saas'
            scale = 'small'

        #  
        startup_cost_str = business.get('startup_cost', '100')
        if isinstance(startup_cost_str, str):
            # "500"  "100-300"  
            cost_str = startup_cost_str.replace('', '').replace('', '')
            if '-' in cost_str:
                cost_str = cost_str.split('-')[0]  #  

            try:
                startup_cost = int(cost_str) * 10000
            except:
                startup_cost = 1000000
        else:
            startup_cost = 1000000

        #  
        revenue_str = business.get('monthly_revenue',
                                   business.get('revenue_potential', '100-300'))
        if isinstance(revenue_str, str):
            revenue_str = revenue_str.replace(' ', '').replace('', '')
            if '-' in revenue_str:
                #  
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

        #    (  /   )
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
        """   DB  (  )"""
        business = opportunity['business']
        name = business.get('name', '')

        start_time = time.time()

        print(f"\n{'='*80}")
        print(f"[ANALYSIS] {name}")
        print(f"{'='*80}")

        try:
            #  
            keyword = self.generate_keyword(name)

            #  
            config = self.create_business_config(opportunity)

            #  AI   (SmartBusinessSystem )
            print("   [AI]  AI  ...")
            analysis_result = self.smart_system.analyze_business_idea(name, keyword, config)

            #    
            if not analysis_result.get('passed'):
                print(f"   [FAIL]  : {analysis_result.get('reason', 'Unknown')}")
                #     
                market_score = analysis_result.get('market_score', 0)
                total_score = market_score
                revenue_score = 0

                self.history_tracker.record_analysis(
                    business_name=name,
                    business_type=config['type'],
                    category=opportunity.get('category', 'IT/'),
                    keyword=keyword,
                    total_score=total_score,
                    market_score=market_score,
                    revenue_score=revenue_score,
                    saved_to_db=False,
                    discovery_batch=discovery_batch,
                    market_analysis=f": {analysis_result.get('reason', 'Unknown')}",
                    revenue_analysis="N/A",
                    full_analysis=json.dumps(analysis_result, ensure_ascii=False),
                    analysis_duration_ms=int((time.time() - start_time) * 1000)
                )

                return {'saved': False, 'reason': analysis_result.get('reason')}

            #   -  
            market_data = analysis_result.get('market_data', {})
            revenue_data = analysis_result.get('revenue_data', {})

            market_score = market_data.get('market_score', 0)
            revenue_score = revenue_data.get('verdict', {}).get('score', 0)
            total_score = analysis_result.get('total_score', 0)

            print(f"    : {int(total_score)}/100")
            print(f"    : {int(market_score)}/100")
            print(f"    : {int(revenue_score)}/100")

            #   
            analysis_duration_ms = int((time.time() - start_time) * 1000)

            #    
            market_analysis = market_data
            revenue_analysis = revenue_data

            #    ()
            action_plan = analysis_result.get('action_plan')

            saved_to_db = total_score >= 70  # 70   ( AI   )

            # [HISTORY]   (   )
            self.history_tracker.record_analysis(
                business_name=name,
                business_type=config['type'],
                category=opportunity.get('category', 'IT/'),
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

            # 50  low_score_businesses  
            if total_score < 60:
                #   
                if market_score < 60 and revenue_score < 60:
                    failure_reason = 'both'
                elif market_score < 60:
                    failure_reason = 'low_market'
                else:
                    failure_reason = 'low_revenue'

                self.history_tracker.save_low_score_business(
                    business_name=name,
                    business_type=config['type'],
                    category=opportunity.get('category', 'IT/'),
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

                print(f"   [LOW]   (50 ). low_score_businesses   ( )")
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

            # 50  business_plans   (50-69:  , 70+: )
            elif total_score >= 50:
                print(f"   [SAVE]  ! DB  ...")

                #   DB 
                existing = self.session.query(BusinessPlan).filter_by(
                    plan_name=name
                ).first()

                if existing:
                    print(f"   [UPDATE]   .  ")
                    existing.feasibility_score = total_score / 10
                else:
                    #  AI     
                    realistic_scenario = revenue_data.get('scenarios', {}).get('realistic', {})
                    monthly_profit = realistic_scenario.get('monthly_profit', 0)
                    monthly_revenue_estimate = realistic_scenario.get('monthly_revenue', 0)
                    annual_revenue = monthly_revenue_estimate * 12 if monthly_revenue_estimate > 0 else config['pricing'].get('monthly', 50000) * 12 * 20

                    business_plan = BusinessPlan(
                        plan_name=name,
                        plan_type='IT Service',
                        description=business.get('description', f"{name} "),
                        target_market=f" , IT  ",
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
                            'priority_reason': f"AI  : {int(total_score)}",
                            'ai_analysis': {
                                'market_analysis': market_analysis,
                                'revenue_analysis': revenue_analysis,
                                'action_plan': action_plan
                            }
                        }
                    )

                    self.session.add(business_plan)

                self.session.commit()
                print(f"   [OK] business_plans & history   !")
                logging.info(f"Saved business idea: {name} (Score: {total_score})")

                return {
                    'saved': True,
                    'name': name,
                    'score': total_score,
                    'market_score': market_score,
                    'revenue_score': revenue_score
                }

            else:
                print(f"   [SKIP]   (80 ). business_plans  ( )")
                logging.info(f"Skipped business_plans but recorded in history: {name} (Score: {total_score})")

                return {
                    'saved': False,
                    'name': name,
                    'score': total_score,
                    'market_score': market_score,
                    'revenue_score': revenue_score
                }

        except Exception as e:
            print(f"   [ERROR]  : {e}")
            logging.error(f"Error analyzing {name}: {e}")
            return {
                'saved': False,
                'name': name,
                'error': str(e)
            }

    def run_hourly_discovery(self):
        """   (    )"""
        now = get_kst_now()
        discovery_batch = now.strftime('%Y-%m-%d-%H')  #  ID

        print(f"\n{'='*80}")
        print(f"[TIME] {now.strftime('%Y-%m-%d %H:%M:%S')} -   ")
        print(f"[BATCH]  ID: {discovery_batch}")
        print(f"{'='*80}\n")

        # IT   
        it_ideas = self.get_it_business_ideas()
        print(f"[IDEAS]    : {len(it_ideas)}\n")

        results = []
        saved_count = 0

        for i, idea in enumerate(it_ideas, 1):
            print(f"\n[{i}/{len(it_ideas)}]")
            result = self.analyze_and_save(idea, discovery_batch)
            results.append(result)

            if result.get('saved'):
                saved_count += 1

            # API   (   )
            time.sleep(2)

        #  
        print(f"\n{'='*80}")
        print(f"[RESULT]   ")
        print(f"{'='*80}")
        print(f": {len(it_ideas)}")
        print(f": {saved_count} (50 )")
        print(f": {len(it_ideas) - saved_count} (50 )\n")

        #   
        print(f"[SNAPSHOT]    ...")
        try:
            snapshot_id = self.history_tracker.create_snapshot(snapshot_type='hourly')
            if snapshot_id:
                print(f"   [OK]    (ID: {snapshot_id})")
        except Exception as e:
            print(f"   [WARNING]   : {e}")

        #  
        print(f"[INSIGHT]   ...")
        try:
            insight_count = self.history_tracker.generate_insights()
            if insight_count > 0:
                print(f"   [OK] {insight_count}  ")
            else:
                print(f"   [INFO]   ")
        except Exception as e:
            print(f"   [WARNING]   : {e}")

        logging.info(f"Hourly discovery completed: {saved_count}/{len(it_ideas)} saved")

        return {
            'timestamp': now.isoformat(),
            'batch_id': discovery_batch,
            'analyzed': len(it_ideas),
            'saved': saved_count,
            'results': results
        }

    def generate_discovery_meeting(self, results):
        """   """
        now = get_kst_now()
        saved_ideas = [r for r in results['results'] if r.get('saved')]

        if not saved_ideas:
            print("     .    .")
            return

        #  
        agenda = [
            " IT     ",
            "  ",
            "  ",
            "   "
        ]

        key_decisions = [
            f"  {results['saved']}   ",
            f" : {int(sum(r['score'] for r in saved_ideas) / len(saved_ideas))}/100"
        ]

        for idea in saved_ideas:
            key_decisions.append(f"[OK] {idea['name']} (: {idea['score']})")

        action_items = [
            " 3    ",
            "     ",
            "ROI  ",
            "   "
        ]

        meeting = BusinessMeeting(
            meeting_type='  ',
            title=f' IT   - {now.strftime("%Y-%m-%d %H")}',
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

        print(f"   [MEETING]   !")
        logging.info(f"Meeting record created with {len(saved_ideas)} ideas")

    def run_continuous(self):
        """  (24/7)"""
        print("[CONTINUOUS] 24/7    ")
        print("    ")
        print("Ctrl+C \n")

        last_hour = -1

        while True:
            try:
                now = get_kst_now()
                current_hour = now.hour
                current_minute = now.minute

                #   
                if current_minute == 0 and current_hour != last_hour:
                    results = self.run_hourly_discovery()

                    #  
                    if results['saved'] > 0:
                        self.generate_discovery_meeting(results)

                    last_hour = current_hour

                    #   
                    print(f"\n[NEXT]  : {(now + timedelta(hours=1)).strftime('%H:00')}")
                    print("="*80 + "\n")

                    time.sleep(60)  # 1 
                else:
                    # 30 
                    time.sleep(30)

            except KeyboardInterrupt:
                print("\n\n[STOP]  ")
                logging.info("System stopped by user")
                break
            except Exception as e:
                print(f"\n[ERROR]  : {e}")
                logging.error(f"System error: {e}")
                time.sleep(60)

    def run_once_now(self):
        """ 1  ()"""
        print("[RUN]   \n")

        results = self.run_hourly_discovery()

        if results['saved'] > 0:
            self.generate_discovery_meeting(results)

        print("\n[DONE] !")
        return results

    def close(self):
        """ """
        self.session.close()


# 
if __name__ == "__main__":
    import sys

    discovery = ContinuousBusinessDiscovery()

    try:
        if len(sys.argv) > 1 and sys.argv[1] == '--once':
            # 1 
            discovery.run_once_now()
        else:
            #  
            discovery.run_continuous()
    finally:
        discovery.close()
