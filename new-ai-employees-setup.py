#!/usr/bin/env python3
"""
확장 예정 AI 직원 3명 셋업
- 마케팅팀: Stella Market
- 고객지원팀: Grace Support  
- 인사팀: Helen HR
"""

from ai_employee_system import AIEmployee, Department
from datetime import datetime
from typing import Dict, List, Any

class AIMarketingEmployee(AIEmployee):
    """AI 마케팅 전문가 - Stella Market"""
    
    def __init__(self, employee_id: str, llm_config: Dict[str, Any]):
        super().__init__(employee_id, "Stella Market", "Marketing Specialist", 
                        Department.MARKETING, llm_config)
        self.skills = [
            "digital_marketing", "content_creation", "seo", "social_media", 
            "campaign_planning", "brand_management", "analytics"
        ]
        self.personality = {
            "trait": "창의적이고 트렌드에 민감한 마케팅 전문가",
            "communication_style": "친근하고 설득력 있는 어조",
            "expertise": "디지털 마케팅 캠페인 기획 및 브랜드 구축"
        }
    
    async def execute_task(self, task) -> Dict[str, Any]:
        prompt = f"""
        당신은 Stella Market, 창의적인 AI 마케팅 전문가입니다.
        
        성격: 트렌드에 민감하고 창의적이며, 고객 중심적 사고를 합니다.
        전문분야: 디지털 마케팅, 콘텐츠 마케팅, SNS 마케팅, 브랜드 관리
        
        업무: {task.title}
        설명: {task.description}
        
        마케팅 전문가로서 다음을 고려하여 업무를 처리하세요:
        1. 타겟 고객 분석
        2. 경쟁사 대비 차별화 포인트
        3. 효과적인 마케팅 채널 선택
        4. 예산 효율성
        5. 측정 가능한 KPI 설정
        
        창의적이고 실행 가능한 마케팅 솔루션을 제시해주세요.
        """
        
        result = await self._call_llm(prompt)
        return {"status": "completed", "result": result, "timestamp": datetime.now()}
    
    async def collaborate(self, other_employee, context: str) -> str:
        prompt = f"""
        마케팅 전문가 Stella로서 {other_employee.role}과 협업합니다.
        
        협업 상황: {context}
        
        마케팅 관점에서 다음을 제공하세요:
        - 시장 트렌드 분석
        - 고객 피드백 및 시장 반응
        - 브랜드 일관성 유지 방안
        - 효과적인 프로모션 전략
        """
        
        return await self._call_llm(prompt)
    
    async def _call_llm(self, prompt: str) -> str:
        return f"Stella Market: {prompt[:100]}..."

class AICustomerSupportEmployee(AIEmployee):
    """AI 고객지원 전문가 - Grace Support"""
    
    def __init__(self, employee_id: str, llm_config: Dict[str, Any]):
        super().__init__(employee_id, "Grace Support", "Customer Support Specialist", 
                        Department.CUSTOMER_SUPPORT, llm_config)
        self.skills = [
            "customer_service", "technical_support", "complaint_handling",
            "communication", "empathy", "problem_solving", "documentation"
        ]
        self.personality = {
            "trait": "친절하고 인내심 있는 고객 서비스 전문가",
            "communication_style": "공감적이고 해결 중심적인 어조",
            "expertise": "고객 문제 해결 및 만족도 향상"
        }
    
    async def execute_task(self, task) -> Dict[str, Any]:
        prompt = f"""
        당신은 Grace Support, 친절하고 전문적인 AI 고객지원 담당자입니다.
        
        성격: 인내심이 많고 공감 능력이 뛰어나며, 항상 고객 입장에서 생각합니다.
        전문분야: 고객 문의 응답, 기술 지원, 불만 처리, 고객 만족도 관리
        
        업무: {task.title}
        설명: {task.description}
        
        고객지원 전문가로서 다음을 고려하여 업무를 처리하세요:
        1. 고객의 감정과 상황 이해
        2. 명확하고 이해하기 쉬운 설명
        3. 단계별 해결 방법 제시
        4. 추가 지원 방안 안내
        5. 고객 만족도 확인
        
        친절하고 전문적인 고객 서비스를 제공해주세요.
        """
        
        result = await self._call_llm(prompt)
        return {"status": "completed", "result": result, "timestamp": datetime.now()}
    
    async def collaborate(self, other_employee, context: str) -> str:
        prompt = f"""
        고객지원 전문가 Grace로서 {other_employee.role}과 협업합니다.
        
        협업 상황: {context}
        
        고객지원 관점에서 다음을 제공하세요:
        - 고객 피드백 및 불만 사항
        - 자주 발생하는 문제점 분석
        - 사용자 경험 개선 제안
        - 고객 만족도 향상 방안
        """
        
        return await self._call_llm(prompt)
    
    async def _call_llm(self, prompt: str) -> str:
        return f"Grace Support: {prompt[:100]}..."

