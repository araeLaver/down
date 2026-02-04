"""
레퍼런스 API
"""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
import uuid
import secrets

from app.schemas.reference import ReferenceRequest, ReferenceResponse, ReferenceSubmit, ReferenceStatus
from app.api.auth import get_current_user
from app.core.database import get_supabase

router = APIRouter()


def generate_reference_code() -> str:
    """레퍼런스 코드 생성 (8자리)"""
    return secrets.token_urlsafe(6)[:8].upper()


@router.post("", response_model=ReferenceResponse)
async def request_reference(
    reference_data: ReferenceRequest,
    current_user: dict = Depends(get_current_user)
):
    """레퍼런스 요청"""
    try:
        supabase = get_supabase()

        reference_id = str(uuid.uuid4())
        request_code = generate_reference_code()
        now = datetime.utcnow().isoformat()

        new_reference = {
            "id": reference_id,
            "tenant_id": current_user["id"],
            "landlord_name": reference_data.landlord_name,
            "landlord_email": reference_data.landlord_email,
            "landlord_phone": reference_data.landlord_phone,
            "address": reference_data.address,
            "rental_start": reference_data.rental_start,
            "rental_end": reference_data.rental_end,
            "monthly_rent": reference_data.monthly_rent,
            "deposit": reference_data.deposit,
            "status": "pending",
            "request_code": request_code,
            "created_at": now,
        }

        result = supabase.table("references").insert(new_reference).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="레퍼런스 요청 실패")

        reference = result.data[0]

        # TODO: 집주인에게 이메일/SMS 발송

        return ReferenceResponse(
            **reference,
            status=ReferenceStatus.PENDING,
            created_at=datetime.fromisoformat(reference["created_at"])
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@router.get("", response_model=list[ReferenceResponse])
async def get_my_references(current_user: dict = Depends(get_current_user)):
    """내 레퍼런스 목록 조회"""
    try:
        supabase = get_supabase()

        result = supabase.table("references").select("*").eq("tenant_id", current_user["id"]).order("created_at", desc=True).execute()

        references = []
        for ref in result.data:
            references.append(ReferenceResponse(
                **ref,
                status=ReferenceStatus(ref["status"]),
                created_at=datetime.fromisoformat(ref["created_at"]),
                completed_at=datetime.fromisoformat(ref["completed_at"]) if ref.get("completed_at") else None
            ))

        return references

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@router.get("/verify/{request_code}")
async def verify_reference_code(request_code: str):
    """레퍼런스 코드 확인 (집주인용)"""
    try:
        supabase = get_supabase()

        result = supabase.table("references").select(
            "id, tenant_id, landlord_name, address, rental_start, rental_end, status"
        ).eq("request_code", request_code).single().execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="유효하지 않은 코드입니다")

        reference = result.data

        if reference["status"] != "pending":
            raise HTTPException(status_code=400, detail="이미 처리된 레퍼런스입니다")

        # 세입자 이름 조회
        tenant_result = supabase.table("users").select("name").eq("id", reference["tenant_id"]).single().execute()
        tenant_name = tenant_result.data["name"] if tenant_result.data else "알 수 없음"

        return {
            "reference_id": reference["id"],
            "tenant_name": tenant_name,
            "address": reference["address"],
            "rental_start": reference["rental_start"],
            "rental_end": reference["rental_end"],
            "message": "레퍼런스 작성을 진행해주세요"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@router.post("/submit")
async def submit_reference(submit_data: ReferenceSubmit):
    """레퍼런스 작성 (집주인용, 인증 불필요)"""
    try:
        supabase = get_supabase()

        # 코드 확인
        result = supabase.table("references").select("*").eq("request_code", submit_data.request_code).single().execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="유효하지 않은 코드입니다")

        reference = result.data

        if reference["status"] != "pending":
            raise HTTPException(status_code=400, detail="이미 처리된 레퍼런스입니다")

        now = datetime.utcnow().isoformat()

        # 레퍼런스 업데이트
        update_data = {
            "rating": submit_data.rating,
            "payment_punctuality": submit_data.payment_punctuality,
            "property_care": submit_data.property_care,
            "communication": submit_data.communication,
            "would_rent_again": submit_data.would_rent_again,
            "comment": submit_data.comment,
            "status": "completed",
            "completed_at": now,
        }

        update_result = supabase.table("references").update(update_data).eq("id", reference["id"]).execute()

        if not update_result.data:
            raise HTTPException(status_code=500, detail="레퍼런스 저장 실패")

        return {"message": "레퍼런스가 성공적으로 작성되었습니다. 감사합니다!"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
