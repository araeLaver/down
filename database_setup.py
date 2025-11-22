"""
Qhyx Inc. 데이터베이스 스키마 설정 및 초기화
Koyeb PostgreSQL 연결 및 전용 스키마 생성
회사명: Qhyx (큐히익스) - Quantum Hope Youth eXcellence
"""

from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, DateTime, Float, JSON, Date, Boolean, ForeignKey, Index
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Koyeb PostgreSQL 연결 설정
connection_string = URL.create(
    'postgresql',
    username='unble',
    password='npg_1kjV0mhECxqs',
    host='ep-divine-bird-a1f4mly5.ap-southeast-1.pg.koyeb.app',
    database='unble',
)

# 엔진 생성
engine = create_engine(connection_string, pool_pre_ping=True, pool_size=10)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# 스키마 이름 - Qhyx Inc.
SCHEMA_NAME = 'qhyx_growth'

def create_schema():
    """전용 스키마 생성"""
    with engine.connect() as conn:
        # 스키마 존재 확인 및 생성
        result = conn.execute(text(f"""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name = '{SCHEMA_NAME}'
        """))
        
        if not result.fetchone():
            conn.execute(text(f"CREATE SCHEMA {SCHEMA_NAME}"))
            conn.commit()
            print(f"스키마 '{SCHEMA_NAME}' 생성됨")
        else:
            print(f"스키마 '{SCHEMA_NAME}' 이미 존재")

# 테이블 정의 (전용 스키마 사용)
class ActivityLog(Base):
    __tablename__ = 'activity_logs'
    __table_args__ = {
        'schema': SCHEMA_NAME,
        'extend_existing': True
    }
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    activity_type = Column(String(50), nullable=False)
    description = Column(String(500))
    details = Column(JSON)
    status = Column(String(20), default='info')
    user_id = Column(String(100))
    ip_address = Column(String(45))
    
    # 인덱스 추가
    __table_args__ = (
        Index('idx_activity_timestamp', 'timestamp'),
        Index('idx_activity_type', 'activity_type'),
        {'schema': SCHEMA_NAME, 'extend_existing': True}
    )

class SyncLog(Base):
    __tablename__ = 'sync_logs'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    action = Column(String(50), nullable=False)
    message = Column(String(1000))
    status = Column(String(20), default='info')
    duration_ms = Column(Integer)  # 동기화 소요 시간
    files_changed = Column(Integer)  # 변경된 파일 수
    
    # 인덱스
    __table_args__ = (
        Index('idx_sync_timestamp', 'timestamp'),
        Index('idx_sync_action', 'action'),
        {'schema': SCHEMA_NAME, 'extend_existing': True}
    )

class CompanyMetric(Base):
    __tablename__ = 'company_metrics'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.utcnow, nullable=False)
    metric_name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(20))
    category = Column(String(50))  # 메트릭 카테고리 (growth, finance, tech 등)
    
    # 복합 인덱스
    __table_args__ = (
        Index('idx_metric_date_name', 'date', 'metric_name'),
        {'schema': SCHEMA_NAME, 'extend_existing': True}
    )

class GitCommit(Base):
    __tablename__ = 'git_commits'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    commit_hash = Column(String(40), unique=True, nullable=False)
    author = Column(String(200))
    email = Column(String(200))
    message = Column(String(1000))
    timestamp = Column(DateTime, nullable=False)
    branch = Column(String(100))
    files_changed = Column(Integer)
    insertions = Column(Integer)
    deletions = Column(Integer)
    
    # 인덱스
    __table_args__ = (
        Index('idx_commit_hash', 'commit_hash'),
        Index('idx_commit_timestamp', 'timestamp'),
        {'schema': SCHEMA_NAME, 'extend_existing': True}
    )

class Employee(Base):
    __tablename__ = 'ai_employees'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(100))
    department = Column(String(100))
    status = Column(String(20), default='active')  # active, inactive, terminated
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime)
    performance_score = Column(Float)
    tasks_completed = Column(Integer, default=0)
    
    # 관계
    tasks = relationship('Task', back_populates='employee')
    suggestions = relationship('EmployeeSuggestion', back_populates='employee')

