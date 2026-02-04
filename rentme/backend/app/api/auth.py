"""
인증 API
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
import uuid

from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.core.config import settings
from app.core.database import get_supabase

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 검증"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """비밀번호 해시"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT 토큰 생성"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """현재 사용자 조회"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

        # Supabase에서 사용자 조회
        supabase = get_supabase()
        result = supabase.table("users").select("*").eq("id", user_id).single().execute()

        if not result.data:
            raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다")

        return result.data
    except JWTError:
        raise HTTPException(status_code=401, detail="토큰 검증 실패")


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    """회원가입"""
    try:
        supabase = get_supabase()

        # 이메일 중복 확인
        existing = supabase.table("users").select("id").eq("email", user_data.email).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다")

        # 사용자 생성
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(user_data.password)

        new_user = {
            "id": user_id,
            "email": user_data.email,
            "password_hash": hashed_password,
            "name": user_data.name,
            "phone": user_data.phone,
            "user_type": "tenant",
            "created_at": datetime.utcnow().isoformat(),
        }

        result = supabase.table("users").insert(new_user).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="회원가입 실패")

        # 토큰 생성
        access_token = create_access_token(data={"sub": user_id})

        user_response = UserResponse(
            id=user_id,
            email=user_data.email,
            name=user_data.name,
            phone=user_data.phone,
            user_type="tenant",
            created_at=datetime.utcnow()
        )

        return Token(access_token=access_token, user=user_response)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """로그인"""
    try:
        supabase = get_supabase()

        # 사용자 조회
        result = supabase.table("users").select("*").eq("email", user_data.email).single().execute()

        if not result.data:
            raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다")

        user = result.data

        # 비밀번호 확인
        if not verify_password(user_data.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다")

        # 토큰 생성
        access_token = create_access_token(data={"sub": user["id"]})

        user_response = UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            phone=user.get("phone"),
            user_type=user.get("user_type", "tenant"),
            created_at=datetime.fromisoformat(user["created_at"])
        )

        return Token(access_token=access_token, user=user_response)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """현재 로그인한 사용자 정보"""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        name=current_user["name"],
        phone=current_user.get("phone"),
        user_type=current_user.get("user_type", "tenant"),
        created_at=datetime.fromisoformat(current_user["created_at"])
    )
