"""
데이터베이스 스키마 설정 및 초기화
Koyeb PostgreSQL 연결 및 전용 스키마 생성
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

# 스키마 이름
SCHEMA_NAME = 'company_growth'

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
        
        # 시스템 초기화 마일스톤 추가
        milestone = session.query(CompanyMilestone).filter_by(
            title="회사 성장 추적 시스템 초기화"
        ).first()
        
        if not milestone:
            initial_milestone = CompanyMilestone(
                milestone_type='technical',
                title='회사 성장 추적 시스템 초기화',
                description='Koyeb PostgreSQL 기반 회사 성장 추적 시스템 구축 완료',
                impact_score=10.0,
                details={
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