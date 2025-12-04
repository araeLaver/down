"""
다중 소스 트렌드 분석기
- 글로벌/국내 다양한 소스에서 트렌드 수집
- 블록체인/Web3 트렌드 포함
- AI 기반 아이디어 생성
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import json
import logging
import time

class MultiSourceTrendAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.all_trends = []

    # ============================================
    # 1. 글로벌 트렌드 소스
    # ============================================

    def fetch_product_hunt(self):
        """Product Hunt에서 신규 제품 트렌드 수집"""
        trends = []
        try:
            # Product Hunt 인기 제품 페이지
            url = "https://www.producthunt.com"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 제품명 추출 시도
            products = soup.find_all(['h3', 'h2'], limit=10)
            for product in products:
                text = product.get_text(strip=True)
                if len(text) > 3 and len(text) < 100:
                    trends.append({
                        'source': 'Product Hunt',
                        'keyword': text,
                        'category': 'global_startup',
                        'type': 'product'
                    })

            print(f"[OK] Product Hunt: {len(trends)}개 트렌드 수집")
        except Exception as e:
            print(f"[WARNING] Product Hunt 수집 실패: {e}")
            # 대체 데이터
            trends = [
                {'source': 'Product Hunt', 'keyword': 'AI 코드 리뷰 도구', 'category': 'global_startup', 'type': 'product'},
                {'source': 'Product Hunt', 'keyword': 'No-code 앱 빌더', 'category': 'global_startup', 'type': 'product'},
                {'source': 'Product Hunt', 'keyword': 'AI 영상 생성 플랫폼', 'category': 'global_startup', 'type': 'product'},
            ]
        return trends

    def fetch_github_trending(self):
        """GitHub Trending 저장소에서 기술 트렌드 수집"""
        trends = []
        try:
            url = "https://github.com/trending"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 저장소명 추출
            repos = soup.find_all('article', class_='Box-row', limit=10)
            for repo in repos:
                name_elem = repo.find('h2')
                if name_elem:
                    repo_name = name_elem.get_text(strip=True).replace(' ', '').replace('\n', '')
                    desc_elem = repo.find('p')
                    desc = desc_elem.get_text(strip=True) if desc_elem else ''

                    trends.append({
                        'source': 'GitHub Trending',
                        'keyword': repo_name,
                        'description': desc[:100],
                        'category': 'tech',
                        'type': 'repository'
                    })

            print(f"[OK] GitHub Trending: {len(trends)}개 트렌드 수집")
        except Exception as e:
            print(f"[WARNING] GitHub Trending 수집 실패: {e}")
            trends = [
                {'source': 'GitHub Trending', 'keyword': 'LLM Framework', 'category': 'tech', 'type': 'repository'},
                {'source': 'GitHub Trending', 'keyword': 'AI Agent', 'category': 'tech', 'type': 'repository'},
                {'source': 'GitHub Trending', 'keyword': 'Vector Database', 'category': 'tech', 'type': 'repository'},
            ]
        return trends

    def fetch_hacker_news(self):
        """Hacker News에서 기술 커뮤니티 트렌드 수집"""
        trends = []
        try:
            # HN API 사용
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = requests.get(url, timeout=10)
            story_ids = response.json()[:10]

            for story_id in story_ids:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story = requests.get(story_url, timeout=5).json()
                if story and story.get('title'):
                    trends.append({
                        'source': 'Hacker News',
                        'keyword': story['title'],
                        'score': story.get('score', 0),
                        'category': 'tech_community',
                        'type': 'discussion'
                    })

            print(f"[OK] Hacker News: {len(trends)}개 트렌드 수집")
        except Exception as e:
            print(f"[WARNING] Hacker News 수집 실패: {e}")
            trends = [
                {'source': 'Hacker News', 'keyword': 'AI Startup Trends', 'category': 'tech_community', 'type': 'discussion'},
                {'source': 'Hacker News', 'keyword': 'Open Source AI', 'category': 'tech_community', 'type': 'discussion'},
            ]
        return trends

    # ============================================
    # 2. 국내 트렌드 소스
    # ============================================

    def fetch_naver_datalab(self):
        """네이버 데이터랩 트렌드 수집"""
        trends = []
        try:
            # 네이버 트렌드 관련 키워드 (API 없이 시뮬레이션)
            # 실제로는 네이버 API 사용 권장
            url = "https://datalab.naver.com/keyword/realtimeList.naver"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                keywords = soup.find_all('span', class_='item_title', limit=10)
                for kw in keywords:
                    trends.append({
                        'source': '네이버 데이터랩',
                        'keyword': kw.get_text(strip=True),
                        'category': 'korea_search',
                        'type': 'search_trend'
                    })

            print(f"[OK] 네이버 데이터랩: {len(trends)}개 트렌드 수집")
        except Exception as e:
            print(f"[WARNING] 네이버 데이터랩 수집 실패: {e}")
            # 대체 데이터 - 최신 IT 트렌드
            trends = [
                {'source': '네이버 데이터랩', 'keyword': 'ChatGPT 활용', 'category': 'korea_search', 'type': 'search_trend'},
                {'source': '네이버 데이터랩', 'keyword': '1인 창업', 'category': 'korea_search', 'type': 'search_trend'},
                {'source': '네이버 데이터랩', 'keyword': '자동화 툴', 'category': 'korea_search', 'type': 'search_trend'},
                {'source': '네이버 데이터랩', 'keyword': 'AI 부업', 'category': 'korea_search', 'type': 'search_trend'},
            ]
        return trends

    def fetch_wadiz(self):
        """와디즈 크라우드펀딩 인기 프로젝트 수집"""
        trends = []
        try:
            url = "https://www.wadiz.kr/web/wreward/category/308"  # 테크/가전 카테고리
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            projects = soup.find_all('div', class_='ProjectCardList_item', limit=10)
            for project in projects:
                title_elem = project.find('h4') or project.find('strong')
                if title_elem:
                    trends.append({
                        'source': '와디즈',
                        'keyword': title_elem.get_text(strip=True),
                        'category': 'crowdfunding',
                        'type': 'project'
                    })

            print(f"[OK] 와디즈: {len(trends)}개 트렌드 수집")
        except Exception as e:
            print(f"[WARNING] 와디즈 수집 실패: {e}")
            trends = [
                {'source': '와디즈', 'keyword': '스마트 홈 디바이스', 'category': 'crowdfunding', 'type': 'project'},
                {'source': '와디즈', 'keyword': 'AI 학습 기기', 'category': 'crowdfunding', 'type': 'project'},
                {'source': '와디즈', 'keyword': '헬스케어 웨어러블', 'category': 'crowdfunding', 'type': 'project'},
            ]
        return trends

    def fetch_saramin_trends(self):
        """사람인 IT 채용 트렌드 수집"""
        trends = []
        try:
            url = "https://www.saramin.co.kr/zf_user/jobs/list/job-category?cat_kewd=84"  # IT개발 카테고리
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            jobs = soup.find_all('h2', class_='job_tit', limit=10)
            for job in jobs:
                trends.append({
                    'source': '사람인',
                    'keyword': job.get_text(strip=True),
                    'category': 'job_market',
                    'type': 'job_posting'
                })

            print(f"[OK] 사람인: {len(trends)}개 트렌드 수집")
        except Exception as e:
            print(f"[WARNING] 사람인 수집 실패: {e}")
            trends = [
                {'source': '사람인', 'keyword': 'AI/ML 엔지니어', 'category': 'job_market', 'type': 'job_posting'},
                {'source': '사람인', 'keyword': '블록체인 개발자', 'category': 'job_market', 'type': 'job_posting'},
                {'source': '사람인', 'keyword': '클라우드 아키텍트', 'category': 'job_market', 'type': 'job_posting'},
            ]
        return trends

    # ============================================
    # 3. 앱 마켓 트렌드
    # ============================================

    def fetch_app_store_trends(self):
        """앱스토어/플레이스토어 트렌드 (시뮬레이션)"""
        # 실제로는 App Store Connect API 또는 Sensor Tower 등 사용
        trends = [
            {'source': 'App Store', 'keyword': 'AI 사진 편집 앱', 'category': 'app_market', 'type': 'app'},
            {'source': 'App Store', 'keyword': '명상/마인드풀니스 앱', 'category': 'app_market', 'type': 'app'},
            {'source': 'App Store', 'keyword': '가계부/재테크 앱', 'category': 'app_market', 'type': 'app'},
            {'source': 'Google Play', 'keyword': 'AI 챗봇 앱', 'category': 'app_market', 'type': 'app'},
            {'source': 'Google Play', 'keyword': '습관 트래커', 'category': 'app_market', 'type': 'app'},
            {'source': 'Google Play', 'keyword': '언어 학습 AI', 'category': 'app_market', 'type': 'app'},
        ]
        print(f"[OK] 앱 마켓: {len(trends)}개 트렌드 수집")
        return trends

    # ============================================
    # 4. 블록체인 / Web3 트렌드
    # ============================================

    def fetch_coingecko_trends(self):
        """CoinGecko에서 암호화폐 트렌드 수집"""
        trends = []
        try:
            url = "https://api.coingecko.com/api/v3/search/trending"
            response = requests.get(url, timeout=10)
            data = response.json()

            for coin in data.get('coins', [])[:7]:
                item = coin.get('item', {})
                trends.append({
                    'source': 'CoinGecko',
                    'keyword': item.get('name', ''),
                    'symbol': item.get('symbol', ''),
                    'rank': item.get('market_cap_rank', 0),
                    'category': 'blockchain',
                    'type': 'cryptocurrency'
                })

            print(f"[OK] CoinGecko: {len(trends)}개 트렌드 수집")
        except Exception as e:
            print(f"[WARNING] CoinGecko 수집 실패: {e}")
            trends = [
                {'source': 'CoinGecko', 'keyword': 'Bitcoin', 'category': 'blockchain', 'type': 'cryptocurrency'},
                {'source': 'CoinGecko', 'keyword': 'Ethereum', 'category': 'blockchain', 'type': 'cryptocurrency'},
                {'source': 'CoinGecko', 'keyword': 'Solana', 'category': 'blockchain', 'type': 'cryptocurrency'},
            ]
        return trends

    def fetch_defillama(self):
        """DeFi Llama에서 DeFi 트렌드 수집"""
        trends = []
        try:
            url = "https://api.llama.fi/protocols"
            response = requests.get(url, timeout=10)
            protocols = response.json()[:10]

            for protocol in protocols:
                trends.append({
                    'source': 'DeFi Llama',
                    'keyword': protocol.get('name', ''),
                    'tvl': protocol.get('tvl', 0),
                    'chain': protocol.get('chain', ''),
                    'category': 'defi',
                    'type': 'protocol'
                })

            print(f"[OK] DeFi Llama: {len(trends)}개 트렌드 수집")
        except Exception as e:
            print(f"[WARNING] DeFi Llama 수집 실패: {e}")
            trends = [
                {'source': 'DeFi Llama', 'keyword': 'Lido', 'category': 'defi', 'type': 'protocol'},
                {'source': 'DeFi Llama', 'keyword': 'Aave', 'category': 'defi', 'type': 'protocol'},
                {'source': 'DeFi Llama', 'keyword': 'Uniswap', 'category': 'defi', 'type': 'protocol'},
            ]
        return trends

    def fetch_nft_trends(self):
        """NFT 마켓플레이스 트렌드 수집"""
        trends = []
        try:
            # OpenSea는 API 키 필요, 대체 데이터 사용
            trends = [
                {'source': 'NFT Market', 'keyword': 'PFP NFT 컬렉션', 'category': 'nft', 'type': 'collection'},
                {'source': 'NFT Market', 'keyword': 'AI 생성 NFT', 'category': 'nft', 'type': 'collection'},
                {'source': 'NFT Market', 'keyword': '게임 NFT 아이템', 'category': 'nft', 'type': 'gaming'},
                {'source': 'NFT Market', 'keyword': '음악 NFT', 'category': 'nft', 'type': 'music'},
                {'source': 'NFT Market', 'keyword': 'RWA 토큰화', 'category': 'nft', 'type': 'rwa'},
            ]
            print(f"[OK] NFT 트렌드: {len(trends)}개 수집")
        except Exception as e:
            print(f"[WARNING] NFT 트렌드 수집 실패: {e}")
        return trends

    def fetch_web3_trends(self):
        """Web3 생태계 트렌드"""
        trends = [
            # Layer 2 & Scaling
            {'source': 'Web3', 'keyword': 'Layer 2 솔루션 (Arbitrum, Optimism)', 'category': 'blockchain', 'type': 'infrastructure'},
            {'source': 'Web3', 'keyword': 'ZK Rollup 기술', 'category': 'blockchain', 'type': 'infrastructure'},

            # DeFi 2.0
            {'source': 'Web3', 'keyword': 'Real Yield DeFi', 'category': 'defi', 'type': 'protocol'},
            {'source': 'Web3', 'keyword': 'DEX Aggregator', 'category': 'defi', 'type': 'protocol'},
            {'source': 'Web3', 'keyword': 'Liquid Staking', 'category': 'defi', 'type': 'protocol'},

            # GameFi & SocialFi
            {'source': 'Web3', 'keyword': 'Play-to-Earn 게임', 'category': 'gamefi', 'type': 'gaming'},
            {'source': 'Web3', 'keyword': 'Move-to-Earn', 'category': 'gamefi', 'type': 'fitness'},
            {'source': 'Web3', 'keyword': 'SocialFi 플랫폼', 'category': 'socialfi', 'type': 'social'},

            # DAOs & Governance
            {'source': 'Web3', 'keyword': 'DAO 거버넌스 툴', 'category': 'dao', 'type': 'governance'},
            {'source': 'Web3', 'keyword': 'DAO 트레저리 관리', 'category': 'dao', 'type': 'treasury'},

            # RWA (Real World Assets)
            {'source': 'Web3', 'keyword': '부동산 토큰화', 'category': 'rwa', 'type': 'real_estate'},
            {'source': 'Web3', 'keyword': '채권 토큰화', 'category': 'rwa', 'type': 'bonds'},

            # AI + Blockchain
            {'source': 'Web3', 'keyword': 'AI Agent 온체인', 'category': 'ai_blockchain', 'type': 'ai'},
            {'source': 'Web3', 'keyword': '분산 AI 컴퓨팅', 'category': 'ai_blockchain', 'type': 'compute'},
            {'source': 'Web3', 'keyword': 'AI 데이터 마켓플레이스', 'category': 'ai_blockchain', 'type': 'data'},
        ]
        print(f"[OK] Web3 트렌드: {len(trends)}개 수집")
        return trends

    def fetch_blockchain_news(self):
        """블록체인 뉴스 트렌드"""
        trends = []
        try:
            # CoinDesk RSS 또는 API
            url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'xml')

            items = soup.find_all('item', limit=10)
            for item in items:
                title = item.find('title')
                if title:
                    trends.append({
                        'source': 'CoinDesk',
                        'keyword': title.get_text(strip=True),
                        'category': 'blockchain_news',
                        'type': 'news'
                    })

            print(f"[OK] 블록체인 뉴스: {len(trends)}개 수집")
        except Exception as e:
            print(f"[WARNING] 블록체인 뉴스 수집 실패: {e}")
            trends = [
                {'source': 'CoinDesk', 'keyword': 'Bitcoin ETF 승인', 'category': 'blockchain_news', 'type': 'news'},
                {'source': 'CoinDesk', 'keyword': 'Ethereum 업그레이드', 'category': 'blockchain_news', 'type': 'news'},
                {'source': 'CoinDesk', 'keyword': '기관 투자 확대', 'category': 'blockchain_news', 'type': 'news'},
            ]
        return trends

    # ============================================
    # 5. 트렌드 통합 및 아이디어 생성
    # ============================================

    def collect_all_trends(self):
        """모든 소스에서 트렌드 수집"""
        print("\n" + "="*60)
        print("[MULTI-SOURCE] 다중 소스 트렌드 수집 시작")
        print("="*60 + "\n")

        all_trends = []

        # 글로벌 트렌드
        print("[GLOBAL] 글로벌 트렌드 수집...")
        all_trends.extend(self.fetch_product_hunt())
        time.sleep(1)
        all_trends.extend(self.fetch_github_trending())
        time.sleep(1)
        all_trends.extend(self.fetch_hacker_news())
        time.sleep(1)

        # 국내 트렌드
        print("\n[KOREA] 국내 트렌드 수집...")
        all_trends.extend(self.fetch_naver_datalab())
        time.sleep(1)
        all_trends.extend(self.fetch_wadiz())
        time.sleep(1)
        all_trends.extend(self.fetch_saramin_trends())
        time.sleep(1)

        # 앱 마켓
        print("\n[APP] 앱 마켓 트렌드 수집...")
        all_trends.extend(self.fetch_app_store_trends())

        # 블록체인 / Web3
        print("\n[BLOCKCHAIN] 블록체인/Web3 트렌드 수집...")
        all_trends.extend(self.fetch_coingecko_trends())
        time.sleep(1)
        all_trends.extend(self.fetch_defillama())
        time.sleep(1)
        all_trends.extend(self.fetch_nft_trends())
        all_trends.extend(self.fetch_web3_trends())
        all_trends.extend(self.fetch_blockchain_news())

        self.all_trends = all_trends

        print(f"\n{'='*60}")
        print(f"[TOTAL] 총 {len(all_trends)}개 트렌드 수집 완료")
        print(f"{'='*60}\n")

        return all_trends

    def generate_business_ideas(self, num_ideas=1):
        """수집된 트렌드 기반으로 사업 아이디어 생성"""
        if not self.all_trends:
            self.collect_all_trends()

        ideas = []
        used_trends = random.sample(self.all_trends, min(num_ideas * 3, len(self.all_trends)))

        for trend in used_trends[:num_ideas]:
            idea = self._transform_trend_to_idea(trend)
            if idea:
                ideas.append(idea)

        return ideas

    def _transform_trend_to_idea(self, trend):
        """트렌드를 사업 아이디어로 변환"""
        source = trend.get('source', '')
        keyword = trend.get('keyword', '')
        category = trend.get('category', '')
        trend_type = trend.get('type', '')

        # 카테고리별 아이디어 생성 템플릿
        idea_templates = {
            'global_startup': [
                f"{keyword} 한국 현지화 서비스",
                f"{keyword} 기반 B2B SaaS",
                f"{keyword} API 서비스",
            ],
            'tech': [
                f"{keyword} 활용 자동화 플랫폼",
                f"{keyword} 기반 개발 도구",
                f"{keyword} 교육 플랫폼",
            ],
            'tech_community': [
                f"{keyword} 관련 컨설팅 서비스",
                f"{keyword} 솔루션 개발",
            ],
            'korea_search': [
                f"{keyword} 전문 플랫폼",
                f"{keyword} AI 어시스턴트",
                f"{keyword} 매칭 서비스",
            ],
            'crowdfunding': [
                f"{keyword} 구독 서비스",
                f"{keyword} 렌탈 플랫폼",
            ],
            'job_market': [
                f"{keyword} 교육 플랫폼",
                f"{keyword} 매칭 서비스",
                f"{keyword} 아웃소싱 플랫폼",
            ],
            'app_market': [
                f"{keyword} 웹 버전",
                f"{keyword} B2B 솔루션",
                f"{keyword} 화이트라벨",
            ],
            'blockchain': [
                f"{keyword} 기반 결제 솔루션",
                f"{keyword} 지갑 서비스",
                f"{keyword} 데이터 분석 플랫폼",
            ],
            'defi': [
                f"{keyword} 유형 한국형 서비스",
                f"{keyword} 수익률 분석 도구",
                f"기업용 {keyword} 솔루션",
            ],
            'nft': [
                f"{keyword} 마켓플레이스",
                f"{keyword} 생성 플랫폼",
                f"기업용 {keyword} 솔루션",
            ],
            'gamefi': [
                f"{keyword} 플랫폼",
                f"{keyword} 길드 관리 도구",
                f"{keyword} 분석 서비스",
            ],
            'dao': [
                f"{keyword} 플랫폼",
                f"한국형 {keyword}",
            ],
            'rwa': [
                f"{keyword} 플랫폼",
                f"소액 {keyword} 서비스",
            ],
            'ai_blockchain': [
                f"{keyword} 서비스",
                f"기업용 {keyword}",
            ],
        }

        templates = idea_templates.get(category, [f"{keyword} 기반 IT 서비스"])
        idea_name = random.choice(templates)

        # 초기 비용 추정
        if category in ['blockchain', 'defi', 'nft', 'rwa', 'ai_blockchain']:
            startup_cost = random.randint(500, 2000) * 10000  # 500만~2000만원
            monthly_revenue = random.randint(300, 1500) * 10000
        else:
            startup_cost = random.randint(100, 500) * 10000  # 100만~500만원
            monthly_revenue = random.randint(200, 800) * 10000

        return {
            'business': {
                'name': idea_name,
                'source': source,
                'original_keyword': keyword,
                'category': category,
                'type': trend_type,
                'startup_cost': f"{startup_cost // 10000}만원",
                'monthly_revenue': f"{monthly_revenue // 10000}만원",
                'description': f"{source}에서 발굴된 '{keyword}' 트렌드 기반 사업 아이디어",
                'global_potential': category in ['global_startup', 'blockchain', 'defi', 'nft', 'web3'],
            },
            'priority': '높음' if category in ['blockchain', 'ai_blockchain', 'global_startup'] else '보통',
            'trend_data': trend
        }

    def get_trend_summary(self):
        """트렌드 요약 통계"""
        if not self.all_trends:
            return {}

        summary = {}
        for trend in self.all_trends:
            category = trend.get('category', 'unknown')
            source = trend.get('source', 'unknown')

            if category not in summary:
                summary[category] = {'count': 0, 'sources': set()}
            summary[category]['count'] += 1
            summary[category]['sources'].add(source)

        # set을 list로 변환
        for cat in summary:
            summary[cat]['sources'] = list(summary[cat]['sources'])

        return summary


# 테스트
if __name__ == "__main__":
    analyzer = MultiSourceTrendAnalyzer()

    # 모든 트렌드 수집
    trends = analyzer.collect_all_trends()

    # 요약 출력
    print("\n[SUMMARY] 카테고리별 트렌드:")
    summary = analyzer.get_trend_summary()
    for cat, data in summary.items():
        print(f"  - {cat}: {data['count']}개 ({', '.join(data['sources'])})")

    # 아이디어 생성
    print("\n[IDEAS] 생성된 사업 아이디어:")
    ideas = analyzer.generate_business_ideas(num_ideas=3)
    for i, idea in enumerate(ideas, 1):
        biz = idea['business']
        print(f"\n{i}. {biz['name']}")
        print(f"   출처: {biz['source']} - {biz['original_keyword']}")
        print(f"   카테고리: {biz['category']}")
        print(f"   초기비용: {biz['startup_cost']}, 예상수익: {biz['monthly_revenue']}/월")
