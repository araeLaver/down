"""
Qhyx Inc. API 인증 모듈
- API 키 기반 인증
- JWT 토큰 인증
- 데코레이터 기반 보호
"""

import os
import time
import hmac
import hashlib
import secrets
from functools import wraps
from typing import Optional, Callable
from datetime import datetime, timedelta
from flask import request, jsonify, g

from config import APIConfig


# ============================================
# API 키 관리
# ============================================

class APIKeyManager:
    """API 키 관리자"""

    def __init__(self):
        self._secret_key = APIConfig.get_secret_key()

    def generate_api_key(self, client_id: str) -> str:
        """클라이언트 ID 기반 API 키 생성"""
        timestamp = str(int(time.time()))
        data = f"{client_id}:{timestamp}:{secrets.token_hex(16)}"
        signature = hmac.new(
            self._secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"{data}:{signature}"

    def validate_api_key(self, api_key: str) -> tuple:
        """API 키 검증 (client_id, valid 반환)"""
        try:
            parts = api_key.rsplit(':', 1)
            if len(parts) != 2:
                return None, False

            data, provided_signature = parts
            expected_signature = hmac.new(
                self._secret_key.encode(),
                data.encode(),
                hashlib.sha256
            ).hexdigest()

            if hmac.compare_digest(provided_signature, expected_signature):
                client_id = data.split(':')[0]
                return client_id, True

            return None, False
        except Exception:
            return None, False


# ============================================
# JWT 토큰 관리 (간단 구현)
# ============================================

class SimpleJWT:
    """간단한 JWT 구현 (외부 라이브러리 없이)"""

    def __init__(self):
        self._secret_key = APIConfig.get_secret_key()
        self._expiry_hours = APIConfig.get_token_expiry_hours()

    def _base64_encode(self, data: str) -> str:
        """Base64 URL-safe 인코딩"""
        import base64
        return base64.urlsafe_b64encode(data.encode()).decode().rstrip('=')

    def _base64_decode(self, data: str) -> str:
        """Base64 URL-safe 디코딩"""
        import base64
        padding = 4 - len(data) % 4
        if padding != 4:
            data += '=' * padding
        return base64.urlsafe_b64decode(data).decode()

    def create_token(self, payload: dict) -> str:
        """JWT 토큰 생성"""
        import json

        # 헤더
        header = {"alg": "HS256", "typ": "JWT"}
        header_encoded = self._base64_encode(json.dumps(header))

        # 페이로드에 만료 시간 추가
        payload['exp'] = int((datetime.now() + timedelta(hours=self._expiry_hours)).timestamp())
        payload['iat'] = int(datetime.now().timestamp())
        payload_encoded = self._base64_encode(json.dumps(payload))

        # 서명
        message = f"{header_encoded}.{payload_encoded}"
        signature = hmac.new(
            self._secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        signature_encoded = self._base64_encode(signature)

        return f"{header_encoded}.{payload_encoded}.{signature_encoded}"

    def verify_token(self, token: str) -> tuple:
        """JWT 토큰 검증 (payload, valid 반환)"""
        import json

        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None, False

            header_encoded, payload_encoded, signature_encoded = parts

            # 서명 검증
            message = f"{header_encoded}.{payload_encoded}"
            expected_signature = hmac.new(
                self._secret_key.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()

            provided_signature = self._base64_decode(signature_encoded)
            if not hmac.compare_digest(expected_signature, provided_signature):
                return None, False

            # 페이로드 디코딩
            payload = json.loads(self._base64_decode(payload_encoded))

            # 만료 확인
            if payload.get('exp', 0) < time.time():
                return None, False

            return payload, True

        except Exception:
            return None, False


# ============================================
# Flask 인증 데코레이터
# ============================================

def require_api_key(func: Callable) -> Callable:
    """API 키 인증 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 인증이 비활성화된 경우 통과
        if not APIConfig.is_auth_enabled():
            return func(*args, **kwargs)

        # API 키 확인
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')

        if not api_key:
            return jsonify({
                'error': 'API key required',
                'message': 'X-API-Key 헤더 또는 api_key 파라미터가 필요합니다.'
            }), 401

        manager = APIKeyManager()
        client_id, valid = manager.validate_api_key(api_key)

        if not valid:
            return jsonify({
                'error': 'Invalid API key',
                'message': '유효하지 않은 API 키입니다.'
            }), 401

        # 요청 컨텍스트에 클라이언트 ID 저장
        g.client_id = client_id
        return func(*args, **kwargs)

    return wrapper


def require_jwt(func: Callable) -> Callable:
    """JWT 토큰 인증 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 인증이 비활성화된 경우 통과
        if not APIConfig.is_auth_enabled():
            return func(*args, **kwargs)

        # Authorization 헤더 확인
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return jsonify({
                'error': 'JWT required',
                'message': 'Authorization: Bearer <token> 헤더가 필요합니다.'
            }), 401

        token = auth_header[7:]  # 'Bearer ' 제거

        jwt = SimpleJWT()
        payload, valid = jwt.verify_token(token)

        if not valid:
            return jsonify({
                'error': 'Invalid or expired token',
                'message': '유효하지 않거나 만료된 토큰입니다.'
            }), 401

        # 요청 컨텍스트에 페이로드 저장
        g.jwt_payload = payload
        return func(*args, **kwargs)

    return wrapper


def optional_auth(func: Callable) -> Callable:
    """선택적 인증 데코레이터 (인증 시 추가 권한)"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        g.authenticated = False
        g.client_id = None

        # API 키 확인
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        if api_key:
            manager = APIKeyManager()
            client_id, valid = manager.validate_api_key(api_key)
            if valid:
                g.authenticated = True
                g.client_id = client_id

        # JWT 확인
        if not g.authenticated:
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
                jwt = SimpleJWT()
                payload, valid = jwt.verify_token(token)
                if valid:
                    g.authenticated = True
                    g.jwt_payload = payload

        return func(*args, **kwargs)

    return wrapper


# ============================================
# 인증 관련 API 엔드포인트 헬퍼
# ============================================

def create_auth_routes(app):
    """인증 관련 라우트 등록"""

    @app.route('/api/auth/token', methods=['POST'])
    def get_token():
        """JWT 토큰 발급"""
        if not APIConfig.is_auth_enabled():
            return jsonify({
                'error': 'Auth disabled',
                'message': '인증이 비활성화되어 있습니다.'
            }), 400

        data = request.get_json() or {}
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')

        if not client_id or not client_secret:
            return jsonify({
                'error': 'Missing credentials',
                'message': 'client_id와 client_secret이 필요합니다.'
            }), 400

        # 간단한 검증 (실제로는 DB에서 확인해야 함)
        expected_secret = hmac.new(
            APIConfig.get_secret_key().encode(),
            client_id.encode(),
            hashlib.sha256
        ).hexdigest()[:32]

        if client_secret != expected_secret:
            return jsonify({
                'error': 'Invalid credentials',
                'message': '잘못된 인증 정보입니다.'
            }), 401

        jwt = SimpleJWT()
        token = jwt.create_token({
            'client_id': client_id,
            'scope': 'read write'
        })

        return jsonify({
            'access_token': token,
            'token_type': 'Bearer',
            'expires_in': APIConfig.get_token_expiry_hours() * 3600
        })

    @app.route('/api/auth/verify', methods=['GET'])
    @require_jwt
    def verify_token():
        """토큰 검증"""
        return jsonify({
            'valid': True,
            'payload': g.jwt_payload
        })

    @app.route('/api/auth/status', methods=['GET'])
    def auth_status():
        """인증 시스템 상태"""
        return jsonify({
            'auth_enabled': APIConfig.is_auth_enabled(),
            'token_expiry_hours': APIConfig.get_token_expiry_hours()
        })


# 싱글톤 인스턴스
_api_key_manager: Optional[APIKeyManager] = None
_jwt_manager: Optional[SimpleJWT] = None


def get_api_key_manager() -> APIKeyManager:
    """API 키 관리자 싱글톤"""
    global _api_key_manager
    if _api_key_manager is None:
        _api_key_manager = APIKeyManager()
    return _api_key_manager


def get_jwt_manager() -> SimpleJWT:
    """JWT 관리자 싱글톤"""
    global _jwt_manager
    if _jwt_manager is None:
        _jwt_manager = SimpleJWT()
    return _jwt_manager
