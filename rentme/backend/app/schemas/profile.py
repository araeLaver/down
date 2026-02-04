"""
프로필 스키마
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class VerificationStatus(str, Enum):
    """인증 상태"""
    NONE = "none"
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


class TrustScore(BaseModel):
    """신뢰점수"""
    total: int = 0  # 0-100
    employment: int = 0  # 재직 인증 점수
    income: int = 0  # 소득 인증 점수
    credit: int = 0  # 신용 인증 점수
    reference: int = 0  # 레퍼런스 점수
    profile_completion: int = 0  # 프로필 완성도


class ProfileCreate(BaseModel):
    """프로필 생성 요청"""
    # 기본 정보
    birth_year: Optional[int] = None
    gender: Optional[str] = None  # male | female | other

    # 직업 정보
    occupation: Optional[str] = None  # 직업
    company_name: Optional[str] = None  # 회사명
    employment_type: Optional[str] = None  # 정규직 | 계약직 | 프리랜서 | 학생 | 무직
    work_duration_months: Optional[int] = None  # 근속 기간 (월)

    # 소득 정보
    monthly_income: Optional[int] = None  # 월 소득 (만원)
    income_type: Optional[str] = None  # 급여 | 사업 | 프리랜서 | 기타

    # 라이프스타일
    has_pet: bool = False
    pet_type: Optional[str] = None  # 강아지 | 고양이 | 기타
    is_smoker: bool = False
    living_alone: bool = True
    move_in_date: Optional[str] = None  # 희망 입주일

    # 선호 조건
    preferred_area: Optional[str] = None  # 희망 지역
    max_deposit: Optional[int] = None  # 최대 보증금 (만원)
    max_monthly_rent: Optional[int] = None  # 최대 월세 (만원)

    # 자기소개
    introduction: Optional[str] = None  # 직접 작성 자기소개


class ProfileUpdate(ProfileCreate):
    """프로필 수정 요청"""
    pass


class ProfileResponse(BaseModel):
    """프로필 응답"""
    id: str
    user_id: str

    # 기본 정보
    birth_year: Optional[int] = None
    gender: Optional[str] = None

    # 직업 정보
    occupation: Optional[str] = None
    company_name: Optional[str] = None
    employment_type: Optional[str] = None
    work_duration_months: Optional[int] = None

    # 소득 정보
    monthly_income: Optional[int] = None
    income_type: Optional[str] = None

    # 라이프스타일
    has_pet: bool = False
    pet_type: Optional[str] = None
    is_smoker: bool = False
    living_alone: bool = True
    move_in_date: Optional[str] = None

    # 선호 조건
    preferred_area: Optional[str] = None
    max_deposit: Optional[int] = None
    max_monthly_rent: Optional[int] = None

    # 자기소개
    introduction: Optional[str] = None
    ai_introduction: Optional[str] = None  # AI 생성 자기소개

    # 인증 상태
    employment_verified: VerificationStatus = VerificationStatus.NONE
    income_verified: VerificationStatus = VerificationStatus.NONE
    credit_verified: VerificationStatus = VerificationStatus.NONE

    # 신뢰점수
    trust_score: TrustScore = TrustScore()

    # 메타
    is_public: bool = False  # 공개 여부
    created_at: datetime
    updated_at: datetime
