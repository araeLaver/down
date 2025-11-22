"""
실시간 시장 분석 모듈
- 웹 스크래핑으로 실제 시장 데이터 수집
- 다중 플랫폼 시장 분석
- 경쟁사 및 수요 자동 파악
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
        """크몽에서 실제 시장 데이터 수집"""
        try:
            url = f"https://kmong.com/search?keyword={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 서비스 개수 파악
            services = soup.find_all('div', class_='service-card')

            prices = []
            reviews = []
            for service in services[:20]:  # 상위 20개만
                try:
                    price_elem = service.find('span', class_='price')
                    if price_elem:
                        price_text = price_elem.text.replace(',', '').replace('원', '')
                        prices.append(int(price_text))

                    review_elem = service.find('span', class_='review-count')
                    if review_elem:
                        review_count = int(review_elem.text.replace('(', '').replace(')', ''))
                        reviews.append(review_count)
                except:
                    continue

            return {
                'platform': '크몽',
                'service_count': len(services),
                'avg_price': sum(prices) // len(prices) if prices else 0,
                'min_price': min(prices) if prices else 0,
                'max_price': max(prices) if prices else 0,
                'avg_reviews': sum(reviews) // len(reviews) if reviews else 0,
                'competition_level': self._calculate_competition(len(services)),
                'market_saturation': self._calculate_saturation(len(services), sum(reviews))
            }
        except Exception as e:
            print(f"크몽 분석 실패: {e}")
            return {'platform': '크몽', 'error': str(e)}

    def analyze_naver_search_volume(self, keyword):
        """네이버 검색량 추정"""
        try:
            url = f"https://search.naver.com/search.naver?query={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)

            # 자동완성 검색어로 인기도 추정
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
            print(f"네이버 검색량 분석 실패: {e}")
            return {'keyword': keyword, 'error': str(e)}

    def analyze_competitors_google(self, keyword):
        """구글 검색으로 경쟁사 파악"""
        try:
            url = f"https://www.google.com/search?q={quote(keyword + ' 서비스')}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 검색 결과 개수 파악
            results = soup.find_all('div', class_='g')

            # 광고 여부 확인
            ads = soup.find_all('div', {'data-text-ad': True})

            return {
                'organic_results': len(results),
                'paid_ads': len(ads),
                'has_competition': len(results) > 0,
                'ad_competition': 'high' if len(ads) > 5 else 'medium' if len(ads) > 0 else 'low',
                'entry_difficulty': 'hard' if len(ads) > 5 and len(results) > 50 else 'medium' if len(results) > 20 else 'easy'
            }
        except Exception as e:
            print(f"구글 경쟁사 분석 실패: {e}")
            return {'error': str(e)}

    def analyze_youtube_interest(self, keyword):
        """유튜브 관심도 분석"""
        try:
            url = f"https://www.youtube.com/results?search_query={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)

            # 간단한 관심도 추정 (응답 크기 기반)
            content_length = len(response.content)

            return {
                'interest_indicator': 'high' if content_length > 500000 else 'medium' if content_length > 300000 else 'low',
                'estimated_videos': content_length // 10000  # 대략적 추정
            }
        except Exception as e:
            print(f"유튜브 관심도 분석 실패: {e}")
            return {'error': str(e)}

    def analyze_wishket_market(self, keyword):
        """위시켓 프리랜서 시장 분석"""
        try:
            url = f"https://www.wishket.com/project/?q={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 프로젝트 개수 파악
            projects = soup.find_all('div', class_='project-card') or soup.find_all('div', class_='item')

            # 평균 예산 추정
            budgets = []
            for project in projects[:10]:
                try:
                    budget_elem = project.find('span', class_='budget') or project.find('div', class_='price')
                    if budget_elem:
                        budget_text = budget_elem.text.replace(',', '').replace('만원', '0000').replace('원', '')
                        budgets.append(int(budget_text))
                except:
                    continue

            return {
                'platform': '위시켓',
                'project_count': len(projects),
                'avg_budget': sum(budgets) // len(budgets) if budgets else 0,
                'demand_level': 'high' if len(projects) > 20 else 'medium' if len(projects) > 5 else 'low',
                'market_active': len(projects) > 0
            }
        except Exception as e:
            print(f"위시켓 분석 실패: {e}")
            return {'platform': '위시켓', 'error': str(e)}

    def analyze_soomgo_market(self, keyword):
        """숨고 서비스 시장 분석"""
        try:
            url = f"https://soomgo.com/search/pro?keyword={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 전문가 개수
            pros = soup.find_all('div', class_='pro-card') or soup.find_all('a', class_='pro-item')

            # 리뷰 수 파악
            reviews = []
            for pro in pros[:20]:
                try:
                    review_elem = pro.find('span', class_='review-count')
                    if review_elem:
                        review_count = int(review_elem.text.replace('리뷰', '').replace(',', '').strip())
                        reviews.append(review_count)
                except:
                    continue

            return {
                'platform': '숨고',
                'expert_count': len(pros),
                'avg_reviews': sum(reviews) // len(reviews) if reviews else 0,
                'competition': 'high' if len(pros) > 50 else 'medium' if len(pros) > 10 else 'low',
                'market_maturity': 'mature' if sum(reviews) > 500 else 'growing'
            }
        except Exception as e:
            print(f"숨고 분석 실패: {e}")
            return {'platform': '숨고', 'error': str(e)}

    def analyze_brokerage_platforms(self, keyword):
        """중개 플랫폼 종합 분석 (탈잉, 프립 등)"""
        try:
            # 탈잉 (재능 마켓)
            taling_url = f"https://taling.me/search?keyword={quote(keyword)}"
            response = requests.get(taling_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            classes = soup.find_all('div', class_='class-card') or soup.find_all('a', class_='talent-item')

            return {
                'platform': '탈잉',
                'class_count': len(classes),
                'market_presence': len(classes) > 0,
                'category': '교육/재능공유'
            }
        except Exception as e:
            print(f"중개 플랫폼 분석 실패: {e}")
            return {'platform': '중개플랫폼', 'error': str(e)}

    def analyze_coupang_marketplace(self, keyword):
        """쿠팡 마켓플레이스 분석"""
        try:
            url = f"https://www.coupang.com/np/search?q={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 상품 개수
            products = soup.find_all('li', class_='search-product') or soup.find_all('a', class_='search-product-link')

            # 가격 정보
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
                'platform': '쿠팡',
                'product_count': len(products),
                'avg_price': sum(prices) // len(prices) if prices else 0,
                'e_commerce_potential': 'high' if len(products) > 100 else 'medium' if len(products) > 20 else 'low'
            }
        except Exception as e:
            print(f"쿠팡 분석 실패: {e}")
            return {'platform': '쿠팡', 'error': str(e)}

    def analyze_blog_trend(self, keyword):
        """네이버 블로그 트렌드 분석"""
        try:
            url = f"https://section.blog.naver.com/Search/Post.naver?keyword={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 블로그 포스트 개수
            posts = soup.find_all('div', class_='desc_inner') or soup.find_all('a', class_='post_link')

            return {
                'platform': '네이버 블로그',
                'post_count': len(posts),
                'content_volume': 'high' if len(posts) > 30 else 'medium' if len(posts) > 10 else 'low',
                'trend_indicator': '상승중' if len(posts) > 20 else '보통'
            }
        except Exception as e:
            print(f"블로그 트렌드 분석 실패: {e}")
            return {'platform': '네이버 블로그', 'error': str(e)}

    def analyze_instagram_business(self, keyword):
        """인스타그램 비즈니스 활성도 분석"""
        try:
            # 인스타그램은 로그인 필요하므로 간접 지표 사용
            # 네이버에서 "keyword 인스타그램" 검색
            url = f"https://search.naver.com/search.naver?query={quote(keyword + ' 인스타그램')}"
            response = requests.get(url, headers=self.headers, timeout=10)

            content_length = len(response.content)

            return {
                'platform': '인스타그램',
                'social_presence': 'high' if content_length > 300000 else 'medium' if content_length > 150000 else 'low',
                'marketing_potential': 'SNS 마케팅 가능' if content_length > 200000 else '제한적'
            }
        except Exception as e:
            print(f"인스타그램 분석 실패: {e}")
            return {'platform': '인스타그램', 'error': str(e)}

    def _calculate_competition(self, service_count):
        """경쟁 강도 계산"""
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
        """시장 포화도 계산"""
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
        """종합 시장 분석"""
        print(f"\n{'='*60}")
        print(f"시장 분석 시작: {business_idea}")
        print(f"키워드: {keyword}")
        print(f"{'='*60}\n")

        results = {
            'business_idea': business_idea,
            'keyword': keyword,
            'analysis_date': datetime.now().isoformat(),
            'data_sources': {}
        }

        # 크몽 분석
        print("1. 크몽 시장 분석 중...")
        kmong_data = self.analyze_kmong_market(keyword)
        results['data_sources']['kmong'] = kmong_data
        time.sleep(2)  # API 호출 간격

        # 네이버 검색량
        print("2. 네이버 검색량 분석 중...")
        naver_data = self.analyze_naver_search_volume(keyword)
        results['data_sources']['naver'] = naver_data
        time.sleep(2)

        # 구글 경쟁사
        print("3. 구글 경쟁사 분석 중...")
        google_data = self.analyze_competitors_google(keyword)
        results['data_sources']['google'] = google_data
        time.sleep(2)

        # 유튜브 관심도
        print("4. 유튜브 관심도 분석 중...")
        youtube_data = self.analyze_youtube_interest(keyword)
        results['data_sources']['youtube'] = youtube_data
        time.sleep(2)

        # 위시켓 프리랜서 시장
        print("5. 위시켓 프리랜서 시장 분석 중...")
        wishket_data = self.analyze_wishket_market(keyword)
        results['data_sources']['wishket'] = wishket_data
        time.sleep(2)

        # 숨고 서비스 시장
        print("6. 숨고 서비스 시장 분석 중...")
        soomgo_data = self.analyze_soomgo_market(keyword)
        results['data_sources']['soomgo'] = soomgo_data
        time.sleep(2)

        # 탈잉 교육/재능 플랫폼
        print("7. 탈잉 플랫폼 분석 중...")
        brokerage_data = self.analyze_brokerage_platforms(keyword)
        results['data_sources']['brokerage'] = brokerage_data
        time.sleep(2)

        # 쿠팡 마켓플레이스
        print("8. 쿠팡 마켓플레이스 분석 중...")
        coupang_data = self.analyze_coupang_marketplace(keyword)
        results['data_sources']['coupang'] = coupang_data
        time.sleep(2)

        # 네이버 블로그 트렌드
        print("9. 네이버 블로그 트렌드 분석 중...")
        blog_data = self.analyze_blog_trend(keyword)
        results['data_sources']['blog'] = blog_data
        time.sleep(2)

        # 인스타그램 비즈니스
        print("10. 인스타그램 비즈니스 활성도 분석 중...")
        instagram_data = self.analyze_instagram_business(keyword)
        results['data_sources']['instagram'] = instagram_data

        # 종합 점수 계산
        results['market_score'] = self._calculate_market_score(results['data_sources'])
        results['recommendation'] = self._generate_recommendation(results['market_score'])

        print(f"\n{'='*60}")
        print(f"분석 완료!")
        print(f"시장 점수: {results['market_score']}/100")
        print(f"추천 여부: {results['recommendation']['verdict']}")
        print(f"{'='*60}\n")

        return results

    def _calculate_market_score(self, data_sources):
        """종합 시장 점수 계산 (0-100) - 10개 플랫폼 통합"""
        score = 0

        # 크몽 데이터 평가 (20점)
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

        # 네이버 인기도 (15점)
        naver = data_sources.get('naver', {})
        if not naver.get('error'):
            popularity = naver.get('popularity_score', 0)
            score += min(popularity * 0.15, 15)

        # 구글 경쟁 강도 (10점)
        google = data_sources.get('google', {})
        if not google.get('error'):
            difficulty = google.get('entry_difficulty', 'hard')
            if difficulty == 'easy':
                score += 10
            elif difficulty == 'medium':
                score += 7
            elif difficulty == 'hard':
                score += 3

        # 유튜브 관심도 (5점)
        youtube = data_sources.get('youtube', {})
        if not youtube.get('error'):
            interest = youtube.get('interest_indicator', 'low')
            if interest == 'high':
                score += 5
            elif interest == 'medium':
                score += 3
            elif interest == 'low':
                score += 1

        # 위시켓 프리랜서 시장 (15점)
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

        # 숨고 서비스 시장 (10점)
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

        # 탈잉 교육/재능 플랫폼 (5점)
        brokerage = data_sources.get('brokerage', {})
        if not brokerage.get('error'):
            if brokerage.get('market_presence'):
                score += 3
            class_count = brokerage.get('class_count', 0)
            if class_count > 10:
                score += 2
            elif class_count > 0:
                score += 1

        # 쿠팡 마켓플레이스 (10점)
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

        # 네이버 블로그 트렌드 (5점)
        blog = data_sources.get('blog', {})
        if not blog.get('error'):
            trend = blog.get('trend_indicator', '보통')
            if trend == '상승중':
                score += 5
            elif trend == '보통':
                score += 3

        # 인스타그램 비즈니스 (5점)
        instagram = data_sources.get('instagram', {})
        if not instagram.get('error'):
            presence = instagram.get('social_presence', 'low')
            if presence == 'high':
                score += 5
            elif presence == 'medium':
                score += 3

        return min(int(score), 100)

    def _generate_recommendation(self, score):
        """점수 기반 추천 생성"""
        if score >= 80:
            return {
                'verdict': '매우 유망',
                'action': '즉시 실행 계획 수립 권장',
                'priority': 'high',
                'confidence': '높음'
            }
        elif score >= 60:
            return {
                'verdict': '유망',
                'action': '추가 검증 후 진행',
                'priority': 'medium',
                'confidence': '중간'
            }
        elif score >= 40:
            return {
                'verdict': '보통',
                'action': '신중한 접근 필요',
                'priority': 'low',
                'confidence': '낮음'
            }
        else:
            return {
                'verdict': '비추천',
                'action': '다른 아이디어 탐색',
                'priority': 'none',
                'confidence': '매우 낮음'
            }

    def save_analysis(self, results, filename='market_analysis.json'):
        """분석 결과 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"분석 결과 저장됨: {filename}")