class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    task_id = Column(String(50), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(1000))
    status = Column(String(20), default='pending')  # pending, in_progress, completed, failed
    priority = Column(String(20), default='medium')  # low, medium, high, critical
    assigned_to = Column(String(50), ForeignKey(f'{SCHEMA_NAME}.ai_employees.employee_id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    due_date = Column(DateTime)
    
    # 관계
    employee = relationship('Employee', back_populates='tasks')

class SystemHealth(Base):
    __tablename__ = 'system_health'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    service_name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)  # healthy, degraded, down
    response_time_ms = Column(Integer)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    error_count = Column(Integer, default=0)
    details = Column(JSON)

class CompanyMilestone(Base):
    __tablename__ = 'company_milestones'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    milestone_type = Column(String(50), nullable=False)  # technical, business, team
    title = Column(String(200), nullable=False)
    description = Column(String(1000))
    achieved_at = Column(DateTime, default=datetime.utcnow)
    impact_score = Column(Float)  # 1-10 중요도
    details = Column(JSON)

class Revenue(Base):
    __tablename__ = 'revenue_tracking'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.utcnow, nullable=False)
    source = Column(String(100))  # 수익원
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default='KRW')
    category = Column(String(50))  # subscription, one-time, consulting 등
    customer_id = Column(String(100))
    notes = Column(String(500))

class BusinessMeeting(Base):
    __tablename__ = 'business_meetings'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    meeting_type = Column(String(100), nullable=False)  # 사업성검토, 전략회의, 실적검토 등
    title = Column(String(200), nullable=False)
    agenda = Column(String(1000))
    participants = Column(JSON)  # 참석자 리스트
    key_decisions = Column(JSON)  # 주요 결정사항
    action_items = Column(JSON)  # 실행 항목
    meeting_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='planned')  # planned, ongoing, completed
    meeting_notes = Column(String(2000))
    follow_up_date = Column(DateTime)

class BusinessPlan(Base):
    __tablename__ = 'business_plans'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    plan_name = Column(String(200), nullable=False)
    plan_type = Column(String(50))  # product, service, expansion, strategy
    description = Column(String(1000))
    target_market = Column(String(500))
    revenue_model = Column(String(500))
    projected_revenue_12m = Column(Float)
    investment_required = Column(Float)
    risk_level = Column(String(20))  # low, medium, high
    feasibility_score = Column(Float)  # 1-10 실현 가능성
    priority = Column(String(20), default='medium')
    status = Column(String(20), default='draft')  # draft, approved, in_progress, completed
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime)
    details = Column(JSON)

class EmployeeSuggestion(Base):
    __tablename__ = 'employee_suggestions'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    suggestion_id = Column(String(50), unique=True, nullable=False)  # SUG_YYYYMMDD_XXX
    employee_id = Column(String(50), ForeignKey(f'{SCHEMA_NAME}.ai_employees.employee_id'), nullable=False)
    category = Column(String(50), nullable=False)  # efficiency, resource, process, idea, concern
    priority = Column(String(20), default='medium')  # low, medium, high, urgent
    title = Column(String(200), nullable=False)
    description = Column(String(2000), nullable=False)
    suggested_solution = Column(String(2000))
    expected_benefit = Column(String(1000))
    implementation_difficulty = Column(String(20), default='medium')  # easy, medium, hard, very_hard
    status = Column(String(20), default='submitted')  # submitted, reviewing, approved, rejected, implemented
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    reviewed_at = Column(DateTime)
    implemented_at = Column(DateTime)
    reviewer_notes = Column(String(1000))
    implementation_cost = Column(Float)
    estimated_impact = Column(Float)  # 1-10 expected impact score
    tags = Column(JSON)  # 태그 리스트
    
    # 관계
    employee = relationship('Employee', back_populates='suggestions')

class SuggestionFeedback(Base):
    __tablename__ = 'suggestion_feedback'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    suggestion_id = Column(String(50), ForeignKey(f'{SCHEMA_NAME}.employee_suggestions.suggestion_id'), nullable=False)
    feedback_type = Column(String(20), nullable=False)  # comment, update, decision
    feedback_text = Column(String(1000), nullable=False)
    created_by = Column(String(100))  # 누가 피드백을 남겼는지
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_internal = Column(Boolean, default=False)  # 내부 메모인지 직원에게 공개되는지

