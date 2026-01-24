"""
인증 모듈 테스트
- API Key 인증
- JWT 토큰 인증
"""
import os
import sys
import pytest
import time
from unittest.mock import patch, MagicMock

# 테스트 환경 설정
os.environ['API_SECRET_KEY'] = 'test-secret-key-for-testing-only'

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import APIKeyManager, SimpleJWT, get_api_key_manager, get_jwt_manager


class TestAPIKeyManager:
    """API 키 관리자 테스트"""

    def test_generate_api_key(self):
        """API 키 생성 테스트"""
        manager = APIKeyManager()
        api_key = manager.generate_api_key('test-client')

        assert api_key is not None
        assert len(api_key) > 0
        assert ':' in api_key  # 형식: client_id:timestamp:random:signature

    def test_validate_valid_api_key(self):
        """유효한 API 키 검증 테스트"""
        manager = APIKeyManager()
        api_key = manager.generate_api_key('test-client')

        client_id, valid = manager.validate_api_key(api_key)

        assert valid is True
        assert client_id == 'test-client'

    def test_validate_invalid_api_key(self):
        """잘못된 API 키 검증 테스트"""
        manager = APIKeyManager()

        client_id, valid = manager.validate_api_key('invalid-api-key')

        assert valid is False
        assert client_id is None

    def test_validate_tampered_api_key(self):
        """변조된 API 키 검증 테스트"""
        manager = APIKeyManager()
        api_key = manager.generate_api_key('test-client')

        # 서명 변조
        tampered_key = api_key[:-10] + 'aaaaaaaaaa'

        client_id, valid = manager.validate_api_key(tampered_key)

        assert valid is False
        assert client_id is None

    def test_validate_empty_api_key(self):
        """빈 API 키 검증 테스트"""
        manager = APIKeyManager()

        client_id, valid = manager.validate_api_key('')

        assert valid is False
        assert client_id is None

    def test_validate_malformed_api_key(self):
        """형식 오류 API 키 검증 테스트"""
        manager = APIKeyManager()

        # 콜론 없는 키
        client_id, valid = manager.validate_api_key('no-colons-here')

        assert valid is False
        assert client_id is None

    def test_different_clients_get_different_keys(self):
        """다른 클라이언트는 다른 키 생성"""
        manager = APIKeyManager()
        key1 = manager.generate_api_key('client-1')
        key2 = manager.generate_api_key('client-2')

        assert key1 != key2