# 사용 예시
if __name__ == "__main__":
    analyzer = RealMarketAnalyzer()

    # IT 사업 아이디어 분석
    test_ideas = [
        ("웹사이트 제작 서비스", "홈페이지 제작"),
        ("SEO 컨설팅", "검색엔진최적화"),
        ("챗봇 개발", "챗봇 제작"),
        ("모바일 앱 개발", "앱 개발"),
        ("마케팅 자동화", "마케팅 자동화")
    ]

    all_results = []

    for business_idea, keyword in test_ideas:
        result = analyzer.comprehensive_analysis(business_idea, keyword)
        all_results.append(result)

        # 결과 출력
        print(f"\n📊 {business_idea}")
        print(f"   키워드: {keyword}")
        print(f"   시장 점수: {result['market_score']}/100")
        print(f"   추천: {result['recommendation']['verdict']}")
        print(f"   우선순위: {result['recommendation']['priority']}")
        print("-" * 60)

        time.sleep(5)  # API 호출 간격

    # 상위 3개 추천
    all_results.sort(key=lambda x: x['market_score'], reverse=True)

    print("\n" + "="*60)
    print("🏆 TOP 3 추천 사업")
    print("="*60)

    for i, result in enumerate(all_results[:3], 1):
        print(f"\n{i}. {result['business_idea']}")
        print(f"   점수: {result['market_score']}/100")
        print(f"   추천: {result['recommendation']['action']}")

        kmong = result['data_sources'].get('kmong', {})
        if not kmong.get('error'):
            print(f"   평균 가격: {kmong.get('avg_price', 0):,}원")
            print(f"   경쟁 강도: {kmong.get('competition_level', 'N/A')}")

    # 전체 결과 저장
    analyzer.save_analysis({
        'analysis_date': datetime.now().isoformat(),
        'total_analyzed': len(all_results),
        'results': all_results
    }, 'comprehensive_market_analysis.json')
