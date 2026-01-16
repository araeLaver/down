"""
Qhyx Inc. 통합 로깅 시스템
- 파일 및 콘솔 로깅
- 로그 레벨 관리
- 로그 포맷 표준화
- 로그 로테이션
"""

import os
import logging
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from typing import Optional

from config import LogConfig


# ============================================
# 커스텀 로그 포맷터
# ============================================

class QhyxFormatter(logging.Formatter):
    """Qhyx 전용 로그 포맷터"""

    # 레벨별 색상 (터미널용)
    COLORS = {
        'DEBUG': '\033[36m',      # 청록
        'INFO': '\033[32m',       # 녹색
        'WARNING': '\033[33m',    # 노란색
        'ERROR': '\033[31m',      # 빨간색
        'CRITICAL': '\033[35m',   # 자주색
    }
    RESET = '\033[0m'

    def __init__(self, use_colors: bool = False):
        self.use_colors = use_colors
        super().__init__(
            fmt=LogConfig.FORMAT,
            datefmt=LogConfig.DATE_FORMAT
        )

    def format(self, record: logging.LogRecord) -> str:
        # 모듈명 축약
        if len(record.name) > 20:
            record.name = '...' + record.name[-17:]

        formatted = super().format(record)

        if self.use_colors and record.levelname in self.COLORS:
            color = self.COLORS[record.levelname]
            formatted = f"{color}{formatted}{self.RESET}"

        return formatted


# ============================================
# 로거 설정
# ============================================

def setup_logging(
    name: str = "qhyx",
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    console: bool = True,
    rotation: str = "size"  # 'size', 'time', 'none'
) -> logging.Logger:
    """통합 로거 설정

    Args:
        name: 로거 이름
        level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 로그 파일 경로
        console: 콘솔 출력 여부
        rotation: 로테이션 방식 ('size', 'time', 'none')

    Returns:
        설정된 로거
    """
    logger = logging.getLogger(name)

    # 이미 핸들러가 있으면 스킵
    if logger.handlers:
        return logger

    # 레벨 설정
    log_level = getattr(logging, level or LogConfig.get_level(), logging.INFO)
    logger.setLevel(log_level)

    # 콘솔 핸들러
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(QhyxFormatter(use_colors=True))
        logger.addHandler(console_handler)

    # 파일 핸들러
    file_path = log_file or LogConfig.get_file()
    if file_path:
        # 로그 디렉토리 생성
        log_dir = os.path.dirname(file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        if rotation == "size":
            # 크기 기반 로테이션 (10MB, 최대 5개)
            file_handler = RotatingFileHandler(
                file_path,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
        elif rotation == "time":
            # 시간 기반 로테이션 (매일 자정)
            file_handler = TimedRotatingFileHandler(
                file_path,
                when='midnight',
                interval=1,
                backupCount=7,
                encoding='utf-8'
            )
        else:
            # 로테이션 없음
            file_handler = logging.FileHandler(file_path, encoding='utf-8')

        file_handler.setLevel(log_level)
        file_handler.setFormatter(QhyxFormatter(use_colors=False))
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "qhyx") -> logging.Logger:
    """로거 가져오기 (없으면 생성)"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logging(name)
    return logger


# ============================================
# 모듈별 로거
# ============================================

def get_app_logger() -> logging.Logger:
    """Flask 앱 로거"""
    return get_logger("qhyx.app")


def get_discovery_logger() -> logging.Logger:
    """사업 발굴 로거"""
    return get_logger("qhyx.discovery")


def get_db_logger() -> logging.Logger:
    """데이터베이스 로거"""
    return get_logger("qhyx.db")


def get_api_logger() -> logging.Logger:
    """API 로거"""
    return get_logger("qhyx.api")


def get_auth_logger() -> logging.Logger:
    """인증 로거"""
    return get_logger("qhyx.auth")


def get_notification_logger() -> logging.Logger:
    """알림 로거"""
    return get_logger("qhyx.notification")


# ============================================
# 로깅 유틸리티
# ============================================

class LogContext:
    """로그 컨텍스트 관리자"""

    def __init__(self, logger: logging.Logger, operation: str, **context):
        self.logger = logger
        self.operation = operation
        self.context = context
        self.start_time = None

    def __enter__(self):
        self.start_time = datetime.now()
        context_str = ', '.join(f"{k}={v}" for k, v in self.context.items())
        self.logger.info(f"[START] {self.operation} - {context_str}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()

        if exc_type:
            self.logger.error(
                f"[FAIL] {self.operation} - {duration:.2f}s - {exc_type.__name__}: {exc_val}"
            )
        else:
            self.logger.info(f"[DONE] {self.operation} - {duration:.2f}s")

        return False  # 예외 전파


def log_function_call(logger: Optional[logging.Logger] = None):
    """함수 호출 로깅 데코레이터"""
    def decorator(func):
        import functools

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _logger = logger or get_logger()
            func_name = func.__name__

            _logger.debug(f"[CALL] {func_name}(args={len(args)}, kwargs={list(kwargs.keys())})")

            try:
                result = func(*args, **kwargs)
                _logger.debug(f"[RETURN] {func_name} -> {type(result).__name__}")
                return result
            except Exception as e:
                _logger.error(f"[ERROR] {func_name} -> {type(e).__name__}: {e}")
                raise

        return wrapper
    return decorator


# ============================================
# 초기화
# ============================================

def init_logging():
    """애플리케이션 로깅 초기화"""
    # 루트 로거 설정
    root_logger = setup_logging(
        name="qhyx",
        log_file=LogConfig.get_file(),
        console=True,
        rotation="size"
    )

    # 모듈별 로거도 동일 설정 상속
    for module in ['app', 'discovery', 'db', 'api', 'auth', 'notification']:
        child_logger = logging.getLogger(f"qhyx.{module}")
        child_logger.setLevel(root_logger.level)

    root_logger.info("=" * 60)
    root_logger.info("Qhyx Inc. Logging System Initialized")
    root_logger.info(f"Log Level: {LogConfig.get_level()}")
    root_logger.info(f"Log File: {LogConfig.get_file()}")
    root_logger.info("=" * 60)

    return root_logger


# 모듈 로드 시 기본 설정
_default_logger = None


def ensure_logging_initialized():
    """로깅이 초기화되었는지 확인"""
    global _default_logger
    if _default_logger is None:
        _default_logger = init_logging()
    return _default_logger
