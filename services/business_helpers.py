import hashlib


def generate_default_action_plan(business_name, business_type):
    """기본 실행 계획 생성 (DB에 없는 경우)"""
    return {
        'week_1': {
            'goal': 'MVP 개발 및 시장 조사',
            'tasks': [
                f'{business_name} 핵심 기능 정의',
                '경쟁사 분석 및 차별화 포인트 도출',
                '랜딩페이지 제작 (Webflow/Notion)',
                '초기 고객 타겟 정의'
            ]
        },
        'week_2': {
            'goal': '프로토타입 및 검증',
            'tasks': [
                'MVP 프로토타입 제작',
                '베타 테스터 10명 모집',
                '사용자 피드백 수집',
                '가격 책정 테스트'
            ]
        },
        'week_3': {
            'goal': '마케팅 및 고객 확보',
            'tasks': [
                'SNS 마케팅 시작 (인스타/페이스북)',
                '소규모 유료 광고 테스트 (일 1만원)',
                '첫 유료 고객 확보',
                '고객 후기 수집'
            ]
        },
        'week_4': {
            'goal': '최적화 및 확장',
            'tasks': [
                '전환율 최적화',
                '자동화 시스템 구축',
                '추가 기능 개발',
                '월 목표 매출 달성'
            ]
        },
        'total_budget': 1000000,
        'summary': f'{business_name}를 4주 안에 런칭하기 위한 실행 계획입니다.'
    }


def generate_startup_guide(business_name, business_type, score):
    """상세 시작 가이드 생성"""
    tech_stacks = {
        'saas': {
            'recommended': 'No-Code / Low-Code',
            'tools': ['Bubble.io', 'Webflow', 'Airtable', 'Zapier'],
            'cost': '월 5-10만원',
            'learning_time': '1-2주',
            'reason': 'SaaS는 빠른 MVP 검증이 중요. 코딩 없이 2주 내 런칭 가능'
        },
        'agency': {
            'recommended': '포트폴리오 + 프리랜서 플랫폼',
            'tools': ['Notion', 'Figma', '크몽', '숨고', 'LinkedIn'],
            'cost': '월 0-5만원',
            'learning_time': '즉시 시작 가능',
            'reason': '에이전시는 기술보다 영업력이 중요. 플랫폼 활용으로 즉시 시작'
        },
        'marketplace': {
            'recommended': 'No-Code 마켓플레이스 빌더',
            'tools': ['Sharetribe', 'Bubble.io', 'Webflow + Memberstack'],
            'cost': '월 10-30만원',
            'learning_time': '2-3주',
            'reason': '마켓플레이스는 양면 시장. 빠른 런칭 후 수요/공급 테스트 필요'
        }
    }

    tech = tech_stacks.get(business_type, tech_stacks['saas'])

    return {
        'day1_checklist': {
            'title': 'Day 1: 오늘 당장 시작하기',
            'tasks': [
                {
                    'task': '도메인 구매',
                    'detail': f'{business_name.replace(" ", "").lower()}.com 또는 .kr',
                    'tool': 'Namecheap, 가비아',
                    'cost': '1-2만원/년',
                    'time': '10분'
                },
                {
                    'task': '랜딩페이지 제작',
                    'detail': '서비스 소개 + 이메일 수집 폼',
                    'tool': 'Notion, Webflow (무료)',
                    'cost': '0원',
                    'time': '2-3시간'
                },
                {
                    'task': '경쟁사 5개 분석',
                    'detail': '가격, 기능, 리뷰 정리',
                    'tool': 'Google 스프레드시트',
                    'cost': '0원',
                    'time': '1-2시간'
                },
                {
                    'task': 'SNS 계정 생성',
                    'detail': '인스타그램 비즈니스 계정',
                    'tool': 'Instagram, 페이스북',
                    'cost': '0원',
                    'time': '30분'
                }
            ]
        },
        'tech_stack': tech,
        'marketing_channels': {
            'free': [
                {'channel': '인스타그램', 'strategy': '관련 해시태그로 일 1포스팅', 'expected': '월 100-500 팔로워'},
                {'channel': '블로그/브런치', 'strategy': '주 2회 전문 콘텐츠 발행', 'expected': '월 1000-5000 방문자'},
                {'channel': '커뮤니티', 'strategy': '네이버 카페, 오픈카톡 참여', 'expected': '초기 베타 테스터 확보'},
                {'channel': '지인 네트워크', 'strategy': '카톡/링크드인으로 런칭 알림', 'expected': '첫 10명 고객'}
            ],
            'paid': [
                {'channel': '페이스북/인스타 광고', 'budget': '일 1-3만원', 'expected': 'CPC 300-500원'},
                {'channel': '네이버 검색광고', 'budget': '일 1-2만원', 'expected': '타겟 키워드 노출'},
                {'channel': '인플루언서', 'budget': '건당 5-30만원', 'expected': '신뢰도 확보'}
            ]
        },
        'first_customer_strategy': {
            'title': '첫 10명 고객 확보 전략',
            'steps': [
                {
                    'step': 1,
                    'action': '무료/할인 제공',
                    'detail': '첫 달 무료 또는 50% 할인으로 진입 장벽 낮추기',
                    'target': '3명'
                },
                {
                    'step': 2,
                    'action': '지인 영업',
                    'detail': '카톡, 인스타 DM으로 직접 연락. 솔직하게 도움 요청',
                    'target': '3명'
                },
                {
                    'step': 3,
                    'action': '커뮤니티 활동',
                    'detail': '관련 오픈카톡, 페이스북 그룹에서 무료 상담 제공',
                    'target': '2명'
                },
                {
                    'step': 4,
                    'action': '콘텐츠 마케팅',
                    'detail': '블로그 글 하단에 CTA 삽입',
                    'target': '2명'
                }
            ]
        },
        'cost_breakdown': {
            'essential': [
                {'item': '도메인', 'cost': 15000, 'period': '년'},
                {'item': '호스팅/서버', 'cost': 0, 'period': '월', 'note': 'Vercel/Netlify 무료'},
                {'item': '이메일 서비스', 'cost': 0, 'period': '월', 'note': 'Mailchimp 무료 (500명까지)'}
            ],
            'recommended': [
                {'item': 'No-Code 툴', 'cost': 50000, 'period': '월'},
                {'item': '광고비', 'cost': 300000, 'period': '월'},
                {'item': '디자인 툴', 'cost': 15000, 'period': '월', 'note': 'Canva Pro'}
            ],
            'total_minimum': 15000,
            'total_recommended': 380000
        },
        'risk_management': [
            {
                'risk': '고객이 안 모임',
                'solution': '가격 낮추기, 무료 체험 연장, 타겟 재설정',
                'prevention': '런칭 전 최소 10명 사전 등록 확보'
            },
            {
                'risk': '경쟁사가 너무 강함',
                'solution': '니치 시장 집중, 특정 고객군 전문화',
                'prevention': '차별화 포인트 3개 이상 준비'
            },
            {
                'risk': '기술적 문제',
                'solution': 'No-Code로 우회, 외주 활용',
                'prevention': 'MVP는 최대한 단순하게'
            }
        ],
        'success_metrics': {
            'week1': {'goal': '랜딩페이지 완성 + 이메일 20개 수집', 'importance': '시장 관심도 검증'},
            'week2': {'goal': '베타 테스터 10명 + 피드백 수집', 'importance': '제품-시장 적합성 확인'},
            'week4': {'goal': '유료 고객 5명 + 월 50만원 매출', 'importance': '수익 모델 검증'},
            'month3': {'goal': '월 200만원 매출 + 고객 30명', 'importance': '지속 가능성 확인'}
        }
    }


