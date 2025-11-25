"""
 IT   
-    +   +    
- 80        
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from real_market_analyzer import RealMarketAnalyzer
from revenue_validator import RevenueValidator
from action_plan_generator import ActionPlanGenerator
from realistic_business_generator import RealisticBusinessGenerator

import json
from datetime import datetime
import time

class SmartBusinessSystem:
    def __init__(self):
        self.market_analyzer = RealMarketAnalyzer()
        self.revenue_validator = RevenueValidator()
        self.action_planner = ActionPlanGenerator()
        self.idea_generator = RealisticBusinessGenerator()

        # Windows     
        print("="*80)
        print("[SMART]  IT   ")
        print("="*80)
        print("   ->   ->    \n")

    def analyze_business_idea(self, business_idea, keyword, business_config):
        """    """
        print(f"\n{'='*80}")
        print(f"[ANALYSIS]   : {business_idea}")
        print(f"{'='*80}\n")

        # 1:  
        print("[1]    ...")
        market_data = self.market_analyzer.comprehensive_analysis(business_idea, keyword)
        market_score = market_data['market_score']

        print(f"    : {market_score}/100")

        #    
        if market_score < 60:
            print(f"   [X]    (60 ).   .\n")
            return {
                'business_idea': business_idea,
                'passed': False,
                'reason': '  ',
                'market_score': market_score
            }

        # 2:  
        print("\n[2]   ...")
        revenue_data = self.revenue_validator.comprehensive_validation(business_config)
        realistic_scenario = revenue_data['scenarios']['realistic']
        verdict_score = revenue_data['verdict']['score']

        print(f"    : {verdict_score}/100")
        print(f"     : {realistic_scenario['monthly_profit']:,}")

        #    
        if verdict_score < 60:
            print(f"   [X]  .   .\n")
            return {
                'business_idea': business_idea,
                'passed': False,
                'reason': ' ',
                'market_score': market_score,
                'revenue_score': verdict_score
            }

        #   
        total_score = (market_score * 0.6) + (verdict_score * 0.4)

        print(f"\n   [SCORE]  : {int(total_score)}/100")

        # 70    
        if total_score >= 70:
            print(f"   [OK]  !    ...\n")

            # 3:    
            print("[3] 4    ...")
            action_plan = None
            try:
                action_plan = self.action_planner.generate_comprehensive_plan(business_config)
                print(f"\n   [OK]   !")
            except Exception as e:
                print(f"\n   [WARN]    : {e}")
                print(f"   [INFO]    .")

            return {
                'business_idea': business_idea,
                'passed': True,
                'total_score': total_score,
                'market_data': market_data,
                'revenue_data': revenue_data,
                'action_plan': action_plan,
                'recommendation': 'IMMEDIATE_ACTION'
            }

        else:
            print(f"   [WARN]  .   .\n")
            return {
                'business_idea': business_idea,
                'passed': True,
                'total_score': total_score,
                'market_data': market_data,
                'revenue_data': revenue_data,
                'recommendation': 'FURTHER_VALIDATION'
            }

    def batch_analyze_ideas(self, ideas_list):
        """   """
        print(f"\n{'='*80}")
        print(f"[BATCH] {len(ideas_list)}    ")
        print(f"{'='*80}\n")

        results = []

        for i, idea_data in enumerate(ideas_list, 1):
            print(f"\n[{i}/{len(ideas_list)}]  ...")

            result = self.analyze_business_idea(
                idea_data['business_idea'],
                idea_data['keyword'],
                idea_data['config']
            )

            results.append(result)

            # API  
            if i < len(ideas_list):
                print("\n[WAIT] 5  ...")
                time.sleep(5)

        #  
        passed = [r for r in results if r['passed'] and r.get('total_score', 0) >= 70]
        further_validation = [r for r in results if r['passed'] and 60 <= r.get('total_score', 0) < 70]
        rejected = [r for r in results if not r['passed'] or r.get('total_score', 0) < 60]

        #  
        self._print_final_report(passed, further_validation, rejected)

        return {
            'total_analyzed': len(ideas_list),
            'immediate_action': passed,
            'further_validation': further_validation,
            'rejected': rejected,
            'analysis_date': datetime.now().isoformat()
        }

    def _print_final_report(self, passed, further_validation, rejected):
        """  """
        print(f"\n\n{'='*80}")
        print(f"[REPORT]   ")
        print(f"{'='*80}\n")

        print(f" : {len(passed) + len(further_validation) + len(rejected)}")
        print(f"[OK]   : {len(passed)} (80 )")
        print(f"[WARN]   : {len(further_validation)} (60-80)")
        print(f"[X] : {len(rejected)} (60 )\n")

        if passed:
            print(f"{'='*80}")
            print(f"[TOP]     (TOP {len(passed)})")
            print(f"{'='*80}\n")

            #   
            passed.sort(key=lambda x: x.get('total_score', 0), reverse=True)

            for i, idea in enumerate(passed, 1):
                print(f"{i}. {idea['business_idea']}")
                print(f"    : {int(idea['total_score'])}/100")

                #  
                kmong = idea['market_data']['data_sources'].get('kmong', {})
                if not kmong.get('error'):
                    print(f"     : {kmong.get('avg_price', 0):,}")
                    print(f"    : {kmong.get('competition_level', 'N/A')}")

                #  
                realistic = idea['revenue_data']['scenarios']['realistic']
                print(f"     : {realistic['monthly_profit']:,}")
                print(f"   : {realistic['break_even'].get('months', 'N/A')}")
                print(f"    ROI: {realistic['roi']['roi_percentage']}%")

                #  
                if 'action_plan' in idea:
                    plan = idea['action_plan']
                    print(f"   4  : [OK]  ")
                    print(f"    : {plan['total_budget']:,}")

                print()

        if further_validation:
            print(f"\n{'='*80}")
            print(f"[WARN]    ({len(further_validation)})")
            print(f"{'='*80}\n")

            for idea in further_validation:
                print(f"• {idea['business_idea']} (: {int(idea['total_score'])})")

        print(f"\n{'='*80}\n")

    def generate_it_business_ideas(self):
        """IT    """
        # realistic_business_generator IT  
        all_opportunities = self.idea_generator.generate_monthly_opportunities()

        # IT/  
        it_opportunities = [
            opp for opp in all_opportunities
            if opp['type'] in ['  ', ' ', '  ']
               or '' in opp['business'].get('name', '')
               or '' in opp['business'].get('name', '')
               or 'AI' in opp['business'].get('name', '')
               or 'IT' in opp['business'].get('name', '')
        ]

        return it_opportunities[:10]  #  10

    def save_results(self, results, filename='business_analysis_results.json'):
        """  """
        # action_plan     
        summary = {
            'total_analyzed': results['total_analyzed'],
            'immediate_action_count': len(results['immediate_action']),
            'further_validation_count': len(results['further_validation']),
            'rejected_count': len(results['rejected']),
            'analysis_date': results['analysis_date'],
            'immediate_action_ideas': [
                {
                    'business_idea': r['business_idea'],
                    'total_score': r.get('total_score', 0),
                    'market_score': r['market_data']['market_score'],
                    'revenue_score': r['revenue_data']['verdict']['score'],
                    'monthly_profit': r['revenue_data']['scenarios']['realistic']['monthly_profit'],
                    'action_plan_generated': 'action_plan' in r
                }
                for r in results['immediate_action']
            ]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print(f"[OK]   : {filename}")


#  
if __name__ == "__main__":
    system = SmartBusinessSystem()

    #  IT   
    ideas_to_analyze = [
        {
            'business_idea': 'AI   ',
            'keyword': ' ',
            'config': {
                'name': 'AI   ',
                'type': 'saas',
                'scale': 'small',
                'revenue_model': 'one_time',
                'pricing': {'one_time': 29000},
                'target_market_size': 5000,
                'budget': 2000000,
                'timeline_weeks': 4
            }
        },
        {
            'business_idea': 'SEO ',
            'keyword': 'SEO ',
            'config': {
                'name': 'SEO  ',
                'type': 'agency',
                'scale': 'small',
                'revenue_model': 'subscription',
                'pricing': {'monthly': 500000},
                'target_market_size': 200,
                'budget': 1000000,
                'timeline_weeks': 2
            }
        },
        {
            'business_idea': '  ',
            'keyword': ' ',
            'config': {
                'name': '  ',
                'type': 'agency',
                'scale': 'small',
                'revenue_model': 'one_time',
                'pricing': {'one_time': 3000000},
                'target_market_size': 100,
                'budget': 1500000,
                'timeline_weeks': 4
            }
        }
    ]

    #   
    results = system.batch_analyze_ideas(ideas_to_analyze)

    #  
    system.save_results(results)

    #        
    if results['immediate_action']:
        print(f"\n{'='*80}")
        print("[RECOMMEND] : 1   !")
        print(f"{'='*80}\n")

        top_idea = results['immediate_action'][0]
        print(f"[#1] {top_idea['business_idea']}")
        print(f"   : {int(top_idea['total_score'])}/100")
        print(f"     : {top_idea['revenue_data']['scenarios']['realistic']['monthly_profit']:,}")

        if 'action_plan' in top_idea:
            plan_file = f"plan_{top_idea['business_idea'].replace(' ', '_')}.json"
            system.action_planner.save_plan(top_idea['action_plan'], plan_file)
            print(f"   [PLAN]  : {plan_file}")

    print("\n" + "="*80)
    print("[COMPLETE]   !")
    print("="*80 + "\n")
