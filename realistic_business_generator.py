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
        
        agenda = [
            "시장 검증된 비즈니스 모델 분석",
            "즉시 실행 가능한 사업 아이템 검토",
            "최소 투자 고수익 모델 발굴",
            "계절별 기회 사업 평가",
            "기술 활용 저비용 창업 방안"
        ]
        
        decisions = [
            f"이번 달 우선 검토 사업: {opportunities[0]['business']['name']}",
            f"목표 초기 투자금: {opportunities[0]['business']['startup_cost']}",
            f"예상 수익 달성 시점: {opportunities[0]['business']['timeline']}"
        ]
        
        action_items = [
            f"{opportunities[0]['business']['name']} 시장 조사 실시",
            "경쟁업체 가격 분석 및 차별화 포인트 도출",
            "최소 실행 가능 제품(MVP) 개발 계획 수립",
            "초기 고객 100명 확보 전략 수립",
            "월 손익분기점 달성 로드맵 작성"
        ]
        
        return {
            "meeting_type": "현실적 사업 발굴 회의",
            "agenda": agenda,
            "key_decisions": decisions,
            "action_items": action_items,
            "opportunities": opportunities,
            "validated_models": validated_models
        }

if __name__ == "__main__":
    generator = RealisticBusinessGenerator()
    result = generator.generate_business_meeting_agenda()
    
    print("=== 현실적 사업 기회 발굴 결과 ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))