"""
    
- 4    
-    
-  
-   
"""

from datetime import datetime, timedelta
import json

class ActionPlanGenerator:
    def __init__(self):
        self.tech_stacks = {
            'nocode': {
                'tools': ['Bubble.io', 'Webflow', 'Airtable', 'Zapier'],
                'cost': 100000,  # 
                'development_time': '1-2',
                'skill_required': '',
                'suitable_for': ['MVP', ' ', '']
            },
            'lowcode': {
                'tools': ['Next.js + Supabase', 'Firebase', 'Vercel'],
                'cost': 50000,  # 
                'development_time': '2-4',
                'skill_required': '',
                'suitable_for': ['', ' SaaS', ' ']
            },
            'fullstack': {
                'tools': ['React + Node.js + PostgreSQL', 'AWS/Azure'],
                'cost': 200000,  # 
                'development_time': '2-3',
                'skill_required': '',
                'suitable_for': [' ', ' SaaS', '']
            }
        }

    def recommend_tech_stack(self, business_type, budget, timeline_weeks):
        """  """
        if budget < 1000000 or timeline_weeks <= 2:
            return self.tech_stacks['nocode']
        elif budget < 5000000 or timeline_weeks <= 8:
            return self.tech_stacks['lowcode']
        else:
            return self.tech_stacks['fullstack']

    def generate_week1_plan(self, business_config):
        """1: MVP  """
        tech_stack = business_config.get('tech_stack', {})

        tasks = [
            {
                'day': '1',
                'title': '    ',
                'tasks': [
                    '   ( 10)',
                    '  vs   ',
                    'MVP   (1-3  )',
                    '  (5 )'
                ],
                'deliverable': 'MVP  (1)',
                'time_required': '4-6'
            },
            {
                'day': '2',
                'title': ' ',
                'tasks': [
                    '   ',
                    'Webflow/Notion  ',
                    '   ( + )',
                    'CTA      ',
                    'Google Analytics '
                ],
                'deliverable': '  URL',
                'tools': ['Webflow ( )', 'Google Analytics'],
                'time_required': '6-8'
            },
            {
                'day': '3',
                'title': '  ',
                'tasks': [
                    f"{tech_stack.get('tools', ['Bubble.io'])[0]}  UI ",
                    ' / ',
                    '  1  (80% )',
                    '  '
                ],
                'deliverable': '  ',
                'time_required': '8-10'
            },
            {
                'day': '4',
                'title': '  ',
                'tasks': [
                    'Stripe/Toss Payments  ',
                    '  ',
                    '  ',
                    '    '
                ],
                'deliverable': '  ',
                'tools': ['Stripe', 'Gmail SMTP'],
                'time_required': '4-6'
            },
            {
                'day': '5',
                'title': '  ',
                'tasks': [
                    '/   (10-20 )',
                    '/  ',
                    '  50%   ',
                    '   '
                ],
                'deliverable': '  10 ',
                'budget': '0 (  )',
                'time_required': '2-3'
            }
        ]

        return {
            'week': 1,
            'goal': 'MVP     ',
            'tasks': tasks,
            'total_time': '24-33',
            'budget': 100000,
            'success_criteria': [' MVP', '  10', '  ']
        }

    def generate_week2_plan(self, business_config):
        """2:  """
        tasks = [
            {
                'day': '6-7',
                'title': '  ',
                'tasks': [
                    '   ',
                    '   (/)',
                    '  3 ',
                    '  1  ',
                    '  '
                ],
                'deliverable': '  ',
                'budget': 100000,
                'kpis': ['CPC < 500', 'CTR > 1%', ' > 2%']
            },
            {
                'day': '8-9',
                'title': ' ',
                'tasks': [
                    '  5 1:1  ( 30)',
                    '  ',
                    '   (  )',
                    '  '
                ],
                'deliverable': '   ',
                'questions': [
                    '   ?',
                    '    ?',
                    '   ?',
                    '  ?',
                    ' ?'
                ]
            },
            {
                'day': '10-11',
                'title': ' ',
                'tasks': [
                    '   ',
                    'Critical  ',
                    'UI/UX  ( 3)',
                    '  1  (  )'
                ],
                'deliverable': '  2.0',
                'time_required': '16-20'
            },
            {
                'day': '12',
                'title': '   ',
                'tasks': [
                    '    ',
                    '  50% ',
                    '  ',
                    '   '
                ],
                'deliverable': '   ',
                'target': ' 1,  3-5'
            }
        ]

        return {
            'week': 2,
            'goal': '    ',
            'tasks': tasks,
            'budget': 150000,
            'success_criteria': ['   ', ' 2% ', '  7/10 ']
        }

    def generate_week3_plan(self, business_config):
        """3:  """
        tasks = [
            {
                'day': '13-15',
                'title': '  ',
                'tasks': [
                    '  3  (SEO )',
                    '    (3 )',
                    '/  5',
                    '  (Reddit, ) '
                ],
                'deliverable': '  ',
                'budget': 50000
            },
            {
                'day': '16-17',
                'title': '  ',
                'tasks': [
                    '   (Mailchimp)',
                    '    ',
                    '    ',
                    '    '
                ],
                'deliverable': '  ',
                'tools': ['Mailchimp ( 2000)', 'Zapier']
            },
            {
                'day': '18-19',
                'title': ' ',
                'tasks': [
                    '   (/  )',
                    '    ',
                    '   ',
                    '   ( )'
                ],
                'deliverable': '  ',
                'expected_effect': '   50% '
            }
        ]

        return {
            'week': 3,
            'goal': '  ',
            'tasks': tasks,
            'budget': 100000,
            'success_criteria': ['   20', '  10%', 'CAC 30% ']
        }

    def generate_week4_plan(self, business_config):
        """4: """
        tasks = [
            {
                'day': '20-22',
                'title': ' ',
                'tasks': [
                    'A/B :   10',
                    '   (5 )',
                    '    ',
                    '  '
                ],
                'deliverable': 'CAC 30% ',
                'budget': 300000
            },
            {
                'day': '23-24',
                'title': '  ',
                'tasks': [
                    '  3 ',
                    '    (Before/After)',
                    '  ',
                    '   '
                ],
                'deliverable': '  ',
                'expected_effect': ' 20% '
            },
            {
                'day': '25-26',
                'title': '   ',
                'tasks': [
                    'Google Analytics  ',
                    '   ',
                    '  ',
                    ' KPI  '
                ],
                'deliverable': '   '
            }
        ]

        return {
            'week': 4,
            'goal': '  ',
            'tasks': tasks,
            'budget': 400000,
            'success_criteria': ['   50', '  300', 'LTV/CAC > 3']
        }

    def generate_comprehensive_plan(self, business_config):
        """4   """
        print(f"\n{'='*80}")
        print(f"[PLAN] 4  : {business_config['name']}")
        print(f"{'='*80}\n")

        #   
        tech_stack = self.recommend_tech_stack(
            business_config['type'],
            business_config.get('budget', 3000000),
            business_config.get('timeline_weeks', 4)
        )
        business_config['tech_stack'] = tech_stack

        print(f"[TECH]   : {tech_stack['tools'][0]}")
        print(f"    : {tech_stack['development_time']}")
        print(f"    : {tech_stack['skill_required']}")
        print(f"    : {tech_stack['cost']:,}\n")

        #  
        week1 = self.generate_week1_plan(business_config)
        week2 = self.generate_week2_plan(business_config)
        week3 = self.generate_week3_plan(business_config)
        week4 = self.generate_week4_plan(business_config)

        weeks = [week1, week2, week3, week4]

        for week_plan in weeks:
            print(f"\n{'='*80}")
            print(f"[WEEK {week_plan['week']}] {week_plan['goal']}")
            print(f"{'='*80}\n")

            for task_group in week_plan['tasks']:
                print(f"> {task_group['day']}: {task_group['title']}")

                for task in task_group['tasks']:
                    print(f"  [ ] {task}")

                print(f"\n  [OUTPUT] : {task_group['deliverable']}")

                if 'budget' in task_group:
                    print(f"  [BUDGET] : {task_group['budget']:,}")

                if 'time_required' in task_group:
                    print(f"  [TIME]  : {task_group['time_required']}")

                if 'tools' in task_group:
                    print(f"  [TOOLS] : {', '.join(task_group['tools'])}")

                print()

            print(f"[SUCCESS]  : {', '.join(week_plan['success_criteria'])}")
            print(f"[BUDGET]  : {week_plan['budget']:,}\n")

        #  
        total_budget = sum(w['budget'] for w in weeks)

        print(f"\n{'='*80}")
        print(f"[SUMMARY]  ")
        print(f"{'='*80}\n")
        print(f" : 4")
        print(f" : {total_budget:,}")
        print(f" : {tech_stack['tools'][0]}")
        print(f"\n :")
        print(f"  • 1: MVP  +   10")
        print(f"  • 2:    ")
        print(f"  • 3:   ")
        print(f"  • 4:  50  ")
        print(f"\n :")
        print(f"  •  : 80-150")
        print(f"  •  : 300-800")
        print(f"  • : 2-3")

        return {
            'business_name': business_config['name'],
            'tech_stack': tech_stack,
            'weeks': weeks,
            'total_budget': total_budget,
            'generated_at': datetime.now().isoformat()
        }

    def generate_checklist(self, plan):
        """ """
        checklist = []

        for week in plan['weeks']:
            for task_group in week['tasks']:
                for task in task_group['tasks']:
                    checklist.append({
                        'week': week['week'],
                        'day': task_group['day'],
                        'task': task,
                        'completed': False,
                        'notes': ''
                    })

        return checklist

    def save_plan(self, plan, filename='action_plan.json'):
        """  """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        print(f"\n[OK]   : {filename}")


#  
if __name__ == "__main__":
    generator = ActionPlanGenerator()

    # IT  
    business_configs = [
        {
            'name': 'AI   ',
            'type': 'saas',
            'budget': 2000000,
            'timeline_weeks': 4
        },
        {
            'name': '  ',
            'type': 'marketplace',
            'budget': 5000000,
            'timeline_weeks': 8
        },
        {
            'name': 'SEO  ',
            'type': 'agency',
            'budget': 1000000,
            'timeline_weeks': 2
        }
    ]

    for config in business_configs:
        plan = generator.generate_comprehensive_plan(config)
        generator.save_plan(plan, f"plan_{config['name'].replace(' ', '_')}.json")

        #  
        checklist = generator.generate_checklist(plan)
        print(f"\n {len(checklist)}   ")
        print("-" * 80)