class StartupSupportProgram(Base):
    """창업 지원 사업 정보"""
    __tablename__ = 'startup_support_programs'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    program_id = Column(String(100), unique=True, nullable=False)  # 고유 ID
    name = Column(String(200), nullable=False)  # 사업명
    organization = Column(String(200), nullable=False)  # 주관기관
    category = Column(String(50), nullable=False)  # 창업 초기, 성장 단계, IT/기술, 융자, 투자 등
    program_type = Column(String(50))  # startup_packages, regional_support, tech_support 등
    target = Column(String(500))  # 지원대상
    support_type = Column(String(200))  # 지원형태
    support_amount = Column(String(200))  # 지원금액
    application_period = Column(String(200))  # 신청기간
    website = Column(String(500))  # 웹사이트
    description = Column(String(2000))  # 설명
    requirements = Column(JSON)  # 신청요건 리스트
    benefits = Column(JSON)  # 혜택 리스트
    region = Column(String(50))  # 지역 (해당시)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)  # 현재 진행중인 사업인지

class UserStartupProfile(Base):
    """사용자 창업 프로필"""
    __tablename__ = 'user_startup_profiles'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), unique=True, nullable=False)
    age = Column(Integer)
    business_age = Column(Integer, default=0)  # 사업 연차 (0: 예비창업)
    industry = Column(String(100))  # IT, 기술, 제조, 서비스 등
    region = Column(String(50))  # 지역
    business_type = Column(String(50))  # 1인, 팀, 법인 등
    funding_needs = Column(Float)  # 필요자금
    current_status = Column(String(100))  # 현재 상태
    interests = Column(JSON)  # 관심 지원사업 카테고리
    applied_programs = Column(JSON)  # 신청한 사업 ID 리스트
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class StartupProgramBookmark(Base):
    """지원사업 북마크"""
    __tablename__ = 'startup_program_bookmarks'
    __table_args__ = {'schema': SCHEMA_NAME, 'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), nullable=False)
    program_id = Column(String(100), ForeignKey(f'{SCHEMA_NAME}.startup_support_programs.program_id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String(1000))  # 개인 메모

def initialize_database():
    """데이터베이스 초기화 및 테이블 생성"""
    try:
        # 스키마 생성
        create_schema()
        
        # 테이블 생성
        Base.metadata.create_all(engine, checkfirst=True)
        print("모든 테이블이 성공적으로 생성되었습니다.")
        
        # 초기 데이터 삽입
        session = Session()
        
        # Qhyx Inc. 설립 마일스톤 추가
        qhyx_milestone = session.query(CompanyMilestone).filter_by(
            title="Qhyx Inc. 회사 설립 및 시스템 구축"
        ).first()
        
        if not qhyx_milestone:
            initial_milestone = CompanyMilestone(
                milestone_type='business',
                title='Qhyx Inc. 회사 설립 및 시스템 구축',
                description='Qhyx (큐히익스) - Quantum Hope Youth eXcellence 회사 설립 및 PostgreSQL 기반 성장 추적 시스템 구축 완료',
                impact_score=10.0,
                details={
                    'company_name': 'Qhyx Inc.',
                    'korean_name': '주식회사 큐히익스',
                    'philosophy': 'Quantum Hope Youth eXcellence',
                    'database': 'PostgreSQL',
                    'hosting': 'Koyeb',
                    'schema': SCHEMA_NAME,
                    'tables_created': len(Base.metadata.tables)
                }
            )
            session.add(initial_milestone)
            
            # 초기 시스템 상태 기록
            system_health = SystemHealth(
                service_name='database',
                status='healthy',
                response_time_ms=50,
                details={'message': 'Database initialized successfully'}
            )
            session.add(system_health)
            
            session.commit()
            print("초기 데이터가 삽입되었습니다.")
        
        session.close()
        
    except Exception as e:
        print(f"데이터베이스 초기화 오류: {e}")
        raise

def get_table_stats():
    """테이블 통계 조회"""
    session = Session()
    try:
        stats = {}
        for table_name in Base.metadata.tables.keys():
            if '.' in table_name:
                schema, name = table_name.split('.')
                result = session.execute(text(f"""
                    SELECT COUNT(*) as count 
                    FROM {schema}.{name}
                """))
                stats[name] = result.fetchone()[0]
        
        return stats
    finally:
        session.close()

if __name__ == "__main__":
    # 데이터베이스 초기화 실행
    initialize_database()
    
    # 테이블 통계 출력
    stats = get_table_stats()
    print("\n=== 테이블 통계 ===")
    for table, count in stats.items():
        print(f"{table}: {count} rows")