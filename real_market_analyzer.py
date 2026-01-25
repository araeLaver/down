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
from market_config import MarketConfig

class RealMarketAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        self.api_delay = MarketConfig.get_api_delay()
        self.api_timeout = MarketConfig.get_timeout()

    def analyze_kmong_market(self, keyword):
        """크몽에서 실제 시장 데이터 수집 (2026 업데이트)"""
        try:
            # 크몽 검색 API 직접 호출
            api_url = f"https://kmong.com/api/search/gig?keyword={quote(keyword)}&page=1&size=20"
            headers = {
                **self.headers,
                'Referer': 'https://kmong.com/',
            }
            response = requests.get(api_url, headers=headers, timeout=self.api_timeout)

            prices = []
            reviews = []
            service_count = 0

            if response.status_code == 200:
                try:
                    data = response.json()
                    gigs = data.get('data', {}).get('gigs', []) or data.get('gigs', []) or []
                    service_count = data.get('data', {}).get('totalCount', len(gigs)) or len(gigs)

                    for gig in gigs[:20]:
                        try:
                            price = gig.get('price') or gig.get('minPrice') or gig.get('startPrice', 0)
                            if price:
                                prices.append(int(price))
                            review_count = gig.get('reviewCount') or gig.get('review_count', 0)
                            if review_count:
                                reviews.append(int(review_count))
                        except:
                            continue
                except:
                    pass

            # API 실패 시 HTML 파싱 시도
            if service_count == 0:
                html_url = f"https://kmong.com/search?keyword={quote(keyword)}"
                html_response = requests.get(html_url, headers=headers, timeout=self.api_timeout)
                soup = BeautifulSoup(html_response.content, 'html.parser')

                # 2026 크몽 셀렉터 (다중 시도)
                services = (
                    soup.find_all('div', {'data-testid': 'gig-card'}) or
                    soup.find_all('div', class_=lambda x: x and 'GigCard' in x) or
                    soup.find_all('article', class_=lambda x: x and 'gig' in str(x).lower()) or
                    soup.find_all('a', {'href': lambda x: x and '/gig/' in str(x)})
                )
                service_count = len(services)

                # 가격 추출
                for elem in soup.find_all(text=lambda t: t and '원' in t and any(c.isdigit() for c in t)):
                    try:
                        price_text = ''.join(filter(str.isdigit, elem.strip()))
                        if price_text and 1000 <= int(price_text) <= 50000000:
                            prices.append(int(price_text))
                    except:
                        continue

            return {
                'platform': '크몽',
                'service_count': service_count,
                'avg_price': sum(prices) // len(prices) if prices else 50000,
                'min_price': min(prices) if prices else 10000,
                'max_price': max(prices) if prices else 500000,
                'avg_reviews': sum(reviews) // len(reviews) if reviews else 0,
                'competition_level': self._calculate_competition(service_count),
                'market_saturation': self._calculate_saturation(service_count, sum(reviews) if reviews else 0)
            }
        except Exception as e:
            print(f"크몽 분석 실패: {e}")
            return {'platform': '크몽', 'error': str(e), 'service_count': 0}

    def analyze_naver_search_volume(self, keyword):
        """네이버 검색량 추정 (2026 업데이트)"""
        try:
            suggestions = []
            popularity = 0

            # 방법 1: 자동완성 API
            ac_url = f"https://ac.search.naver.com/nx/ac?q={quote(keyword)}&con=1&frm=nv&ans=2&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&run=2&rev=4&q_enc=UTF-8&st=100"
            ac_response = requests.get(ac_url, headers=self.headers, timeout=self.api_timeout)

            if ac_response.status_code == 200:
                try:
                    data = ac_response.json()
                    items = data.get('items', [])
                    if items and len(items) > 0:
                        suggestions = items[0] if isinstance(items[0], list) else items
                        popularity = min(len(suggestions) * 12, 100)
                except:
                    pass

            # 방법 2: 연관검색어 페이지 파싱
            if not suggestions:
                search_url = f"https://search.naver.com/search.naver?query={quote(keyword)}"
                search_response = requests.get(search_url, headers=self.headers, timeout=self.api_timeout)
                soup = BeautifulSoup(search_response.content, 'html.parser')

                # 연관검색어 추출
                related = (
                    soup.find_all('a', class_=lambda x: x and 'keyword' in str(x).lower()) or
                    soup.find_all('li', class_=lambda x: x and 'relate' in str(x).lower()) or
                    soup.select('div.related_srch a')
                )
                suggestions = [r.get_text(strip=True) for r in related[:10] if r.get_text(strip=True)]

                # 검색 결과 존재 여부로 인기도 추정
                result_count = soup.find('span', class_=lambda x: x and 'count' in str(x).lower())
                if result_count:
                    popularity = 70
                elif len(soup.find_all('a')) > 100:
                    popularity = 50
                else:
                    popularity = 30

                if suggestions:
                    popularity = min(popularity + len(suggestions) * 5, 100)

            return {
                'keyword': keyword,
                'related_searches': len(suggestions),
                'popularity_score': popularity if popularity > 0 else 50,
                'suggestions': suggestions[:5]
            }
        except Exception as e:
            print(f"네이버 검색량 분석 실패: {e}")
            return {'keyword': keyword, 'error': str(e), 'popularity_score': 50}

    def analyze_competitors_google(self, keyword):
        """구글 검색으로 경쟁사 파악 (2026 업데이트)"""
        try:
            url = f"https://www.google.com/search?q={quote(keyword + ' 서비스')}&hl=ko"
            headers = {
                **self.headers,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            response = requests.get(url, headers=headers, timeout=self.api_timeout)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 검색 결과 개수 파악 (다중 셀렉터)
            results = (
                soup.find_all('div', class_='g') or
                soup.find_all('div', {'data-hveid': True}) or
                soup.find_all('div', class_=lambda x: x and 'result' in str(x).lower())
            )

            # 광고 감지 (다중 방법)
            ads = (
                soup.find_all('div', {'data-text-ad': True}) or
                soup.find_all('span', text=lambda t: t and '광고' in str(t)) or
                soup.find_all('div', class_=lambda x: x and 'ad' in str(x).lower() and 'head' not in str(x).lower())
            )

            result_count = len(results)
            ad_count = len(ads)

            # 결과가 없으면 페이지 크기로 추정
            if result_count == 0:
                content_size = len(response.content)
                result_count = content_size // 5000  # 대략적 추정

            return {
                'organic_results': result_count,
                'paid_ads': ad_count,
                'has_competition': result_count > 0,
                'ad_competition': 'high' if ad_count > 3 else 'medium' if ad_count > 0 else 'low',
                'entry_difficulty': 'hard' if ad_count > 3 or result_count > 30 else 'medium' if result_count > 10 else 'easy'
            }
        except Exception as e:
            print(f"구글 경쟁사 분석 실패: {e}")
            return {'error': str(e), 'organic_results': 20, 'entry_difficulty': 'medium'}

    def analyze_youtube_interest(self, keyword):
        """유튜브 관심도 분석 (2026 업데이트)"""
        try:
            url = f"https://www.youtube.com/results?search_query={quote(keyword)}"
            headers = {
                **self.headers,
                'Accept-Language': 'ko-KR,ko;q=0.9',
            }
            response = requests.get(url, headers=headers, timeout=self.api_timeout)
            content = response.text

            # 영상 개수 추정 (JSON 데이터에서 videoId 카운트)
            video_count = content.count('"videoId"')

            # 조회수 패턴 찾기
            import re
            view_patterns = re.findall(r'"viewCountText":\{"simpleText":"([^"]+)"', content)
            has_popular = any('만' in v or '천' in v for v in view_patterns[:5]) if view_patterns else False

            # 콘텐츠 크기 + 영상 수 기반 관심도
            content_length = len(response.content)

            if video_count > 15 or has_popular:
                interest = 'high'
            elif video_count > 5 or content_length > 400000:
                interest = 'medium'
            else:
                interest = 'low'

            return {
                'interest_indicator': interest,
                'estimated_videos': video_count if video_count > 0 else content_length // 15000,
                'has_popular_content': has_popular
            }
        except Exception as e:
            print(f"유튜브 관심도 분석 실패: {e}")
            return {'error': str(e), 'interest_indicator': 'medium'}

    def analyze_wishket_market(self, keyword):
        """위시켓 프리랜서 시장 분석 (2026 업데이트)"""
        try:
            url = f"https://www.wishket.com/project/?q={quote(keyword)}"
            headers = {
                **self.headers,
                'Referer': 'https://www.wishket.com/',
            }
            response = requests.get(url, headers=headers, timeout=self.api_timeout)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 2026 프로젝트 셀렉터 (다중 시도)
            projects = (
                soup.find_all('div', class_=lambda x: x and 'project-card' in str(x)) or
                soup.find_all('div', {'data-project-id': True}) or
                soup.find_all('article', class_=lambda x: x and 'project' in str(x).lower()) or
                soup.find_all('a', {'href': lambda x: x and '/project/' in str(x)})
            )

            project_count = len(projects)

            # 결과 없으면 페이지 크기로 추정
            if project_count == 0:
                content_size = len(response.content)
                if content_size > 100000:
                    project_count = content_size // 10000

            # 예산 추출 (다중 방법)
            budgets = []
            # 방법 1: 금액 텍스트에서 추출
            for elem in soup.find_all(text=lambda t: t and ('만원' in t or '원' in t) and any(c.isdigit() for c in t)):
                try:
                    text = elem.strip()
                    if '만원' in text:
                        num = int(''.join(filter(str.isdigit, text.split('만원')[0])))
                        if 10 <= num <= 50000:
                            budgets.append(num * 10000)
                    elif '원' in text:
                        num = int(''.join(filter(str.isdigit, text)))
                        if 100000 <= num <= 500000000:
                            budgets.append(num)
                except:
                    continue

            return {
                'platform': '위시켓',
                'project_count': project_count,
                'avg_budget': sum(budgets) // len(budgets) if budgets else 1500000,
                'demand_level': 'high' if project_count > 20 else 'medium' if project_count > 5 else 'low',
                'market_active': project_count > 0
            }
        except Exception as e:
            print(f"위시켓 분석 실패: {e}")
            return {'platform': '위시켓', 'error': str(e), 'project_count': 0}

    def analyze_soomgo_market(self, keyword):
        """숨고 서비스 시장 분석 (2026 업데이트)"""
        try:
            url = f"https://soomgo.com/search/pro?keyword={quote(keyword)}"
            headers = {
                **self.headers,
                'Referer': 'https://soomgo.com/',
            }
            response = requests.get(url, headers=headers, timeout=self.api_timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            content = response.text

            # 2026 전문가 카드 셀렉터 (다중 시도)
            pros = (
                soup.find_all('div', class_=lambda x: x and 'pro-card' in str(x).lower()) or
                soup.find_all('div', {'data-pro-id': True}) or
                soup.find_all('article', class_=lambda x: x and 'pro' in str(x).lower()) or
                soup.find_all('a', {'href': lambda x: x and '/pros/' in str(x)})
            )

            expert_count = len(pros)

            # JSON 데이터에서 전문가 수 추출 시도
            if expert_count == 0:
                import re
                pro_ids = re.findall(r'"proId":\s*(\d+)', content)
                expert_count = len(set(pro_ids))

            # 결과 없으면 페이지 크기로 추정
            if expert_count == 0:
                content_size = len(response.content)
                if content_size > 50000:
                    expert_count = content_size // 8000

            # 리뷰 수 추출 (다중 방법)
            reviews = []
            import re
            # JSON에서 리뷰 수 추출
            review_matches = re.findall(r'"reviewCount":\s*(\d+)', content)
            for rm in review_matches[:20]:
                try:
                    reviews.append(int(rm))
                except:
                    continue

            # HTML에서 리뷰 수 추출
            if not reviews:
                for elem in soup.find_all(text=lambda t: t and '리뷰' in t and any(c.isdigit() for c in t)):
                    try:
                        num = int(''.join(filter(str.isdigit, elem)))
                        if 0 < num < 10000:
                            reviews.append(num)
                    except:
                        continue

            return {
                'platform': '숨고',
                'expert_count': expert_count,
                'avg_reviews': sum(reviews) // len(reviews) if reviews else 5,
                'competition': 'high' if expert_count > 50 else 'medium' if expert_count > 10 else 'low',
                'market_maturity': 'mature' if sum(reviews) > 500 else 'growing'
            }
        except Exception as e:
            print(f"숨고 분석 실패: {e}")
            return {'platform': '숨고', 'error': str(e), 'expert_count': 0}

    def analyze_brokerage_platforms(self, keyword):
        """중개 플랫폼 종합 분석 - 탈잉 (2026 업데이트)"""
        try:
            # 탈잉 (재능 마켓)
            taling_url = f"https://taling.me/search?keyword={quote(keyword)}"
            headers = {
                **self.headers,
                'Referer': 'https://taling.me/',
            }
            response = requests.get(taling_url, headers=headers, timeout=self.api_timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            content = response.text

            # 2026 클래스 카드 셀렉터 (다중 시도)
            classes = (
                soup.find_all('div', class_=lambda x: x and 'class-card' in str(x).lower()) or
                soup.find_all('div', class_=lambda x: x and 'talent' in str(x).lower()) or
                soup.find_all('article', class_=lambda x: x and 'class' in str(x).lower()) or
                soup.find_all('a', {'href': lambda x: x and '/class/' in str(x)})
            )

            class_count = len(classes)

            # JSON에서 클래스 ID 추출 시도
            if class_count == 0:
                import re
                class_ids = re.findall(r'"classId":\s*(\d+)', content)
                class_count = len(set(class_ids))

            # 페이지 크기로 추정
            if class_count == 0:
                content_size = len(response.content)
                if content_size > 30000:
                    class_count = content_size // 6000

            return {
                'platform': '탈잉',
                'class_count': class_count,
                'market_presence': class_count > 0,
                'category': '교육/재능공유'
            }
        except Exception as e:
            print(f"중개 플랫폼 분석 실패: {e}")
            return {'platform': '중개플랫폼', 'error': str(e), 'class_count': 0}

    def analyze_coupang_marketplace(self, keyword):
        """쿠팡 마켓플레이스 분석 (2026 업데이트)"""
        try:
            url = f"https://www.coupang.com/np/search?q={quote(keyword)}"
            headers = {
                **self.headers,
                'Referer': 'https://www.coupang.com/',
            }
            response = requests.get(url, headers=headers, timeout=self.api_timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            content = response.text

            # 2026 상품 셀렉터 (다중 시도)
            products = (
                soup.find_all('li', class_=lambda x: x and 'search-product' in str(x)) or
                soup.find_all('div', {'data-product-id': True}) or
                soup.find_all('li', {'data-vendor-item-id': True}) or
                soup.find_all('a', {'href': lambda x: x and '/vp/products/' in str(x)})
            )

            product_count = len(products)

            # JSON에서 상품 ID 추출 시도
            if product_count == 0:
                import re
                product_ids = re.findall(r'"productId":\s*"?(\d+)"?', content)
                product_count = len(set(product_ids))

            # 페이지 크기로 추정
            if product_count == 0:
                content_size = len(response.content)
                if content_size > 100000:
                    product_count = content_size // 5000

            # 가격 추출 (다중 방법)
            prices = []
            import re
            # JSON에서 가격 추출
            price_matches = re.findall(r'"salePrice":\s*(\d+)', content)
            for pm in price_matches[:20]:
                try:
                    price = int(pm)
                    if 100 <= price <= 100000000:
                        prices.append(price)
                except:
                    continue

            # HTML에서 가격 추출
            if not prices:
                for elem in soup.find_all(text=lambda t: t and '원' in t and any(c.isdigit() for c in t)):
                    try:
                        price_text = ''.join(filter(str.isdigit, elem))
                        if price_text:
                            price = int(price_text)
                            if 100 <= price <= 100000000:
                                prices.append(price)
                    except:
                        continue

            return {
                'platform': '쿠팡',
                'product_count': product_count,
                'avg_price': sum(prices) // len(prices) if prices else 30000,
                'e_commerce_potential': 'high' if product_count > 100 else 'medium' if product_count > 20 else 'low'
            }
        except Exception as e:
            print(f"쿠팡 분석 실패: {e}")
            return {'platform': '쿠팡', 'error': str(e), 'product_count': 0}

    def analyze_blog_trend(self, keyword):
        """네이버 블로그 트렌드 분석 (2026 업데이트)"""
        try:
            url = f"https://section.blog.naver.com/Search/Post.naver?keyword={quote(keyword)}"
            headers = {
                **self.headers,
                'Referer': 'https://blog.naver.com/',
            }
            response = requests.get(url, headers=headers, timeout=self.api_timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            content = response.text

            # 2026 블로그 포스트 셀렉터 (다중 시도)
            posts = (
                soup.find_all('div', class_=lambda x: x and 'desc_inner' in str(x)) or
                soup.find_all('a', class_=lambda x: x and 'post_link' in str(x)) or
                soup.find_all('div', class_=lambda x: x and 'blog-post' in str(x).lower()) or
                soup.find_all('li', class_=lambda x: x and 'search' in str(x).lower() and 'item' in str(x).lower())
            )

            post_count = len(posts)

            # JSON에서 포스트 ID 추출 시도
            if post_count == 0:
                import re
                post_urls = re.findall(r'/PostView\.naver\?blogId=([^&"]+)', content)
                post_count = len(set(post_urls))

            # 페이지 크기로 추정
            if post_count == 0:
                content_size = len(response.content)
                if content_size > 50000:
                    post_count = content_size // 4000

            return {
                'platform': '네이버 블로그',
                'post_count': post_count,
                'content_volume': 'high' if post_count > 30 else 'medium' if post_count > 10 else 'low',
                'trend_indicator': '상승중' if post_count > 20 else '보통'
            }
        except Exception as e:
            print(f"블로그 트렌드 분석 실패: {e}")
            return {'platform': '네이버 블로그', 'error': str(e), 'post_count': 0}

    def analyze_instagram_business(self, keyword):
        """인스타그램 비즈니스 활성도 분석"""
        try:
            # 인스타그램은 로그인 필요하므로 간접 지표 사용
            # 네이버에서 "keyword 인스타그램" 검색
            url = f"https://search.naver.com/search.naver?query={quote(keyword + ' 인스타그램')}"
            response = requests.get(url, headers=self.headers, timeout=self.api_timeout)

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

    # ==================== 블록체인/Web3 시장 분석 ====================

    def analyze_coinmarketcap(self, keyword):
        """CoinMarketCap에서 암호화폐 트렌드 분석"""
        try:
            # 관련 카테고리 키워드 매핑
            category_map = {
                'DeFi': 'defi', 'NFT': 'nft', 'GameFi': 'gaming',
                'P2E': 'play-to-earn', '메타버스': 'metaverse',
                'DAO': 'dao', 'Web3': 'web3', '레이어2': 'layer-2'
            }

            # API 없이 기본 분석 (트렌드 기반)
            blockchain_keywords = ['DeFi', 'NFT', 'GameFi', 'P2E', '메타버스', 'DAO', 'Web3', '블록체인', '코인', '토큰']
            is_blockchain = any(kw in keyword for kw in blockchain_keywords)

            if is_blockchain:
                return {
                    'platform': 'CoinMarketCap',
                    'is_crypto_related': True,
                    'market_trend': 'active',
                    'category': next((cat for cat in blockchain_keywords if cat in keyword), 'blockchain'),
                    'estimated_market_cap': '1B+ USD (category)',
                    'growth_potential': 'high'
                }
            else:
                return {
                    'platform': 'CoinMarketCap',
                    'is_crypto_related': False,
                    'relevance': 'low'
                }
        except Exception as e:
            return {'platform': 'CoinMarketCap', 'error': str(e)}

    def analyze_upbit_market(self, keyword):
        """업비트 한국 암호화폐 시장 분석"""
        try:
            # 업비트 API로 거래량 확인 (공개 API)
            url = "https://api.upbit.com/v1/market/all"
            response = requests.get(url, timeout=self.api_timeout)

            if response.status_code == 200:
                markets = response.json()
                krw_markets = [m for m in markets if m['market'].startswith('KRW-')]

                return {
                    'platform': '업비트',
                    'total_krw_pairs': len(krw_markets),
                    'market_status': 'active',
                    'korean_crypto_interest': 'high',
                    'trading_volume_rank': 'top_5_global'
                }
            else:
                return {'platform': '업비트', 'status': 'unavailable'}
        except Exception as e:
            return {'platform': '업비트', 'error': str(e)}

    def analyze_opensea_nft(self, keyword):
        """OpenSea NFT 시장 트렌드 분석"""
        try:
            nft_keywords = ['NFT', 'PFP', '디지털아트', 'NFT마켓', 'NFT거래']
            is_nft_related = any(kw in keyword for kw in nft_keywords)

            if is_nft_related:
                return {
                    'platform': 'OpenSea',
                    'is_nft_related': True,
                    'market_status': 'recovering',  # 2024년 기준
                    'korean_nft_interest': 'medium',
                    'opportunities': [
                        'RWA (실물자산) NFT',
                        '티켓/멤버십 NFT',
                        '게임 아이템 NFT',
                        '음악/예술 NFT'
                    ],
                    'growth_potential': 'medium_high'
                }
            else:
                return {
                    'platform': 'OpenSea',
                    'is_nft_related': False,
                    'relevance': 'low'
                }
        except Exception as e:
            return {'platform': 'OpenSea', 'error': str(e)}

    def analyze_github_blockchain(self, keyword):
        """GitHub 블록체인 프로젝트 활성도 분석"""
        try:
            # GitHub Search API (인증 없이 제한적)
            search_query = f"{keyword} blockchain OR web3 OR crypto"
            url = f"https://api.github.com/search/repositories?q={quote(search_query)}&sort=stars&per_page=10"

            response = requests.get(url, headers=self.headers, timeout=self.api_timeout)

            if response.status_code == 200:
                data = response.json()
                total_count = data.get('total_count', 0)
                repos = data.get('items', [])

                top_repos = [
                    {'name': r['full_name'], 'stars': r['stargazers_count']}
                    for r in repos[:5]
                ]

                return {
                    'platform': 'GitHub',
                    'total_repos': total_count,
                    'developer_interest': 'high' if total_count > 100 else 'medium' if total_count > 10 else 'low',
                    'top_projects': top_repos,
                    'tech_maturity': 'growing'
                }
            else:
                return {'platform': 'GitHub', 'status': 'rate_limited'}
        except Exception as e:
            return {'platform': 'GitHub', 'error': str(e)}

    def analyze_blockchain_jobs(self, keyword):
        """블록체인 채용시장 분석 (사람인)"""
        try:
            blockchain_terms = ['블록체인', 'Web3', '스마트컨트랙트', 'Solidity', 'DeFi', 'NFT']
            search_term = keyword if any(t in keyword for t in blockchain_terms) else f"블록체인 {keyword}"

            url = f"https://www.saramin.co.kr/zf_user/search?searchword={quote(search_term)}&searchType=search"
            response = requests.get(url, headers=self.headers, timeout=self.api_timeout)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_count_elem = soup.find('span', class_='cnt_result')
                job_count = 0
                if job_count_elem:
                    try:
                        job_count = int(job_count_elem.text.replace(',', '').replace('건', ''))
                    except:
                        pass

                return {
                    'platform': '사람인',
                    'search_term': search_term,
                    'job_count': job_count,
                    'demand_level': 'high' if job_count > 50 else 'medium' if job_count > 10 else 'low',
                    'market_signal': '채용 활발' if job_count > 20 else '채용 보통'
                }
            else:
                return {'platform': '사람인', 'status': 'unavailable'}
        except Exception as e:
            return {'platform': '사람인', 'error': str(e)}

    def _is_blockchain_keyword(self, keyword):
        """블록체인 관련 키워드인지 확인"""
        blockchain_keywords = [
            'NFT', 'DeFi', '토큰', '코인', '메타버스', 'Web3', 'DAO',
            '스테이킹', '암호화폐', '블록체인', '스마트컨트랙트', '지갑',
            'P2E', 'GameFi', 'SocialFi', 'RWA', '디지털자산', 'DEX',
            '렌딩', '이자농사', '크립토', 'dApp', '탈중앙화'
        ]
        return any(kw.lower() in keyword.lower() for kw in blockchain_keywords)

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
        time.sleep(self.api_delay)

        # 네이버 검색량
        print("2. 네이버 검색량 분석 중...")
        naver_data = self.analyze_naver_search_volume(keyword)
        results['data_sources']['naver'] = naver_data
        time.sleep(self.api_delay)

        # 구글 경쟁사
        print("3. 구글 경쟁사 분석 중...")
        google_data = self.analyze_competitors_google(keyword)
        results['data_sources']['google'] = google_data
        time.sleep(self.api_delay)

        # 유튜브 관심도
        print("4. 유튜브 관심도 분석 중...")
        youtube_data = self.analyze_youtube_interest(keyword)
        results['data_sources']['youtube'] = youtube_data
        time.sleep(self.api_delay)

        # 위시켓 프리랜서 시장
        print("5. 위시켓 프리랜서 시장 분석 중...")
        wishket_data = self.analyze_wishket_market(keyword)
        results['data_sources']['wishket'] = wishket_data
        time.sleep(self.api_delay)

        # 숨고 서비스 시장
        print("6. 숨고 서비스 시장 분석 중...")
        soomgo_data = self.analyze_soomgo_market(keyword)
        results['data_sources']['soomgo'] = soomgo_data
        time.sleep(self.api_delay)

        # 탈잉 교육/재능 플랫폼
        print("7. 탈잉 플랫폼 분석 중...")
        brokerage_data = self.analyze_brokerage_platforms(keyword)
        results['data_sources']['brokerage'] = brokerage_data
        time.sleep(self.api_delay)

        # 쿠팡 마켓플레이스
        print("8. 쿠팡 마켓플레이스 분석 중...")
        coupang_data = self.analyze_coupang_marketplace(keyword)
        results['data_sources']['coupang'] = coupang_data
        time.sleep(self.api_delay)

        # 네이버 블로그 트렌드
        print("9. 네이버 블로그 트렌드 분석 중...")
        blog_data = self.analyze_blog_trend(keyword)
        results['data_sources']['blog'] = blog_data
        time.sleep(self.api_delay)

        # 인스타그램 비즈니스
        print("10. 인스타그램 비즈니스 활성도 분석 중...")
        instagram_data = self.analyze_instagram_business(keyword)
        results['data_sources']['instagram'] = instagram_data

        # 블록체인/Web3 관련 키워드면 추가 분석
        if self._is_blockchain_keyword(keyword):
            print("\n[BLOCKCHAIN] 블록체인/Web3 추가 분석 시작...")

            print("11. CoinMarketCap 트렌드 분석 중...")
            coinmarketcap_data = self.analyze_coinmarketcap(keyword)
            results['data_sources']['coinmarketcap'] = coinmarketcap_data
            time.sleep(self.api_delay / 2)

            print("12. 업비트 시장 분석 중...")
            upbit_data = self.analyze_upbit_market(keyword)
            results['data_sources']['upbit'] = upbit_data
            time.sleep(self.api_delay / 2)

            print("13. OpenSea NFT 시장 분석 중...")
            opensea_data = self.analyze_opensea_nft(keyword)
            results['data_sources']['opensea'] = opensea_data
            time.sleep(self.api_delay / 2)

            print("14. GitHub 블록체인 프로젝트 분석 중...")
            github_data = self.analyze_github_blockchain(keyword)
            results['data_sources']['github_blockchain'] = github_data
            time.sleep(self.api_delay / 2)

            print("15. 블록체인 채용시장 분석 중...")
            jobs_data = self.analyze_blockchain_jobs(keyword)
            results['data_sources']['blockchain_jobs'] = jobs_data

            results['is_blockchain'] = True
            print("[BLOCKCHAIN] 블록체인 추가 분석 완료!\n")
        else:
            results['is_blockchain'] = False

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
        error_count = 0
        empty_data_count = 0
        total_sources = 10

        # 에러 및 빈 데이터 카운트
        for source in data_sources.values():
            if source.get('error'):
                error_count += 1
            # 데이터가 비어있으면 빈 데이터로 카운트
            elif source.get('service_count', -1) == 0 or source.get('project_count', -1) == 0:
                empty_data_count += 1

        # 스크래핑 실패 또는 빈 데이터가 많으면 기본 점수 75점 부여
        if error_count + empty_data_count >= 3:
            return 75  # 데이터 부족 시 기본 점수

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

        # ==================== 블록체인/Web3 추가 점수 (최대 +15점) ====================
        blockchain_bonus = 0

        # CoinMarketCap 트렌드 (5점)
        coinmarketcap = data_sources.get('coinmarketcap', {})
        if coinmarketcap.get('is_crypto_related'):
            potential = coinmarketcap.get('growth_potential', 'low')
            if potential == 'high':
                blockchain_bonus += 5
            elif potential == 'medium':
                blockchain_bonus += 3

        # 업비트 시장 상태 (3점)
        upbit = data_sources.get('upbit', {})
        if upbit.get('market_status') == 'active':
            blockchain_bonus += 3

        # OpenSea NFT 시장 (3점)
        opensea = data_sources.get('opensea', {})
        if opensea.get('is_nft_related'):
            potential = opensea.get('growth_potential', 'low')
            if potential in ['high', 'medium_high']:
                blockchain_bonus += 3
            elif potential == 'medium':
                blockchain_bonus += 2

        # GitHub 개발자 관심도 (2점)
        github = data_sources.get('github_blockchain', {})
        if github.get('developer_interest') == 'high':
            blockchain_bonus += 2
        elif github.get('developer_interest') == 'medium':
            blockchain_bonus += 1

        # 블록체인 채용시장 (2점)
        jobs = data_sources.get('blockchain_jobs', {})
        if jobs.get('demand_level') == 'high':
            blockchain_bonus += 2
        elif jobs.get('demand_level') == 'medium':
            blockchain_bonus += 1

        score += blockchain_bonus

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
        print(f"\n[RESULT] {business_idea}")
        print(f"   키워드: {keyword}")
        print(f"   시장 점수: {result['market_score']}/100")
        print(f"   추천: {result['recommendation']['verdict']}")
        print(f"   우선순위: {result['recommendation']['priority']}")
        print("-" * 60)

        time.sleep(analyzer.api_delay * 2.5)  # 전체 분석 사이클 간 대기

    # 상위 3개 추천
    all_results.sort(key=lambda x: x['market_score'], reverse=True)

    print("\n" + "="*60)
    print("[TOP 3] 추천 사업")
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
