"""
렌트미 (RentMe) - 세입자 신뢰 프로필 플랫폼
FastAPI Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import auth, profiles, references, ai_intro
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    print("🏠 렌트미 서버 시작...")
    yield
    print("👋 렌트미 서버 종료...")


app = FastAPI(
    title="렌트미 API",
    description="세입자 신뢰 프로필 플랫폼 - 좋은 세입자임을 증명하면 보증금이 달라집니다",
    version="0.1.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["인증"])
app.include_router(profiles.router, prefix="/api/profiles", tags=["프로필"])
app.include_router(references.router, prefix="/api/references", tags=["레퍼런스"])
app.include_router(ai_intro.router, prefix="/api/ai", tags=["AI"])


@app.get("/")
async def root():
    return {
        "service": "렌트미 API",
        "version": "0.1.0",
        "status": "running",
        "message": "좋은 세입자임을 증명하면 보증금이 달라집니다"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
