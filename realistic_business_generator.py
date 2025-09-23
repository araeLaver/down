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

    def generate_monthly_opportunities(self):
        """매월 새로운 현실적 사업 기회 생성"""
        current_month = datetime.now().month
        seasons = ["겨울", "겨울", "봄", "봄", "봄", "여름", "여름", "여름", "가을", "가을", "가을", "겨울"]
        current_season = seasons[current_month - 1]

        opportunities = []

        # 즉시 시작 가능한 사업 2개
        for category_data in random.sample(self.immediate_businesses, 2):
            business = random.choice(category_data["businesses"])
            opportunities.append({
                "type": "즉시 시작 가능",
                "category": category_data["category"],
                "business": business,
                "priority": "높음"
            })

        # 고수익 앱 테마 2개 (새로 추가)
        for app_category in random.sample(self.high_potential_app_themes, 2):
            app = random.choice(app_category["apps"])
            opportunities.append({
                "type": "고수익 앱 개발",
                "category": app_category["category"],
                "business": app,
                "priority": "매우 높음"
            })

        # 혁신 사업 아이디어 1개 (새로 추가)
        innovation_category = random.choice(self.innovative_business_ideas)
        innovation_idea = random.choice(innovation_category["ideas"])
        opportunities.append({
            "type": "혁신 사업 모델",
            "category": innovation_category["category"],
            "business": innovation_idea,
            "priority": "높음"
        })

        # 계절 특화 사업 1개
        seasonal_business = random.choice(self.seasonal_opportunities[current_season])
        opportunities.append({
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

        # 기술 활용 사업 1개
        tech_business = random.choice(self.tech_enabled_businesses)
        opportunities.append({
            "type": "기술 활용",
            "business": tech_business,
            "priority": "높음"
        })

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