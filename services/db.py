from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import DatabaseConfig

DATABASE_URL = DatabaseConfig.get_database_url()
engine = create_engine(DATABASE_URL, **DatabaseConfig.get_engine_options())
Session = sessionmaker(bind=engine)


def get_db_session():
    """안전한 DB 세션 생성 (재연결 포함)"""
    try:
        session = Session()
        session.execute(text("SELECT 1"))
        return session
    except Exception as e:
        print(f"[DB] Connection error, retrying: {e}")
        try:
            engine.dispose()
            session = Session()
            return session
        except Exception as e2:
            print(f"[DB] Retry failed: {e2}")
            return None
