"""
유틸리티 모듈 테스트
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    truncate_string, clean_keyword, format_score, score_to_grade,
    format_duration, get_next_scheduled_time, retry_on_failure,
    DatabaseManager
)


class TestTruncateString:
    """문자열 자르기 함수 테스트"""

    def test_short_string_unchanged(self):
        """짧은 문자열은 변경 없음"""
        result = truncate_string("Hello", max_length=100)
        assert result == "Hello"

    def test_exact_length_unchanged(self):
        """정확한 길이는 변경 없음"""
        result = truncate_string("Hello", max_length=5)
        assert result == "Hello"

    def test_long_string_truncated(self):
        """긴 문자열은 잘림"""
        result = truncate_string("Hello World", max_length=8)
        assert result == "Hello..."
        assert len(result) <= 8

    def test_custom_suffix(self):
        """커스텀 접미사"""
        result = truncate_string("Hello World", max_length=10, suffix="…")
        assert result.endswith("…")

    def test_empty_string(self):
        """빈 문자열"""
        result = truncate_string("", max_length=10)
        assert result == ""

    def test_korean_string(self):
        """한글 문자열"""
        result = truncate_string("안녕하세요 반갑습니다", max_length=10)
        assert len(result) <= 10


class TestCleanKeyword:
    """키워드 정리 함수 테스트"""

    def test_remove_common_words(self):
        """일반 단어 제거"""
        result = clean_keyword("AI 마케팅 앱")
        assert "앱" not in result

    def test_remove_platform_word(self):
        """'플랫폼' 단어 제거"""
        # "여행"이 2글자라 원본 반환되므로, 더 긴 키워드 사용
        result = clean_keyword("여행 예약 플랫폼")
        assert "플랫폼" not in result
        assert "여행" in result

    def test_short_result_uses_original(self):
        """결과가 너무 짧으면 원본 사용"""
        result = clean_keyword("앱")
        assert result == "앱"  # 원본 반환

    def test_preserve_meaningful_words(self):
        """의미 있는 단어 유지"""
        result = clean_keyword("AI 마케팅 자동화")
        assert "AI" in result or "마케팅" in result or "자동화" in result


class TestFormatScore:
    """점수 포맷팅 함수 테스트"""

    def test_default_decimal_places(self):
        """기본 소수점 1자리"""
        result = format_score(85.567)
        assert result == "85.6"

    def test_custom_decimal_places(self):
        """커스텀 소수점"""
        result = format_score(85.567, decimal_places=2)
        assert result == "85.57"

    def test_integer_score(self):
        """정수 점수"""
        result = format_score(85.0)
        assert result == "85.0"

    def test_zero_score(self):
        """0점"""
        result = format_score(0)
        assert result == "0.0"


class TestScoreToGrade:
    """점수 등급 변환 테스트"""

    def test_a_plus(self):
        """A+ 등급"""
        assert score_to_grade(95) == 'A+'
        assert score_to_grade(90) == 'A+'

    def test_a(self):
        """A 등급"""
        assert score_to_grade(89) == 'A'
        assert score_to_grade(85) == 'A'

    def test_b_plus(self):
        """B+ 등급"""
        assert score_to_grade(84) == 'B+'
        assert score_to_grade(80) == 'B+'

    def test_b(self):
        """B 등급"""
        assert score_to_grade(79) == 'B'
        assert score_to_grade(75) == 'B'

    def test_c_plus(self):
        """C+ 등급"""
        assert score_to_grade(74) == 'C+'
        assert score_to_grade(70) == 'C+'

    def test_c(self):
        """C 등급"""
        assert score_to_grade(69) == 'C'
        assert score_to_grade(65) == 'C'

    def test_d(self):
        """D 등급"""
        assert score_to_grade(64) == 'D'
        assert score_to_grade(60) == 'D'

    def test_f(self):
        """F 등급"""
        assert score_to_grade(59) == 'F'
        assert score_to_grade(0) == 'F'


class TestFormatDuration:
    """시간 포맷팅 테스트"""

    def test_seconds(self):
        """초 단위"""
        result = format_duration(30)
        assert "초" in result

    def test_minutes(self):
        """분 단위"""
        result = format_duration(120)
        assert "분" in result

    def test_hours(self):
        """시간 단위"""
        result = format_duration(7200)
        assert "시간" in result

    def test_zero(self):
        """0초"""
        result = format_duration(0)
        assert "0.0초" == result

    def test_boundary_60_seconds(self):
        """60초 경계"""
        result = format_duration(60)
        assert "분" in result


class TestGetNextScheduledTime:
    """다음 스케줄 시간 계산 테스트"""

    def test_next_hour_in_list(self):
        """리스트에서 다음 시간"""
        schedule = [8, 12, 18]
        result = get_next_scheduled_time(schedule, 10)
        assert result == 12

    def test_wrap_to_first_hour(self):
        """다음 날 첫 시간으로"""
        schedule = [8, 12, 18]
        result = get_next_scheduled_time(schedule, 20)
        assert result == 8

    def test_exact_current_hour(self):
        """현재 시간과 같으면 다음으로"""
        schedule = [8, 12, 18]
        result = get_next_scheduled_time(schedule, 12)
        assert result == 18

    def test_single_schedule(self):
        """단일 스케줄"""
        schedule = [9]
        result = get_next_scheduled_time(schedule, 10)
        assert result == 9


class TestRetryOnFailure:
    """재시도 데코레이터 테스트"""

    def test_success_on_first_try(self):
        """첫 시도에 성공"""
        call_count = 0

        @retry_on_failure(max_retries=3, delay=0.01)
        def succeed():
            nonlocal call_count
            call_count += 1
            return "success"

        result = succeed()
        assert result == "success"
        assert call_count == 1

    def test_retry_on_failure_then_success(self):
        """실패 후 재시도하여 성공"""
        call_count = 0

        @retry_on_failure(max_retries=3, delay=0.01)
        def fail_then_succeed():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Temporary error")
            return "success"

        result = fail_then_succeed()
        assert result == "success"
        assert call_count == 2

    def test_max_retries_exceeded(self):
        """최대 재시도 횟수 초과"""
        call_count = 0

        @retry_on_failure(max_retries=3, delay=0.01)
        def always_fail():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")

        with pytest.raises(ValueError):
            always_fail()
        assert call_count == 3

    def test_specific_exception_type(self):
        """특정 예외 타입만 재시도"""
        call_count = 0

        @retry_on_failure(max_retries=3, delay=0.01, exceptions=(ValueError,))
        def raise_type_error():
            nonlocal call_count
            call_count += 1
            raise TypeError("Different error")

        with pytest.raises(TypeError):
            raise_type_error()
        assert call_count == 1  # 재시도 없이 바로 예외


class TestDatabaseManager:
    """DatabaseManager 클래스 테스트"""

    def test_context_manager_usage(self):
        """컨텍스트 매니저 사용"""
        mock_session = MagicMock()
        mock_factory = MagicMock(return_value=mock_session)

        with patch('utils.get_session_factory', return_value=mock_factory):
            with DatabaseManager() as db:
                assert db.session is not None

    def test_safe_commit_success(self):
        """안전한 커밋 성공"""
        mock_session = MagicMock()
        mock_factory = MagicMock(return_value=mock_session)

        with patch('utils.get_session_factory', return_value=mock_factory):
            db = DatabaseManager()
            result = db.safe_commit()
            assert result is True
            mock_session.commit.assert_called_once()

    def test_safe_commit_retry(self):
        """커밋 실패 시 재시도"""
        mock_session = MagicMock()
        mock_session.commit.side_effect = [Exception("Error"), None]
        mock_factory = MagicMock(return_value=mock_session)

        with patch('utils.get_session_factory', return_value=mock_factory):
            with patch('time.sleep'):  # 대기 시간 스킵
                db = DatabaseManager()
                result = db.safe_commit(max_retries=2)
                assert result is True

    def test_safe_rollback(self):
        """안전한 롤백"""
        mock_session = MagicMock()
        mock_factory = MagicMock(return_value=mock_session)

        with patch('utils.get_session_factory', return_value=mock_factory):
            db = DatabaseManager()
            db.safe_rollback()
            mock_session.rollback.assert_called_once()

    def test_close_session(self):
        """세션 종료"""
        mock_session = MagicMock()
        mock_factory = MagicMock(return_value=mock_session)

        with patch('utils.get_session_factory', return_value=mock_factory):
            db = DatabaseManager()
            db.close()
            mock_session.close.assert_called_once()


class TestEdgeCases:
    """엣지 케이스 테스트"""

    def test_truncate_with_unicode(self):
        """유니코드 문자열 처리"""
        emoji_text = "Hello 😀 World 🌍"
        result = truncate_string(emoji_text, max_length=10)
        assert len(result) <= 10

    def test_score_to_grade_boundary(self):
        """등급 경계값"""
        assert score_to_grade(90.0) == 'A+'
        assert score_to_grade(89.9) == 'A'
        assert score_to_grade(85.0) == 'A'
        assert score_to_grade(84.9) == 'B+'

    def test_format_duration_large_value(self):
        """큰 시간 값"""
        result = format_duration(36000)  # 10시간
        assert "시간" in result

    def test_clean_keyword_special_chars(self):
        """특수 문자 포함 키워드"""
        result = clean_keyword("AI@마케팅#플랫폼")
        assert "@" in result or "#" in result or result != ""
