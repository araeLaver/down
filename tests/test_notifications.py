"""
알림 시스템 테스트
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from notifications import (
    NotificationService, DiscoveryNotifier,
    get_notification_service, get_discovery_notifier,
    notify, notify_discovery_complete, notify_high_score_idea, notify_error
)


class TestNotificationService:
    """NotificationService 클래스 테스트"""

    def test_init_reads_config(self):
        """초기화 시 설정 읽기"""
        with patch('notifications.NotificationConfig') as mock_config:
            mock_config.is_enabled.return_value = True
            mock_config.is_slack_configured.return_value = False
            mock_config.is_email_configured.return_value = False

            service = NotificationService()
            assert service.enabled is True

    def test_notify_when_disabled(self):
        """알림 비활성화 시"""
        with patch('notifications.NotificationConfig') as mock_config:
            mock_config.is_enabled.return_value = False
            mock_config.is_slack_configured.return_value = False
            mock_config.is_email_configured.return_value = False

            service = NotificationService()
            result = service.notify("Test", "Message")
            assert result is None  # 아무것도 전송 안 함

    def test_notify_calls_slack_when_configured(self):
        """Slack 설정 시 Slack 전송"""
        with patch('notifications.NotificationConfig') as mock_config:
            mock_config.is_enabled.return_value = True
            mock_config.is_slack_configured.return_value = True
            mock_config.is_email_configured.return_value = False

            service = NotificationService()
            with patch.object(service, 'send_slack', return_value=True) as mock_slack:
                result = service.notify("Test", "Message")
                mock_slack.assert_called_once()

    def test_send_slack_without_requests(self):
        """requests 모듈 없이 Slack 전송 시도"""
        with patch('notifications.REQUESTS_AVAILABLE', False):
            with patch('notifications.NotificationConfig') as mock_config:
                mock_config.is_enabled.return_value = True
                mock_config.is_slack_configured.return_value = True
                mock_config.is_email_configured.return_value = False

                service = NotificationService()
                result = service.send_slack("Test", "Message")
                assert result is False

    def test_send_slack_success(self):
        """Slack 전송 성공"""
        with patch('notifications.REQUESTS_AVAILABLE', True):
            with patch('notifications.NotificationConfig') as mock_config:
                mock_config.get_slack_webhook.return_value = "https://hooks.slack.com/test"
                mock_config.is_enabled.return_value = True
                mock_config.is_slack_configured.return_value = True
                mock_config.is_email_configured.return_value = False

                with patch('notifications.requests') as mock_requests:
                    mock_response = MagicMock()
                    mock_response.status_code = 200
                    mock_requests.post.return_value = mock_response

                    service = NotificationService()
                    result = service.send_slack("Test", "Message", "info")
                    assert result is True

    def test_send_slack_failure(self):
        """Slack 전송 실패"""
        with patch('notifications.REQUESTS_AVAILABLE', True):
            with patch('notifications.NotificationConfig') as mock_config:
                mock_config.get_slack_webhook.return_value = "https://hooks.slack.com/test"
                mock_config.is_enabled.return_value = True
                mock_config.is_slack_configured.return_value = True
                mock_config.is_email_configured.return_value = False

                with patch('notifications.requests') as mock_requests:
                    mock_response = MagicMock()
                    mock_response.status_code = 500
                    mock_response.text = "Error"
                    mock_requests.post.return_value = mock_response

                    service = NotificationService()
                    result = service.send_slack("Test", "Message")
                    assert result is False

    def test_send_slack_with_data(self):
        """추가 데이터와 함께 Slack 전송"""
        with patch('notifications.REQUESTS_AVAILABLE', True):
            with patch('notifications.NotificationConfig') as mock_config:
                mock_config.get_slack_webhook.return_value = "https://hooks.slack.com/test"

                with patch('notifications.requests') as mock_requests:
                    mock_response = MagicMock()
                    mock_response.status_code = 200
                    mock_requests.post.return_value = mock_response

                    service = NotificationService()
                    result = service.send_slack(
                        "Test", "Message", "success",
                        data={"Key1": "Value1", "Key2": "Value2"}
                    )
                    assert result is True

                    # 전송된 데이터 확인
                    call_args = mock_requests.post.call_args
                    payload = call_args.kwargs.get('json') or call_args[1].get('json')
                    assert 'attachments' in payload

    def test_send_email_unconfigured(self):
        """이메일 미설정 시"""
        with patch('notifications.NotificationConfig') as mock_config:
            mock_config.get_email_config.return_value = {
                'smtp_host': '',
                'username': '',
                'password': '',
                'from_email': ''
            }

            service = NotificationService()
            result = service.send_email("Test", "Message")
            assert result is False

    def test_color_map_for_levels(self):
        """알림 레벨별 색상"""
        with patch('notifications.REQUESTS_AVAILABLE', True):
            with patch('notifications.NotificationConfig') as mock_config:
                mock_config.get_slack_webhook.return_value = "https://hooks.slack.com/test"

                with patch('notifications.requests') as mock_requests:
                    mock_response = MagicMock()
                    mock_response.status_code = 200
                    mock_requests.post.return_value = mock_response

                    service = NotificationService()

                    # 각 레벨 테스트
                    for level in ["info", "warning", "error", "success"]:
                        service.send_slack("Test", "Message", level)


class TestDiscoveryNotifier:
    """DiscoveryNotifier 클래스 테스트"""

    def test_init(self):
        """초기화 테스트"""
        with patch('notifications.NotificationConfig') as mock_config:
            mock_config.is_enabled.return_value = False
            mock_config.is_slack_configured.return_value = False
            mock_config.is_email_configured.return_value = False

            with patch('notifications.DiscoveryConfig') as mock_disc_config:
                mock_disc_config.get_min_score.return_value = 70

                notifier = DiscoveryNotifier()
                assert notifier.min_score == 70

    def test_notify_discovery_complete_with_saved(self):
        """저장된 아이디어가 있을 때"""
        with patch('notifications.NotificationConfig') as mock_config:
            mock_config.is_enabled.return_value = True
            mock_config.is_slack_configured.return_value = False
            mock_config.is_email_configured.return_value = False

            with patch('notifications.DiscoveryConfig') as mock_disc_config:
                mock_disc_config.get_min_score.return_value = 70

                notifier = DiscoveryNotifier()
                with patch.object(notifier.service, 'notify') as mock_notify:
                    results = {
                        'analyzed': 5,
                        'saved': 3,
                        'batch_id': 'TEST123',
                        'results': [
                            {'name': 'Idea 1', 'score': 85, 'saved': True},
                            {'name': 'Idea 2', 'score': 75, 'saved': True},
                        ]
                    }
                    notifier.notify_discovery_complete(results)
                    mock_notify.assert_called_once()

                    # 레벨이 success인지 확인
                    call_args = mock_notify.call_args
                    assert call_args[0][2] == "success"  # level

    def test_notify_discovery_complete_no_saved(self):
        """저장된 아이디어가 없을 때"""
        with patch('notifications.NotificationConfig') as mock_config:
            mock_config.is_enabled.return_value = True
            mock_config.is_slack_configured.return_value = False
            mock_config.is_email_configured.return_value = False

            with patch('notifications.DiscoveryConfig') as mock_disc_config:
                mock_disc_config.get_min_score.return_value = 70

                notifier = DiscoveryNotifier()
                with patch.object(notifier.service, 'notify') as mock_notify:
                    results = {
                        'analyzed': 5,
                        'saved': 0,
                        'batch_id': 'TEST123'
                    }
                    notifier.notify_discovery_complete(results)

                    # 레벨이 warning인지 확인
                    call_args = mock_notify.call_args
                    assert call_args[0][2] == "warning"

    def test_notify_high_score_idea(self):
        """고득점 아이디어 알림"""
        with patch('notifications.NotificationConfig') as mock_config:
            mock_config.is_enabled.return_value = True
            mock_config.is_slack_configured.return_value = False
            mock_config.is_email_configured.return_value = False

            with patch('notifications.DiscoveryConfig') as mock_disc_config:
                mock_disc_config.get_min_score.return_value = 70
                mock_disc_config.DEFAULT_HIGH_SCORE_THRESHOLD = 85
                mock_disc_config.get_priority.return_value = 'high'

                notifier = DiscoveryNotifier()
                with patch.object(notifier.service, 'notify') as mock_notify:
                    idea = {
                        'name': 'High Score Idea',
                        'score': 90,
                        'market_score': 88,
                        'revenue_score': 92
                    }
                    notifier.notify_high_score_idea(idea)
                    mock_notify.assert_called_once()

    def test_notify_error(self):
        """오류 알림"""
        with patch('notifications.NotificationConfig') as mock_config:
            mock_config.is_enabled.return_value = True
            mock_config.is_slack_configured.return_value = False
            mock_config.is_email_configured.return_value = False

            with patch('notifications.DiscoveryConfig') as mock_disc_config:
                mock_disc_config.get_min_score.return_value = 70

                notifier = DiscoveryNotifier()
                with patch.object(notifier.service, 'notify') as mock_notify:
                    notifier.notify_error("Test error", {"context": "value"})
                    mock_notify.assert_called_once()

                    # 레벨이 error인지 확인
                    call_args = mock_notify.call_args
                    assert call_args[0][2] == "error"


class TestSingletons:
    """싱글톤 테스트"""

    def test_get_notification_service_singleton(self):
        """NotificationService 싱글톤"""
        # 싱글톤 리셋
        import notifications
        notifications._notification_service = None

        with patch('notifications.NotificationConfig') as mock_config:
            mock_config.is_enabled.return_value = False
            mock_config.is_slack_configured.return_value = False
            mock_config.is_email_configured.return_value = False

            service1 = get_notification_service()
            service2 = get_notification_service()
            assert service1 is service2

    def test_get_discovery_notifier_singleton(self):
        """DiscoveryNotifier 싱글톤"""
        # 싱글톤 리셋
        import notifications
        notifications._discovery_notifier = None

        with patch('notifications.NotificationConfig') as mock_config:
            mock_config.is_enabled.return_value = False
            mock_config.is_slack_configured.return_value = False
            mock_config.is_email_configured.return_value = False

            with patch('notifications.DiscoveryConfig') as mock_disc_config:
                mock_disc_config.get_min_score.return_value = 70

                notifier1 = get_discovery_notifier()
                notifier2 = get_discovery_notifier()
                assert notifier1 is notifier2


class TestConvenienceFunctions:
    """편의 함수 테스트"""

    def test_notify_function(self):
        """notify 편의 함수"""
        with patch('notifications.get_notification_service') as mock_get:
            mock_service = MagicMock()
            mock_get.return_value = mock_service

            notify("Title", "Message", "info", {"key": "value"})
            mock_service.notify.assert_called_once_with(
                "Title", "Message", "info", {"key": "value"}
            )

    def test_notify_discovery_complete_function(self):
        """notify_discovery_complete 편의 함수"""
        with patch('notifications.get_discovery_notifier') as mock_get:
            mock_notifier = MagicMock()
            mock_get.return_value = mock_notifier

            results = {'analyzed': 1, 'saved': 1}
            notify_discovery_complete(results)
            mock_notifier.notify_discovery_complete.assert_called_once_with(results)

    def test_notify_high_score_idea_function(self):
        """notify_high_score_idea 편의 함수"""
        with patch('notifications.get_discovery_notifier') as mock_get:
            mock_notifier = MagicMock()
            mock_get.return_value = mock_notifier

            idea = {'name': 'Test', 'score': 90}
            notify_high_score_idea(idea)
            mock_notifier.notify_high_score_idea.assert_called_once_with(idea)

    def test_notify_error_function(self):
        """notify_error 편의 함수"""
        with patch('notifications.get_discovery_notifier') as mock_get:
            mock_notifier = MagicMock()
            mock_get.return_value = mock_notifier

            notify_error("Error message", {"context": "value"})
            mock_notifier.notify_error.assert_called_once_with(
                "Error message", {"context": "value"}
            )
