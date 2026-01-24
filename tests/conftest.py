"""
Pytest 설정 및 공통 Fixture
"""
import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 테스트 환경 설정 (실제 DB 연결 방지)
os.environ['TESTING'] = 'true'
os.environ['API_SECRET_KEY'] = 'test-secret-key-for-testing-only'


@pytest.fixture
def mock_db_session():
    """Mock 데이터베이스 세션"""
    session = MagicMock()
    session.query.return_value.filter.return_value.first.return_value = None
    session.query.return_value.filter_by.return_value.first.return_value = None
    session.query.return_value.order_by.return_value.limit.return_value.all.return_value = []
    session.query.return_value.count.return_value = 0
    return session


@pytest.fixture
def app():
    """Flask 테스트 앱 (DB Mock 처리)"""
    # SQLAlchemy 엔진 Mock
    mock_engine = MagicMock()
    mock_session = MagicMock()
    mock_session.execute.return_value = MagicMock()

    # DB 초기화 함수 Mock
    with patch('database_setup.create_engine', return_value=mock_engine), \
         patch('database_setup.Session', return_value=mock_session), \
         patch('database_setup.initialize_database'), \
         patch('business_discovery_history.initialize_history_tables'), \
         patch.dict('os.environ', {'DATABASE_URL': 'postgresql://mock:mock@localhost/mockdb'}):

        # config 모듈의 엔진 옵션 Mock (SQLite 호환)
        with patch('config.DatabaseConfig.get_engine_options', return_value={
            'pool_pre_ping': True
        }):
            # app 모듈의 엔진/세션 Mock
            with patch('app.create_engine', return_value=mock_engine), \
                 patch('app.Session', return_value=mock_session), \
                 patch('app.get_db_session', return_value=mock_session), \
                 patch('app.repo', None):

                from app import app as flask_app

                flask_app.config['TESTING'] = True
                flask_app.config['WTF_CSRF_ENABLED'] = False

                yield flask_app


@pytest.fixture
def client(app):
    """Flask 테스트 클라이언트"""
    return app.test_client()


@pytest.fixture
def api_key():
    """테스트용 API 키 생성"""
    from auth import APIKeyManager
    manager = APIKeyManager()
    return manager.generate_api_key('test-client')


@pytest.fixture
def jwt_token():
    """테스트용 JWT 토큰 생성"""
    from auth import SimpleJWT
    jwt = SimpleJWT()
    return jwt.create_token({
        'client_id': 'test-client',
        'scope': 'read write'
    })


@pytest.fixture
def expired_jwt_token():
    """만료된 JWT 토큰"""
    from auth import SimpleJWT
    import time
    import json
    import hmac
    import hashlib

    jwt = SimpleJWT()

    # 만료된 페이로드로 직접 토큰 생성
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        'client_id': 'test-client',
        'exp': int(time.time()) - 3600,  # 1시간 전 만료
        'iat': int(time.time()) - 7200
    }

    header_encoded = jwt._base64_encode(json.dumps(header))
    payload_encoded = jwt._base64_encode(json.dumps(payload))

    message = f"{header_encoded}.{payload_encoded}"
    signature = hmac.new(
        jwt._secret_key.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    signature_encoded = jwt._base64_encode(signature)

    return f"{header_encoded}.{payload_encoded}.{signature_encoded}"


@pytest.fixture
def mock_git_repo():
    """Mock Git 저장소"""
    repo = MagicMock()
    repo.active_branch.name = 'main'
    repo.iter_commits.return_value = [MagicMock() for _ in range(10)]
    repo.index.diff.return_value = []
    repo.untracked_files = []
    repo.head.commit.hexsha = 'abc1234567890'
    repo.head.commit.message = 'Test commit message'
    repo.head.commit.author = 'Test Author'
    repo.head.commit.committed_date = 1700000000
    return repo
