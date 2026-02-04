"""
AI 자기소개서 API
"""
from fastapi import APIRouter, HTTPException, Depends
from openai import OpenAI

from app.schemas.ai_intro import AIIntroRequest, AIIntroResponse
from app.api.auth import get_current_user
from app.core.config import settings
from app.core.database import get_supabase

router = APIRouter()


def get_openai_client() -> OpenAI:
    """OpenAI 클라이언트"""
    if not settings.OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API 키가 설정되지 않았습니다")
    return OpenAI(api_key=settings.OPENAI_API_KEY)


def build_prompt(profile_data: dict, tone: str, length: str) -> str:
    """AI 자기소개서 프롬프트 생성"""

    tone_guide = {
        "professional": "전문적이고 신뢰감 있는 톤으로",
        "friendly": "친근하고 따뜻한 톤으로",
        "formal": "격식 있고 정중한 톤으로"
    }

    length_guide = {
        "short": "100자 내외로 간결하게",
        "medium": "200자 내외로",
        "long": "300자 내외로 상세하게"
    }

    prompt = f"""당신은 부동산 임대 시장에서 세입자가 집주인에게 좋은 인상을 줄 수 있도록 자기소개서를 작성해주는 전문가입니다.

다음 정보를 바탕으로 세입자 자기소개서를 작성해주세요.
{tone_guide.get(tone, tone_guide['professional'])} 작성하고, {length_guide.get(length, length_guide['medium'])} 작성해주세요.

[세입자 정보]
- 직업: {profile_data.get('occupation', '미입력')}
- 고용형태: {profile_data.get('employment_type', '미입력')}
- 근속기간: {profile_data.get('work_duration_months', '미입력')}개월
- 반려동물: {'있음 (' + profile_data.get('pet_type', '') + ')' if profile_data.get('has_pet') else '없음'}
- 흡연 여부: {'흡연' if profile_data.get('is_smoker') else '비흡연'}
- 거주 형태: {'1인 거주' if profile_data.get('living_alone') else '동거'}
- 참고 자기소개: {profile_data.get('introduction', '없음')}

[작성 지침]
1. 집주인이 안심할 수 있는 내용 위주로 작성
2. 월세 납부 성실성, 시설 관리 의지를 자연스럽게 언급
3. 부정적인 요소(반려동물, 흡연 등)는 긍정적으로 프레이밍
4. 과장하지 말고 진정성 있게 작성
5. 한국어로 작성

[출력 형식]
자기소개서 본문만 출력하세요. 제목이나 부가 설명 없이 본문만 작성해주세요.
"""
    return prompt


def extract_keywords(introduction: str) -> list[str]:
    """자기소개서에서 키워드 추출"""
    keywords = []

    keyword_map = {
        "직장인": ["직장", "회사", "근무"],
        "안정적": ["안정", "정규직", "근속"],
        "비흡연": ["비흡연", "흡연하지"],
        "반려동물 없음": ["반려동물 없", "펫 없"],
        "1인 거주": ["혼자", "1인"],
        "깔끔함": ["깔끔", "청결", "정리"],
        "성실함": ["성실", "꼼꼼", "책임"],
    }

    for keyword, patterns in keyword_map.items():
        for pattern in patterns:
            if pattern in introduction:
                keywords.append(keyword)
                break

    return keywords[:5]  # 최대 5개


def extract_trust_highlights(introduction: str) -> list[str]:
    """신뢰 포인트 추출"""
    highlights = []

    trust_patterns = [
        ("월세 납부", ["월세", "납부", "제때"]),
        ("시설 관리", ["시설", "관리", "깔끔", "청결"]),
        ("안정적 소득", ["안정", "소득", "직장", "정규직"]),
        ("조용한 생활", ["조용", "이웃", "소음"]),
        ("장기 거주 희망", ["장기", "오래"]),
    ]

    for highlight, patterns in trust_patterns:
        for pattern in patterns:
            if pattern in introduction:
                highlights.append(highlight)
                break

    return highlights[:3]  # 최대 3개


@router.post("/introduction", response_model=AIIntroResponse)
async def generate_ai_introduction(
    request: AIIntroRequest,
    current_user: dict = Depends(get_current_user)
):
    """AI 자기소개서 생성"""
    try:
        profile_data = {}

        # 프로필 ID로 조회하거나 직접 입력 데이터 사용
        if request.profile_id:
            supabase = get_supabase()
            result = supabase.table("profiles").select("*").eq("id", request.profile_id).eq("user_id", current_user["id"]).single().execute()

            if not result.data:
                raise HTTPException(status_code=404, detail="프로필을 찾을 수 없습니다")

            profile_data = result.data
        else:
            profile_data = {
                "occupation": request.occupation,
                "employment_type": request.employment_type,
                "work_duration_months": request.work_duration_months,
                "has_pet": request.has_pet,
                "pet_type": request.pet_type,
                "is_smoker": request.is_smoker,
                "living_alone": request.living_alone,
                "introduction": request.introduction,
            }

        # OpenAI API 호출
        client = get_openai_client()
        prompt = build_prompt(profile_data, request.tone, request.length)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 부동산 임대 시장 전문 카피라이터입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        introduction = response.choices[0].message.content.strip()

        # 키워드 및 신뢰 포인트 추출
        keywords = extract_keywords(introduction)
        trust_highlights = extract_trust_highlights(introduction)

        return AIIntroResponse(
            introduction=introduction,
            keywords=keywords,
            trust_highlights=trust_highlights
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 자기소개서 생성 실패: {str(e)}")


@router.post("/introduction/save")
async def save_ai_introduction(
    introduction: str,
    current_user: dict = Depends(get_current_user)
):
    """AI 자기소개서 저장"""
    try:
        supabase = get_supabase()

        result = supabase.table("profiles").update({
            "ai_introduction": introduction
        }).eq("user_id", current_user["id"]).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="프로필을 찾을 수 없습니다")

        return {"message": "AI 자기소개서가 저장되었습니다"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"저장 실패: {str(e)}")
