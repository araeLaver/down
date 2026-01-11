"""
시장 분석 설정 모듈
- 환경변수 기반 모드 전환 지원
- Koyeb 유료 플랜 전환 시 환경변수만 변경하면 됨
"""

import os
from enum import Enum


class MarketAnalysisMode(Enum):
    """시장 분석 모드"""
    LIGHTWEIGHT = "lightweight"  # 경량 모드 (외부 API 미사용)
    FULL = "full"                # 전체 모드 (외부 API 사용)


class MarketConfig:
    """시장 분석 설정"""

    # 환경변수 키
    ENV_ANALYSIS_MODE = "MARKET_ANALYSIS_MODE"
    ENV_API_TIMEOUT = "MARKET_API_TIMEOUT"
    ENV_API_DELAY = "MARKET_API_DELAY"

    # 기본값
    DEFAULT_MODE = MarketAnalysisMode.LIGHTWEIGHT
    DEFAULT_TIMEOUT = 10  # 초
    DEFAULT_DELAY = 2     # API 호출 간 대기 시간 (초)

    @classmethod
    def get_mode(cls) -> MarketAnalysisMode:
        """현재 분석 모드 반환"""
        mode_str = os.environ.get(cls.ENV_ANALYSIS_MODE, "").lower()

        if mode_str == "full":
            return MarketAnalysisMode.FULL
        return MarketAnalysisMode.LIGHTWEIGHT

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
            return int(os.environ.get(cls.ENV_API_TIMEOUT, cls.DEFAULT_TIMEOUT))
        except ValueError:
            return cls.DEFAULT_TIMEOUT

    @classmethod
    def get_api_delay(cls) -> float:
        """API 호출 간 대기 시간 (초)"""
        try:
            return float(os.environ.get(cls.ENV_API_DELAY, cls.DEFAULT_DELAY))
        except ValueError:
            return cls.DEFAULT_DELAY

    @classmethod
    def get_status(cls) -> dict:
        """현재 설정 상태 반환"""
        mode = cls.get_mode()
        return {
            "mode": mode.value,
            "mode_description": "경량 모드 (외부 API 미사용)" if mode == MarketAnalysisMode.LIGHTWEIGHT else "전체 모드 (외부 API 사용)",
            "is_lightweight": cls.is_lightweight(),
            "api_timeout": cls.get_timeout(),
            "api_delay": cls.get_api_delay(),
            "env_vars": {
                cls.ENV_ANALYSIS_MODE: os.environ.get(cls.ENV_ANALYSIS_MODE, "(미설정 - 기본값: lightweight)"),
                cls.ENV_API_TIMEOUT: os.environ.get(cls.ENV_API_TIMEOUT, f"(미설정 - 기본값: {cls.DEFAULT_TIMEOUT})"),
                cls.ENV_API_DELAY: os.environ.get(cls.ENV_API_DELAY, f"(미설정 - 기본값: {cls.DEFAULT_DELAY})")
            },
            "switch_instructions": {
                "to_full_mode": f"환경변수 설정: {cls.ENV_ANALYSIS_MODE}=full",
                "to_lightweight": f"환경변수 설정: {cls.ENV_ANALYSIS_MODE}=lightweight (또는 삭제)"
            }
        }


# 모듈 로드 시 현재 모드 출력
def _print_current_mode():
    mode = MarketConfig.get_mode()
    mode_desc = "경량 모드" if mode == MarketAnalysisMode.LIGHTWEIGHT else "전체 모드"
    print(f"[CONFIG] 시장 분석 모드: {mode_desc} ({mode.value})")


_print_current_mode()
