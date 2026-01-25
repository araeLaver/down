"""
Qhyx Inc. 통합 설정 모듈
- 환경변수 기반 설정 관리
- 데이터베이스, API, 스케줄, 점수 기준 등 모든 설정 통합
"""

import os
from enum import Enum
from typing import Optional
from urllib.parse import quote_plus


# ============================================
# 환경변수 키 상수
# ============================================
class EnvKeys:
    """환경변수 키 정의"""
    # 데이터베이스
    DATABASE_URL = "DATABASE_URL"
    DB_USERNAME = "DB_USERNAME"
    DB_PASSWORD = "DB_PASSWORD"
    DB_HOST = "DB_HOST"
    DB_PORT = "DB_PORT"
    DB_NAME = "DB_NAME"

    # 시장 분석
    MARKET_ANALYSIS_MODE = "MARKET_ANALYSIS_MODE"
    MARKET_API_TIMEOUT = "MARKET_API_TIMEOUT"
    MARKET_API_DELAY = "MARKET_API_DELAY"

    # 사업 발굴
    DISCOVERY_MIN_SCORE = "DISCOVERY_MIN_SCORE"
    DISCOVERY_SCHEDULE_HOURS = "DISCOVERY_SCHEDULE_HOURS"
    DISCOVERY_IDEAS_PER_RUN = "DISCOVERY_IDEAS_PER_RUN"

    # API 인증
    API_SECRET_KEY = "API_SECRET_KEY"
    API_TOKEN_EXPIRY_HOURS = "API_TOKEN_EXPIRY_HOURS"

    # 알림
    SLACK_WEBHOOK_URL = "SLACK_WEBHOOK_URL"
    EMAIL_SMTP_HOST = "EMAIL_SMTP_HOST"
    EMAIL_SMTP_PORT = "EMAIL_SMTP_PORT"
    EMAIL_USERNAME = "EMAIL_USERNAME"
    EMAIL_PASSWORD = "EMAIL_PASSWORD"
    EMAIL_FROM = "EMAIL_FROM"
    NOTIFICATION_ENABLED = "NOTIFICATION_ENABLED"

    # 로깅
    LOG_LEVEL = "LOG_LEVEL"
    LOG_FILE = "LOG_FILE"


# ============================================
# 데이터베이스 설정
# ============================================
class DatabaseConfig:
    """데이터베이스 설정"""

    # 기본값 (환경변수 미설정 시 - 개발용)
    DEFAULT_USERNAME = "unble"
    DEFAULT_HOST = "ep-divine-bird-a1f4mly5.ap-southeast-1.pg.koyeb.app"
    DEFAULT_PORT = "5432"
    DEFAULT_NAME = "unble"

    # 연결 풀 설정
    POOL_SIZE = 5
    MAX_OVERFLOW = 5
    POOL_RECYCLE = 1800  # 30분
    POOL_TIMEOUT = 30

    # Keep-alive 설정
    KEEPALIVES = 1
    KEEPALIVES_IDLE = 30
    KEEPALIVES_INTERVAL = 10
    KEEPALIVES_COUNT = 5

    # 스키마
    SCHEMA_NAME = "qhyx_growth"

    @classmethod
    def get_database_url(cls) -> str:
        """DATABASE_URL 반환 (환경변수 우선)"""
        # 1. DATABASE_URL 환경변수 확인
        db_url = os.environ.get(EnvKeys.DATABASE_URL)
        if db_url:
            return db_url

        # 2. 개별 환경변수로 URL 구성
        username = os.environ.get(EnvKeys.DB_USERNAME, cls.DEFAULT_USERNAME)
        password = os.environ.get(EnvKeys.DB_PASSWORD, "")
        host = os.environ.get(EnvKeys.DB_HOST, cls.DEFAULT_HOST)
        port = os.environ.get(EnvKeys.DB_PORT, cls.DEFAULT_PORT)
        database = os.environ.get(EnvKeys.DB_NAME, cls.DEFAULT_NAME)

        if password:
            # 비밀번호에 특수문자가 있을 수 있으므로 URL 인코딩
            encoded_password = quote_plus(password)
            return f"postgresql://{username}:{encoded_password}@{host}:{port}/{database}"

        # 비밀번호 없이 (로컬 개발용)
        return f"postgresql://{username}@{host}:{port}/{database}"

    @classmethod
    def get_connection_args(cls) -> dict:
        """SQLAlchemy 연결 인자 반환"""
        return {
            'connect_timeout': 10,
            'keepalives': cls.KEEPALIVES,
            'keepalives_idle': cls.KEEPALIVES_IDLE,
            'keepalives_interval': cls.KEEPALIVES_INTERVAL,
            'keepalives_count': cls.KEEPALIVES_COUNT
        }

    @classmethod
    def get_engine_options(cls) -> dict:
        """SQLAlchemy 엔진 옵션 반환"""
        return {
            'pool_pre_ping': True,
            'pool_recycle': cls.POOL_RECYCLE,
            'pool_size': cls.POOL_SIZE,
            'max_overflow': cls.MAX_OVERFLOW,
            'pool_timeout': cls.POOL_TIMEOUT,
            'connect_args': cls.get_connection_args()
        }


