"""
   
-      
-    
-     
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
from urllib.parse import quote

class RealMarketAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def analyze_kmong_market(self, keyword):
        """    """
        try:
            url = f"https://kmong.com/search?keyword={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            #   
            services = soup.find_all('div', class_='service-card')

            prices = []
            reviews = []
            for service in services[:20]:  #  20
                try:
                    price_elem = service.find('span', class_='price')
                    if price_elem:
                        price_text = price_elem.text.replace(',', '').replace('', '')
                        prices.append(int(price_text))

                    review_elem = service.find('span', class_='review-count')
                    if review_elem:
                        review_count = int(review_elem.text.replace('(', '').replace(')', ''))
                        reviews.append(review_count)
                except:
                    continue

            return {
                'platform': '',
                'service_count': len(services),
                'avg_price': sum(prices) // len(prices) if prices else 0,
                'min_price': min(prices) if prices else 0,
                'max_price': max(prices) if prices else 0,
                'avg_reviews': sum(reviews) // len(reviews) if reviews else 0,
                'competition_level': self._calculate_competition(len(services)),
                'market_saturation': self._calculate_saturation(len(services), sum(reviews))
            }
        except Exception as e:
            print(f"  : {e}")
            return {'platform': '', 'error': str(e)}

    def analyze_naver_search_volume(self, keyword):
        """  """
        try:
            url = f"https://search.naver.com/search.naver?query={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)

            #    
            autocomplete_url = f"https://ac.search.naver.com/nx/ac?q={quote(keyword)}&con=0&frm=nv&ans=2&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&run=2&rev=4&q_enc=UTF-8&st=100&r_lt=10000"
            ac_response = requests.get(autocomplete_url, timeout=10)

            if ac_response.status_code == 200:
                data = ac_response.json()
                suggestions = data.get('items', [[]])[0]

                return {
                    'keyword': keyword,
                    'related_searches': len(suggestions),
                    'popularity_score': min(len(suggestions) * 10, 100),
                    'suggestions': suggestions[:5]
                }
        except Exception as e:
            print(f"   : {e}")
            return {'keyword': keyword, 'error': str(e)}

    def analyze_competitors_google(self, keyword):
        """   """
        try:
            url = f"https://www.google.com/search?q={quote(keyword + ' ')}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            #    
            results = soup.find_all('div', class_='g')

            #   
            ads = soup.find_all('div', {'data-text-ad': True})

            return {
                'organic_results': len(results),
                'paid_ads': len(ads),
                'has_competition': len(results) > 0,
                'ad_competition': 'high' if len(ads) > 5 else 'medium' if len(ads) > 0 else 'low',
                'entry_difficulty': 'hard' if len(ads) > 5 and len(results) > 50 else 'medium' if len(results) > 20 else 'easy'
            }
        except Exception as e:
            print(f"   : {e}")
            return {'error': str(e)}

    def analyze_youtube_interest(self, keyword):
        """  """
        try:
            url = f"https://www.youtube.com/results?search_query={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)

            #    (  )
            content_length = len(response.content)

            return {
                'interest_indicator': 'high' if content_length > 500000 else 'medium' if content_length > 300000 else 'low',
                'estimated_videos': content_length // 10000  #  
            }
        except Exception as e:
            print(f"   : {e}")
            return {'error': str(e)}

    def analyze_wishket_market(self, keyword):
        """   """
        try:
            url = f"https://www.wishket.com/project/?q={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            #   
            projects = soup.find_all('div', class_='project-card') or soup.find_all('div', class_='item')

            #   
            budgets = []
            for project in projects[:10]:
                try:
                    budget_elem = project.find('span', class_='budget') or project.find('div', class_='price')
                    if budget_elem:
                        budget_text = budget_elem.text.replace(',', '').replace('', '0000').replace('', '')
                        budgets.append(int(budget_text))
                except:
                    continue

            return {
                'platform': '',
                'project_count': len(projects),
                'avg_budget': sum(budgets) // len(budgets) if budgets else 0,
                'demand_level': 'high' if len(projects) > 20 else 'medium' if len(projects) > 5 else 'low',
                'market_active': len(projects) > 0
            }
        except Exception as e:
            print(f"  : {e}")
            return {'platform': '', 'error': str(e)}

    def analyze_soomgo_market(self, keyword):
        """   """
        try:
            url = f"https://soomgo.com/search/pro?keyword={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            #  
            pros = soup.find_all('div', class_='pro-card') or soup.find_all('a', class_='pro-item')

            #   
            reviews = []
            for pro in pros[:20]:
                try:
                    review_elem = pro.find('span', class_='review-count')
                    if review_elem:
                        review_count = int(review_elem.text.replace('', '').replace(',', '').strip())
                        reviews.append(review_count)
                except:
                    continue

            return {
                'platform': '',
                'expert_count': len(pros),
                'avg_reviews': sum(reviews) // len(reviews) if reviews else 0,
                'competition': 'high' if len(pros) > 50 else 'medium' if len(pros) > 10 else 'low',
                'market_maturity': 'mature' if sum(reviews) > 500 else 'growing'
            }
        except Exception as e:
            print(f"  : {e}")
            return {'platform': '', 'error': str(e)}

    def analyze_brokerage_platforms(self, keyword):
        """    (,  )"""
        try:
            #  ( )
            taling_url = f"https://taling.me/search?keyword={quote(keyword)}"
            response = requests.get(taling_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            classes = soup.find_all('div', class_='class-card') or soup.find_all('a', class_='talent-item')

            return {
                'platform': '',
                'class_count': len(classes),
                'market_presence': len(classes) > 0,
                'category': '/'
            }
        except Exception as e:
            print(f"   : {e}")
            return {'platform': '', 'error': str(e)}

    def analyze_coupang_marketplace(self, keyword):
        """  """
        try:
            url = f"https://www.coupang.com/np/search?q={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            #  
            products = soup.find_all('li', class_='search-product') or soup.find_all('a', class_='search-product-link')

            #  
            prices = []
            for product in products[:20]:
                try:
                    price_elem = product.find('strong', class_='price-value')
                    if price_elem:
                        price = int(price_elem.text.replace(',', ''))
                        prices.append(price)
                except:
                    continue

            return {
                'platform': '',
                'product_count': len(products),
                'avg_price': sum(prices) // len(prices) if prices else 0,
                'e_commerce_potential': 'high' if len(products) > 100 else 'medium' if len(products) > 20 else 'low'
            }
        except Exception as e:
            print(f"  : {e}")
            return {'platform': '', 'error': str(e)}

    def analyze_blog_trend(self, keyword):
        """   """
        try:
            url = f"https://section.blog.naver.com/Search/Post.naver?keyword={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            #   
            posts = soup.find_all('div', class_='desc_inner') or soup.find_all('a', class_='post_link')

            return {
                'platform': ' ',
                'post_count': len(posts),
                'content_volume': 'high' if len(posts) > 30 else 'medium' if len(posts) > 10 else 'low',
                'trend_indicator': '' if len(posts) > 20 else ''
            }
        except Exception as e:
            print(f"   : {e}")
            return {'platform': ' ', 'error': str(e)}

    def analyze_instagram_business(self, keyword):
        """   """
        try:
            #      
            #  "keyword " 
            url = f"https://search.naver.com/search.naver?query={quote(keyword + ' ')}"
            response = requests.get(url, headers=self.headers, timeout=10)

            content_length = len(response.content)

            return {
                'platform': '',
                'social_presence': 'high' if content_length > 300000 else 'medium' if content_length > 150000 else 'low',
                'marketing_potential': 'SNS  ' if content_length > 200000 else ''
            }
        except Exception as e:
            print(f"  : {e}")
            return {'platform': '', 'error': str(e)}

    def _calculate_competition(self, service_count):
        """  """
        if service_count > 100:
            return 'very_high'
        elif service_count > 50:
            return 'high'
        elif service_count > 20:
            return 'medium'
        elif service_count > 5:
            return 'low'
        else:
            return 'very_low'

    def _calculate_saturation(self, service_count, total_reviews):
        """  """
        if service_count == 0:
            return 'unexplored'

        avg_reviews_per_service = total_reviews / service_count if service_count > 0 else 0

        if avg_reviews_per_service > 100:
            return 'saturated'
        elif avg_reviews_per_service > 50:
            return 'competitive'
        elif avg_reviews_per_service > 10:
            return 'growing'
        else:
            return 'emerging'

    def comprehensive_analysis(self, business_idea, keyword):
        """  """
        print(f"\n{'='*60}")
        print(f"  : {business_idea}")
        print(f": {keyword}")
        print(f"{'='*60}\n")

        results = {
            'business_idea': business_idea,
            'keyword': keyword,
            'analysis_date': datetime.now().isoformat(),
            'data_sources': {}
        }

        #  
        print("1.    ...")
        kmong_data = self.analyze_kmong_market(keyword)
        results['data_sources']['kmong'] = kmong_data
        time.sleep(2)  # API  

        #  
        print("2.    ...")
        naver_data = self.analyze_naver_search_volume(keyword)
        results['data_sources']['naver'] = naver_data
        time.sleep(2)

        #  
        print("3.    ...")
        google_data = self.analyze_competitors_google(keyword)
        results['data_sources']['google'] = google_data
        time.sleep(2)

        #  
        print("4.    ...")
        youtube_data = self.analyze_youtube_interest(keyword)
        results['data_sources']['youtube'] = youtube_data
        time.sleep(2)

        #   
        print("5.     ...")
        wishket_data = self.analyze_wishket_market(keyword)
        results['data_sources']['wishket'] = wishket_data
        time.sleep(2)

        #   
        print("6.     ...")
        soomgo_data = self.analyze_soomgo_market(keyword)
        results['data_sources']['soomgo'] = soomgo_data
        time.sleep(2)

        #  / 
        print("7.    ...")
        brokerage_data = self.analyze_brokerage_platforms(keyword)
        results['data_sources']['brokerage'] = brokerage_data
        time.sleep(2)

        #  
        print("8.    ...")
        coupang_data = self.analyze_coupang_marketplace(keyword)
        results['data_sources']['coupang'] = coupang_data
        time.sleep(2)

        #   
        print("9.     ...")
        blog_data = self.analyze_blog_trend(keyword)
        results['data_sources']['blog'] = blog_data
        time.sleep(2)

        #  
        print("10.     ...")
        instagram_data = self.analyze_instagram_business(keyword)
        results['data_sources']['instagram'] = instagram_data

        #   
        results['market_score'] = self._calculate_market_score(results['data_sources'])
        results['recommendation'] = self._generate_recommendation(results['market_score'])

        print(f"\n{'='*60}")
        print(f" !")
        print(f" : {results['market_score']}/100")
        print(f" : {results['recommendation']['verdict']}")
        print(f"{'='*60}\n")

        return results

    def _calculate_market_score(self, data_sources):
        """    (0-100) - 10  """
        score = 0

        #    (20)
        kmong = data_sources.get('kmong', {})
        if not kmong.get('error'):
            competition = kmong.get('competition_level', 'high')
            if competition == 'very_low':
                score += 15
            elif competition == 'low':
                score += 12
            elif competition == 'medium':
                score += 10
            elif competition == 'high':
                score += 5

            avg_price = kmong.get('avg_price', 0)
            if avg_price > 100000:
                score += 5
            elif avg_price > 50000:
                score += 3
            elif avg_price > 20000:
                score += 2

        #   (15)
        naver = data_sources.get('naver', {})
        if not naver.get('error'):
            popularity = naver.get('popularity_score', 0)
            score += min(popularity * 0.15, 15)

        #    (10)
        google = data_sources.get('google', {})
        if not google.get('error'):
            difficulty = google.get('entry_difficulty', 'hard')
            if difficulty == 'easy':
                score += 10
            elif difficulty == 'medium':
                score += 7
            elif difficulty == 'hard':
                score += 3

        #   (5)
        youtube = data_sources.get('youtube', {})
        if not youtube.get('error'):
            interest = youtube.get('interest_indicator', 'low')
            if interest == 'high':
                score += 5
            elif interest == 'medium':
                score += 3
            elif interest == 'low':
                score += 1

        #    (15)
        wishket = data_sources.get('wishket', {})
        if not wishket.get('error'):
            demand = wishket.get('demand_level', 'low')
            if demand == 'high':
                score += 10
            elif demand == 'medium':
                score += 6
            elif demand == 'low':
                score += 2

            avg_budget = wishket.get('avg_budget', 0)
            if avg_budget > 2000000:
                score += 5
            elif avg_budget > 1000000:
                score += 3
            elif avg_budget > 500000:
                score += 2

        #    (10)
        soomgo = data_sources.get('soomgo', {})
        if not soomgo.get('error'):
            competition = soomgo.get('competition', 'high')
            if competition == 'low':
                score += 7
            elif competition == 'medium':
                score += 5
            elif competition == 'high':
                score += 2

            expert_count = soomgo.get('expert_count', 0)
            if expert_count > 0:
                score += 3

        #  /  (5)
        brokerage = data_sources.get('brokerage', {})
        if not brokerage.get('error'):
            if brokerage.get('market_presence'):
                score += 3
            class_count = brokerage.get('class_count', 0)
            if class_count > 10:
                score += 2
            elif class_count > 0:
                score += 1

        #   (10)
        coupang = data_sources.get('coupang', {})
        if not coupang.get('error'):
            potential = coupang.get('e_commerce_potential', 'low')
            if potential == 'high':
                score += 7
            elif potential == 'medium':
                score += 4

            product_count = coupang.get('product_count', 0)
            if product_count > 50:
                score += 3
            elif product_count > 10:
                score += 2

        #    (5)
        blog = data_sources.get('blog', {})
        if not blog.get('error'):
            trend = blog.get('trend_indicator', '')
            if trend == '':
                score += 5
            elif trend == '':
                score += 3

        #   (5)
        instagram = data_sources.get('instagram', {})
        if not instagram.get('error'):
            presence = instagram.get('social_presence', 'low')
            if presence == 'high':
                score += 5
            elif presence == 'medium':
                score += 3

        return min(int(score), 100)

    def _generate_recommendation(self, score):
        """   """
        if score >= 80:
            return {
                'verdict': ' ',
                'action': '    ',
                'priority': 'high',
                'confidence': ''
            }
        elif score >= 60:
            return {
                'verdict': '',
                'action': '   ',
                'priority': 'medium',
                'confidence': ''
            }
        elif score >= 40:
            return {
                'verdict': '',
                'action': '  ',
                'priority': 'low',
                'confidence': ''
            }
        else:
            return {
                'verdict': '',
                'action': '  ',
                'priority': 'none',
                'confidence': ' '
            }

    def save_analysis(self, results, filename='market_analysis.json'):
        """  """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"  : {filename}")


#  
if __name__ == "__main__":
    analyzer = RealMarketAnalyzer()

    # IT   
    test_ideas = [
        ("  ", " "),
        ("SEO ", ""),
        (" ", " "),
        ("  ", " "),
        (" ", " ")
    ]

    all_results = []

    for business_idea, keyword in test_ideas:
        result = analyzer.comprehensive_analysis(business_idea, keyword)
        all_results.append(result)

        #  
        print(f"\n[RESULT] {business_idea}")
        print(f"   : {keyword}")
        print(f"    : {result['market_score']}/100")
        print(f"   : {result['recommendation']['verdict']}")
        print(f"   : {result['recommendation']['priority']}")
        print("-" * 60)

        time.sleep(5)  # API  

    #  3 
    all_results.sort(key=lambda x: x['market_score'], reverse=True)

    print("\n" + "="*60)
    print("[TOP 3]  ")
    print("="*60)

    for i, result in enumerate(all_results[:3], 1):
        print(f"\n{i}. {result['business_idea']}")
        print(f"   : {result['market_score']}/100")
        print(f"   : {result['recommendation']['action']}")

        kmong = result['data_sources'].get('kmong', {})
        if not kmong.get('error'):
            print(f"    : {kmong.get('avg_price', 0):,}")
            print(f"    : {kmong.get('competition_level', 'N/A')}")

    #   
    analyzer.save_analysis({
        'analysis_date': datetime.now().isoformat(),
        'total_analyzed': len(all_results),
        'results': all_results
    }, 'comprehensive_market_analysis.json')
