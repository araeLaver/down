"""
AI 자기소개서 스키마
"""
from pydantic import BaseModel
from typing import Optional


class AIIntroRequest(BaseModel):
    """AI 자기소개서 생성 요청"""
    # 프로필 ID로 생성하거나, 직접 정보 입력
    profile_id: Optional[str] = None

    # 직접 입력 시
    occupation: Optional[str] = None
    employment_type: Optional[str] = None
    work_duration_months: Optional[int] = None
    has_pet: bool = False
    pet_type: Optional[str] = None
    is_smoker: bool = False
    living_alone: bool = True
    introduction: Optional[str] = None  # 참고할 자기소개

    # 스타일 옵션
    tone: str = "professional"  # professional | friendly | formal
    length: str = "medium"  # short | medium | long


class AIIntroResponse(BaseModel):
    """AI 자기소개서 응답"""
    introduction: str
    keywords: list[str]  # 추출된 키워드
    trust_highlights: list[str]  # 신뢰 포인트
