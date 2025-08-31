#!/usr/bin/env python3
"""
AI 임직원 시스템 아키텍처
AI 기반 법인회사의 핵심 시스템
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
import asyncio
import json
import logging

class Department(Enum):
    EXECUTIVE = "executive"
    DEVELOPMENT = "development"
    SALES = "sales"
    MARKETING = "marketing"
    FINANCE = "finance"
    CUSTOMER_SUPPORT = "customer_support"
    HR = "hr"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    id: str
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    assigned_to: str
    created_at: datetime
    due_date: Optional[datetime]
    metadata: Dict[str, Any]

class AIEmployee(ABC):
    """AI 직원 기본 클래스"""
    
    def __init__(self, 
                 employee_id: str, 
                 name: str, 
                 role: str, 
                 department: Department,
                 llm_config: Dict[str, Any]):
        self.employee_id = employee_id
        self.name = name
        self.role = role
        self.department = department
        self.llm_config = llm_config
        self.tasks: List[Task] = []
        self.skills: List[str] = []
        self.performance_metrics: Dict[str, Any] = {}
        self.is_active = True
        
    @abstractmethod
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """작업 실행"""
        pass
    
    @abstractmethod
    async def collaborate(self, other_employee: 'AIEmployee', context: str) -> str:
        """다른 AI 직원과 협업"""
        pass
    
    def add_skill(self, skill: str):
        """스킬 추가"""
        if skill not in self.skills:
            self.skills.append(skill)
    
    def update_performance(self, metric: str, value: Any):
        """성과 지표 업데이트"""
        self.performance_metrics[metric] = value
        self.performance_metrics['last_updated'] = datetime.now()

class AICEOEmployee(AIEmployee):
    """AI CEO"""
    
    def __init__(self, employee_id: str, llm_config: Dict[str, Any]):
        super().__init__(employee_id, "AI CEO", "Chief Executive Officer", 
                        Department.EXECUTIVE, llm_config)
        self.skills = ["strategic_planning", "decision_making", "leadership", "vision_setting"]
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        # CEO 업무 처리 로직
        prompt = f"""
        당신은 회사의 CEO입니다. 다음 업무를 처리해주세요:
        
        업무: {task.title}
        설명: {task.description}
        우선순위: {task.priority.name}
        
        CEO로서 전략적 관점에서 이 업무를 어떻게 처리할지 계획을 세우고 실행하세요.
        """
        
        result = await self._call_llm(prompt)
        return {"status": "completed", "result": result, "timestamp": datetime.now()}
    
    async def collaborate(self, other_employee: AIEmployee, context: str) -> str:
        prompt = f"""
        당신은 CEO로서 {other_employee.role}({other_employee.name})과 협업하고 있습니다.
        
        협업 상황: {context}
        
        CEO로서 어떤 지시사항이나 의견을 제시하시겠습니까?
        """
        
        return await self._call_llm(prompt)
    
    async def _call_llm(self, prompt: str) -> str:
        # 실제 LLM API 호출 로직
        # 여기서는 모의 응답 반환
        return f"CEO 응답: {prompt[:50]}..."

class AICFOEmployee(AIEmployee):
    """AI CFO (재무 담당)"""
    
    def __init__(self, employee_id: str, llm_config: Dict[str, Any]):
        super().__init__(employee_id, "AI CFO", "Chief Financial Officer", 
                        Department.FINANCE, llm_config)
        self.skills = ["financial_analysis", "budgeting", "accounting", "risk_management"]
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        prompt = f"""
        당신은 회사의 CFO입니다. 다음 재무 관련 업무를 처리해주세요:
        
        업무: {task.title}
        설명: {task.description}
        
        재무적 관점에서 분석하고 필요한 조치를 취하세요.
        """
        
        result = await self._call_llm(prompt)
        return {"status": "completed", "result": result, "timestamp": datetime.now()}
    
    async def collaborate(self, other_employee: AIEmployee, context: str) -> str:
        prompt = f"""
        CFO로서 {other_employee.role}과 재무 관련 협업을 진행합니다.
        
        상황: {context}
        
        재무적 조언이나 승인 사항을 제시하세요.
        """
        
        return await self._call_llm(prompt)
    
    async def _call_llm(self, prompt: str) -> str:
        return f"CFO 응답: {prompt[:50]}..."

class AIDeveloperEmployee(AIEmployee):
    """AI 개발자"""
    
    def __init__(self, employee_id: str, name: str, llm_config: Dict[str, Any]):
        super().__init__(employee_id, name, "Software Developer", 
                        Department.DEVELOPMENT, llm_config)
        self.skills = ["python", "javascript", "database", "api_development", "testing"]
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        prompt = f"""
        당신은 소프트웨어 개발자입니다. 다음 개발 업무를 처리해주세요:
        
        업무: {task.title}
        설명: {task.description}
        
        코드 작성, 디버깅, 테스트 등 개발 업무를 수행하세요.
        """
        
        result = await self._call_llm(prompt)
        return {"status": "completed", "result": result, "timestamp": datetime.now()}
    
    async def collaborate(self, other_employee: AIEmployee, context: str) -> str:
        prompt = f"""
        개발자로서 {other_employee.role}과 협업합니다.
        
        상황: {context}
        
        기술적 관점에서 조언이나 해결책을 제시하세요.
        """
        
        return await self._call_llm(prompt)
    
    async def _call_llm(self, prompt: str) -> str:
        return f"개발자 응답: {prompt[:50]}..."

class AISalesEmployee(AIEmployee):
    """AI 영업 담당자"""
    
    def __init__(self, employee_id: str, name: str, llm_config: Dict[str, Any]):
        super().__init__(employee_id, name, "Sales Representative", 
                        Department.SALES, llm_config)
        self.skills = ["sales", "customer_relationship", "negotiation", "product_knowledge"]
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        prompt = f"""
        당신은 영업 담당자입니다. 다음 영업 업무를 처리해주세요:
        
        업무: {task.title}
        설명: {task.description}
        
        고객과의 관계 구축, 제안서 작성, 계약 협상 등을 수행하세요.
        """
        
        result = await self._call_llm(prompt)
        return {"status": "completed", "result": result, "timestamp": datetime.now()}
    
    async def collaborate(self, other_employee: AIEmployee, context: str) -> str:
        prompt = f"""
        영업 담당자로서 {other_employee.role}과 협업합니다.
        
        상황: {context}
        
        영업 관점에서 고객 요구사항이나 시장 피드백을 공유하세요.
        """
        
        return await self._call_llm(prompt)
    
    async def _call_llm(self, prompt: str) -> str:
        return f"영업 담당자 응답: {prompt[:50]}..."

class AIEmployeeManager:
    """AI 직원 관리 시스템"""
    
    def __init__(self):
        self.employees: Dict[str, AIEmployee] = {}
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        
    def add_employee(self, employee: AIEmployee):
        """AI 직원 추가"""
        self.employees[employee.employee_id] = employee
        logging.info(f"AI 직원 추가됨: {employee.name} ({employee.role})")
    
    def remove_employee(self, employee_id: str):
        """AI 직원 제거"""
        if employee_id in self.employees:
            employee = self.employees[employee_id]
            del self.employees[employee_id]
            logging.info(f"AI 직원 제거됨: {employee.name}")
    
    def assign_task(self, task: Task, employee_id: str):
        """업무 할당"""
        if employee_id in self.employees:
            employee = self.employees[employee_id]
            employee.tasks.append(task)
            task.assigned_to = employee_id
            self.task_queue.append(task)
            logging.info(f"업무 할당: {task.title} -> {employee.name}")
    
    async def execute_pending_tasks(self):
        """대기 중인 모든 업무 실행"""
        pending_tasks = [task for task in self.task_queue if task.status == TaskStatus.PENDING]
        
        for task in pending_tasks:
            if task.assigned_to in self.employees:
                employee = self.employees[task.assigned_to]
                task.status = TaskStatus.IN_PROGRESS
                
                try:
                    result = await employee.execute_task(task)
                    task.status = TaskStatus.COMPLETED
                    self.completed_tasks.append(task)
                    logging.info(f"업무 완료: {task.title} by {employee.name}")
                except Exception as e:
                    task.status = TaskStatus.FAILED
                    logging.error(f"업무 실패: {task.title} - {str(e)}")
    
    def get_employee_performance(self, employee_id: str) -> Dict[str, Any]:
        """직원 성과 조회"""
        if employee_id in self.employees:
            employee = self.employees[employee_id]
            completed_tasks = len([t for t in employee.tasks if t.status == TaskStatus.COMPLETED])
            failed_tasks = len([t for t in employee.tasks if t.status == TaskStatus.FAILED])
            
            return {
                "employee_id": employee_id,
                "name": employee.name,
                "role": employee.role,
                "completed_tasks": completed_tasks,
                "failed_tasks": failed_tasks,
                "success_rate": completed_tasks / (completed_tasks + failed_tasks) if (completed_tasks + failed_tasks) > 0 else 0,
                "skills": employee.skills,
                "metrics": employee.performance_metrics
            }
        return {}
    
    def get_department_status(self, department: Department) -> Dict[str, Any]:
        """부서별 현황 조회"""
        dept_employees = [emp for emp in self.employees.values() if emp.department == department]
        
        total_tasks = sum(len(emp.tasks) for emp in dept_employees)
        completed_tasks = sum(len([t for t in emp.tasks if t.status == TaskStatus.COMPLETED]) for emp in dept_employees)
        
        return {
            "department": department.value,
            "employee_count": len(dept_employees),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
            "employees": [{"id": emp.employee_id, "name": emp.name, "role": emp.role} for emp in dept_employees]
        }

# 사용 예시 및 초기 설정
async def initialize_ai_company():
    """AI 회사 초기 설정"""
    manager = AIEmployeeManager()
    
    # LLM 설정
    llm_config = {
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    # AI 임원진 추가
    ceo = AICEOEmployee("ceo_001", llm_config)
    cfo = AICFOEmployee("cfo_001", llm_config)
    
    manager.add_employee(ceo)
    manager.add_employee(cfo)
    
    # AI 개발팀 추가
    dev1 = AIDeveloperEmployee("dev_001", "AI Developer Alpha", llm_config)
    dev2 = AIDeveloperEmployee("dev_002", "AI Developer Beta", llm_config)
    
    manager.add_employee(dev1)
    manager.add_employee(dev2)
    
    # AI 영업팀 추가
    sales1 = AISalesEmployee("sales_001", "AI Sales Rep Alpha", llm_config)
    
    manager.add_employee(sales1)
    
    # 샘플 업무 생성
    task1 = Task(
        id="task_001",
        title="Q4 사업 계획 수립",
        description="4분기 사업 계획을 수립하고 각 부서별 목표를 설정하세요",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PENDING,
        assigned_to="",
        created_at=datetime.now(),
        due_date=None,
        metadata={}
    )
    
    task2 = Task(
        id="task_002",
        title="고객 관리 시스템 개발",
        description="CRM 시스템의 새로운 기능을 개발하세요",
        priority=TaskPriority.MEDIUM,
        status=TaskStatus.PENDING,
        assigned_to="",
        created_at=datetime.now(),
        due_date=None,
        metadata={}
    )
    
    # 업무 할당
    manager.assign_task(task1, "ceo_001")
    manager.assign_task(task2, "dev_001")
    
    # 업무 실행
    await manager.execute_pending_tasks()
    
    # 성과 리포트
    print("=== AI 직원 성과 리포트 ===")
    for emp_id in manager.employees:
        performance = manager.get_employee_performance(emp_id)
        print(f"{performance['name']} ({performance['role']})")
        print(f"  완료 업무: {performance['completed_tasks']}")
        print(f"  실패 업무: {performance['failed_tasks']}")
        print(f"  성공률: {performance['success_rate']:.2%}")
        print()
    
    return manager

if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # AI 회사 초기화 및 실행
    asyncio.run(initialize_ai_company())