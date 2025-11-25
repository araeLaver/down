"""
  
-   
-   
-  
-  ROI 
"""

from datetime import datetime, timedelta
import json

class RevenueValidator:
    def __init__(self):
        # IT   
        self.standard_costs = {
            'domain': 15000,  # 
            'hosting': {
                'shared': 10000,  # 
                'vps': 30000,
                'cloud_small': 50000,
                'cloud_medium': 150000,
                'cloud_large': 500000
            },
            'ssl': 0,  # Let's Encrypt 
            'email': 5000,  #  (G Suite)
            'tools': {
                'design': 20000,  # Figma, Canva 
                'development': 30000,  #   
                'marketing': 50000,  #  
                'analytics': 10000,  # GA, Mixpanel 
                'crm': 30000  #  
            },
            'marketing': {
                'google_ads_cpc': 800,  # 
                'facebook_ads_cpm': 5000,  # 1000
                'seo': 500000,  #  ()
                'content_marketing': 300000  # 
            },
            'outsourcing': {
                'designer': 50000,  # 
                'developer': 80000,  # 
                'marketer': 40000,  # 
                'writer': 30000  # 
            }
        }

    def calculate_startup_costs(self, business_type, scale='small'):
        """   """
        costs = {
            'development': 0,
            'infrastructure': 0,
            'marketing': 0,
            'operations': 0,
            'total': 0
        }

        if business_type == 'saas':
            if scale == 'small':
                costs['development'] = 2000000  #    
                costs['infrastructure'] = 100000  #   
                costs['marketing'] = 500000  #  
                costs['operations'] = 200000  # 
            elif scale == 'medium':
                costs['development'] = 5000000  #  
                costs['infrastructure'] = 300000
                costs['marketing'] = 1500000
                costs['operations'] = 500000
            else:  # large
                costs['development'] = 15000000  #  
                costs['infrastructure'] = 1000000
                costs['marketing'] = 5000000
                costs['operations'] = 2000000

        elif business_type == 'agency':
            if scale == 'small':
                costs['development'] = 500000  #  + 
                costs['infrastructure'] = 50000
                costs['marketing'] = 1000000  #  
                costs['operations'] = 300000
            elif scale == 'medium':
                costs['development'] = 2000000
                costs['infrastructure'] = 200000
                costs['marketing'] = 3000000
                costs['operations'] = 1000000

        elif business_type == 'marketplace':
            if scale == 'small':
                costs['development'] = 3000000
                costs['infrastructure'] = 200000
                costs['marketing'] = 2000000  #  
                costs['operations'] = 500000
            elif scale == 'medium':
                costs['development'] = 10000000
                costs['infrastructure'] = 1000000
                costs['marketing'] = 10000000
                costs['operations'] = 2000000

        elif business_type == 'tool':
            if scale == 'small':
                costs['development'] = 1000000  #  
                costs['infrastructure'] = 50000
                costs['marketing'] = 300000
                costs['operations'] = 100000

        costs['total'] = sum(costs.values())
        return costs

    def calculate_monthly_costs(self, business_type, scale='small', customer_count=0):
        """   """
        costs = {
            'hosting': 0,
            'tools': 0,
            'marketing': 0,
            'support': 0,
            'payment_fees': 0,
            'total': 0
        }

        #  (   )
        if customer_count < 100:
            costs['hosting'] = self.standard_costs['hosting']['cloud_small']
        elif customer_count < 1000:
            costs['hosting'] = self.standard_costs['hosting']['cloud_medium']
        else:
            costs['hosting'] = self.standard_costs['hosting']['cloud_large']

        # SaaS 
        if scale == 'small':
            costs['tools'] = 50000
        elif scale == 'medium':
            costs['tools'] = 150000
        else:
            costs['tools'] = 500000

        # 
        if business_type == 'saas':
            costs['marketing'] = 500000 if scale == 'small' else 2000000
        elif business_type == 'agency':
            costs['marketing'] = 300000 if scale == 'small' else 1000000

        #  
        costs['support'] = customer_count * 1000  #   1000

        costs['total'] = sum(costs.values())
        return costs

    def simulate_revenue(self, business_model, pricing, target_market_size):
        """  (//)"""
        scenarios = {
            'conservative': {},
            'realistic': {},
            'optimistic': {}
        }

        #  
        conversion_rates = {
            'conservative': 0.01,  # 1%
            'realistic': 0.03,     # 3%
            'optimistic': 0.05     # 5%
        }

        for scenario, conversion_rate in conversion_rates.items():
            monthly_customers = int(target_market_size * conversion_rate)

            if business_model == 'subscription':
                monthly_revenue = monthly_customers * pricing['monthly']
                annual_revenue = monthly_revenue * 12

            elif business_model == 'one_time':
                #    
                monthly_revenue = monthly_customers * pricing['one_time']
                annual_revenue = monthly_revenue * 12

            elif business_model == 'commission':
                #  
                avg_transaction = pricing['avg_transaction']
                commission_rate = pricing['commission_rate']
                transactions_per_customer = pricing.get('transactions_per_month', 5)

                monthly_revenue = monthly_customers * transactions_per_customer * avg_transaction * commission_rate
                annual_revenue = monthly_revenue * 12

            scenarios[scenario] = {
                'monthly_customers': monthly_customers,
                'monthly_revenue': int(monthly_revenue),
                'annual_revenue': int(annual_revenue),
                'customer_ltv': int(annual_revenue / monthly_customers) if monthly_customers > 0 else 0
            }

        return scenarios

    def calculate_break_even(self, startup_costs, monthly_costs, monthly_revenue):
        """ """
        if monthly_revenue <= monthly_costs:
            return {
                'break_even_possible': False,
                'message': '    .     '
            }

        monthly_profit = monthly_revenue - monthly_costs
        months_to_break_even = startup_costs / monthly_profit

        return {
            'break_even_possible': True,
            'months': round(months_to_break_even, 1),
            'date': (datetime.now() + timedelta(days=30 * months_to_break_even)).strftime('%Y-%m-%d'),
            'monthly_profit': int(monthly_profit),
            'annual_profit': int(monthly_profit * 12)
        }

    def calculate_roi(self, startup_costs, annual_revenue, annual_costs):
        """ROI """
        annual_profit = annual_revenue - annual_costs
        roi_percentage = (annual_profit / startup_costs) * 100

        return {
            'annual_profit': int(annual_profit),
            'roi_percentage': round(roi_percentage, 2),
            'payback_period_years': round(startup_costs / annual_profit, 2) if annual_profit > 0 else None,
            'rating': self._rate_roi(roi_percentage)
        }

    def _rate_roi(self, roi_percentage):
        """ROI """
        if roi_percentage >= 200:
            return ' '
        elif roi_percentage >= 100:
            return ''
        elif roi_percentage >= 50:
            return ''
        elif roi_percentage >= 20:
            return ''
        else:
            return ''

    def comprehensive_validation(self, business_config):
        """  """
        print(f"\n{'='*60}")
        print(f" : {business_config['name']}")
        print(f"{'='*60}\n")

        # 1.  
        startup_costs_detail = self.calculate_startup_costs(
            business_config['type'],
            business_config.get('scale', 'small')
        )
        startup_costs = startup_costs_detail['total']

        print(f"1.   ")
        for key, value in startup_costs_detail.items():
            if key != 'total':
                print(f"   {key}: {value:,}")
        print(f"    : {startup_costs:,}\n")

        # 2.   ()
        scenarios_costs = {}
        scenarios_revenue = self.simulate_revenue(
            business_config['revenue_model'],
            business_config['pricing'],
            business_config['target_market_size']
        )

        print(f"2.  \n")

        results = {}

        for scenario_name, scenario_data in scenarios_revenue.items():
            monthly_customers = scenario_data['monthly_customers']

            monthly_costs_detail = self.calculate_monthly_costs(
                business_config['type'],
                business_config.get('scale', 'small'),
                monthly_customers
            )
            monthly_costs = monthly_costs_detail['total']

            # 
            break_even = self.calculate_break_even(
                startup_costs,
                monthly_costs,
                scenario_data['monthly_revenue']
            )

            # ROI
            annual_costs = monthly_costs * 12
            roi = self.calculate_roi(
                startup_costs,
                scenario_data['annual_revenue'],
                annual_costs
            )

            results[scenario_name] = {
                'customers': monthly_customers,
                'monthly_revenue': scenario_data['monthly_revenue'],
                'monthly_costs': monthly_costs,
                'monthly_profit': scenario_data['monthly_revenue'] - monthly_costs,
                'annual_revenue': scenario_data['annual_revenue'],
                'annual_costs': annual_costs,
                'break_even': break_even,
                'roi': roi
            }

            # 
            print(f"   [{scenario_name.upper()}]")
            print(f"    : {monthly_customers}")
            print(f"    : {scenario_data['monthly_revenue']:,}")
            print(f"    : {monthly_costs:,}")
            print(f"    : {scenario_data['monthly_revenue'] - monthly_costs:,}")

            if break_even['break_even_possible']:
                print(f"   : {break_even['months']}")
            else:
                print(f"   :  ({break_even['message']})")

            print(f"    ROI: {roi['roi_percentage']}% ({roi['rating']})")
            print()

        # 3.  
        realistic = results['realistic']
        verdict = self._generate_verdict(realistic)

        print(f"3.  ")
        print(f"   : {verdict['verdict']}")
        print(f"   : {verdict['confidence']}")
        print(f"   : {verdict['recommendation']}")
        print(f"\n{'='*60}\n")

        return {
            'business_name': business_config['name'],
            'startup_costs': startup_costs_detail,
            'scenarios': results,
            'verdict': verdict,
            'analysis_date': datetime.now().isoformat()
        }

    def _generate_verdict(self, realistic_scenario):
        """ """
        roi = realistic_scenario['roi']['roi_percentage']
        break_even_months = realistic_scenario['break_even'].get('months', 999)
        monthly_profit = realistic_scenario['monthly_profit']

        if roi >= 100 and break_even_months <= 12 and monthly_profit > 1000000:
            return {
                'verdict': ' ',
                'confidence': '',
                'recommendation': '  ',
                'score': 90
            }
        elif roi >= 50 and break_even_months <= 18 and monthly_profit > 500000:
            return {
                'verdict': '',
                'confidence': '',
                'recommendation': '   ',
                'score': 70
            }
        elif roi >= 20 and break_even_months <= 24:
            return {
                'verdict': '',
                'confidence': '',
                'recommendation': '  ',
                'score': 50
            }
        else:
            return {
                'verdict': '',
                'confidence': ' ',
                'recommendation': '   ',
                'score': 30
            }

    def save_validation(self, results, filename='revenue_validation.json'):
        """  """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"   : {filename}")


