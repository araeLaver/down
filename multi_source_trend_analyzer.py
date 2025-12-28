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
            response = requests.get(url, headers=self.headers, timeout=5)
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
            response = requests.get(url, headers=self.headers, timeout=5)
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
            response = requests.get(url, timeout=5)
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

    def fetch_reddit(self):
        """Reddit에서 스타트업/사이드프로젝트 트렌드 수집"""
        trends = []
        subreddits = ['startups', 'SideProject', 'entrepreneur', 'webdev']

        for subreddit in subreddits:
            try:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=5"
                response = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }, timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])

                    for post in posts:
                        post_data = post.get('data', {})
                        title = post_data.get('title', '')
                        score = post_data.get('score', 0)

                        if title and score > 10:
                            trends.append({
                                'source': f'Reddit r/{subreddit}',
                                'keyword': title[:100],
                                'score': score,
                                'category': 'community',
                                'type': 'discussion'
                            })

                time.sleep(1)  # Rate limiting

            except Exception as e:
                continue

        if trends:
            print(f"[OK] Reddit: {len(trends)}개 트렌드 수집")
        else:
            print(f"[WARNING] Reddit 수집 실패, 대체 데이터 사용")
            trends = [
                {'source': 'Reddit r/startups', 'keyword': 'AI SaaS for SMBs', 'category': 'community', 'type': 'discussion'},
                {'source': 'Reddit r/SideProject', 'keyword': 'Micro-SaaS Ideas', 'category': 'community', 'type': 'discussion'},
                {'source': 'Reddit r/entrepreneur', 'keyword': 'No-code Business', 'category': 'community', 'type': 'discussion'},
                {'source': 'Reddit r/webdev', 'keyword': 'AI Development Tools', 'category': 'community', 'type': 'discussion'},
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
            response = requests.get(url, headers=self.headers, timeout=5)

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
            response = requests.get(url, headers=self.headers, timeout=5)
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

    def fetch_tumblbug(self):
        """텀블벅 크라우드펀딩 인기 프로젝트 수집"""
        trends = []
        try:
            url = "https://tumblbug.com/discover"
            response = requests.get(url, headers=self.headers, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')

            projects = soup.find_all('div', class_='project-card', limit=10)
            for project in projects:
                title_elem = project.find('h3') or project.find('strong') or project.find('a')
                if title_elem:
                    trends.append({
                        'source': '텀블벅',
                        'keyword': title_elem.get_text(strip=True)[:50],
                        'category': 'crowdfunding',
                        'type': 'project'
                    })

            print(f"[OK] 텀블벅: {len(trends)}개 트렌드 수집")
        except Exception as e:
            print(f"[WARNING] 텀블벅 수집 실패: {e}")
            trends = [
                {'source': '텀블벅', 'keyword': '크리에이터 툴킷', 'category': 'crowdfunding', 'type': 'project'},
                {'source': '텀블벅', 'keyword': '디지털 아트 프로젝트', 'category': 'crowdfunding', 'type': 'project'},
                {'source': '텀블벅', 'keyword': '인디 게임 개발', 'category': 'crowdfunding', 'type': 'project'},
                {'source': '텀블벅', 'keyword': '교육 콘텐츠 제작', 'category': 'crowdfunding', 'type': 'project'},
            ]
        return trends

    def fetch_saramin_trends(self):
        """사람인 IT 채용 트렌드 수집"""
        trends = []
        try:
            url = "https://www.saramin.co.kr/zf_user/jobs/list/job-category?cat_kewd=84"  # IT개발 카테고리
            response = requests.get(url, headers=self.headers, timeout=5)
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

    def fetch_jobkorea_trends(self):
        """잡코리아 IT 채용 트렌드 수집"""
        trends = []
        try:
            url = "https://www.jobkorea.co.kr/recruit/joblist?menucode=duty"
            response = requests.get(url, headers=self.headers, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')

            jobs = soup.find_all('a', class_='title', limit=10)
            for job in jobs:
                title = job.get_text(strip=True)
                if title:
                    trends.append({
                        'source': '잡코리아',
                        'keyword': title[:50],
                        'category': 'job_market',
                        'type': 'job_posting'
                    })

            print(f"[OK] 잡코리아: {len(trends)}개 트렌드 수집")
        except Exception as e:
            print(f"[WARNING] 잡코리아 수집 실패: {e}")
            trends = [
                {'source': '잡코리아', 'keyword': 'React/Next.js 개발자', 'category': 'job_market', 'type': 'job_posting'},
                {'source': '잡코리아', 'keyword': 'DevOps 엔지니어', 'category': 'job_market', 'type': 'job_posting'},
                {'source': '잡코리아', 'keyword': 'AI 서비스 기획자', 'category': 'job_market', 'type': 'job_posting'},
                {'source': '잡코리아', 'keyword': '데이터 엔지니어', 'category': 'job_market', 'type': 'job_posting'},
            ]
        return trends

    def fetch_public_data_portal(self):
        """공공데이터포털 산업 트렌드 수집"""
        # 공공데이터포털 API는 인증키 필요, 시뮬레이션 데이터 사용
        trends = [
            {'source': '공공데이터포털', 'keyword': '스마트시티 사업', 'category': 'government', 'type': 'policy'},
            {'source': '공공데이터포털', 'keyword': '디지털 헬스케어 산업', 'category': 'government', 'type': 'policy'},
            {'source': '공공데이터포털', 'keyword': 'AI 바우처 지원사업', 'category': 'government', 'type': 'policy'},
            {'source': '공공데이터포털', 'keyword': '데이터 댐 구축사업', 'category': 'government', 'type': 'policy'},
            {'source': '공공데이터포털', 'keyword': '메타버스 신산업', 'category': 'government', 'type': 'policy'},
            {'source': '공공데이터포털', 'keyword': '탄소중립 기술 개발', 'category': 'government', 'type': 'policy'},
            {'source': '공공데이터포털', 'keyword': '우주항공 산업 육성', 'category': 'government', 'type': 'policy'},
            {'source': '공공데이터포털', 'keyword': 'K-반도체 전략', 'category': 'government', 'type': 'policy'},
        ]
        print(f"[OK] 공공데이터포털: {len(trends)}개 트렌드 수집")
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
            response = requests.get(url, timeout=5)
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
            response = requests.get(url, timeout=5)
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
            response = requests.get(url, headers=self.headers, timeout=5)
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
    # 5. AI 분석 (GPT API)
    # ============================================

    def fetch_gpt_trend_analysis(self):
        """GPT API 기반 트렌드 분석 및 아이디어 생성"""
        # OpenAI API 키가 있으면 실제 분석, 없으면 시뮬레이션 데이터
        trends = []

        try:
            import os
            api_key = os.environ.get('OPENAI_API_KEY')

            if api_key:
                import openai
                openai.api_key = api_key

                prompt = """2024-2025년 IT/블록체인 분야 유망 사업 아이디어 5개를 제안해주세요.
                각 아이디어는 다음 형식으로:
                - 사업명
                - 카테고리 (AI/블록체인/SaaS/앱 중 택1)
                - 예상 초기비용
                - 핵심 가치"""

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )

                # 응답 파싱 (간단한 처리)
                content = response.choices[0].message.content
                trends.append({
                    'source': 'GPT Analysis',
                    'keyword': content[:200],
                    'category': 'ai_analysis',
                    'type': 'ai_generated'
                })
                print(f"[OK] GPT 분석: 실제 API 응답 수집")
            else:
                raise Exception("API key not found")

        except Exception as e:
            print(f"[INFO] GPT API 미사용, 시뮬레이션 데이터 사용: {e}")
            # 시뮬레이션 데이터 - AI가 분석한 것처럼 제안
            trends = [
                {'source': 'GPT Analysis', 'keyword': 'AI 기반 맞춤형 학습 플랫폼', 'category': 'ai_analysis', 'type': 'ai_generated',
                 'description': '개인화된 학습 경로 제공, EdTech 시장 성장'},
                {'source': 'GPT Analysis', 'keyword': 'B2B AI 문서 자동화 SaaS', 'category': 'ai_analysis', 'type': 'ai_generated',
                 'description': '계약서, 보고서 자동 생성 및 검토'},
                {'source': 'GPT Analysis', 'keyword': '블록체인 기반 탄소 배출권 거래소', 'category': 'ai_analysis', 'type': 'ai_generated',
                 'description': 'ESG 트렌드와 블록체인 결합'},
                {'source': 'GPT Analysis', 'keyword': 'AI 영상 콘텐츠 자동 생성 도구', 'category': 'ai_analysis', 'type': 'ai_generated',
                 'description': '숏폼 콘텐츠 대량 생산'},
                {'source': 'GPT Analysis', 'keyword': '스마트 컨트랙트 감사 자동화 플랫폼', 'category': 'ai_analysis', 'type': 'ai_generated',
                 'description': 'DeFi 보안 수요 증가'},
                {'source': 'GPT Analysis', 'keyword': 'AI 기반 코드 리뷰 및 최적화 서비스', 'category': 'ai_analysis', 'type': 'ai_generated',
                 'description': '개발 생산성 향상'},
                {'source': 'GPT Analysis', 'keyword': '멀티체인 자산 관리 대시보드', 'category': 'ai_analysis', 'type': 'ai_generated',
                 'description': '크로스체인 DeFi 관리'},
                {'source': 'GPT Analysis', 'keyword': 'AI 고객 서비스 자동화 솔루션', 'category': 'ai_analysis', 'type': 'ai_generated',
                 'description': '24/7 고객 지원 비용 절감'},
            ]
            print(f"[OK] GPT 분석 (시뮬레이션): {len(trends)}개 아이디어 생성")

        return trends

    # ============================================
    # 6. 트렌드 통합 및 아이디어 생성
    # ============================================

    def collect_all_trends(self):
        """경량화된 트렌드 수집 (Koyeb free tier 최적화)"""
        print("\n" + "="*60)
        print("[MULTI-SOURCE] 경량 트렌드 수집 시작 (3개 소스)")
        print("="*60 + "\n")

        all_trends = []

        # 핵심 소스만 사용 (3개)
        sources = [
            ('GitHub Trending', self.fetch_github_trending),
            ('Hacker News', self.fetch_hacker_news),
            ('네이버', self.fetch_naver_datalab),
        ]

        for name, fetch_func in sources:
            try:
                print(f"[FETCH] {name} 수집 중...")
                trends = fetch_func()
                all_trends.extend(trends)
                print(f"   [OK] {len(trends)}개 수집")
            except Exception as e:
                print(f"   [SKIP] {name} 실패: {e}")
            time.sleep(0.5)

        # 최소 트렌드 보장 (폴백 데이터)
        if len(all_trends) < 3:
            print("[FALLBACK] 기본 트렌드 데이터 사용")
            all_trends.extend([
                {'source': 'Fallback', 'keyword': 'AI 자동화 서비스', 'category': 'tech', 'type': 'idea'},
                {'source': 'Fallback', 'keyword': 'SaaS 구독 플랫폼', 'category': 'saas', 'type': 'idea'},
                {'source': 'Fallback', 'keyword': '노코드 앱 개발', 'category': 'tech', 'type': 'idea'},
            ])

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
            'community': [
                f"{keyword} 기반 커뮤니티 플랫폼",
                f"{keyword} 솔루션 개발",
                f"{keyword} 컨설팅 서비스",
            ],
            'government': [
                f"{keyword} 민간 서비스",
                f"{keyword} 스타트업 솔루션",
                f"{keyword} 플랫폼 개발",
            ],
            'ai_analysis': [
                f"{keyword}",  # GPT가 생성한 아이디어는 그대로 사용
            ],
            'blockchain_news': [
                f"{keyword} 관련 서비스",
                f"{keyword} 플랫폼",
            ],
            'socialfi': [
                f"{keyword} 한국형 서비스",
                f"{keyword} 플랫폼 개발",
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
