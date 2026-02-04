"""
프로필 API
"""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
import uuid

from app.schemas.profile import (
    ProfileCreate, ProfileUpdate, ProfileResponse,
    TrustScore, VerificationStatus
)
from app.api.auth import get_current_user
from app.core.database import get_supabase

router = APIRouter()


def calculate_trust_score(profile: dict) -> TrustScore:
    """신뢰점수 계산"""
    score = TrustScore()

    # 프로필 완성도 (최대 20점)
    completion = 0
    fields = ['birth_year', 'gender', 'occupation', 'employment_type',
              'monthly_income', 'preferred_area', 'introduction']
    for field in fields:
        if profile.get(field):
            completion += 3
    score.profile_completion = min(completion, 20)

    # 재직 인증 (최대 25점)
    if profile.get('employment_verified') == 'verified':
        score.employment = 25
    elif profile.get('employment_verified') == 'pending':
        score.employment = 5

    # 소득 인증 (최대 25점)
    if profile.get('income_verified') == 'verified':
        score.income = 25
    elif profile.get('income_verified') == 'pending':
        score.income = 5

    # 신용 인증 (최대 15점)
    if profile.get('credit_verified') == 'verified':
        score.credit = 15

    # 레퍼런스 (최대 15점, 레퍼런스 수와 평점에 따라)
    # TODO: 실제 레퍼런스 조회하여 계산
    score.reference = 0

    # 총점 계산
    score.total = min(
        score.profile_completion + score.employment +
        score.income + score.credit + score.reference,
        100
    )

    return score


@router.post("", response_model=ProfileResponse)
async def create_profile(
    profile_data: ProfileCreate,
    current_user: dict = Depends(get_current_user)
):
    """프로필 생성"""
    try:
        supabase = get_supabase()

        # 기존 프로필 확인
        existing = supabase.table("profiles").select("id").eq("user_id", current_user["id"]).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="이미 프로필이 존재합니다. 수정해주세요.")

        profile_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        new_profile = {
            "id": profile_id,
            "user_id": current_user["id"],
            **profile_data.model_dump(),
            "employment_verified": "none",
            "income_verified": "none",
            "credit_verified": "none",
            "is_public": False,
            "created_at": now,
            "updated_at": now,
        }

        result = supabase.table("profiles").insert(new_profile).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="프로필 생성 실패")

        profile = result.data[0]
        trust_score = calculate_trust_score(profile)

        return ProfileResponse(
            **profile,
            trust_score=trust_score,
            created_at=datetime.fromisoformat(profile["created_at"]),
            updated_at=datetime.fromisoformat(profile["updated_at"])
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    """내 프로필 조회"""
    try:
        supabase = get_supabase()

        result = supabase.table("profiles").select("*").eq("user_id", current_user["id"]).single().execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="프로필이 없습니다. 먼저 생성해주세요.")

        profile = result.data
        trust_score = calculate_trust_score(profile)

        return ProfileResponse(
            **profile,
            trust_score=trust_score,
            created_at=datetime.fromisoformat(profile["created_at"]),
            updated_at=datetime.fromisoformat(profile["updated_at"])
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@router.put("/me", response_model=ProfileResponse)
async def update_my_profile(
    profile_data: ProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    """내 프로필 수정"""
    try:
        supabase = get_supabase()

        # 기존 프로필 확인
        existing = supabase.table("profiles").select("id").eq("user_id", current_user["id"]).single().execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="프로필이 없습니다. 먼저 생성해주세요.")

        update_data = {
            **profile_data.model_dump(exclude_unset=True),
            "updated_at": datetime.utcnow().isoformat()
        }

        result = supabase.table("profiles").update(update_data).eq("user_id", current_user["id"]).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="프로필 수정 실패")

        profile = result.data[0]
        trust_score = calculate_trust_score(profile)

        return ProfileResponse(
            **profile,
            trust_score=trust_score,
            created_at=datetime.fromisoformat(profile["created_at"]),
            updated_at=datetime.fromisoformat(profile["updated_at"])
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@router.patch("/me/visibility")
async def toggle_profile_visibility(
    is_public: bool,
    current_user: dict = Depends(get_current_user)
):
    """프로필 공개/비공개 설정"""
    try:
        supabase = get_supabase()

        result = supabase.table("profiles").update({
            "is_public": is_public,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("user_id", current_user["id"]).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="프로필을 찾을 수 없습니다")

        return {"message": f"프로필이 {'공개' if is_public else '비공개'}로 설정되었습니다"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile(profile_id: str):
    """프로필 조회 (공개된 프로필만)"""
    try:
        supabase = get_supabase()

        result = supabase.table("profiles").select("*").eq("id", profile_id).eq("is_public", True).single().execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="프로필을 찾을 수 없거나 비공개 상태입니다")

        profile = result.data
        trust_score = calculate_trust_score(profile)

        return ProfileResponse(
            **profile,
            trust_score=trust_score,
            created_at=datetime.fromisoformat(profile["created_at"]),
            updated_at=datetime.fromisoformat(profile["updated_at"])
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
