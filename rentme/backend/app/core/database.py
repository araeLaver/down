"""
Supabase 데이터베이스 연결
"""
from supabase import create_client, Client
from app.core.config import settings

supabase: Client = None


def get_supabase() -> Client:
    """Supabase 클라이언트 반환"""
    global supabase
    if supabase is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise ValueError("Supabase URL과 Key가 설정되지 않았습니다.")
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return supabase


def init_db():
    """데이터베이스 초기화 (테이블 생성은 Supabase 대시보드에서)"""
    try:
        client = get_supabase()
        print("✅ Supabase 연결 성공")
        return True
    except Exception as e:
        print(f"❌ Supabase 연결 실패: {e}")
        return False
