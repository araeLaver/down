"""
경량 시장 분석 모듈 (Lightweight Market Analyzer)
- 외부 API 호출 없이 사전 정의된 데이터 기반 분석
- Koyeb 무료 티어 메모리 제약에 최적화
- 업종별/도메인별 정교한 점수 산정
"""

import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class LightweightMarketAnalyzer:
    def __init__(self):
        # IT 사업 유형별 기본 점수 및 특성 (12개 유형)
        self.it_type_scores = {
            # 고성장/고수익 유형
            "saas": {
                "base_score": 76,
                "market_growth": "높음",
                "competition": "중간",
                "entry_barrier": "낮음",
                "scalability": "매우 높음",
                "recurring_revenue": True,
                "avg_margin": 70,
                "time_to_profit": "6-12개월",
                "best_domains": ["AI", "자동화", "생산성", "협업"]
            },
            "ai_service": {
                "base_score": 80,
                "market_growth": "매우 높음",
                "competition": "중간",
                "entry_barrier": "중간",
                "scalability": "매우 높음",
                "recurring_revenue": True,
                "avg_margin": 75,
                "time_to_profit": "3-6개월",
                "best_domains": ["AI", "자동화", "콘텐츠", "마케팅"]
            },
            "mobile_app": {
                "base_score": 72,
                "market_growth": "보통",
                "competition": "높음",
                "entry_barrier": "중간",
                "scalability": "높음",
                "recurring_revenue": True,
                "avg_margin": 65,
                "time_to_profit": "6-12개월",
                "best_domains": ["헬스케어", "피트니스", "생산성", "소셜"]
            },
            "marketplace": {
                "base_score": 71,
                "market_growth": "높음",
                "competition": "높음",
                "entry_barrier": "중간",
                "scalability": "매우 높음",
                "recurring_revenue": False,
                "avg_margin": 15,
                "time_to_profit": "12-18개월",
                "best_domains": ["프리랜서", "중고거래", "서비스매칭"]
            },
            "agency": {
                "base_score": 68,
                "market_growth": "보통",
                "competition": "높음",
                "entry_barrier": "낮음",
                "scalability": "낮음",
                "recurring_revenue": True,
                "avg_margin": 40,
                "time_to_profit": "1-3개월",
                "best_domains": ["마케팅", "디자인", "개발", "컨설팅"]
            },
            "tools": {
                "base_score": 70,
                "market_growth": "보통",
                "competition": "중간",
                "entry_barrier": "중간",
                "scalability": "높음",
                "recurring_revenue": False,
                "avg_margin": 60,
                "time_to_profit": "3-6개월",
                "best_domains": ["생산성", "개발도구", "디자인", "분석"]
            },
            "platform": {
                "base_score": 73,
                "market_growth": "높음",
                "competition": "중간",
                "entry_barrier": "중간",
                "scalability": "매우 높음",
                "recurring_revenue": True,
                "avg_margin": 50,
                "time_to_profit": "12-24개월",
                "best_domains": ["교육", "커뮤니티", "콘텐츠", "커머스"]
            },
            # 추가 유형들
            "chrome_extension": {
                "base_score": 69,
                "market_growth": "보통",
                "competition": "낮음",
                "entry_barrier": "매우 낮음",
                "scalability": "높음",
                "recurring_revenue": True,
                "avg_margin": 80,
                "time_to_profit": "1-3개월",
                "best_domains": ["생산성", "AI", "SEO", "소셜미디어"]
            },
            "api_service": {
                "base_score": 74,
                "market_growth": "높음",
                "competition": "낮음",
                "entry_barrier": "중간",
                "scalability": "매우 높음",
                "recurring_revenue": True,
                "avg_margin": 85,
                "time_to_profit": "3-6개월",
                "best_domains": ["AI", "데이터", "결제", "인증"]
            },
            "consulting": {
                "base_score": 66,
                "market_growth": "보통",
                "competition": "높음",
                "entry_barrier": "낮음",
                "scalability": "매우 낮음",
                "recurring_revenue": True,
                "avg_margin": 60,
                "time_to_profit": "즉시",
                "best_domains": ["전략", "기술", "마케팅", "법률"]
            },
            "content_business": {
                "base_score": 67,
                "market_growth": "높음",
                "competition": "높음",
                "entry_barrier": "낮음",
                "scalability": "중간",
                "recurring_revenue": True,
                "avg_margin": 50,
                "time_to_profit": "3-6개월",
                "best_domains": ["교육", "엔터테인먼트", "정보", "취미"]
            },
            "nocode_solution": {
                "base_score": 75,
                "market_growth": "매우 높음",
                "competition": "중간",
                "entry_barrier": "낮음",
                "scalability": "높음",
                "recurring_revenue": True,
                "avg_margin": 70,
                "time_to_profit": "1-3개월",
                "best_domains": ["자동화", "웹사이트", "앱개발", "데이터"]
            }
        }

        # 도메인별 시장 규모 및 트렌드 데이터 (한국 기준, 2025)
        self.domain_market_data = {
            # === AI/자동화 분야 (최고 성장) ===
            "AI": {"market_size": "대형", "growth_rate": 40, "trend": "급상승", "score_bonus": 18, "category": "tech"},
            "자동화": {"market_size": "대형", "growth_rate": 35, "trend": "급상승", "score_bonus": 16, "category": "tech"},
            "생성AI": {"market_size": "대형", "growth_rate": 50, "trend": "급상승", "score_bonus": 20, "category": "tech"},
            "챗봇": {"market_size": "중형", "growth_rate": 30, "trend": "급상승", "score_bonus": 14, "category": "tech"},
            "RPA": {"market_size": "중형", "growth_rate": 25, "trend": "상승", "score_bonus": 12, "category": "tech"},

            # === 헬스/웰니스 분야 ===
            "헬스케어": {"market_size": "대형", "growth_rate": 15, "trend": "상승", "score_bonus": 12, "category": "health"},
            "피트니스": {"market_size": "중형", "growth_rate": 10, "trend": "상승", "score_bonus": 8, "category": "health"},
            "멘탈헬스": {"market_size": "중형", "growth_rate": 25, "trend": "급상승", "score_bonus": 14, "category": "health"},
            "수면": {"market_size": "중형", "growth_rate": 28, "trend": "급상승", "score_bonus": 14, "category": "health"},
            "명상": {"market_size": "소형", "growth_rate": 22, "trend": "상승", "score_bonus": 10, "category": "health"},
            "다이어트": {"market_size": "대형", "growth_rate": 8, "trend": "안정", "score_bonus": 6, "category": "health"},
            "영양": {"market_size": "중형", "growth_rate": 12, "trend": "상승", "score_bonus": 8, "category": "health"},

            # === 시니어/실버 분야 (고성장) ===
            "시니어": {"market_size": "대형", "growth_rate": 22, "trend": "급상승", "score_bonus": 15, "category": "senior"},
            "실버케어": {"market_size": "대형", "growth_rate": 20, "trend": "급상승", "score_bonus": 14, "category": "senior"},
            "요양": {"market_size": "대형", "growth_rate": 18, "trend": "상승", "score_bonus": 12, "category": "senior"},
            "시니어일자리": {"market_size": "중형", "growth_rate": 25, "trend": "급상승", "score_bonus": 14, "category": "senior"},

            # === 반려동물 분야 (고성장) ===
            "반려동물": {"market_size": "대형", "growth_rate": 18, "trend": "급상승", "score_bonus": 14, "category": "pet"},
            "펫": {"market_size": "대형", "growth_rate": 18, "trend": "급상승", "score_bonus": 14, "category": "pet"},
            "펫시터": {"market_size": "소형", "growth_rate": 25, "trend": "급상승", "score_bonus": 12, "category": "pet"},
            "펫푸드": {"market_size": "중형", "growth_rate": 15, "trend": "상승", "score_bonus": 10, "category": "pet"},
            "동물병원": {"market_size": "중형", "growth_rate": 12, "trend": "상승", "score_bonus": 8, "category": "pet"},

            # === 교육 분야 ===
            "교육": {"market_size": "대형", "growth_rate": 10, "trend": "상승", "score_bonus": 8, "category": "edu"},
            "코딩교육": {"market_size": "중형", "growth_rate": 18, "trend": "상승", "score_bonus": 12, "category": "edu"},
            "언어": {"market_size": "대형", "growth_rate": 8, "trend": "안정", "score_bonus": 6, "category": "edu"},
            "자격증": {"market_size": "중형", "growth_rate": 10, "trend": "상승", "score_bonus": 7, "category": "edu"},
            "취업": {"market_size": "대형", "growth_rate": 12, "trend": "상승", "score_bonus": 9, "category": "edu"},
            "이러닝": {"market_size": "대형", "growth_rate": 15, "trend": "상승", "score_bonus": 10, "category": "edu"},

            # === 금융/투자 분야 ===
            "재테크": {"market_size": "대형", "growth_rate": 18, "trend": "급상승", "score_bonus": 12, "category": "finance"},
            "투자": {"market_size": "대형", "growth_rate": 15, "trend": "상승", "score_bonus": 10, "category": "finance"},
            "주식": {"market_size": "대형", "growth_rate": 10, "trend": "안정", "score_bonus": 7, "category": "finance"},
            "부동산": {"market_size": "대형", "growth_rate": 5, "trend": "안정", "score_bonus": 5, "category": "finance"},
            "보험": {"market_size": "대형", "growth_rate": 6, "trend": "안정", "score_bonus": 5, "category": "finance"},
            "가계부": {"market_size": "중형", "growth_rate": 12, "trend": "상승", "score_bonus": 8, "category": "finance"},

            # === 라이프스타일 분야 ===
            "1인가구": {"market_size": "대형", "growth_rate": 15, "trend": "상승", "score_bonus": 11, "category": "lifestyle"},
            "싱글": {"market_size": "대형", "growth_rate": 12, "trend": "상승", "score_bonus": 9, "category": "lifestyle"},
            "육아": {"market_size": "중형", "growth_rate": 8, "trend": "안정", "score_bonus": 6, "category": "lifestyle"},
            "신혼": {"market_size": "소형", "growth_rate": 5, "trend": "안정", "score_bonus": 4, "category": "lifestyle"},
            "취미": {"market_size": "중형", "growth_rate": 12, "trend": "상승", "score_bonus": 8, "category": "lifestyle"},
            "여행": {"market_size": "대형", "growth_rate": 10, "trend": "상승", "score_bonus": 7, "category": "lifestyle"},

            # === 커머스/리테일 ===
            "이커머스": {"market_size": "대형", "growth_rate": 8, "trend": "안정", "score_bonus": 5, "category": "commerce"},
            "쇼핑": {"market_size": "대형", "growth_rate": 5, "trend": "포화", "score_bonus": 3, "category": "commerce"},
            "배달": {"market_size": "대형", "growth_rate": 3, "trend": "포화", "score_bonus": 2, "category": "commerce"},
            "중고거래": {"market_size": "대형", "growth_rate": 12, "trend": "상승", "score_bonus": 8, "category": "commerce"},
            "구독커머스": {"market_size": "중형", "growth_rate": 18, "trend": "상승", "score_bonus": 11, "category": "commerce"},
            "라이브커머스": {"market_size": "중형", "growth_rate": 20, "trend": "상승", "score_bonus": 12, "category": "commerce"},

            # === 마케팅/비즈니스 ===
            "마케팅": {"market_size": "대형", "growth_rate": 12, "trend": "상승", "score_bonus": 9, "category": "biz"},
            "SNS마케팅": {"market_size": "중형", "growth_rate": 15, "trend": "상승", "score_bonus": 10, "category": "biz"},
            "SEO": {"market_size": "중형", "growth_rate": 10, "trend": "상승", "score_bonus": 8, "category": "biz"},
            "인플루언서": {"market_size": "중형", "growth_rate": 15, "trend": "상승", "score_bonus": 9, "category": "biz"},
            "CRM": {"market_size": "중형", "growth_rate": 14, "trend": "상승", "score_bonus": 10, "category": "biz"},
            "HR": {"market_size": "대형", "growth_rate": 12, "trend": "상승", "score_bonus": 9, "category": "biz"},

            # === ESG/친환경 (신규 성장) ===
            "ESG": {"market_size": "중형", "growth_rate": 30, "trend": "급상승", "score_bonus": 15, "category": "green"},
            "친환경": {"market_size": "중형", "growth_rate": 22, "trend": "급상승", "score_bonus": 12, "category": "green"},
            "탄소중립": {"market_size": "소형", "growth_rate": 35, "trend": "급상승", "score_bonus": 14, "category": "green"},
            "리사이클": {"market_size": "소형", "growth_rate": 20, "trend": "상승", "score_bonus": 10, "category": "green"},

            # === 블록체인/Web3 (회복세) ===
            "블록체인": {"market_size": "중형", "growth_rate": 10, "trend": "회복", "score_bonus": 6, "category": "web3"},
            "Web3": {"market_size": "소형", "growth_rate": 12, "trend": "회복", "score_bonus": 6, "category": "web3"},
            "DeFi": {"market_size": "소형", "growth_rate": 8, "trend": "회복", "score_bonus": 4, "category": "web3"},
            "NFT": {"market_size": "소형", "growth_rate": -5, "trend": "하락", "score_bonus": -3, "category": "web3"},
            "메타버스": {"market_size": "소형", "growth_rate": -3, "trend": "하락", "score_bonus": -2, "category": "web3"},

            # === 기타/전문 분야 ===
            "법률": {"market_size": "중형", "growth_rate": 10, "trend": "상승", "score_bonus": 8, "category": "pro"},
            "회계": {"market_size": "중형", "growth_rate": 8, "trend": "안정", "score_bonus": 6, "category": "pro"},
            "디자인": {"market_size": "중형", "growth_rate": 10, "trend": "상승", "score_bonus": 7, "category": "pro"},
            "개발": {"market_size": "대형", "growth_rate": 15, "trend": "상승", "score_bonus": 10, "category": "pro"},
            "프리랜서": {"market_size": "대형", "growth_rate": 18, "trend": "상승", "score_bonus": 11, "category": "pro"},

            # === 엔터테인먼트/콘텐츠 ===
            "게임": {"market_size": "대형", "growth_rate": 8, "trend": "안정", "score_bonus": 5, "category": "ent"},
            "음악": {"market_size": "중형", "growth_rate": 10, "trend": "상승", "score_bonus": 7, "category": "ent"},
            "영상": {"market_size": "대형", "growth_rate": 15, "trend": "상승", "score_bonus": 9, "category": "ent"},
            "웹툰": {"market_size": "중형", "growth_rate": 12, "trend": "상승", "score_bonus": 8, "category": "ent"},
            "스트리밍": {"market_size": "대형", "growth_rate": 10, "trend": "안정", "score_bonus": 6, "category": "ent"},
        }

        # 도메인 시너지 매트릭스 (조합 보너스)
        self.domain_synergy = {
            ("AI", "헬스케어"): 8,
            ("AI", "교육"): 7,
            ("AI", "마케팅"): 8,
            ("AI", "시니어"): 9,
            ("시니어", "헬스케어"): 10,
            ("반려동물", "헬스케어"): 6,
            ("1인가구", "반려동물"): 7,
            ("ESG", "이커머스"): 6,
            ("자동화", "마케팅"): 8,
            ("자동화", "HR"): 7,
        }

        # 타겟 고객층별 시장 규모 (한국 기준, 2025 업데이트)
        self.target_audience_data = {
            # === 직업 기반 ===
            "직장인": {"population": 2800, "digital_affinity": "높음", "spending_power": "높음", "score_bonus": 8, "category": "job"},
            "프리랜서": {"population": 250, "digital_affinity": "매우 높음", "spending_power": "중간", "score_bonus": 7, "category": "job"},
            "자영업자": {"population": 550, "digital_affinity": "중간", "spending_power": "중간", "score_bonus": 6, "category": "job"},
            "소상공인": {"population": 600, "digital_affinity": "중간", "spending_power": "중간", "score_bonus": 6, "category": "job"},
            "전문직": {"population": 200, "digital_affinity": "높음", "spending_power": "매우 높음", "score_bonus": 9, "category": "job"},
            "크리에이터": {"population": 80, "digital_affinity": "매우 높음", "spending_power": "중간", "score_bonus": 7, "category": "job"},
            "개발자": {"population": 150, "digital_affinity": "매우 높음", "spending_power": "높음", "score_bonus": 8, "category": "job"},
            "마케터": {"population": 100, "digital_affinity": "매우 높음", "spending_power": "높음", "score_bonus": 8, "category": "job"},
            "디자이너": {"population": 80, "digital_affinity": "매우 높음", "spending_power": "중간", "score_bonus": 7, "category": "job"},

            # === 연령/세대 기반 ===
            "MZ세대": {"population": 1700, "digital_affinity": "매우 높음", "spending_power": "중간", "score_bonus": 8, "category": "gen"},
            "Z세대": {"population": 800, "digital_affinity": "매우 높음", "spending_power": "낮음", "score_bonus": 6, "category": "gen"},
            "밀레니얼": {"population": 900, "digital_affinity": "매우 높음", "spending_power": "높음", "score_bonus": 9, "category": "gen"},
            "X세대": {"population": 850, "digital_affinity": "높음", "spending_power": "매우 높음", "score_bonus": 8, "category": "gen"},
            "시니어": {"population": 1200, "digital_affinity": "낮음", "spending_power": "높음", "score_bonus": 7, "category": "gen"},
            "액티브시니어": {"population": 400, "digital_affinity": "중간", "spending_power": "매우 높음", "score_bonus": 9, "category": "gen"},
            "대학생": {"population": 280, "digital_affinity": "매우 높음", "spending_power": "낮음", "score_bonus": 4, "category": "gen"},
            "취준생": {"population": 150, "digital_affinity": "매우 높음", "spending_power": "낮음", "score_bonus": 5, "category": "gen"},

            # === 라이프스타일 기반 ===
            "싱글족": {"population": 750, "digital_affinity": "높음", "spending_power": "높음", "score_bonus": 8, "category": "life"},
            "1인가구": {"population": 950, "digital_affinity": "높음", "spending_power": "높음", "score_bonus": 9, "category": "life"},
            "맞벌이": {"population": 450, "digital_affinity": "높음", "spending_power": "매우 높음", "score_bonus": 9, "category": "life"},
            "워킹맘": {"population": 320, "digital_affinity": "높음", "spending_power": "높음", "score_bonus": 8, "category": "life"},
            "워킹대디": {"population": 320, "digital_affinity": "높음", "spending_power": "높음", "score_bonus": 7, "category": "life"},
            "신혼부부": {"population": 140, "digital_affinity": "높음", "spending_power": "높음", "score_bonus": 7, "category": "life"},
            "주부": {"population": 450, "digital_affinity": "중간", "spending_power": "중간", "score_bonus": 5, "category": "life"},
            "펫부모": {"population": 600, "digital_affinity": "높음", "spending_power": "높음", "score_bonus": 8, "category": "life"},

            # === 비즈니스 기반 ===
            "스타트업": {"population": 60, "digital_affinity": "매우 높음", "spending_power": "중간", "score_bonus": 6, "category": "biz"},
            "1인기업": {"population": 120, "digital_affinity": "높음", "spending_power": "중간", "score_bonus": 6, "category": "biz"},
            "중소기업": {"population": 400, "digital_affinity": "중간", "spending_power": "높음", "score_bonus": 8, "category": "biz"},
            "대기업": {"population": 100, "digital_affinity": "높음", "spending_power": "매우 높음", "score_bonus": 7, "category": "biz"},
            "B2B": {"population": 500, "digital_affinity": "중간", "spending_power": "높음", "score_bonus": 8, "category": "biz"},
            "SaaS사용자": {"population": 200, "digital_affinity": "높음", "spending_power": "높음", "score_bonus": 9, "category": "biz"},
        }

        # 타겟-도메인 시너지 (특정 타겟에 특화된 도메인)
        self.target_domain_synergy = {
            ("시니어", "헬스케어"): 10,
            ("시니어", "실버케어"): 12,
            ("액티브시니어", "여행"): 8,
            ("펫부모", "반려동물"): 10,
            ("1인가구", "배달"): 6,
            ("1인가구", "반려동물"): 8,
            ("MZ세대", "재테크"): 8,
            ("개발자", "AI"): 9,
            ("마케터", "자동화"): 9,
            ("크리에이터", "영상"): 10,
            ("스타트업", "AI"): 8,
            ("중소기업", "자동화"): 9,
            ("B2B", "CRM"): 10,
        }

        # 트렌드 키워드 (2025년 업데이트)
        self.trending_keywords = {
            # 매우 핫한 키워드 (+18점) - 2025 메가트렌드
            "hot": [
                "AI", "GPT", "생성AI", "LLM", "에이전트", "자동화", "노코드",
                "시니어케어", "실버테크", "반려동물", "펫테크",
                "1인가구", "솔로이코노미", "구독경제", "개인화"
            ],

            # 급상승 키워드 (+12점)
            "rising": [
                "헬스케어", "디지털헬스", "멘탈케어", "수면테크", "웰니스",
                "ESG", "친환경", "탄소중립", "리유저블",
                "재택", "하이브리드", "원격협업",
                "숏폼", "라이브커머스", "크리에이터이코노미"
            ],

            # 상승 키워드 (+8점)
            "stable": [
                "교육", "이러닝", "에듀테크", "취업", "자격증",
                "재테크", "투자", "핀테크", "P2P",
                "여행", "호캉스", "워케이션",
                "피트니스", "홈트", "다이어트"
            ],

            # 보통 키워드 (+4점)
            "moderate": [
                "배달", "커머스", "쇼핑", "패션", "뷰티",
                "부동산", "인테리어", "이사",
                "게임", "음악", "영화"
            ],

            # 하락 키워드 (-5점)
            "declining": [
                "NFT", "메타버스", "P2E", "암호화폐",
                "클럽하우스", "VR", "AR글래스"
            ]
        }

        # 수익 모델별 점수
        self.revenue_model_scores = {
            "월정액 구독": {"score": 12, "stability": "매우 높음", "scalability": "높음"},
            "거래 수수료": {"score": 10, "stability": "중간", "scalability": "매우 높음"},
            "프리미엄 요금제": {"score": 8, "stability": "높음", "scalability": "높음"},
            "광고 수익": {"score": 5, "stability": "낮음", "scalability": "매우 높음"},
            "일회성 구매": {"score": 6, "stability": "낮음", "scalability": "중간"},
            "프로젝트 단가": {"score": 7, "stability": "낮음", "scalability": "낮음"},
            "리테이너 계약": {"score": 10, "stability": "높음", "scalability": "낮음"},
            "성과 수수료": {"score": 8, "stability": "중간", "scalability": "중간"},
            "API 사용료": {"score": 9, "stability": "높음", "scalability": "높음"},
            "사용량 기반 과금": {"score": 9, "stability": "중간", "scalability": "높음"},
        }

        # 경쟁 강도별 진입 난이도
        self.competition_levels = {
            "매우 낮음": {"score_bonus": 15, "description": "블루오션, 선점 기회"},
            "낮음": {"score_bonus": 10, "description": "경쟁자 적음, 진입 용이"},
            "중간": {"score_bonus": 5, "description": "적정 경쟁, 차별화 필요"},
            "높음": {"score_bonus": 0, "description": "경쟁 치열, 강력한 차별화 필수"},
            "매우 높음": {"score_bonus": -5, "description": "레드오션, 진입 어려움"}
        }

    def analyze(self, business_data: Dict) -> Dict:
        """
        사업 아이디어 종합 분석

        Args:
            business_data: 사업 아이디어 데이터
                - name: 사업명
                - it_type: IT 사업 유형 (saas, marketplace, agency, tools, platform)
                - domain: 도메인 (헬스케어, 교육 등)
                - target_audience: 타겟 고객층
                - revenue_models: 수익 모델 리스트
                - description: 사업 설명 (키워드 추출용)

        Returns:
            분석 결과 딕셔너리
        """
        name = business_data.get('name', '')
        it_type = business_data.get('it_type', 'saas')
        domain = business_data.get('domain', '')
        target = business_data.get('target_audience', '')
        revenue_models = business_data.get('revenue_models', [])
        description = business_data.get('description', '')

        # 1. 기본 점수 (IT 유형 기반)
        base_score = self._get_base_score(it_type)

        # 2. 도메인 점수
        domain_analysis = self._analyze_domain(domain)
        domain_score = domain_analysis['score_bonus']

        # 3. 타겟 고객 점수
        target_analysis = self._analyze_target(target)
        target_score = target_analysis['score_bonus']

        # 4. 트렌드 키워드 점수
        trend_score = self._analyze_trends(name, description)

        # 5. 수익 모델 점수
        revenue_analysis = self._analyze_revenue_models(revenue_models)
        revenue_score = revenue_analysis['total_score']

        # 6. 경쟁 강도 추정
        competition = self._estimate_competition(domain, it_type)
        competition_score = competition['score_bonus']

        # 7. 시너지 보너스 (도메인-타겟-IT유형 조합)
        synergy_bonus = self._calculate_synergy_bonus(domain, target, it_type)

        # 종합 점수 계산 (가중 평균) - 2025 업데이트
        raw_score = (
            base_score * 0.25 +          # IT 유형 25%
            domain_score * 1.5 +         # 도메인 보너스
            target_score * 1.2 +         # 타겟 보너스
            trend_score * 0.8 +          # 트렌드 보너스
            revenue_score * 0.5 +        # 수익 모델
            competition_score * 0.5 +    # 경쟁 보너스
            synergy_bonus * 0.8          # 시너지 보너스 (신규)
        )

        # 점수 정규화 (50-95 범위)
        final_score = max(50, min(95, int(raw_score)))

        # 변동성 추가 (±3점)
        final_score += random.randint(-3, 3)
        final_score = max(50, min(95, final_score))

        # 시장 규모 추정
        market_size = self._estimate_market_size(domain, target)

        # 추천 생성
        recommendation = self._generate_recommendation(final_score, domain_analysis, competition)

        return {
            'business_name': name,
            'market_score': final_score,
            'analysis_date': datetime.now().isoformat(),
            'mode': 'lightweight',

            # 상세 분석
            'score_breakdown': {
                'base_score': base_score,
                'domain_bonus': domain_score,
                'target_bonus': target_score,
                'trend_bonus': trend_score,
                'revenue_bonus': revenue_score,
                'competition_bonus': competition_score,
                'synergy_bonus': synergy_bonus  # 신규: 조합 시너지
            },

            # 시장 분석
            'market_analysis': {
                'domain': domain_analysis,
                'target_audience': target_analysis,
                'competition': competition,
                'market_size': market_size,
                'trend_keywords_found': self._find_trend_keywords(name, description)
            },

            # 수익 분석
            'revenue_analysis': revenue_analysis,

            # 추천
            'recommendation': recommendation,

            # 데이터 소스
            'data_sources': {
                'naver': self._generate_naver_estimate(domain, final_score),
                'google': self._generate_google_estimate(domain, competition),
                'youtube': self._generate_youtube_estimate(domain),
                'kmong': self._generate_kmong_estimate(domain, it_type)
            }
        }

    def _get_base_score(self, it_type: str) -> int:
        """IT 유형별 기본 점수"""
        if it_type in self.it_type_scores:
            return self.it_type_scores[it_type]['base_score']
        return 70  # 기본값

    def _analyze_domain(self, domain: str) -> Dict:
        """도메인 분석"""
        if domain in self.domain_market_data:
            data = self.domain_market_data[domain]
            return {
                'domain': domain,
                'market_size': data['market_size'],
                'growth_rate': f"{data['growth_rate']}%",
                'trend': data['trend'],
                'score_bonus': data['score_bonus']
            }

        # 도메인이 없으면 유사 도메인 찾기
        for key in self.domain_market_data:
            if key in domain or domain in key:
                data = self.domain_market_data[key]
                return {
                    'domain': key,
                    'market_size': data['market_size'],
                    'growth_rate': f"{data['growth_rate']}%",
                    'trend': data['trend'],
                    'score_bonus': data['score_bonus']
                }

        # 기본값
        return {
            'domain': domain,
            'market_size': '중형',
            'growth_rate': '5%',
            'trend': '안정',
            'score_bonus': 5
        }

    def _analyze_target(self, target: str) -> Dict:
        """타겟 고객층 분석"""
        if target in self.target_audience_data:
            data = self.target_audience_data[target]
            return {
                'target': target,
                'population_millions': data['population'],
                'digital_affinity': data['digital_affinity'],
                'spending_power': data['spending_power'],
                'score_bonus': data['score_bonus']
            }

        # 유사 타겟 찾기
        for key in self.target_audience_data:
            if key in target or target in key:
                data = self.target_audience_data[key]
                return {
                    'target': key,
                    'population_millions': data['population'],
                    'digital_affinity': data['digital_affinity'],
                    'spending_power': data['spending_power'],
                    'score_bonus': data['score_bonus']
                }

        # 기본값
        return {
            'target': target,
            'population_millions': 500,
            'digital_affinity': '중간',
            'spending_power': '중간',
            'score_bonus': 5
        }

    def _analyze_trends(self, name: str, description: str) -> int:
        """트렌드 키워드 분석 (2025 업데이트)"""
        text = f"{name} {description}".lower()
        score = 0
        matched_categories = set()

        # 각 카테고리별 점수 (중복 방지를 위해 카테고리당 최대 1회)
        keyword_scores = {
            'hot': 18,
            'rising': 12,
            'stable': 8,
            'moderate': 4,
            'declining': -5
        }

        for category, keywords in self.trending_keywords.items():
            if category in matched_categories:
                continue
            for keyword in keywords:
                if keyword.lower() in text:
                    score += keyword_scores.get(category, 0)
                    matched_categories.add(category)
                    break

        return score

    def _calculate_synergy_bonus(self, domain: str, target: str, it_type: str) -> int:
        """도메인-타겟-IT유형 시너지 보너스 계산"""
        synergy_score = 0

        # 도메인 시너지 체크
        for (d1, d2), bonus in self.domain_synergy.items():
            if d1.lower() in domain.lower() or d2.lower() in domain.lower():
                synergy_score += bonus // 2  # 부분 매칭

        # 타겟-도메인 시너지 체크
        for (t, d), bonus in self.target_domain_synergy.items():
            if t.lower() in target.lower() and d.lower() in domain.lower():
                synergy_score += bonus

        # IT 유형-도메인 시너지 체크
        it_type_data = self.it_type_scores.get(it_type, {})
        best_domains = it_type_data.get('best_domains', [])
        for best_domain in best_domains:
            if best_domain.lower() in domain.lower():
                synergy_score += 5
                break

        return min(synergy_score, 20)  # 최대 20점

    def _find_trend_keywords(self, name: str, description: str) -> List[str]:
        """발견된 트렌드 키워드 목록"""
        text = f"{name} {description}".lower()
        found = []

        for category, keywords in self.trending_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    found.append(f"{keyword} ({category})")

        return found

    def _analyze_revenue_models(self, revenue_models: List[str]) -> Dict:
        """수익 모델 분석"""
        total_score = 0
        models_analysis = []

        for model in revenue_models:
            if model in self.revenue_model_scores:
                data = self.revenue_model_scores[model]
                total_score += data['score']
                models_analysis.append({
                    'model': model,
                    'score': data['score'],
                    'stability': data['stability'],
                    'scalability': data['scalability']
                })
            else:
                # 부분 매칭
                for key, data in self.revenue_model_scores.items():
                    if key in model or model in key:
                        total_score += data['score']
                        models_analysis.append({
                            'model': model,
                            'score': data['score'],
                            'stability': data['stability'],
                            'scalability': data['scalability']
                        })
                        break

        if not models_analysis:
            total_score = 6  # 기본값
            models_analysis = [{'model': '미정', 'score': 6, 'stability': '중간', 'scalability': '중간'}]

        return {
            'total_score': min(total_score, 20),  # 최대 20점
            'models': models_analysis,
            'recurring_potential': any(m['stability'] in ['높음', '매우 높음'] for m in models_analysis)
        }

    def _estimate_competition(self, domain: str, it_type: str) -> Dict:
        """경쟁 강도 추정"""
        # 도메인별 기본 경쟁도
        high_competition_domains = ["배달", "쇼핑", "교육", "투자", "부동산"]
        medium_competition_domains = ["헬스케어", "피트니스", "여행", "패션"]
        low_competition_domains = ["시니어", "수면", "명상", "반려동물"]

        if domain in high_competition_domains:
            level = "높음"
        elif domain in low_competition_domains:
            level = "낮음"
        else:
            level = "중간"

        # IT 유형에 따른 조정
        if it_type == "agency":
            level = "높음"  # 에이전시는 경쟁 치열
        elif it_type == "saas" and domain in low_competition_domains:
            level = "낮음"  # 틈새 SaaS는 경쟁 낮음

        comp_data = self.competition_levels.get(level, self.competition_levels["중간"])

        return {
            'level': level,
            'score_bonus': comp_data['score_bonus'],
            'description': comp_data['description'],
            'entry_difficulty': "쉬움" if level in ["낮음", "매우 낮음"] else "보통" if level == "중간" else "어려움"
        }

    def _estimate_market_size(self, domain: str, target: str) -> Dict:
        """시장 규모 추정"""
        domain_data = self.domain_market_data.get(domain, {'market_size': '중형'})
        target_data = self.target_audience_data.get(target, {'population': 500})

        # 시장 규모 추정 (억원)
        size_multipliers = {"대형": 10000, "중형": 3000, "소형": 500}
        base_size = size_multipliers.get(domain_data.get('market_size', '중형'), 3000)

        # 타겟 인구 기반 조정
        population_factor = target_data.get('population', 500) / 1000
        estimated_size = int(base_size * population_factor)

        return {
            'estimated_size_billion_krw': estimated_size,
            'size_category': domain_data.get('market_size', '중형'),
            'addressable_market': f"약 {estimated_size:,}억원",
            'target_population_thousands': target_data.get('population', 500)
        }

    def _generate_recommendation(self, score: int, domain_analysis: Dict, competition: Dict) -> Dict:
        """추천 생성"""
        if score >= 85:
            verdict = "매우 유망"
            action = "즉시 MVP 개발 착수 권장"
            priority = "최우선"
        elif score >= 75:
            verdict = "유망"
            action = "시장 검증 후 개발 착수 권장"
            priority = "높음"
        elif score >= 65:
            verdict = "보통"
            action = "추가 시장 조사 필요"
            priority = "중간"
        elif score >= 55:
            verdict = "주의 필요"
            action = "차별화 전략 필수"
            priority = "낮음"
        else:
            verdict = "비추천"
            action = "다른 아이디어 탐색 권장"
            priority = "제외"

        return {
            'verdict': verdict,
            'action': action,
            'priority': priority,
            'confidence': "높음" if score >= 75 else "중간" if score >= 60 else "낮음",
            'key_success_factors': self._get_success_factors(domain_analysis, competition)
        }

    def _get_success_factors(self, domain_analysis: Dict, competition: Dict) -> List[str]:
        """핵심 성공 요소 도출"""
        factors = []

        if domain_analysis.get('trend') == '급상승':
            factors.append("시장 성장 트렌드 활용")

        if competition.get('level') in ['낮음', '매우 낮음']:
            factors.append("선점 효과 극대화")
        else:
            factors.append("명확한 차별화 포인트 필수")

        if domain_analysis.get('market_size') == '대형':
            factors.append("대규모 타겟 시장 공략")
        else:
            factors.append("니치 마켓 집중 전략")

        factors.append("빠른 MVP 출시 및 피드백 반영")
        factors.append("효과적인 고객 획득 채널 확보")

        return factors[:4]

    # 플랫폼별 추정 데이터 생성 (기존 시스템 호환용)
    def _generate_naver_estimate(self, domain: str, score: int) -> Dict:
        """네이버 검색량 추정"""
        popularity = min(100, score + random.randint(-5, 10))
        return {
            'platform': '네이버',
            'keyword': domain,
            'popularity_score': popularity,
            'related_searches': random.randint(5, 15),
            'estimated': True
        }

    def _generate_google_estimate(self, domain: str, competition: Dict) -> Dict:
        """구글 경쟁사 추정"""
        difficulty_map = {"쉬움": "easy", "보통": "medium", "어려움": "hard"}
        return {
            'platform': '구글',
            'organic_results': random.randint(100, 500),
            'entry_difficulty': difficulty_map.get(competition.get('entry_difficulty', '보통'), 'medium'),
            'estimated': True
        }

    def _generate_youtube_estimate(self, domain: str) -> Dict:
        """유튜브 관심도 추정"""
        domain_data = self.domain_market_data.get(domain, {})
        trend = domain_data.get('trend', '안정')

        interest = "high" if trend in ['급상승', '상승'] else "medium" if trend == '안정' else "low"
        return {
            'platform': '유튜브',
            'interest_indicator': interest,
            'estimated_videos': random.randint(50, 200),
            'estimated': True
        }

    def _generate_kmong_estimate(self, domain: str, it_type: str) -> Dict:
        """크몽 시장 추정"""
        # IT 유형별 평균 가격
        price_ranges = {
            "saas": (100000, 300000),
            "marketplace": (50000, 150000),
            "agency": (200000, 1000000),
            "tools": (30000, 100000),
            "platform": (100000, 500000)
        }
        price_range = price_ranges.get(it_type, (50000, 200000))
        avg_price = random.randint(*price_range)

        return {
            'platform': '크몽',
            'avg_price': avg_price,
            'service_count': random.randint(10, 100),
            'competition_level': 'medium',
            'estimated': True
        }

    def quick_score(self, business_name: str, it_type: str = "saas", domain: str = "") -> int:
        """빠른 점수 산정 (간이 분석)"""
        base = self._get_base_score(it_type)
        domain_bonus = self._analyze_domain(domain).get('score_bonus', 0)
        trend_bonus = self._analyze_trends(business_name, "")

        score = base + domain_bonus + trend_bonus
        score += random.randint(-5, 5)

        return max(50, min(95, int(score)))


