"""
시장 분석 설정 모듈 (호환성 유지)
- 실제 설정은 config.py에서 관리
- 기존 코드 호환성을 위해 re-export
"""

# config.py에서 가져와서 re-export (기존 코드 호환성)
from config import MarketAnalysisMode, MarketConfig

# 모듈 로드 시 현재 모드 출력
def _print_current_mode():
    mode = MarketConfig.get_mode()
    mode_desc = "경량 모드" if mode == MarketAnalysisMode.LIGHTWEIGHT else "전체 모드"
    print(f"[CONFIG] 시장 분석 모드: {mode_desc} ({mode.value})")


_print_current_mode()