# ============================================
# 시장 분석 설정
# ============================================
class MarketAnalysisMode(Enum):
    """시장 분석 모드"""
    LIGHTWEIGHT = "lightweight"  # 경량 모드 (외부 API 미사용)
    FULL = "full"                # 전체 모드 (외부 API 사용)


class MarketConfig:
    """시장 분석 설정"""

    DEFAULT_MODE = MarketAnalysisMode.FULL
    DEFAULT_TIMEOUT = 10  # 초
    DEFAULT_DELAY = 2.0   # API 호출 간 대기 시간 (초)

    @classmethod
    def get_mode(cls) -> MarketAnalysisMode:
        """현재 분석 모드 반환"""
        mode_str = os.environ.get(EnvKeys.MARKET_ANALYSIS_MODE, "").lower()
        if mode_str == "full":
            return MarketAnalysisMode.FULL
        elif mode_str == "lightweight":
            return MarketAnalysisMode.LIGHTWEIGHT
        # 환경변수 미설정 시 DEFAULT_MODE 사용
        return cls.DEFAULT_MODE

    @classmethod
    def is_lightweight(cls) -> bool:
        """경량 모드 여부"""
        return cls.get_mode() == MarketAnalysisMode.LIGHTWEIGHT

    @classmethod
    def is_full_mode(cls) -> bool:
        """전체 모드 여부"""
        return cls.get_mode() == MarketAnalysisMode.FULL

    @classmethod
    def get_timeout(cls) -> int:
        """API 타임아웃 (초)"""
        try:
            return int(os.environ.get(EnvKeys.MARKET_API_TIMEOUT, cls.DEFAULT_TIMEOUT))
        except ValueError:
            return cls.DEFAULT_TIMEOUT

    @classmethod
    def get_api_delay(cls) -> float:
        """API 호출 간 대기 시간 (초)"""
        try:
            return float(os.environ.get(EnvKeys.MARKET_API_DELAY, cls.DEFAULT_DELAY))
        except ValueError:
            return cls.DEFAULT_DELAY


# ============================================
# 사업 발굴 설정
# ============================================
class DiscoveryConfig:
    """사업 발굴 설정"""

    # 점수 기준 (상수화)
    DEFAULT_MIN_SCORE = 70          # 최소 저장 점수
    DEFAULT_LOW_SCORE_THRESHOLD = 50  # 저점수 기준
    DEFAULT_HIGH_SCORE_THRESHOLD = 85  # 고득점 기준 (high priority)

    # 스케줄 (하루 1회)
    DEFAULT_SCHEDULE_HOURS = [9]  # KST 기준 오전 9시

    # 실행당 아이디어 수
    DEFAULT_IDEAS_PER_RUN = 3

    # 중복 방지 기간 (일)
    DUPLICATE_CHECK_DAYS = 7

    @classmethod
    def get_min_score(cls) -> int:
        """최소 저장 점수"""
        try:
            return int(os.environ.get(EnvKeys.DISCOVERY_MIN_SCORE, cls.DEFAULT_MIN_SCORE))
        except ValueError:
            return cls.DEFAULT_MIN_SCORE

    @classmethod
    def get_schedule_hours(cls) -> list:
        """스케줄 시간 목록"""
        hours_str = os.environ.get(EnvKeys.DISCOVERY_SCHEDULE_HOURS, "")
        if hours_str:
            try:
                return [int(h.strip()) for h in hours_str.split(",")]
            except ValueError:
                pass
        return cls.DEFAULT_SCHEDULE_HOURS

    @classmethod
    def get_ideas_per_run(cls) -> int:
        """실행당 아이디어 수"""
        try:
            return int(os.environ.get(EnvKeys.DISCOVERY_IDEAS_PER_RUN, cls.DEFAULT_IDEAS_PER_RUN))
        except ValueError:
            return cls.DEFAULT_IDEAS_PER_RUN

    @classmethod
    def get_priority(cls, score: float) -> str:
        """점수 기반 우선순위 반환"""
        if score >= cls.DEFAULT_HIGH_SCORE_THRESHOLD:
            return 'high'
        elif score >= cls.get_min_score():
            return 'medium'
        return 'low'

    @classmethod
    def get_risk_level(cls, score: float) -> str:
        """점수 기반 위험도 반환"""
        if score >= 80:
            return 'low'
        elif score >= 70:
            return 'medium'
        return 'high'


