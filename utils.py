"""
Qhyx Inc. 공통 유틸리티 모듈
- DB 세션 관리
- 안전한 커밋
- 공통 헬퍼 함수
"""

import time
import logging
from functools import wraps
from typing import Optional, Callable, Any
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DatabaseConfig


# ============================================
# 데이터베이스 유틸리티
# ============================================

def get_engine():
    """SQLAlchemy 엔진 생성"""
    return create_engine(
        DatabaseConfig.get_database_url(),
        **DatabaseConfig.get_engine_options()
    )


def get_session_factory():
    """세션 팩토리 생성"""
    engine = get_engine()
    return sessionmaker(bind=engine)


class DatabaseManager:
    """데이터베이스 세션 관리자"""

    def __init__(self, session: Optional[Session] = None):
        self._session_factory = get_session_factory()
        self._session = session or self._session_factory()
        self._logger = logging.getLogger(__name__)

    @property
    def session(self) -> Session:
        """현재 세션 반환"""
        return self._session

    def refresh_session(self) -> Session:
        """DB 세션 새로고침 (연결 오류 복구용)"""
        try:
            self._session.rollback()
            self._session.close()
        except Exception as e:
            self._logger.warning(f"Session cleanup warning: {e}")

        self._session = self._session_factory()
        self._logger.info("Session refreshed due to connection error")
        return self._session

    def safe_commit(self, max_retries: int = 3) -> bool:
        """안전한 커밋 (재시도 로직 포함)"""
        for attempt in range(max_retries):
            try:
                self._session.commit()
                return True
            except Exception as e:
                self._logger.warning(f"Commit attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    self.refresh_session()
                    time.sleep(1)
                else:
                    self._logger.error(f"DB commit failed after {max_retries} retries: {e}")
                    return False
        return False

    def safe_rollback(self):
        """안전한 롤백"""
        try:
            self._session.rollback()
        except Exception as e:
            self._logger.warning(f"Rollback warning: {e}")

    def close(self):
        """세션 종료"""
        try:
            self._session.close()
        except Exception as e:
            self._logger.warning(f"Session close warning: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.safe_rollback()
        self.close()


def with_db_session(func: Callable) -> Callable:
    """DB 세션 자동 관리 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        db_manager = DatabaseManager()
        try:
            kwargs['db_manager'] = db_manager
            result = func(*args, **kwargs)
            db_manager.safe_commit()
            return result
        except Exception as e:
            db_manager.safe_rollback()
            raise e
        finally:
            db_manager.close()
    return wrapper


# ============================================
# 에러 핸들링 유틸리티
# ============================================

def retry_on_failure(max_retries: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """실패 시 재시도 데코레이터"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))  # 점진적 대기
            raise last_exception
        return wrapper
    return decorator


# ============================================
# 문자열 유틸리티
# ============================================

def truncate_string(s: str, max_length: int = 100, suffix: str = "...") -> str:
    """문자열 자르기"""
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix


def clean_keyword(business_name: str) -> str:
    """사업 이름에서 검색 키워드 생성"""
    remove_words = ['앱', '서비스', '플랫폼', '시스템', '솔루션', '도구', '개발']
    keyword = business_name

    for word in remove_words:
        keyword = keyword.replace(word, '')

    keyword = keyword.strip()

    # 너무 짧으면 원본 사용
    if len(keyword) < 3:
        keyword = business_name

    return keyword


# ============================================
# 점수 유틸리티
# ============================================

def format_score(score: float, decimal_places: int = 1) -> str:
    """점수 포맷팅"""
    return f"{score:.{decimal_places}f}"


def score_to_grade(score: float) -> str:
    """점수를 등급으로 변환"""
    if score >= 90:
        return 'A+'
    elif score >= 85:
        return 'A'
    elif score >= 80:
        return 'B+'
    elif score >= 75:
        return 'B'
    elif score >= 70:
        return 'C+'
    elif score >= 65:
        return 'C'
    elif score >= 60:
        return 'D'
    return 'F'


# ============================================
# 시간 유틸리티
# ============================================

def format_duration(seconds: float) -> str:
    """초를 읽기 쉬운 형식으로 변환"""
    if seconds < 60:
        return f"{seconds:.1f}초"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}분"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}시간"


def get_next_scheduled_time(schedule_hours: list, current_hour: int) -> int:
    """다음 스케줄 시간 계산"""
    next_hours = [h for h in schedule_hours if h > current_hour]
    return next_hours[0] if next_hours else schedule_hours[0]
