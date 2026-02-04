"""
레퍼런스 스키마
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class ReferenceStatus(str, Enum):
    """레퍼런스 상태"""
    PENDING = "pending"  # 요청됨
    COMPLETED = "completed"  # 작성 완료
    DECLINED = "declined"  # 거절됨
    EXPIRED = "expired"  # 만료됨


class ReferenceRequest(BaseModel):
    """레퍼런스 요청"""
    landlord_name: str  # 집주인 이름
    landlord_email: Optional[EmailStr] = None  # 집주인 이메일
    landlord_phone: Optional[str] = None  # 집주인 연락처

    # 임대 정보
    address: str  # 주소
    rental_start: str  # 임대 시작일 (YYYY-MM)
    rental_end: str  # 임대 종료일 (YYYY-MM)
    monthly_rent: Optional[int] = None  # 월세 (만원)
    deposit: Optional[int] = None  # 보증금 (만원)


class ReferenceResponse(BaseModel):
    """레퍼런스 응답"""
    id: str
    tenant_id: str

    # 집주인 정보
    landlord_name: str
    landlord_email: Optional[str] = None
    landlord_phone: Optional[str] = None

    # 임대 정보
    address: str
    rental_start: str
    rental_end: str
    monthly_rent: Optional[int] = None
    deposit: Optional[int] = None

    # 평가 (집주인이 작성)
    rating: Optional[int] = None  # 1-5
    payment_punctuality: Optional[int] = None  # 월세 납부 성실도 1-5
    property_care: Optional[int] = None  # 시설 관리 상태 1-5
    communication: Optional[int] = None  # 소통 원활도 1-5
    would_rent_again: Optional[bool] = None  # 재계약 의향
    comment: Optional[str] = None  # 코멘트

    # 상태
    status: ReferenceStatus = ReferenceStatus.PENDING
    request_code: Optional[str] = None  # 레퍼런스 작성 코드

    # 메타
    created_at: datetime
    completed_at: Optional[datetime] = None


class ReferenceSubmit(BaseModel):
    """집주인이 레퍼런스 작성"""
    request_code: str  # 레퍼런스 코드
    rating: int  # 1-5 전체 평점
    payment_punctuality: int  # 1-5
    property_care: int  # 1-5
    communication: int  # 1-5
    would_rent_again: bool
    comment: Optional[str] = None
