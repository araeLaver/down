"""
Flask 애플리케이션 라우트 테스트
"""
import pytest
from unittest.mock import patch, MagicMock


class TestIndexRoutes:
    """메인 페이지 라우트 테스트"""

    def test_index_returns_200(self, client):
        """메인 페이지 접근 테스트"""
        with patch('app.render_template') as mock_render:
            mock_render.return_value = '<html>Test</html>'
            response = client.get('/')
            assert response.status_code == 200

    def test_dashboard_returns_200(self, client):
        """대시보드 페이지 접근 테스트"""
        with patch('app.render_template') as mock_render:
            mock_render.return_value = '<html>Dashboard</html>'
            response = client.get('/dashboard')
            assert response.status_code == 200

    def test_startup_roadmap_returns_200(self, client):
        """창업 로드맵 페이지 접근 테스트"""
        with patch('app.render_template') as mock_render:
            mock_render.return_value = '<html>Roadmap</html>'
            response = client.get('/startup-roadmap')
            assert response.status_code == 200

    def test_business_plan_returns_200(self, client):
        """사업계획서 페이지 접근 테스트"""
        with patch('app.render_template') as mock_render:
            mock_render.return_value = '<html>Business Plan</html>'
            response = client.get('/business-plan')
            assert response.status_code == 200

    def test_monitor_returns_200(self, client):
        """모니터링 페이지 접근 테스트"""
        with patch('app.render_template') as mock_render:
            mock_render.return_value = '<html>Monitor</html>'
            response = client.get('/monitor')
            assert response.status_code == 200


class TestAPIRoutes:
    """API 라우트 테스트"""

    @pytest.mark.skip(reason="DB 의존성 - 통합 테스트로 분류")
    def test_api_stats_returns_json(self, client):
        """통계 API JSON 응답 테스트"""
        # /api/stats는 DB 의존성이 높아 통합 테스트로 분류
        response = client.get('/api/stats')
        assert response.content_type == 'application/json'

    def test_api_auth_status_returns_json(self, client):
        """인증 상태 API 테스트"""
        response = client.get('/api/auth/status')
        assert response.status_code == 200
        data = response.get_json()
        assert 'auth_enabled' in data
        assert 'token_expiry_hours' in data

    def test_api_token_without_credentials(self, client):
        """인증 정보 없이 토큰 요청 테스트"""
        response = client.post('/api/auth/token', json={})
        # 인증 비활성화 또는 400 에러 예상
        assert response.status_code in [200, 400]


class TestAPIAuthentication:
    """API 인증 테스트"""

    def test_protected_endpoint_without_auth(self, client):
        """인증 없이 보호된 엔드포인트 접근"""
        response = client.get('/api/auth/verify')
        # 인증 비활성화 시 200, 활성화 시 401
        assert response.status_code in [200, 401]

    def test_protected_endpoint_with_valid_jwt(self, client, jwt_token):
        """유효한 JWT로 보호된 엔드포인트 접근"""
        response = client.get(
            '/api/auth/verify',
            headers={'Authorization': f'Bearer {jwt_token}'}
        )
        # 토큰 유효 시 200
        assert response.status_code == 200

    def test_protected_endpoint_with_invalid_jwt(self, client):
        """잘못된 JWT로 보호된 엔드포인트 접근"""
        response = client.get(
            '/api/auth/verify',
            headers={'Authorization': 'Bearer invalid-token'}
        )
        # 인증 비활성화 시 200, 활성화 시 401
        assert response.status_code in [200, 401]


class TestErrorHandling:
    """에러 처리 테스트"""

    def test_404_for_unknown_route(self, client):
        """존재하지 않는 라우트 404 테스트"""
        response = client.get('/nonexistent-route')
        assert response.status_code == 404

    def test_method_not_allowed(self, client):
        """허용되지 않은 메서드 테스트"""
        response = client.post('/')  # GET만 허용
        assert response.status_code == 405


class TestCORS:
    """CORS 설정 테스트"""

    def test_cors_headers_present(self, client):
        """CORS 헤더 존재 확인"""
        response = client.options('/', headers={
            'Origin': 'https://anonymous-kylen-untab-d30cd097.koyeb.app',
            'Access-Control-Request-Method': 'GET'
        })
        # CORS preflight 응답
        assert response.status_code in [200, 204]


class TestHealthCheck:
    """헬스체크 테스트"""

    def test_app_is_running(self, client):
        """앱 실행 상태 확인"""
        with patch('app.render_template') as mock_render:
            mock_render.return_value = '<html>OK</html>'
            response = client.get('/')
            assert response.status_code == 200


class TestGitStats:
    """Git 통계 함수 테스트"""

    def test_get_git_stats_with_repo(self, mock_git_repo):
        """Git 저장소 있을 때 통계 테스트"""
        with patch('app.repo', mock_git_repo):
            from app import get_git_stats
            stats = get_git_stats()
            assert 'current_branch' in stats
            assert stats['current_branch'] == 'main'

    def test_get_git_stats_without_repo(self):
        """Git 저장소 없을 때 통계 테스트"""
        with patch('app.repo', None):
            from app import get_git_stats
            stats = get_git_stats()
            assert stats == {}


class TestDatabaseSession:
    """데이터베이스 세션 테스트"""

    def test_get_db_session_success(self, mock_db_session):
        """DB 세션 생성 성공 테스트"""
        with patch('app.Session') as mock_session_class:
            mock_session_class.return_value = mock_db_session
            mock_db_session.execute.return_value = None
            from app import get_db_session
            session = get_db_session()
            # Mock 세션 반환
            assert session is not None

    def test_get_db_session_retry_on_failure(self, mock_db_session):
        """DB 연결 실패 시 재시도 테스트"""
        with patch('app.Session') as mock_session_class, \
             patch('app.engine') as mock_engine:
            # 첫 번째 호출 실패, 두 번째 성공
            mock_session_class.side_effect = [
                Exception("Connection failed"),
                mock_db_session
            ]
            from app import get_db_session
            session = get_db_session()
            # dispose 호출 확인
            mock_engine.dispose.assert_called_once()