# 사용 예시
if __name__ == "__main__":
    analyzer = LightweightMarketAnalyzer()

    # 테스트 사업 아이디어
    test_businesses = [
        {
            "name": "AI 시니어 헬스케어 플랫폼",
            "it_type": "platform",
            "domain": "시니어",
            "target_audience": "시니어",
            "revenue_models": ["월정액 구독", "프리미엄 요금제"],
            "description": "AI 기반 맞춤 건강관리 서비스"
        },
        {
            "name": "반려동물 펫시터 매칭",
            "it_type": "marketplace",
            "domain": "반려동물",
            "target_audience": "싱글족",
            "revenue_models": ["거래 수수료"],
            "description": "실시간 펫시터 매칭 플랫폼"
        },
        {
            "name": "NFT 아트 마켓플레이스",
            "it_type": "marketplace",
            "domain": "NFT",
            "target_audience": "MZ세대",
            "revenue_models": ["거래 수수료"],
            "description": "디지털 아트 NFT 거래 플랫폼"
        }
    ]

    print("="*80)
    print("경량 시장 분석 테스트")
    print("="*80)

    for biz in test_businesses:
        result = analyzer.analyze(biz)

        print(f"\n[{biz['name']}]")
        print(f"  시장 점수: {result['market_score']}/100")
        print(f"  추천: {result['recommendation']['verdict']}")
        print(f"  우선순위: {result['recommendation']['priority']}")
        print(f"  핵심 성공 요소:")
        for factor in result['recommendation']['key_success_factors']:
            print(f"    - {factor}")
        print(f"  점수 상세:")
        for key, value in result['score_breakdown'].items():
            print(f"    {key}: {value}")