#  
if __name__ == "__main__":
    validator = RevenueValidator()

    #  1: SaaS   
    saas_config = {
        'name': 'AI   ',
        'type': 'saas',
        'scale': 'small',
        'revenue_model': 'subscription',
        'pricing': {
            'monthly': 29000  #  
        },
        'target_market_size': 10000  #    ( )
    }

    result1 = validator.comprehensive_validation(saas_config)

    #  2:   
    agency_config = {
        'name': '  ',
        'type': 'agency',
        'scale': 'small',
        'revenue_model': 'one_time',
        'pricing': {
            'one_time': 3000000  #  
        },
        'target_market_size': 100  #  
    }

    result2 = validator.comprehensive_validation(agency_config)

    #  3:  
    marketplace_config = {
        'name': ' ',
        'type': 'marketplace',
        'scale': 'small',
        'revenue_model': 'commission',
        'pricing': {
            'avg_transaction': 500000,  #  
            'commission_rate': 0.15,    # 15% 
            'transactions_per_month': 3  #    
        },
        'target_market_size': 5000  #  
    }

    result3 = validator.comprehensive_validation(marketplace_config)

    #   
    print("\n" + "="*60)
    print("[COMPARISON]  ")
    print("="*60 + "\n")

    all_results = [
        ('SaaS', result1),
        ('Agency', result2),
        ('Marketplace', result3)
    ]

    for name, result in all_results:
        realistic = result['scenarios']['realistic']
        print(f"{name}:")
        print(f"   : {result['startup_costs']['total']:,}")
        print(f"   : {realistic['monthly_profit']:,}")
        print(f"   ROI: {realistic['roi']['roi_percentage']}%")
        print(f"  : {realistic['break_even'].get('months', 'N/A')}")
        print(f"  : {result['verdict']['verdict']}")
        print()
