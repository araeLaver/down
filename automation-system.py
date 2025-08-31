#!/usr/bin/env python3
"""
AI 기반 회사 운영 자동화 시스템
- ERP 통합
- 업무 프로세스 자동화
- 의사결정 지원 시스템
"""

from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
import asyncio
import json
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ProcessStatus(Enum):
    INITIATED = "initiated"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"

class ApprovalLevel(Enum):
    EMPLOYEE = 1
    MANAGER = 2
    DIRECTOR = 3
    CEO = 4

@dataclass
class BusinessProcess:
    id: str
    name: str
    description: str
    initiator: str
    status: ProcessStatus
    approval_level: ApprovalLevel
    created_at: datetime
    updated_at: datetime
    data: Dict[str, Any]

@dataclass
class Contract:
    id: str
    client_name: str
    contract_type: str
    amount: float
    start_date: datetime
    end_date: datetime
    status: str
    terms: Dict[str, Any]

@dataclass
class Invoice:
    id: str
    contract_id: str
    amount: float
    due_date: datetime
    status: str
    line_items: List[Dict[str, Any]]

@dataclass
class Employee:
    id: str
    name: str
    position: str
    department: str
    salary: float
    hire_date: datetime
    is_ai: bool

class DatabaseManager:
    """데이터베이스 관리 클래스"""
    
    def __init__(self, db_path: str = "company.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """데이터베이스 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 테이블 생성
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processes (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                initiator TEXT,
                status TEXT,
                approval_level INTEGER,
                created_at TEXT,
                updated_at TEXT,
                data TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contracts (
                id TEXT PRIMARY KEY,
                client_name TEXT NOT NULL,
                contract_type TEXT,
                amount REAL,
                start_date TEXT,
                end_date TEXT,
                status TEXT,
                terms TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id TEXT PRIMARY KEY,
                contract_id TEXT,
                amount REAL,
                due_date TEXT,
                status TEXT,
                line_items TEXT,
                FOREIGN KEY (contract_id) REFERENCES contracts (id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                position TEXT,
                department TEXT,
                salary REAL,
                hire_date TEXT,
                is_ai BOOLEAN
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_process(self, process: BusinessProcess):
        """프로세스 저장"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO processes 
            (id, name, description, initiator, status, approval_level, created_at, updated_at, data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            process.id, process.name, process.description, process.initiator,
            process.status.value, process.approval_level.value,
            process.created_at.isoformat(), process.updated_at.isoformat(),
            json.dumps(process.data)
        ))
        
        conn.commit()
        conn.close()
    
    def get_process(self, process_id: str) -> Optional[BusinessProcess]:
        """프로세스 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM processes WHERE id = ?", (process_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return BusinessProcess(
                id=row[0], name=row[1], description=row[2], initiator=row[3],
                status=ProcessStatus(row[4]), approval_level=ApprovalLevel(row[5]),
                created_at=datetime.fromisoformat(row[6]), 
                updated_at=datetime.fromisoformat(row[7]),
                data=json.loads(row[8])
            )
        return None

class WorkflowEngine:
    """업무 프로세스 자동화 엔진"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.workflows: Dict[str, Any] = {}
        self.setup_default_workflows()
    
    def setup_default_workflows(self):
        """기본 워크플로우 설정"""
        self.workflows = {
            "expense_approval": {
                "name": "경비 승인",
                "steps": [
                    {"level": ApprovalLevel.MANAGER, "condition": "amount <= 100000"},
                    {"level": ApprovalLevel.DIRECTOR, "condition": "amount <= 1000000"},
                    {"level": ApprovalLevel.CEO, "condition": "amount > 1000000"}
                ]
            },
            "contract_approval": {
                "name": "계약 승인",
                "steps": [
                    {"level": ApprovalLevel.DIRECTOR, "condition": "amount <= 10000000"},
                    {"level": ApprovalLevel.CEO, "condition": "amount > 10000000"}
                ]
            },
            "hr_approval": {
                "name": "인사 승인",
                "steps": [
                    {"level": ApprovalLevel.MANAGER, "condition": "type == 'leave'"},
                    {"level": ApprovalLevel.DIRECTOR, "condition": "type == 'promotion'"},
                    {"level": ApprovalLevel.CEO, "condition": "type == 'hire'"}
                ]
            }
        }
    
    async def initiate_process(self, workflow_type: str, data: Dict[str, Any], initiator: str) -> str:
        """프로세스 시작"""
        workflow = self.workflows.get(workflow_type)
        if not workflow:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        process_id = f"{workflow_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 승인 레벨 결정
        approval_level = self._determine_approval_level(workflow, data)
        
        process = BusinessProcess(
            id=process_id,
            name=workflow["name"],
            description=f"{workflow['name']} 프로세스",
            initiator=initiator,
            status=ProcessStatus.INITIATED,
            approval_level=approval_level,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            data=data
        )
        
        self.db_manager.save_process(process)
        
        # 자동 승인 처리
        await self._auto_approve_if_eligible(process)
        
        return process_id
    
    def _determine_approval_level(self, workflow: Dict[str, Any], data: Dict[str, Any]) -> ApprovalLevel:
        """필요한 승인 레벨 결정"""
        for step in workflow["steps"]:
            condition = step["condition"]
            # 간단한 조건 평가 (실제로는 더 복잡한 로직 필요)
            if "amount" in condition:
                amount = data.get("amount", 0)
                if eval(condition.replace("amount", str(amount))):
                    return step["level"]
            elif "type" in condition:
                type_val = data.get("type", "")
                if eval(condition.replace("type", f"'{type_val}'")):
                    return step["level"]
        
        return ApprovalLevel.CEO
    
    async def _auto_approve_if_eligible(self, process: BusinessProcess):
        """자동 승인 가능한 경우 처리"""
        # 소액 경비는 자동 승인
        if (process.name == "경비 승인" and 
            process.data.get("amount", 0) <= 50000):
            await self.approve_process(process.id, "system_auto", "자동 승인 (소액)")

    async def approve_process(self, process_id: str, approver: str, comment: str = ""):
        """프로세스 승인"""
        process = self.db_manager.get_process(process_id)
        if not process:
            raise ValueError(f"Process not found: {process_id}")
        
        process.status = ProcessStatus.APPROVED
        process.updated_at = datetime.now()
        process.data["approver"] = approver
        process.data["approval_comment"] = comment
        process.data["approved_at"] = datetime.now().isoformat()
        
        self.db_manager.save_process(process)
        
        # 후속 액션 실행
        await self._execute_post_approval_actions(process)
    
    async def _execute_post_approval_actions(self, process: BusinessProcess):
        """승인 후 액션 실행"""
        if process.name == "경비 승인":
            # 회계 시스템에 경비 등록
            await self._register_expense(process.data)
        elif process.name == "계약 승인":
            # 계약 시스템에 등록
            await self._register_contract(process.data)
    
    async def _register_expense(self, data: Dict[str, Any]):
        """경비 등록"""
        print(f"경비 등록: {data.get('description')} - {data.get('amount')}원")
    
    async def _register_contract(self, data: Dict[str, Any]):
        """계약 등록"""
        print(f"계약 등록: {data.get('client')} - {data.get('amount')}원")

class ERPIntegration:
    """ERP 시스템 통합"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    async def create_contract(self, contract_data: Dict[str, Any]) -> Contract:
        """계약 생성"""
        contract = Contract(
            id=f"CTR_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            client_name=contract_data["client_name"],
            contract_type=contract_data["contract_type"],
            amount=contract_data["amount"],
            start_date=datetime.fromisoformat(contract_data["start_date"]),
            end_date=datetime.fromisoformat(contract_data["end_date"]),
            status="active",
            terms=contract_data.get("terms", {})
        )
        
        # DB에 저장
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contracts (id, client_name, contract_type, amount, start_date, end_date, status, terms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            contract.id, contract.client_name, contract.contract_type, contract.amount,
            contract.start_date.isoformat(), contract.end_date.isoformat(),
            contract.status, json.dumps(contract.terms)
        ))
        conn.commit()
        conn.close()
        
        return contract
    
    async def generate_invoice(self, contract_id: str, billing_data: Dict[str, Any]) -> Invoice:
        """송장 생성"""
        invoice = Invoice(
            id=f"INV_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            contract_id=contract_id,
            amount=billing_data["amount"],
            due_date=datetime.now() + timedelta(days=30),
            status="pending",
            line_items=billing_data.get("line_items", [])
        )
        
        # DB에 저장
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO invoices (id, contract_id, amount, due_date, status, line_items)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            invoice.id, invoice.contract_id, invoice.amount,
            invoice.due_date.isoformat(), invoice.status,
            json.dumps(invoice.line_items)
        ))
        conn.commit()
        conn.close()
        
        return invoice
    
    async def get_financial_dashboard(self) -> Dict[str, Any]:
        """재무 대시보드 데이터"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        # 계약 현황
        cursor.execute("SELECT COUNT(*), SUM(amount) FROM contracts WHERE status = 'active'")
        active_contracts = cursor.fetchone()
        
        # 송장 현황
        cursor.execute("SELECT COUNT(*), SUM(amount) FROM invoices WHERE status = 'pending'")
        pending_invoices = cursor.fetchone()
        
        cursor.execute("SELECT COUNT(*), SUM(amount) FROM invoices WHERE status = 'paid'")
        paid_invoices = cursor.fetchone()
        
        conn.close()
        
        return {
            "active_contracts": {
                "count": active_contracts[0] or 0,
                "total_value": active_contracts[1] or 0
            },
            "pending_invoices": {
                "count": pending_invoices[0] or 0,
                "total_amount": pending_invoices[1] or 0
            },
            "paid_invoices": {
                "count": paid_invoices[0] or 0,
                "total_amount": paid_invoices[1] or 0
            }
        }

class NotificationSystem:
    """알림 시스템"""
    
    def __init__(self):
        self.email_config = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "username": "",  # 설정 필요
            "password": ""   # 설정 필요
        }
    
    async def send_approval_notification(self, approver_email: str, process_id: str, process_name: str):
        """승인 요청 알림 발송"""
        subject = f"[승인 요청] {process_name}"
        body = f"""
        승인이 필요한 프로세스가 있습니다.
        
        프로세스 ID: {process_id}
        프로세스명: {process_name}
        
        승인 페이지에서 확인하시기 바랍니다.
        """
        
        # 이메일 발송 (실제 설정 시 활성화)
        # await self._send_email(approver_email, subject, body)
        
        print(f"알림 발송: {approver_email} - {subject}")
    
    async def _send_email(self, to_email: str, subject: str, body: str):
        """이메일 발송"""
        if not self.email_config["username"]:
            return  # 설정되지 않은 경우 스킵
        
        msg = MIMEMultipart()
        msg['From'] = self.email_config["username"]
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        try:
            server = smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"])
            server.starttls()
            server.login(self.email_config["username"], self.email_config["password"])
            
            text = msg.as_string()
            server.sendmail(self.email_config["username"], to_email, text)
            server.quit()
        except Exception as e:
            print(f"이메일 발송 실패: {e}")

class CompanyAutomationSystem:
    """회사 운영 자동화 시스템 메인 클래스"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.workflow_engine = WorkflowEngine(self.db_manager)
        self.erp_integration = ERPIntegration(self.db_manager)
        self.notification_system = NotificationSystem()
    
    async def process_expense_request(self, employee_id: str, amount: float, description: str, category: str):
        """경비 신청 처리"""
        data = {
            "employee_id": employee_id,
            "amount": amount,
            "description": description,
            "category": category,
            "requested_date": datetime.now().isoformat()
        }
        
        process_id = await self.workflow_engine.initiate_process("expense_approval", data, employee_id)
        print(f"경비 신청 접수: {process_id}")
        
        return process_id
    
    async def process_contract_request(self, client_data: Dict[str, Any], contract_terms: Dict[str, Any]):
        """계약 요청 처리"""
        data = {
            "client_name": client_data["name"],
            "amount": contract_terms["amount"],
            "contract_type": contract_terms["type"],
            "start_date": contract_terms["start_date"],
            "end_date": contract_terms["end_date"],
            "terms": contract_terms
        }
        
        process_id = await self.workflow_engine.initiate_process("contract_approval", data, "sales_team")
        print(f"계약 승인 요청: {process_id}")
        
        return process_id
    
    async def daily_operations_check(self):
        """일일 운영 체크"""
        print("=== 일일 운영 현황 체크 ===")
        
        # 재무 현황
        dashboard = await self.erp_integration.get_financial_dashboard()
        print(f"활성 계약: {dashboard['active_contracts']['count']}건 (총 {dashboard['active_contracts']['total_value']:,.0f}원)")
        print(f"미수금: {dashboard['pending_invoices']['count']}건 (총 {dashboard['pending_invoices']['total_amount']:,.0f}원)")
        
        # 승인 대기 프로세스 확인
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM processes WHERE status = 'initiated'")
        pending_count = cursor.fetchone()[0]
        conn.close()
        
        print(f"승인 대기 프로세스: {pending_count}건")
        
        # 월말 정산 자동 실행 (매월 말일)
        today = datetime.now()
        if today.day == 28 and today.month == 2:  # 2월 28일
            await self._monthly_closing()
        elif today.day == 30 and today.month in [4, 6, 9, 11]:  # 30일이 마지막인 월
            await self._monthly_closing()
        elif today.day == 31:  # 31일이 마지막인 월
            await self._monthly_closing()
    
    async def _monthly_closing(self):
        """월말 정산"""
        print("월말 정산 자동 실행 중...")
        
        # 월별 매출 집계
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        current_month = datetime.now().strftime('%Y-%m')
        cursor.execute("""
            SELECT SUM(amount) FROM invoices 
            WHERE status = 'paid' AND date(due_date) LIKE ?
        """, (f"{current_month}%",))
        
        monthly_revenue = cursor.fetchone()[0] or 0
        conn.close()
        
        print(f"이번 달 매출: {monthly_revenue:,.0f}원")
        
        # 재무 보고서 자동 생성
        await self._generate_financial_report(current_month, monthly_revenue)
    
    async def _generate_financial_report(self, month: str, revenue: float):
        """재무 보고서 생성"""
        report = f"""
        === {month} 월간 재무 보고서 ===
        
        매출: {revenue:,.0f}원
        생성일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        # 보고서 파일 저장
        with open(f"financial_report_{month.replace('-', '_')}.txt", "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"재무 보고서 생성 완료: financial_report_{month.replace('-', '_')}.txt")

# 사용 예시
async def demo_automation_system():
    """자동화 시스템 데모"""
    system = CompanyAutomationSystem()
    
    print("=== AI 회사 운영 자동화 시스템 데모 ===\n")
    
    # 1. 경비 신청 처리
    print("1. 경비 신청 처리")
    await system.process_expense_request("dev_001", 45000, "개발 도구 구입", "소프트웨어")
    await system.process_expense_request("sales_001", 150000, "고객 접대비", "영업비")
    print()
    
    # 2. 계약 요청 처리  
    print("2. 계약 요청 처리")
    client_data = {"name": "ABC 기업"}
    contract_terms = {
        "amount": 50000000,
        "type": "서비스 계약",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
    await system.process_contract_request(client_data, contract_terms)
    print()
    
    # 3. ERP 통합 기능
    print("3. ERP 계약 및 송장 생성")
    contract = await system.erp_integration.create_contract({
        "client_name": "XYZ 회사",
        "contract_type": "개발 용역",
        "amount": 30000000,
        "start_date": "2024-01-01",
        "end_date": "2024-06-30"
    })
    print(f"계약 생성됨: {contract.id}")
    
    invoice = await system.erp_integration.generate_invoice(contract.id, {
        "amount": 10000000,
        "line_items": [{"description": "1월 용역비", "amount": 10000000}]
    })
    print(f"송장 생성됨: {invoice.id}")
    print()
    
    # 4. 일일 운영 체크
    print("4. 일일 운영 현황 체크")
    await system.daily_operations_check()

if __name__ == "__main__":
    asyncio.run(demo_automation_system())