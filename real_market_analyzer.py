"""
실시간 시장 분석 모듈
- 웹 스크래핑으로 실제 시장 데이터 수집
- Claude API로 최신 시장 분석
- 경쟁사 및 수요 자동 파악
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
from urllib.parse import quote

class RealMarketAnalyzer:
    def __init__(self, claude_api_key=None):
        self.claude_api_key = claude_api_key
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
        """종합 시장 점수 계산 (0-100)"""
        score = 0

        # 크몽 데이터 평가 (40점)
        kmong = data_sources.get('kmong', {})
        if not kmong.get('error'):
            competition = kmong.get('competition_level', 'high')
            if competition == 'very_low':
                score += 30
            elif competition == 'low':
                score += 25
            elif competition == 'medium':
                score += 20
            elif competition == 'high':
                score += 10

            avg_price = kmong.get('avg_price', 0)
            if avg_price > 100000:
                score += 10
            elif avg_price > 50000:
                score += 7
            elif avg_price > 20000:
                score += 5

        # 네이버 인기도 (30점)
        naver = data_sources.get('naver', {})
        if not naver.get('error'):
            popularity = naver.get('popularity_score', 0)
            score += min(popularity * 0.3, 30)

        # 구글 경쟁 강도 (20점)
        google = data_sources.get('google', {})
        if not google.get('error'):
            difficulty = google.get('entry_difficulty', 'hard')
            if difficulty == 'easy':
                score += 20
            elif difficulty == 'medium':
                score += 15
            elif difficulty == 'hard':
                score += 5

        # 유튜브 관심도 (10점)
        youtube = data_sources.get('youtube', {})
        if not youtube.get('error'):
            interest = youtube.get('interest_indicator', 'low')
            if interest == 'high':
                score += 10
            elif interest == 'medium':
                score += 7
            elif interest == 'low':
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