# ============================================
# API 인증 설정
# ============================================
class APIConfig:
    """API 인증 설정"""

    DEFAULT_TOKEN_EXPIRY_HOURS = 24

    @classmethod
    def get_secret_key(cls) -> str:
        """API 시크릿 키"""
        key = os.environ.get(EnvKeys.API_SECRET_KEY)
        if not key:
            # 개발용 기본 키 (프로덕션에서는 반드시 환경변수 설정 필요)
            import warnings
            warnings.warn("API_SECRET_KEY not set. Using default key for development only!")
            return "dev-secret-key-change-in-production"
        return key

    @classmethod
    def get_token_expiry_hours(cls) -> int:
        """토큰 만료 시간 (시간)"""
        try:
            return int(os.environ.get(EnvKeys.API_TOKEN_EXPIRY_HOURS, cls.DEFAULT_TOKEN_EXPIRY_HOURS))
        except ValueError:
            return cls.DEFAULT_TOKEN_EXPIRY_HOURS

    @classmethod
    def is_auth_enabled(cls) -> bool:
        """인증 활성화 여부"""
        return bool(os.environ.get(EnvKeys.API_SECRET_KEY))


# ============================================
# 알림 설정
# ============================================
class NotificationConfig:
    """알림 설정"""

    @classmethod
    def is_enabled(cls) -> bool:
        """알림 활성화 여부"""
        return os.environ.get(EnvKeys.NOTIFICATION_ENABLED, "").lower() == "true"

    @classmethod
    def get_slack_webhook(cls) -> Optional[str]:
        """Slack Webhook URL"""
        return os.environ.get(EnvKeys.SLACK_WEBHOOK_URL)

    @classmethod
    def get_email_config(cls) -> dict:
        """이메일 설정"""
        return {
            'smtp_host': os.environ.get(EnvKeys.EMAIL_SMTP_HOST, ""),
            'smtp_port': int(os.environ.get(EnvKeys.EMAIL_SMTP_PORT, 587)),
            'username': os.environ.get(EnvKeys.EMAIL_USERNAME, ""),
            'password': os.environ.get(EnvKeys.EMAIL_PASSWORD, ""),
            'from_email': os.environ.get(EnvKeys.EMAIL_FROM, "")
        }

    @classmethod
    def is_slack_configured(cls) -> bool:
        """Slack 설정 여부"""
        return bool(cls.get_slack_webhook())

    @classmethod
    def is_email_configured(cls) -> bool:
        """이메일 설정 여부"""
        config = cls.get_email_config()
        return all([config['smtp_host'], config['username'], config['password']])


# ============================================
# 로깅 설정
# ============================================
class LogConfig:
    """로깅 설정"""

    DEFAULT_LEVEL = "INFO"
    DEFAULT_FILE = "qhyx.log"

    # 로그 포맷
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def get_level(cls) -> str:
        """로그 레벨"""
        return os.environ.get(EnvKeys.LOG_LEVEL, cls.DEFAULT_LEVEL).upper()

    @classmethod
    def get_file(cls) -> str:
        """로그 파일 경로"""
        return os.environ.get(EnvKeys.LOG_FILE, cls.DEFAULT_FILE)


# ============================================
# 설정 상태 출력
# ============================================
def print_config_status():
    """현재 설정 상태 출력"""
    print("=" * 60)
    print("[CONFIG] Qhyx Inc. 설정 현황")
    print("=" * 60)

    # 데이터베이스
    db_url = DatabaseConfig.get_database_url()
    masked_url = db_url.split("@")[1] if "@" in db_url else db_url
    print(f"[DB] Host: {masked_url}")
    print(f"[DB] Schema: {DatabaseConfig.SCHEMA_NAME}")

    # 시장 분석
    mode = MarketConfig.get_mode()
    print(f"[MARKET] Mode: {mode.value}")

    # 사업 발굴
    print(f"[DISCOVERY] Min Score: {DiscoveryConfig.get_min_score()}")
    print(f"[DISCOVERY] Schedule: {DiscoveryConfig.get_schedule_hours()} (KST)")

    # API 인증
    print(f"[API] Auth Enabled: {APIConfig.is_auth_enabled()}")

    # 알림
    print(f"[NOTIFY] Enabled: {NotificationConfig.is_enabled()}")
    print(f"[NOTIFY] Slack: {NotificationConfig.is_slack_configured()}")
    print(f"[NOTIFY] Email: {NotificationConfig.is_email_configured()}")

    # 로깅
    print(f"[LOG] Level: {LogConfig.get_level()}")

    print("=" * 60)


# 모듈 로드 시 설정 확인
if __name__ == "__main__":
    print_config_status()