def generate_default_market_analysis(business_name, keyword):
    """경량 시장 분석 생성 (도메인별 정적 데이터 기반)"""
    domain_market_data = {
        'ai': {
            'market_size': '2조 5천억원',
            'growth_rate': 35,
            'competition_level': '높음',
            'entry_barrier': '중간',
            'trend': '급성장',
            'naver_search': 85000,
            'seasonality': '연중 꾸준',
            'target_size': '기업 고객 50만+',
            'keywords': ['AI', '인공지능', '머신러닝', 'GPT', '자동화', '챗봇']
        },
        'saas': {
            'market_size': '1조 8천억원',
            'growth_rate': 28,
            'competition_level': '중간',
            'entry_barrier': '낮음',
            'trend': '성장세',
            'naver_search': 45000,
            'seasonality': '연중 꾸준',
            'target_size': '중소기업 200만+',
            'keywords': ['구독', 'SaaS', '클라우드', '서비스', '플랫폼']
        },
        'ecommerce': {
            'market_size': '8조원',
            'growth_rate': 15,
            'competition_level': '매우 높음',
            'entry_barrier': '낮음',
            'trend': '안정적 성장',
            'naver_search': 120000,
            'seasonality': '연말 성수기',
            'target_size': '온라인 소비자 3천만+',
            'keywords': ['쇼핑', '판매', '커머스', '마켓', '스토어', '굿즈']
        },
        'education': {
            'market_size': '3조원',
            'growth_rate': 22,
            'competition_level': '중간',
            'entry_barrier': '중간',
            'trend': '성장세',
            'naver_search': 68000,
            'seasonality': '학기초 성수기',
            'target_size': '학습자 800만+',
            'keywords': ['교육', '강의', '학습', '코딩', '튜터', '멘토링']
        },
        'content': {
            'market_size': '1조 2천억원',
            'growth_rate': 25,
            'competition_level': '높음',
            'entry_barrier': '낮음',
            'trend': '성장세',
            'naver_search': 55000,
            'seasonality': '연중 꾸준',
            'target_size': '콘텐츠 소비자 2천만+',
            'keywords': ['콘텐츠', '블로그', '유튜브', '영상', '크리에이터']
        },
        'marketing': {
            'market_size': '2조원',
            'growth_rate': 18,
            'competition_level': '높음',
            'entry_barrier': '중간',
            'trend': '안정적',
            'naver_search': 72000,
            'seasonality': '연말 성수기',
            'target_size': '사업자 700만+',
            'keywords': ['마케팅', '광고', '홍보', 'SNS', '브랜딩']
        },
        'finance': {
            'market_size': '5조원',
            'growth_rate': 20,
            'competition_level': '매우 높음',
            'entry_barrier': '높음',
            'trend': '성장세',
            'naver_search': 95000,
            'seasonality': '연초/연말 성수기',
            'target_size': '금융 소비자 2천만+',
            'keywords': ['투자', '재테크', '주식', '금융', '핀테크']
        },
        'health': {
            'market_size': '4조원',
            'growth_rate': 30,
            'competition_level': '중간',
            'entry_barrier': '중간',
            'trend': '급성장',
            'naver_search': 88000,
            'seasonality': '연초 성수기',
            'target_size': '건강 관심층 1천만+',
            'keywords': ['건강', '헬스', '다이어트', '운동', '웰니스']
        },
        'default': {
            'market_size': '1조원',
            'growth_rate': 15,
            'competition_level': '중간',
            'entry_barrier': '중간',
            'trend': '안정적',
            'naver_search': 30000,
            'seasonality': '연중 꾸준',
            'target_size': '잠재 고객 100만+',
            'keywords': []
        }
    }

    def detect_domain(name, kw):
        text = f"{name} {kw}".lower()
        for domain, data in domain_market_data.items():
            if domain == 'default':
                continue
            for dk in data.get('keywords', []):
                if dk.lower() in text:
                    return domain
        return 'default'

    domain = detect_domain(business_name, keyword)
    market = domain_market_data[domain]

    hash_val = int(hashlib.md5(f"{business_name}{keyword}".encode()).hexdigest()[:8], 16)
    variation = (hash_val % 20 - 10) / 100

    search_count = int(market['naver_search'] * (1 + variation))
    global_interest = min(95, max(40, 60 + int(market['growth_rate'] * 0.8) + int(variation * 30)))

    competition_scores = {'낮음': 30, '중간': 55, '높음': 75, '매우 높음': 90}
    competition_score = competition_scores.get(market['competition_level'], 55)

    barrier_scores = {'낮음': 25, '중간': 50, '높음': 75}
    barrier_score = barrier_scores.get(market['entry_barrier'], 50)

    return {
        'naver': {
            'search_count': search_count,
            'competition': market['competition_level'],
            'competition_score': competition_score,
            'related_keywords': [keyword, f'{keyword} 추천', f'{keyword} 후기', f'{keyword} 비교']
        },
        'google_trends': {
            'global_interest': global_interest,
            'trend': market['trend'],
            'growth_rate': market['growth_rate']
        },
        'market_info': {
            'market_size': market['market_size'],
            'growth_rate': market['growth_rate'],
            'seasonality': market['seasonality'],
            'target_size': market['target_size'],
            'entry_barrier': market['entry_barrier'],
            'entry_barrier_score': barrier_score,
            'domain': domain
        },
        'market_summary': f"{business_name} 관련 시장 규모는 {market['market_size']}이며, 연 {market['growth_rate']}% 성장 중입니다. 경쟁 강도는 '{market['competition_level']}'이고, 진입 장벽은 '{market['entry_barrier']}' 수준입니다. {market['target_size']}의 잠재 고객이 있습니다."
    }


def generate_default_revenue_analysis(business_name, score):
    """기본 수익 분석 생성 (DB에 없는 경우)"""
    base_revenue = score * 50000
    return {
        'scenarios': {
            'conservative': {
                'monthly_revenue': int(base_revenue * 0.5),
                'monthly_profit': int(base_revenue * 0.3)
            },
            'realistic': {
                'monthly_revenue': base_revenue,
                'monthly_profit': int(base_revenue * 0.6),
                'break_even_months': 3
            },
            'optimistic': {
                'monthly_revenue': int(base_revenue * 2),
                'monthly_profit': int(base_revenue * 1.2)
            }
        },
        'startup_cost': int(score * 50000),
        'annual_roi': int((base_revenue * 12 - score * 50000) / (score * 50000) * 100),
        'revenue_model': 'subscription',
        'revenue_summary': f'{business_name}은 월 {int(base_revenue/10000)}만원 수익이 예상됩니다.'
    }
