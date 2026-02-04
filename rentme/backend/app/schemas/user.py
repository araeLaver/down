"""
사용자 스키마
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """회원가입 요청"""
    email: EmailStr
    password: str
    name: str
    phone: Optional[str] = None


class UserLogin(BaseModel):
    """로그인 요청"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """사용자 응답"""
    id: str
    email: str
    name: str
    phone: Optional[str] = None
    user_type: str = "tenant"  # tenant | landlord
    created_at: datetime


class Token(BaseModel):
    """JWT 토큰 응답"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