class TestSimpleJWT:
    """JWT 토큰 테스트"""

    def test_create_token(self):
        """JWT 토큰 생성 테스트"""
        jwt = SimpleJWT()
        token = jwt.create_token({'client_id': 'test', 'scope': 'read'})

        assert token is not None
        assert len(token) > 0
        assert token.count('.') == 2  # header.payload.signature

    def test_verify_valid_token(self):
        """유효한 JWT 토큰 검증 테스트"""
        jwt = SimpleJWT()
        original_payload = {'client_id': 'test', 'scope': 'read write'}
        token = jwt.create_token(original_payload)

        payload, valid = jwt.verify_token(token)

        assert valid is True
        assert payload['client_id'] == 'test'
        assert payload['scope'] == 'read write'
        assert 'exp' in payload
        assert 'iat' in payload

    def test_verify_invalid_token(self):
        """잘못된 JWT 토큰 검증 테스트"""
        jwt = SimpleJWT()

        payload, valid = jwt.verify_token('invalid.token.here')

        assert valid is False
        assert payload is None

    def test_verify_tampered_token(self):
        """변조된 JWT 토큰 검증 테스트"""
        jwt = SimpleJWT()
        token = jwt.create_token({'client_id': 'test'})

        # 토큰 변조
        parts = token.split('.')
        tampered_token = f"{parts[0]}.{parts[1]}modified.{parts[2]}"

        payload, valid = jwt.verify_token(tampered_token)

        assert valid is False
        assert payload is None

    def test_verify_expired_token(self):
        """만료된 JWT 토큰 검증 테스트"""
        jwt = SimpleJWT()

        # 만료 시간을 1시간으로 설정한 상태에서 토큰 생성 후
        # 시간을 미래로 이동하여 테스트
        with patch.object(jwt, '_expiry_hours', 0):  # 즉시 만료
            # 직접 만료된 페이로드로 토큰 생성
            import json
            import hmac
            import hashlib

            header = {"alg": "HS256", "typ": "JWT"}
            payload = {
                'client_id': 'test',
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

            expired_token = f"{header_encoded}.{payload_encoded}.{signature_encoded}"

        result_payload, valid = jwt.verify_token(expired_token)

        assert valid is False
        assert result_payload is None

    def test_verify_malformed_token(self):
        """형식 오류 JWT 토큰 테스트"""
        jwt = SimpleJWT()

        # 부분이 2개인 토큰
        payload, valid = jwt.verify_token('only.two')
        assert valid is False

        # 부분이 4개인 토큰
        payload, valid = jwt.verify_token('one.two.three.four')
        assert valid is False

    def test_base64_encode_decode(self):
        """Base64 인코딩/디코딩 테스트"""
        jwt = SimpleJWT()
        original = "Hello, World! 한글 테스트"

        encoded = jwt._base64_encode(original)
        decoded = jwt._base64_decode(encoded)

        assert decoded == original


class TestSingletons:
    """싱글톤 인스턴스 테스트"""

    def test_api_key_manager_singleton(self):
        """API 키 관리자 싱글톤 테스트"""
        manager1 = get_api_key_manager()
        manager2 = get_api_key_manager()

        assert manager1 is manager2

    def test_jwt_manager_singleton(self):
        """JWT 관리자 싱글톤 테스트"""
        jwt1 = get_jwt_manager()
        jwt2 = get_jwt_manager()

        assert jwt1 is jwt2


class TestDecorators:
    """인증 데코레이터 테스트 (단위 테스트)"""

    def test_require_api_key_with_disabled_auth(self):
        """인증 비활성화 시 데코레이터 통과"""
        from auth import require_api_key
        from flask import Flask

        test_app = Flask(__name__)

        @test_app.route('/test')
        @require_api_key
        def test_route():
            return 'OK'

        with patch('config.APIConfig.is_auth_enabled', return_value=False):
            with test_app.test_client() as client:
                response = client.get('/test')
                assert response.status_code == 200

    def test_require_api_key_without_key(self):
        """API 키 없이 요청 시 401"""
        from auth import require_api_key
        from flask import Flask

        test_app = Flask(__name__)

        @test_app.route('/test')
        @require_api_key
        def test_route():
            return 'OK'

        with patch('config.APIConfig.is_auth_enabled', return_value=True):
            with test_app.test_client() as client:
                response = client.get('/test')
                assert response.status_code == 401

    def test_require_jwt_with_valid_token(self, jwt_token):
        """유효한 JWT로 인증 테스트"""
        from auth import require_jwt
        from flask import Flask, g

        test_app = Flask(__name__)

        @test_app.route('/test')
        @require_jwt
        def test_route():
            return 'OK'

        with patch('config.APIConfig.is_auth_enabled', return_value=True):
            with test_app.test_client() as client:
                response = client.get(
                    '/test',
                    headers={'Authorization': f'Bearer {jwt_token}'}
                )
                assert response.status_code == 200

    def test_require_jwt_without_bearer_prefix(self, jwt_token):
        """Bearer 접두사 없이 JWT 인증 시 401"""
        from auth import require_jwt
        from flask import Flask

        test_app = Flask(__name__)

        @test_app.route('/test')
        @require_jwt
        def test_route():
            return 'OK'

        with patch('config.APIConfig.is_auth_enabled', return_value=True):
            with test_app.test_client() as client:
                response = client.get(
                    '/test',
                    headers={'Authorization': jwt_token}  # Bearer 없음
                )
                assert response.status_code == 401


class TestAuthRoutes:
    """인증 라우트 테스트 (단위 테스트)"""

    def test_get_token_with_valid_credentials(self):
        """유효한 인증 정보로 토큰 발급"""
        import hmac
        import hashlib
        from flask import Flask
        from auth import create_auth_routes

        test_app = Flask(__name__)
        create_auth_routes(test_app)

        client_id = 'test-client'
        secret_key = os.environ.get('API_SECRET_KEY', 'test-secret-key-for-testing-only')
        client_secret = hmac.new(
            secret_key.encode(),
            client_id.encode(),
            hashlib.sha256
        ).hexdigest()[:32]

        with patch('config.APIConfig.is_auth_enabled', return_value=True):
            with test_app.test_client() as client:
                response = client.post('/api/auth/token', json={
                    'client_id': client_id,
                    'client_secret': client_secret
                })

                assert response.status_code == 200
                data = response.get_json()
                assert 'access_token' in data
                assert data['token_type'] == 'Bearer'

    def test_get_token_with_invalid_credentials(self):
        """잘못된 인증 정보로 토큰 발급 시도"""
        from flask import Flask
        from auth import create_auth_routes

        test_app = Flask(__name__)
        create_auth_routes(test_app)

        with patch('config.APIConfig.is_auth_enabled', return_value=True):
            with test_app.test_client() as client:
                response = client.post('/api/auth/token', json={
                    'client_id': 'test-client',
                    'client_secret': 'wrong-secret'
                })

                assert response.status_code == 401

    def test_get_token_without_credentials(self):
        """인증 정보 없이 토큰 발급 시도"""
        from flask import Flask
        from auth import create_auth_routes

        test_app = Flask(__name__)
        create_auth_routes(test_app)

        with patch('config.APIConfig.is_auth_enabled', return_value=True):
            with test_app.test_client() as client:
                response = client.post('/api/auth/token', json={})

                assert response.status_code == 400

    def test_auth_status_endpoint(self):
        """인증 상태 확인 엔드포인트"""
        from flask import Flask
        from auth import create_auth_routes

        test_app = Flask(__name__)
        create_auth_routes(test_app)

        with test_app.test_client() as client:
            response = client.get('/api/auth/status')

            assert response.status_code == 200
            data = response.get_json()
            assert 'auth_enabled' in data
            assert isinstance(data['auth_enabled'], bool)


class TestSecurityEdgeCases:
    """보안 엣지 케이스 테스트"""

    def test_timing_attack_resistance(self):
        """타이밍 공격 저항성 테스트 (hmac.compare_digest 사용 확인)"""
        manager = APIKeyManager()
        api_key = manager.generate_api_key('test')

        # 여러 번 검증하여 일관된 시간 확인
        import time
        times = []
        for _ in range(10):
            start = time.perf_counter()
            manager.validate_api_key(api_key)
            times.append(time.perf_counter() - start)

        # 시간 편차가 크지 않아야 함 (대략적 확인)
        avg = sum(times) / len(times)
        max_diff = max(abs(t - avg) for t in times)

        # 타이밍 차이가 10ms 이내 (매우 느슨한 기준)
        assert max_diff < 0.01

    def test_large_payload_handling(self):
        """큰 페이로드 처리 테스트"""
        jwt = SimpleJWT()

        large_payload = {
            'client_id': 'test',
            'data': 'x' * 10000  # 10KB 데이터
        }

        token = jwt.create_token(large_payload)
        payload, valid = jwt.verify_token(token)

        assert valid is True
        assert len(payload['data']) == 10000

    def test_special_characters_in_client_id(self):
        """클라이언트 ID 특수문자 처리"""
        manager = APIKeyManager()
        special_ids = [
            'test@client.com',
            'client/with/slashes',
            'client+plus',
            'client with spaces',
            '한글클라이언트'
        ]

        for client_id in special_ids:
            api_key = manager.generate_api_key(client_id)
            result_id, valid = manager.validate_api_key(api_key)

            assert valid is True, f"Failed for client_id: {client_id}"
            assert result_id == client_id
