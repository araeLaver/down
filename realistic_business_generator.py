"""
현실적이고 실행 가능한 사업 아이템 생성기
실제 시장 검증된 비즈니스 모델과 즉시 수익 창출 가능한 분야 중심
"""

import random
from datetime import datetime
import json

class RealisticBusinessGenerator:
    def __init__(self):
        # 현실적이고 즉시 시작 가능한 사업 분야들
        self.immediate_businesses = [
            {
                "category": "디지털 서비스",
                "businesses": [
                    {
                        "name": "온라인 과외/강의 플랫폼",
                        "startup_cost": "50만원 이하",
                        "revenue_potential": "월 200-500만원",
                        "timeline": "2주 내 시작",
                        "difficulty": "쉬움",
                        "description": "전문 분야 1:1 온라인 과외, 화상 강의"
                    },
                    {
                        "name": "소셜미디어 관리 대행",
                        "startup_cost": "30만원 이하",
                        "revenue_potential": "월 150-400만원",
                        "timeline": "1주 내 시작",
                        "difficulty": "쉬움",
                        "description": "소상공인 인스타그램, 페이스북 운영 대행"
                    },
                    {
                        "name": "번역/통역 서비스",
                        "startup_cost": "10만원 이하",
                        "revenue_potential": "월 100-300만원",
                        "timeline": "즉시 시작",
                        "difficulty": "쉬움",
                        "description": "문서 번역, 화상 통역, 웹사이트 현지화"
                    }
                ]
            },
            {
                "category": "로컬 서비스",
                "businesses": [
                    {
                        "name": "펜션/민박 청소 서비스",
                        "startup_cost": "100만원 이하",
                        "revenue_potential": "월 300-800만원",
                        "timeline": "1주 내 시작",
                        "difficulty": "보통",
                        "description": "펜션, 에어비앤비 청소 전문 서비스"
                    },
                    {
                        "name": "반려동물 돌봄 서비스",
                        "startup_cost": "50만원 이하",
                        "revenue_potential": "월 200-600만원",
                        "timeline": "2주 내 시작",
                        "difficulty": "쉬움",
                        "description": "펫시팅, 산책 대행, 호텔 서비스"
                    },
                    {
                        "name": "어르신 IT 교육",
                        "startup_cost": "30만원 이하",
                        "revenue_potential": "월 150-350만원",
                        "timeline": "1주 내 시작",
                        "difficulty": "쉬움",
                        "description": "스마트폰, 키오스크 사용법 개인 교육"
                    }
                ]
            },
            {
                "category": "제품 판매",
                "businesses": [
                    {
                        "name": "수제 간편식 판매",
                        "startup_cost": "200만원 이하",
                        "revenue_potential": "월 400-1000만원",
                        "timeline": "1개월 내 시작",
                        "difficulty": "보통",
                        "description": "쿠팡, 마켓컬리 납품용 수제 도시락, 반찬"
                    },
                    {
                        "name": "중고 전자제품 리퍼비시",
                        "startup_cost": "300만원 이하",
                        "revenue_potential": "월 500-1200만원",
                        "timeline": "2주 내 시작",
                        "difficulty": "보통",
                        "description": "중고 노트북, 폰 수리 후 재판매"
                    },
                    {
                        "name": "개인 맞춤 도시락",
                        "startup_cost": "150만원 이하",
                        "revenue_potential": "월 300-700만원",
                        "timeline": "2주 내 시작",
                        "difficulty": "보통",
                        "description": "직장인 대상 건강식 도시락 배달"
                    }
                ]
            },
            {
                "category": "전문 서비스",
                "businesses": [
                    {
                        "name": "세무 기장 대행",
                        "startup_cost": "100만원 이하",
                        "revenue_potential": "월 400-800만원",
                        "timeline": "자격증 필요",
                        "difficulty": "어려움",
                        "description": "소상공인 세무 기장, 부가세 신고 대행"
                    },
                    {
                        "name": "인테리어 컨설팅",
                        "startup_cost": "50만원 이하",
                        "revenue_potential": "월 200-600만원",
                        "timeline": "1개월 내 시작",
                        "difficulty": "보통",
                        "description": "소형 공간 인테리어 설계 및 시공 관리"
                    },
                    {
                        "name": "개인 재정 컨설팅",
                        "startup_cost": "30만원 이하",
                        "revenue_potential": "월 150-400만원",
                        "timeline": "2주 내 시작",
                        "difficulty": "보통",
                        "description": "가계부 정리, 투자 포트폴리오 조언"
                    }
                ]
            }
        ]
        
        # 계절별/트렌드별 기회 사업
        self.seasonal_opportunities = {
            "봄": ["화분 배달 서비스", "벚꽃 관련 상품", "새학기 용품"],
            "여름": ["빙수/아이스크림 트럭", "캠핑 용품 대여", "에어컨 청소"],
            "가을": ["추석 선물세트", "등산 가이드", "김장 재료 배달"],
            "겨울": ["스키 용품 대여", "연말 파티 케이터링", "김치냉장고 청소"]
        }
        
        # 즉시 수익 가능한 기술 활용 사업
        self.tech_enabled_businesses = [
            {
                "name": "유튜브 채널 운영",
                "niche": ["요리", "정리수납", "반려동물", "육아팁", "노하우"],
                "monetization": "광고수익, 협찬, 제품판매",
                "startup_cost": "50만원 이하",
                "timeline": "즉시 시작"
            },
            {
                "name": "온라인 쇼핑몰",
                "products": ["핸드메이드 액세서리", "빈티지 의류", "반려동물 용품"],
                "platforms": ["스마트스토어", "쿠팡", "지마켓"],
                "startup_cost": "100만원 이하",
                "timeline": "1주 내 시작"
            },
            {
                "name": "앱/웹 서비스",
                "ideas": ["동네 심부름", "중고거래 중개", "공동구매 플랫폼"],
                "development": "노코드 툴 활용",
                "startup_cost": "200만원 이하",
                "timeline": "1개월 내 시작"
            }
        ]

        # 앱 개발 중심 수익성 높은 테마들
        self.high_potential_app_themes = [
            {
                "category": "생활 편의 앱",
                "apps": [
                    {
                        "name": "동네 맛집 주문 통합 앱",
                        "description": "여러 배달앱 통합 비교주문, 할인쿠폰 통합관리",
                        "target": "20-40대 직장인",
                        "revenue_model": "배달 수수료 5%, 광고료",
                        "startup_cost": "500만원",
                        "monthly_revenue": "200-800만원",
                        "development_time": "3개월",
                        "viability": "매우 높음"
                    },
                    {
                        "name": "주차장 실시간 공유 앱",
                        "description": "개인/상업 주차공간 실시간 대여, 예약시스템",
                        "target": "차량 소유자 전체",
                        "revenue_model": "거래 수수료 15%, 프리미엄 기능",
                        "startup_cost": "800만원",
                        "monthly_revenue": "500-2000만원",
                        "development_time": "4개월",
                        "viability": "매우 높음"
                    },
                    {
                        "name": "집안일 도우미 매칭 앱",
                        "description": "청소, 요리, 정리정돈 전문가 실시간 매칭",
                        "target": "맞벌이 부부, 1인가구",
                        "revenue_model": "매칭 수수료 20%, 보험료",
                        "startup_cost": "600만원",
                        "monthly_revenue": "300-1200만원",
                        "development_time": "3개월",
                        "viability": "높음"
                    }
                ]
            },
            {
                "category": "건강/피트니스 앱",
                "apps": [
                    {
                        "name": "AI 개인 트레이너 앱",
                        "description": "AI 기반 맞춤 운동 프로그램, 실시간 자세교정",
                        "target": "20-50대 건강관심층",
                        "revenue_model": "월 구독료 9900원, 프리미엄 19900원",
                        "startup_cost": "1000만원",
                        "monthly_revenue": "800-3000만원",
                        "development_time": "6개월",
                        "viability": "매우 높음"
                    },
                    {
                        "name": "식단 관리 + 배달 연동 앱",
                        "description": "개인 맞춤 식단 추천 후 즉시 주문 연결",
                        "target": "다이어터, 헬스인",
                        "revenue_model": "주문 수수료 8%, 식단 구독료",
                        "startup_cost": "700만원",
                        "monthly_revenue": "400-1500만원",
                        "development_time": "4개월",
                        "viability": "높음"
                    },
                    {
                        "name": "수면 개선 종합 플랫폼",
                        "description": "수면패턴 분석, 맞춤 음악, 환경 자동제어 연동",
                        "target": "불면증, 수면장애인",
                        "revenue_model": "월 구독료 7900원, IoT기기 판매",
                        "startup_cost": "1200만원",
                        "monthly_revenue": "600-2500만원",
                        "development_time": "5개월",
                        "viability": "높음"
                    }
                ]
            },
            {
                "category": "금융/투자 앱",
                "apps": [
                    {
                        "name": "소액투자 소셜 플랫폼",
                        "description": "1만원부터 시작하는 공동투자, 전문가 팔로우",
                        "target": "20-30대 투자 초보자",
                        "revenue_model": "수익 수수료 10%, 프리미엄 정보료",
                        "startup_cost": "1500만원",
                        "monthly_revenue": "1000-5000만원",
                        "development_time": "6개월",
                        "viability": "매우 높음"
                    },
                    {
                        "name": "용돈 관리 교육 앱",
                        "description": "어린이/청소년 대상 용돈 관리, 부모 연동",
                        "target": "초중고생 자녀 부모",
                        "revenue_model": "월 구독료 4900원, 교육 콘텐츠",
                        "startup_cost": "400만원",
                        "monthly_revenue": "200-800만원",
                        "development_time": "3개월",
                        "viability": "높음"
                    }
                ]
            },
            {
                "category": "교육/스킬 앱",
                "apps": [
                    {
                        "name": "실시간 외국어 대화 매칭",
                        "description": "원어민과 1:1 실시간 화상 언어교환",
                        "target": "외국어 학습자 전체",
                        "revenue_model": "분당 500원, 프리미엄 클래스",
                        "startup_cost": "800만원",
                        "monthly_revenue": "600-2000만원",
                        "development_time": "4개월",
                        "viability": "매우 높음"
                    },
                    {
                        "name": "직무 스킬 마이크로러닝",
                        "description": "5분 단위 직무교육, 실무 즉시 적용",
                        "target": "직장인, 취준생",
                        "revenue_model": "월 구독료 12900원, 기업 라이센스",
                        "startup_cost": "600만원",
                        "monthly_revenue": "400-1800만원",
                        "development_time": "3개월",
                        "viability": "높음"
                    }
                ]
            }
        ]

        # 신규 사업 아이디어 (비앱 분야)
        self.innovative_business_ideas = [
            {
                "category": "서비스 혁신",
                "ideas": [
                    {
                        "name": "1시간 배송 로컬 마트",
                        "description": "동네 반경 3km 내 1시간 내 생필품 배송",
                        "startup_cost": "2000만원",
                        "monthly_revenue": "800-3000만원",
                        "viability": "매우 높음"
                    },
                    {
                        "name": "AI 기반 맞춤 도시락",
                        "description": "개인 건강데이터 기반 맞춤 영양식 제작 배달",
                        "startup_cost": "1500만원",
                        "monthly_revenue": "600-2500만원",
                        "viability": "높음"
                    },
                    {
                        "name": "공유 작업공간 + 육아",
                        "description": "부모용 코워킹 스페이스 + 아이 돌봄 통합 서비스",
                        "startup_cost": "3000만원",
                        "monthly_revenue": "1000-4000만원",
                        "viability": "높음"
                    }
                ]
            },
            {
                "category": "구독경제 모델",
                "ideas": [
                    {
                        "name": "펫 케어 구독박스",
                        "description": "반려동물 개체별 맞춤 사료, 간식, 용품 정기배송",
                        "startup_cost": "800만원",
                        "monthly_revenue": "500-2000만원",
                        "viability": "매우 높음"
                    },
                    {
                        "name": "시니어 라이프 케어",
                        "description": "어르신 대상 건강관리, 생활편의 통합 구독서비스",
                        "startup_cost": "1200만원",
                        "monthly_revenue": "700-2800만원",
                        "viability": "높음"
                    }
                ]
            }
        ]

        # 추가: 소규모 앱 아이디어 풀
        self.small_app_ideas = [
            {
                "name": "습관 체크 알림 앱",
                "description": "간단한 습관 체크리스트와 알림 기능",
                "startup_cost": "50만원",
                "monthly_revenue": "50-200만원",
                "development_time": "2주",
                "difficulty": "매우 쉬움"
            },
            {
                "name": "가계부 공유 앱",
                "description": "부부/가족이 함께 쓰는 실시간 가계부",
                "startup_cost": "100만원",
                "monthly_revenue": "100-400만원",
                "development_time": "1개월",
                "difficulty": "쉬움"
            },
            {
                "name": "동네 중고장터 알림",
                "description": "원하는 물건 올라오면 즉시 알림",
                "startup_cost": "80만원",
                "monthly_revenue": "80-300만원",
                "development_time": "3주",
                "difficulty": "쉬움"
            },
            {
                "name": "분할 계산기 프리미엄",
                "description": "더치페이 자동 계산과 송금 연동",
                "startup_cost": "60만원",
                "monthly_revenue": "60-250만원",
                "development_time": "2주",
                "difficulty": "매우 쉬움"
            },
            {
                "name": "일일 미션 챌린지",
                "description": "친구들과 함께하는 일일 챌린지 앱",
                "startup_cost": "70만원",
                "monthly_revenue": "70-280만원",
                "development_time": "3주",
                "difficulty": "쉬움"
            },
            {
                "name": "냉장고 재료 레시피",
                "description": "남은 재료로 만들 수 있는 요리 추천",
                "startup_cost": "90만원",
                "monthly_revenue": "90-350만원",
                "development_time": "1개월",
                "difficulty": "쉬움"
            },
            {
                "name": "운동 파트너 매칭",
                "description": "동네 운동 친구 찾기 앱",
                "startup_cost": "120만원",
                "monthly_revenue": "150-500만원",
                "development_time": "1.5개월",
                "difficulty": "보통"
            },
            {
                "name": "택시 합승 매칭",
                "description": "같은 방향 택시 합승자 실시간 매칭",
                "startup_cost": "150만원",
                "monthly_revenue": "200-700만원",
                "development_time": "2개월",
                "difficulty": "보통"
            },
            {
                "name": "육아 일기 공유",
                "description": "가족이 함께 쓰는 아기 성장 기록",
                "startup_cost": "80만원",
                "monthly_revenue": "100-400만원",
                "development_time": "1개월",
                "difficulty": "쉬움"
            },
            {
                "name": "동네 카페 스탬프",
                "description": "디지털 스탬프 적립 통합 앱",
                "startup_cost": "200만원",
                "monthly_revenue": "300-1000만원",
                "development_time": "2개월",
                "difficulty": "보통"
            }
        ]

        # 동적 조합용 요소들 (수백 가지 조합 가능)
        self.business_prefixes = [
            "AI", "스마트", "자동", "실시간", "맞춤형", "통합", "초간편", "프리미엄",
            "무료", "구독형", "온디맨드", "하이브리드", "올인원", "미니", "마이크로",
            "소셜", "커뮤니티", "P2P", "B2B", "로컬", "글로벌", "모바일", "클라우드",
            # 블록체인/Web3 프리픽스
            "Web3", "탈중앙화", "온체인", "크로스체인", "멀티체인", "레이어2"
        ]

        self.business_domains = [
            "헬스케어", "피트니스", "다이어트", "영양", "수면", "명상", "스트레스관리",
            "육아", "교육", "학습", "언어", "코딩", "자격증", "취업",
            "재테크", "투자", "가계부", "절약", "부업", "창업",
            "반려동물", "펫케어", "펫시터", "펫푸드",
            "여행", "숙소", "맛집", "카페", "배달",
            "패션", "뷰티", "스타일링", "쇼핑",
            "부동산", "인테리어", "이사", "청소",
            "법률", "세무", "회계", "행정",
            "결혼", "데이팅", "소개팅", "모임",
            "취미", "운동", "게임", "독서", "음악", "그림",
            # 블록체인/Web3 도메인
            "NFT", "DeFi", "토큰", "코인", "메타버스", "DAO", "스테이킹",
            "암호화폐", "블록체인", "스마트컨트랙트", "지갑", "P2E", "GameFi",
            "SocialFi", "RWA", "디지털자산", "DEX", "렌딩", "이자농사"
        ]

        self.business_types = [
            "플랫폼", "앱", "서비스", "솔루션", "시스템", "도구", "봇",
            "마켓플레이스", "커뮤니티", "네트워크", "허브", "센터",
            "매칭", "중개", "대행", "컨설팅", "코칭", "멘토링",
            "구독박스", "정기배송", "렌탈", "공유",
            "분석", "리포트", "대시보드", "트래커", "어시스턴트",
            # 블록체인/Web3 타입
            "프로토콜", "dApp", "익스플로러", "브릿지", "오라클", "인덱서"
        ]

        self.target_audiences = [
            "직장인", "대학생", "주부", "시니어", "MZ세대", "프리랜서",
            "소상공인", "스타트업", "1인기업", "중소기업",
            "신혼부부", "싱글족", "맞벌이", "워킹맘", "워킹대디"
        ]

        # 추가: 마이크로 사업 아이디어 풀
        self.micro_business_ideas = [
            {
                "name": "SNS 댓글 관리 서비스",
                "description": "인플루언서 댓글 모니터링 및 응대",
                "startup_cost": "10만원",
                "monthly_revenue": "50-150만원",
                "difficulty": "매우 쉬움"
            },
            {
                "name": "PDF 변환 서비스",
                "description": "대량 문서 PDF 변환 및 편집",
                "startup_cost": "20만원",
                "monthly_revenue": "80-200만원",
                "difficulty": "매우 쉬움"
            },
            {
                "name": "이메일 템플릿 제작",
                "description": "기업용 이메일 템플릿 디자인",
                "startup_cost": "30만원",
                "monthly_revenue": "100-300만원",
                "difficulty": "쉬움"
            },
            {
                "name": "온라인 설문조사 대행",
                "description": "설문 제작부터 분석까지 대행",
                "startup_cost": "40만원",
                "monthly_revenue": "120-350만원",
                "difficulty": "쉬움"
            },
            {
                "name": "챗봇 시나리오 작성",
                "description": "기업 고객센터 챗봇 대화 설계",
                "startup_cost": "50만원",
                "monthly_revenue": "150-400만원",
                "difficulty": "보통"
            },
            {
                "name": "유튜브 자막 제작",
                "description": "다국어 자막 제작 및 싱크 조정",
                "startup_cost": "30만원",
                "monthly_revenue": "100-250만원",
                "difficulty": "쉬움"
            },
            {
                "name": "온라인 명함 제작",
                "description": "디지털 명함 디자인 및 관리",
                "startup_cost": "20만원",
                "monthly_revenue": "60-180만원",
                "difficulty": "매우 쉬움"
            },
            {
                "name": "상품 사진 편집",
                "description": "쇼핑몰 상품 사진 보정 서비스",
                "startup_cost": "40만원",
                "monthly_revenue": "150-400만원",
                "difficulty": "쉬움"
            },
            {
                "name": "엑셀 자동화 컨설팅",
                "description": "반복 업무 엑셀 매크로 제작",
                "startup_cost": "30만원",
                "monthly_revenue": "200-500만원",
                "difficulty": "보통"
            },
            {
                "name": "블로그 대필 서비스",
                "description": "기업 블로그 콘텐츠 작성 대행",
                "startup_cost": "20만원",
                "monthly_revenue": "100-300만원",
                "difficulty": "쉬움"
            }
        ]

    def generate_dynamic_combination_ideas(self, exclude_names=None):
        """동적 조합으로 새로운 사업 아이디어 생성 (품질 향상 버전)"""
        if exclude_names is None:
            exclude_names = set()

        ideas = []
        attempts = 0
        max_attempts = 500

        # IT 사업 유형 정의 (카테고리화)
        it_business_types = {
            "saas": {
                "label": "SaaS",
                "desc": "구독 기반 소프트웨어 서비스",
                "revenue_models": ["월정액 구독", "프리미엄 요금제", "사용량 기반 과금"],
                "tech_stacks": ["Bubble.io", "Webflow", "Supabase", "Vercel"],
                "differentiators": ["자동화 기능", "실시간 동기화", "AI 분석", "맞춤 대시보드"]
            },
            "marketplace": {
                "label": "마켓플레이스",
                "desc": "수요자와 공급자를 연결하는 플랫폼",
                "revenue_models": ["거래 수수료", "프리미엄 리스팅", "광고 수익"],
                "tech_stacks": ["Sharetribe", "Bubble.io", "Webflow + Memberstack"],
                "differentiators": ["신뢰 시스템", "간편 결제", "실시간 매칭", "리뷰 시스템"]
            },
            "agency": {
                "label": "에이전시",
                "desc": "전문 서비스 대행 및 컨설팅",
                "revenue_models": ["프로젝트 단가", "리테이너 계약", "성과 수수료"],
                "tech_stacks": ["Notion", "Figma", "Slack", "Zapier"],
                "differentiators": ["전문 인력 네트워크", "빠른 턴어라운드", "품질 보장", "1:1 맞춤 서비스"]
            },
            "tools": {
                "label": "생산성 도구",
                "desc": "특정 작업을 효율화하는 도구",
                "revenue_models": ["일회성 구매", "프리미엄 기능", "API 사용료"],
                "tech_stacks": ["React", "Next.js", "Chrome Extension", "Electron"],
                "differentiators": ["간편한 UX", "빠른 처리 속도", "오프라인 지원", "다중 플랫폼"]
            },
            "platform": {
                "label": "플랫폼",
                "desc": "커뮤니티 기반 서비스 플랫폼",
                "revenue_models": ["멤버십", "광고", "프리미엄 기능", "데이터 API"],
                "tech_stacks": ["Firebase", "Supabase", "Vercel", "AWS Amplify"],
                "differentiators": ["커뮤니티 효과", "네트워크 효과", "콘텐츠 큐레이션", "개인화"]
            }
        }

        # 핵심 기능 템플릿
        core_features_by_domain = {
            "헬스케어": ["건강 기록 추적", "전문가 상담 연결", "맞춤 건강 리포트", "알림 시스템"],
            "피트니스": ["운동 루틴 관리", "진행 상황 추적", "영상 가이드", "커뮤니티 챌린지"],
            "교육": ["진도 관리", "퀴즈/테스트", "1:1 튜터링", "학습 분석"],
            "재테크": ["자산 관리", "투자 분석", "리스크 평가", "자동 리밸런싱"],
            "반려동물": ["건강 기록", "예약 시스템", "커뮤니티", "위치 추적"],
            "부동산": ["매물 검색", "시세 분석", "가상 투어", "계약 관리"],
            "여행": ["일정 계획", "실시간 정보", "예약 통합", "여행 기록"],
            "default": ["데이터 관리", "알림 시스템", "분석 대시보드", "사용자 맞춤화"]
        }

        # 차별화 포인트 템플릿
        differentiator_templates = [
            "기존 서비스 대비 {percent}% 저렴한 가격",
            "{target} 특화 기능 제공",
            "AI 기반 자동 {action}",
            "5분 만에 시작 가능한 간편 온보딩",
            "무료 플랜으로 부담 없이 시작",
            "실시간 {domain} 데이터 제공",
            "{target} 커뮤니티 네트워크",
            "모바일 앱 + 웹 동시 지원"
        ]

        modifiers = ["", "스마트", "초고속", "맞춤", "프리미엄", "간편", "전문", "AI"]
        version_tags = ["", " 2.0", " Pro", " Lite", " Plus"]

        while len(ideas) < 30 and attempts < max_attempts:
            attempts += 1

            prefix = random.choice(self.business_prefixes)
            domain = random.choice(self.business_domains)
            biz_type = random.choice(self.business_types)
            target = random.choice(self.target_audiences)
            modifier = random.choice(modifiers)
            version = random.choice(version_tags)

            # IT 사업 유형 결정
            if biz_type in ["플랫폼", "커뮤니티", "네트워크", "허브"]:
                it_type = "platform"
            elif biz_type in ["마켓플레이스", "매칭", "중개"]:
                it_type = "marketplace"
            elif biz_type in ["대행", "컨설팅", "코칭", "멘토링"]:
                it_type = "agency"
            elif biz_type in ["도구", "봇", "트래커", "어시스턴트", "분석"]:
                it_type = "tools"
            else:
                it_type = "saas"

            it_info = it_business_types[it_type]

            name_patterns = [
                f"{prefix} {domain} {biz_type}",
                f"{target} 전용 {domain} {biz_type}",
                f"{prefix} {target} {domain} 앱",
                f"{domain} {biz_type} for {target}",
                f"{prefix} {domain} 자동화",
                f"{target} {domain} 매칭 서비스",
                f"{modifier} {domain} {biz_type}",
                f"{prefix} {modifier} {domain} 서비스",
                f"{target} {domain} 솔루션{version}",
                f"{domain} AI {biz_type}",
                f"올인원 {domain} {biz_type}",
                f"넥스트젠 {domain} for {target}"
            ]

            name = random.choice(name_patterns).strip()

            if name in exclude_names:
                continue
            exclude_names.add(name)

            # 핵심 기능 선택
            domain_key = domain if domain in core_features_by_domain else "default"
            core_features = random.sample(core_features_by_domain[domain_key], min(3, len(core_features_by_domain[domain_key])))

            # 차별화 포인트 생성
            diff_template = random.choice(differentiator_templates)
            differentiator = diff_template.format(
                percent=random.choice([30, 40, 50]),
                target=target,
                action=random.choice(["분석", "추천", "매칭", "관리"]),
                domain=domain
            )

            # 비용/수익 설정
            cost_ranges = {
                "saas": {"cost": "100-300만원", "revenue": "200-800만원"},
                "marketplace": {"cost": "300-500만원", "revenue": "300-1500만원"},
                "agency": {"cost": "50-100만원", "revenue": "200-600만원"},
                "tools": {"cost": "100-200만원", "revenue": "100-500만원"},
                "platform": {"cost": "200-400만원", "revenue": "200-1000만원"}
            }
            cost_info = cost_ranges[it_type]

            # 상세 설명 생성
            detailed_description = f"{target}을 위한 {domain} 분야 {it_info['desc']}. {', '.join(core_features[:2])} 기능을 제공하며, {differentiator}."

            ideas.append({
                "type": "동적 조합 아이디어",
                "category": "IT/디지털",
                "business": {
                    "name": name,
                    "description": detailed_description,
                    "it_type": it_type,
                    "it_type_label": it_info["label"],
                    "startup_cost": cost_info["cost"],
                    "monthly_revenue": cost_info["revenue"],
                    "revenue_potential": f"월 {cost_info['revenue']}",
                    "timeline": random.choice(["2주 내 시작", "1개월 내 시작", "2개월 내 시작"]),
                    "difficulty": random.choice(["쉬움", "보통", "보통"]),
                    "viability": random.choice(["높음", "높음", "매우 높음"]),
                    "target_audience": target,
                    "domain": domain,
                    "core_features": core_features,
                    "differentiator": differentiator,
                    "revenue_models": random.sample(it_info["revenue_models"], min(2, len(it_info["revenue_models"]))),
                    "tech_stack": random.sample(it_info["tech_stacks"], min(2, len(it_info["tech_stacks"]))),
                    "competitors_hint": f"{domain} 분야 기존 서비스 대비 {target} 특화"
                },
                "priority": random.choice(["높음", "높음", "매우 높음"])
            })

        return ideas

    def generate_micro_business_ideas(self):
        """마이크로 사업 아이디어 생성"""
        ideas = []
        for micro in random.sample(self.micro_business_ideas, min(5, len(self.micro_business_ideas))):
            ideas.append({
                "type": "마이크로 비즈니스",
                "category": "초소형 창업",
                "business": micro,
                "priority": "보통"
            })
        return ideas

    def generate_small_app_ideas(self):
        """소규모 앱 아이디어 생성"""
        ideas = []
        for app in random.sample(self.small_app_ideas, min(5, len(self.small_app_ideas))):
            ideas.append({
                "type": "소규모 앱 개발",
                "category": "간단 앱",
                "business": app,
                "priority": "높음"
            })
        return ideas

    def generate_monthly_opportunities(self, exclude_names=None):
        """매월 새로운 현실적 사업 기회 생성 - 중복 방지 강화 버전"""
        if exclude_names is None:
            exclude_names = set()

        current_month = datetime.now().month
        seasons = ["겨울", "겨울", "봄", "봄", "봄", "여름", "여름", "여름", "가을", "가을", "가을", "겨울"]
        current_season = seasons[current_month - 1]

        opportunities = []
        # 이번 생성에서 추가된 이름 추적 (내부 중복 방지)
        added_names = set()

        def add_if_not_duplicate(opp):
            """중복이 아닌 경우에만 추가"""
            name = opp.get('business', {}).get('name', '')
            if name and name not in exclude_names and name not in added_names:
                opportunities.append(opp)
                added_names.add(name)
                return True
            return False

        # 즉시 시작 가능한 사업 (중복 체크)
        for category_data in self.immediate_businesses:
            for business in random.sample(category_data["businesses"], min(2, len(category_data["businesses"]))):
                add_if_not_duplicate({
                    "type": "즉시 시작 가능",
                    "category": category_data["category"],
                    "business": business,
                    "priority": "높음"
                })

        # 고수익 앱 테마 (중복 체크)
        for app_category in self.high_potential_app_themes:
            for app in random.sample(app_category["apps"], min(2, len(app_category["apps"]))):
                add_if_not_duplicate({
                    "type": "고수익 앱 개발",
                    "category": app_category["category"],
                    "business": app,
                    "priority": "매우 높음"
                })

        # 혁신 사업 아이디어 (중복 체크)
        for category in self.innovative_business_ideas:
            for idea in category["ideas"]:
                add_if_not_duplicate({
                    "type": "혁신 사업 모델",
                    "category": category["category"],
                    "business": idea,
                    "priority": "높음"
                })

        # 계절 특화 사업 (중복 체크)
        for seasonal_business in random.sample(self.seasonal_opportunities[current_season],
                                              min(3, len(self.seasonal_opportunities[current_season]))):
            add_if_not_duplicate({
                "type": "계절 특화",
                "season": current_season,
                "business": {
                    "name": seasonal_business,
                    "startup_cost": "100-300만원",
                    "revenue_potential": "월 200-500만원",
                    "timeline": "2-4주 내 시작",
                    "difficulty": "보통"
                },
                "priority": "보통"
            })

        # 기술 활용 사업 (중복 체크)
        for tech_business in self.tech_enabled_businesses:
            add_if_not_duplicate({
                "type": "기술 활용",
                "business": tech_business,
                "priority": "높음"
            })

        # 마이크로 사업 아이디어들 (중복 체크)
        for micro in random.sample(self.micro_business_ideas, min(5, len(self.micro_business_ideas))):
            add_if_not_duplicate({
                "type": "마이크로 비즈니스",
                "category": "초소형 창업",
                "business": micro,
                "priority": "보통"
            })

        # 소규모 앱 아이디어들 (중복 체크)
        for app in random.sample(self.small_app_ideas, min(5, len(self.small_app_ideas))):
            add_if_not_duplicate({
                "type": "소규모 앱 개발",
                "category": "간단 앱",
                "business": app,
                "priority": "높음"
            })

        # 동적 조합 아이디어 - exclude_names + added_names 모두 제외
        all_exclude = added_names.union(exclude_names)
        dynamic_ideas = self.generate_dynamic_combination_ideas(exclude_names=all_exclude)
        for idea in dynamic_ideas:
            add_if_not_duplicate(idea)

        return opportunities

    def generate_high_viability_themes(self):
        """사업성 높은 테마들을 체계적으로 생성"""
        themes = []

        # 앱 개발 테마들
        for category in self.high_potential_app_themes:
            for app in category["apps"]:
                themes.append({
                    "theme_type": "앱 개발",
                    "category": category["category"],
                    "idea": app,
                    "market_size": "대형" if app["viability"] == "매우 높음" else "중형",
                    "roi_score": self._calculate_roi_score(app),
                    "implementation_complexity": app["development_time"]
                })

        # 혁신 사업 테마들
        for category in self.innovative_business_ideas:
            for idea in category["ideas"]:
                themes.append({
                    "theme_type": "혁신 사업",
                    "category": category["category"],
                    "idea": idea,
                    "market_size": "대형" if idea["viability"] == "매우 높음" else "중형",
                    "roi_score": self._calculate_roi_score_for_business(idea),
                    "implementation_complexity": "중간"
                })

        # ROI 점수 기준으로 정렬
        themes.sort(key=lambda x: x["roi_score"], reverse=True)

        return themes[:10]  # 상위 10개 테마만 반환

    def _calculate_roi_score(self, app):
        """앱의 ROI 점수 계산"""
        startup_cost = int(app["startup_cost"].replace("만원", ""))
        monthly_revenue = int(app["monthly_revenue"].split("-")[1].replace("만원", ""))
        development_months = int(app["development_time"].replace("개월", ""))

        # ROI = (월매출 * 12 - 초기투자) / 초기투자
        annual_revenue = monthly_revenue * 12
        roi = (annual_revenue - startup_cost) / startup_cost

        # 개발기간 고려하여 조정
        adjusted_roi = roi / (development_months / 3)  # 3개월 기준으로 정규화

        return round(adjusted_roi, 2)

    def _calculate_roi_score_for_business(self, business):
        """일반 사업의 ROI 점수 계산"""
        startup_cost = int(business["startup_cost"].replace("만원", ""))
        monthly_revenue = int(business["monthly_revenue"].split("-")[1].replace("만원", ""))

        annual_revenue = monthly_revenue * 12
        roi = (annual_revenue - startup_cost) / startup_cost

        return round(roi, 2)

    def get_validated_business_models(self):
        """이미 검증된 비즈니스 모델들"""
        return [
            {
                "model": "구독 서비스",
                "examples": ["월간 간식박스", "펫용품 정기배송", "화장품 샘플키트"],
                "pros": "안정적 매출", 
                "cons": "초기 고객 확보 어려움",
                "success_rate": "70%"
            },
            {
                "model": "마켓플레이스",
                "examples": ["지역 특산물 온라인몰", "핸드메이드 작품 판매", "중고 명품 거래"],
                "pros": "확장성 높음",
                "cons": "플랫폼 수수료",
                "success_rate": "60%"
            },
            {
                "model": "서비스 매칭",
                "examples": ["청소 매칭", "과외 매칭", "펫시터 매칭"],
                "pros": "낮은 운영비용",
                "cons": "양방향 확보 필요",
                "success_rate": "50%"
            }
        ]

    def generate_business_meeting_agenda(self):
        """현실적 사업 검토 회의 안건 생성"""
        opportunities = self.generate_monthly_opportunities()
        validated_models = self.get_validated_business_models()
        high_viability_themes = self.generate_high_viability_themes()

        agenda = [
            "시장 검증된 비즈니스 모델 분석",
            "즉시 실행 가능한 사업 아이템 검토",
            "고수익 앱 개발 테마 분석",
            "혁신 사업 모델 검토",
            "최소 투자 고수익 모델 발굴",
            "계절별 기회 사업 평가",
            "기술 활용 저비용 창업 방안",
            "ROI 기반 우선순위 설정"
        ]

        # 가장 높은 우선순위 사업 선택
        top_opportunity = max(opportunities, key=lambda x: 1 if x['priority'] == '매우 높음' else 0.5 if x['priority'] == '높음' else 0.3)

        decisions = [
            f"이번 달 우선 검토 사업: {top_opportunity['business']['name']}",
            f"사업 유형: {top_opportunity['type']}",
            f"목표 초기 투자금: {top_opportunity['business'].get('startup_cost', '미정')}",
            f"예상 월 수익: {top_opportunity['business'].get('monthly_revenue', top_opportunity['business'].get('revenue_potential', '미정'))}",
            f"실행 우선순위: {top_opportunity['priority']}"
        ]

        action_items = [
            f"{top_opportunity['business']['name']} 상세 시장 조사 실시",
            "경쟁업체 TOP 5 분석 및 차별화 포인트 도출",
            "최소 실행 가능 제품(MVP) 개발 계획 수립",
            "타겟 고객 100명 인터뷰 및 니즈 검증",
            "수익 모델 시뮬레이션 및 손익분기점 계산",
            "파일럿 테스트 계획 수립 및 실행",
            "초기 투자 자금 조달 방안 검토",
            "팀 구성 및 역할 분담 계획"
        ]

        return {
            "meeting_type": "고수익 사업 테마 발굴 회의",
            "agenda": agenda,
            "key_decisions": decisions,
            "action_items": action_items,
            "opportunities": opportunities,
            "validated_models": validated_models,
            "high_viability_themes": high_viability_themes,
            "top_priority_business": top_opportunity
        }

if __name__ == "__main__":
    generator = RealisticBusinessGenerator()
    result = generator.generate_business_meeting_agenda()
    
    print("=== 현실적 사업 기회 발굴 결과 ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))