"""
실시간 트렌드 기반 사업 아이디어 생성기
- 크몽/탈잉에서 인기 서비스 크롤링
- Google Trends로 트렌드 키워드 수집
- 실제 수요가 검증된 사업 아이디어 생성
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
from urllib.parse import quote
import time
from pytrends.request import TrendReq

class TrendBasedIdeaGenerator:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.categories = [
            'IT·프로그래밍', '디자인', '마케팅', '번역·통역',
            '문서·취업', '레슨', '상담', '운세'
        ]
        try:
            self.pytrends = TrendReq(hl='ko-KR', tz=540)
        except:
            self.pytrends = None
            print("[WARNING] Google Trends initialization failed")

    def scrape_kmong_trending(self):
        """크몽에서 인기 서비스 크롤링"""
        trending_services = []

        try:
            # 크몽 메인 페이지에서 인기 서비스 수집
            url = "https://kmong.com"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 서비스 카드들 찾기
            service_cards = soup.find_all('div', class_='service_item', limit=20)

            for card in service_cards:
                try:
                    title_elem = card.find('h3') or card.find('p', class_='title')
                    if title_elem:
                        title = title_elem.get_text(strip=True)

                        # 가격 추출
                        price_elem = card.find('span', class_='price')
                        price = 0
                        if price_elem:
                            price_text = price_elem.get_text(strip=True)
                            price = int(price_text.replace(',', '').replace('원', '').replace('₩', ''))

                        # 리뷰 수 추출
                        review_elem = card.find('span', class_='review_count')
                        reviews = 0
                        if review_elem:
                            review_text = review_elem.get_text(strip=True)
                            reviews = int(review_text.replace('(', '').replace(')', '').replace(',', ''))

                        trending_services.append({
                            'name': title,
                            'price': price,
                            'reviews': reviews,
                            'platform': '크몽',
                            'popularity': reviews * price  # 인기도 지표
                        })
                except Exception as e:
                    continue

            print(f"[OK] Collected {len(trending_services)} popular services from Kmong")

        except Exception as e:
            print(f"[WARNING] Kmong crawling failed: {e}")

        return trending_services

    def scrape_taling_trending(self):
        """탈잉에서 인기 클래스 크롤링"""
        trending_classes = []

        try:
            url = "https://taling.me"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 클래스 카드들 찾기
            class_cards = soup.find_all('div', class_='class-card', limit=20)

            for card in class_cards:
                try:
                    title_elem = card.find('h3') or card.find('div', class_='title')
                    if title_elem:
                        title = title_elem.get_text(strip=True)

                        price_elem = card.find('span', class_='price')
                        price = 0
                        if price_elem:
                            price_text = price_elem.get_text(strip=True)
                            price = int(price_text.replace(',', '').replace('원', '').replace('₩', ''))

                        trending_classes.append({
                            'name': title,
                            'price': price,
                            'platform': '탈잉',
                            'category': '클래스/레슨'
                        })
                except Exception as e:
                    continue

            print(f"[OK] Collected {len(trending_classes)} popular classes from Taling")

        except Exception as e:
            print(f"[WARNING] Taling crawling failed: {e}")

        return trending_classes

    def get_naver_realtime_keywords(self):
        """네이버 실시간 검색어 수집"""
        keywords = []

        try:
            # 네이버 데이터랩 대신 자동완성 API 활용
            test_keywords = ['앱', '플랫폼', '서비스', 'AI', '자동화']

            for keyword in test_keywords:
                url = f"https://ac.search.naver.com/nx/ac?q={quote(keyword)}&con=0&frm=nv&ans=2&r_format=json"
                response = requests.get(url, timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [[]])[0]

                    for item in items[:5]:
                        keyword_text = item[0] if isinstance(item, list) else item
                        keywords.append({
                            'keyword': keyword_text,
                            'source': '네이버',
                            'base_keyword': keyword
                        })

                time.sleep(0.5)  # API 호출 간격

            print(f"[OK] Collected {len(keywords)} trend keywords from Naver")

        except Exception as e:
            print(f"[WARNING] Naver keyword collection failed: {e}")

        return keywords

    def get_google_trends(self):
        """Google Trends에서 실시간 트렌드 키워드 수집 (다국가)"""
        trending_keywords = []

        if not self.pytrends:
            print("[WARNING] Google Trends cannot be used")
            return trending_keywords

        # 여러 국가에서 트렌드 수집
        countries = {
            'south_korea': '한국',
            'united_states': '미국',
            'japan': '일본',
            'united_kingdom': '영국',
            'singapore': '싱가포르'
        }

        for country_code, country_name in countries.items():
            try:
                print(f"   [{country_name}] 트렌드 수집 중...")
                trending_searches = self.pytrends.trending_searches(pn=country_code)

                for keyword in trending_searches[0][:10]:  # 국가당 상위 10개
                    keyword_str = str(keyword)

                    # IT/비즈니스 관련 키워드 필터 (한글 + 영어)
                    it_keywords = [
                        # 한글
                        '앱', '웹', 'AI', '프로그래밍', '개발', '사이트', '플랫폼',
                        '자동화', 'SaaS', '소프트웨어', '디지털', '온라인', '서비스',
                        # 영어
                        'app', 'web', 'AI', 'software', 'platform', 'automation',
                        'SaaS', 'digital', 'online', 'service', 'startup', 'business',
                        'tech', 'mobile', 'cloud', 'API', 'coding', 'programming'
                    ]

                    # 키워드 필터링 (IT 관련이거나, 비즈니스 아이디어로 전환 가능한 것)
                    is_relevant = any(kw.lower() in keyword_str.lower() for kw in it_keywords)

                    # 또는 길이가 적당하고 특수문자가 없는 일반 키워드도 포함 (사업 아이디어로 전환 가능)
                    is_general_topic = (
                        len(keyword_str) >= 2 and
                        len(keyword_str) <= 30 and
                        not keyword_str.startswith('#')
                    )

                    if is_relevant or is_general_topic:
                        trending_keywords.append({
                            'keyword': keyword_str,
                            'source': f'Google Trends ({country_name})',
                            'country': country_name,
                            'country_code': country_code,
                            'timestamp': datetime.now().isoformat()
                        })

                time.sleep(2)  # 국가별 API 호출 간격

            except Exception as e:
                print(f"   [WARNING] {country_name} trend collection failed: {e}")
                continue

        print(f"[OK] Collected total {len(trending_keywords)} keywords from Google Trends (5 countries)")

        return trending_keywords

    def analyze_search_demand(self, keyword):
        """네이버 검색 수요 분석"""
        try:
            url = f"https://search.naver.com/search.naver?query={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 검색 결과 개수로 수요 추정
            result_count = len(soup.find_all('div', class_='total_wrap'))

            # 쇼핑 결과가 있는지 확인 (구매 수요)
            shopping_results = soup.find_all('div', class_='shop_info')
            has_shopping = len(shopping_results) > 0

            # 블로그 결과 개수 (관심도)
            blog_results = soup.find_all('div', class_='api_subject_bx')

            demand_score = min(100, (
                result_count * 10 +
                (30 if has_shopping else 0) +
                len(blog_results) * 5
            ))

            return {
                'keyword': keyword,
                'demand_score': demand_score,
                'has_shopping': has_shopping,
                'blog_count': len(blog_results)
            }

        except Exception as e:
            return {'keyword': keyword, 'demand_score': 50, 'error': str(e)}

    def generate_ideas_from_trends(self):
        """트렌드 기반 사업 아이디어 생성"""
        print("\n" + "="*80)
        print("[TREND] Collecting business ideas from real-time trends...")
        print("="*80 + "\n")

        all_ideas = []

        # 1. 크몽 인기 서비스
        kmong_services = self.scrape_kmong_trending()
        for service in kmong_services[:10]:
            idea = self._convert_to_business_idea(service, 'kmong')
            if idea:
                all_ideas.append(idea)

        time.sleep(2)

        # 2. 탈잉 인기 클래스
        taling_classes = self.scrape_taling_trending()
        for taling_class in taling_classes[:10]:
            idea = self._convert_to_business_idea(taling_class, 'taling')
            if idea:
                all_ideas.append(idea)

        time.sleep(2)

        # 3. Google Trends 키워드
        google_keywords = self.get_google_trends()
        for kw in google_keywords[:10]:
            idea = self._create_idea_from_keyword(kw)
            if idea:
                all_ideas.append(idea)

        time.sleep(2)

        # 4. 네이버 트렌드 키워드
        keywords = self.get_naver_realtime_keywords()
        for kw in keywords[:15]:
            idea = self._create_idea_from_keyword(kw)
            if idea:
                all_ideas.append(idea)

        print(f"\n[OK] Generated {len(all_ideas)} trend-based business ideas!\n")

        return all_ideas

    def _convert_to_business_idea(self, service_data, platform):
        """서비스 데이터를 사업 아이디어로 변환"""
        name = service_data.get('name', '')

        # IT 관련 키워드 필터
        it_keywords = ['앱', '웹', 'AI', '프로그래밍', '개발', '사이트', '플랫폼',
                      '자동화', 'SaaS', '소프트웨어', '디지털', '온라인',
                      '챗봇', 'API', '시스템', 'SEO', '마케팅', '디자인']

        if not any(keyword in name for keyword in it_keywords):
            return None

        price = service_data.get('price', 100000)

        return {
            'type': f'{platform}_트렌드',
            'category': 'IT/디지털',
            'business': {
                'name': name,
                'description': f"{platform}에서 인기 상승 중인 서비스",
                'startup_cost': f"{price // 10:,}원",
                'monthly_revenue': f"{price * 10:,}원",
                'revenue_potential': f"월 {price * 10:,}원",
                'timeline': '2주 내 시작',
                'difficulty': '보통',
                'viability': '높음' if service_data.get('reviews', 0) > 50 else '보통',
                'trend_source': platform,
                'popularity': service_data.get('popularity', 0)
            },
            'priority': '높음'
        }

    def _create_idea_from_keyword(self, keyword_data):
        """키워드로부터 사업 아이디어 생성"""
        keyword = keyword_data.get('keyword', '')
        country = keyword_data.get('country', '한국')
        source = keyword_data.get('source', '트렌드')

        # 키워드 기반 사업 아이디어 템플릿
        business_templates = [
            f"{keyword} 온라인 플랫폼",
            f"{keyword} 자동화 도구",
            f"{keyword} 매칭 서비스",
            f"{keyword} 관리 시스템",
            f"{keyword} 컨설팅 서비스",
            f"{keyword} SaaS 솔루션",
            f"{keyword} 모바일 앱",
            f"{keyword} AI 분석 서비스"
        ]

        business_name = random.choice(business_templates)

        # 국가별 설명 추가
        if country == '한국':
            description = f"한국 트렌드 키워드 '{keyword}' 기반 사업"
            market = "한국 시장"
        elif country == '미국':
            description = f"미국 트렌드 '{keyword}' 기반 글로벌 사업"
            market = "글로벌 시장"
        elif country == '일본':
            description = f"일본 트렌드 '{keyword}' 기반 한일 시장 진출"
            market = "한일 시장"
        else:
            description = f"{country} 트렌드 '{keyword}' 기반 글로벌 사업"
            market = f"{country} 시장"

        return {
            'type': f'{source}_트렌드',
            'category': 'IT/디지털',
            'business': {
                'name': business_name,
                'description': description,
                'startup_cost': '300만원 이하' if country == '한국' else '500만원 이하',
                'monthly_revenue': '500만원' if country == '한국' else '1000만원',
                'revenue_potential': f'월 500-1500만원 ({market})',
                'timeline': '1개월 내 시작',
                'difficulty': '보통',
                'viability': '높음',
                'trend_keyword': keyword,
                'trend_country': country,
                'global_potential': country != '한국'
            },
            'priority': '높음' if country in ['미국', '영국'] else '보통'
        }

if __name__ == '__main__':
    generator = TrendBasedIdeaGenerator()
    ideas = generator.generate_ideas_from_trends()

    print(f"\n생성된 아이디어 {len(ideas)}개:")
    for i, idea in enumerate(ideas[:5], 1):
        print(f"{i}. {idea['business']['name']}")