class AIHREmployee(AIEmployee):
    """AI 인사 전문가 - Helen HR"""
    
    def __init__(self, employee_id: str, llm_config: Dict[str, Any]):
        super().__init__(employee_id, "Helen HR", "HR Specialist", 
                        Department.HR, llm_config)
        self.skills = [
            "recruitment", "performance_management", "training_development",
            "employee_relations", "organizational_culture", "compensation"
        ]
        self.personality = {
            "trait": "공정하고 체계적인 인사 관리 전문가",
            "communication_style": "명확하고 배려심 있는 어조",
            "expertise": "조직 관리 및 인재 개발"
        }
    
    async def execute_task(self, task) -> Dict[str, Any]:
        prompt = f"""
        당신은 Helen HR, 전략적 사고를 갖춘 AI 인사 전문가입니다.
        
        성격: 공정하고 체계적이며, 조직과 개인의 성장을 동시에 추구합니다.
        전문분야: 채용, 성과관리, 교육훈련, 조직문화, 급여복리후생
        
        업무: {task.title}
        설명: {task.description}
        
        인사 전문가로서 다음을 고려하여 업무를 처리하세요:
        1. 조직의 전략적 목표와 연계
        2. 공정하고 투명한 프로세스
        3. 개인과 조직의 성장 균형
        4. 법적 컴플라이언스 준수
        5. 데이터 기반 의사결정
        
        전략적이고 실행 가능한 인사 솔루션을 제시해주세요.
        """
        
        result = await self._call_llm(prompt)
        return {"status": "completed", "result": result, "timestamp": datetime.now()}
    
    async def collaborate(self, other_employee, context: str) -> str:
        prompt = f"""
        인사 전문가 Helen으로서 {other_employee.role}과 협업합니다.
        
        협업 상황: {context}
        
        인사 관점에서 다음을 제공하세요:
        - 조직 역량 및 인력 현황 분석
        - 팀 협업 효율성 개선 방안
        - 교육 및 개발 필요사항
        - 성과 관리 및 동기부여 방안
        """
        
        return await self._call_llm(prompt)
    
    async def _call_llm(self, prompt: str) -> str:
        return f"Helen HR: {prompt[:100]}..."

# 새로운 AI 직원들을 기존 시스템에 통합
def setup_new_employees():
    """새로운 AI 직원 3명 셋업"""
    from ai_employee_system import AIEmployeeManager
    
    manager = AIEmployeeManager()
    
    # LLM 설정
    llm_config = {
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    # 새로운 AI 직원들 생성
    stella = AIMarketingEmployee("mkt_001", llm_config)
    grace = AICustomerSupportEmployee("cs_001", llm_config)  
    helen = AIHREmployee("hr_001", llm_config)
    
    # 매니저에 추가
    manager.add_employee(stella)
    manager.add_employee(grace)
    manager.add_employee(helen)
    
    print("=== 새로운 AI 직원 3명 셋업 완료 ===")
    print(f"🎨 {stella.name} ({stella.role}) - 마케팅팀 합류")
    print(f"💬 {grace.name} ({grace.role}) - 고객지원팀 합류") 
    print(f"👥 {helen.name} ({helen.role}) - 인사팀 합류")
    print("\n총 직원 수: 9명 (인간 CEO 1명 + AI 직원 8명)")
    
    return manager

if __name__ == "__main__":
    # 새로운 AI 직원들 셋업 실행
    setup_new_employees()