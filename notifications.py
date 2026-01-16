"""
Qhyx Inc. 알림 시스템
- Slack 웹훅 알림
- 이메일 알림
- 사업 발굴 결과 알림
"""

import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List, Dict, Any
from datetime import datetime

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from config import NotificationConfig, DiscoveryConfig


logger = logging.getLogger(__name__)


class NotificationService:
    """통합 알림 서비스"""

    def __init__(self):
        self.enabled = NotificationConfig.is_enabled()
        self.slack_configured = NotificationConfig.is_slack_configured()
        self.email_configured = NotificationConfig.is_email_configured()

    def notify(self, title: str, message: str, level: str = "info", data: Optional[Dict] = None):
        """모든 설정된 채널로 알림 전송"""
        if not self.enabled:
            logger.debug(f"Notifications disabled. Skipping: {title}")
            return

        results = {}

        if self.slack_configured:
            results['slack'] = self.send_slack(title, message, level, data)

        if self.email_configured:
            results['email'] = self.send_email(title, message, data)

        return results

    def send_slack(self, title: str, message: str, level: str = "info", data: Optional[Dict] = None) -> bool:
        """Slack 웹훅으로 알림 전송"""
        if not REQUESTS_AVAILABLE:
            logger.warning("requests 모듈이 없어 Slack 알림을 보낼 수 없습니다.")
            return False

        webhook_url = NotificationConfig.get_slack_webhook()
        if not webhook_url:
            return False

        # 레벨에 따른 색상
        color_map = {
            "info": "#36a64f",      # 녹색
            "warning": "#ffcc00",   # 노란색
            "error": "#ff0000",     # 빨간색
            "success": "#00ff00",   # 밝은 녹색
        }

        # Slack 메시지 포맷
        payload = {
            "attachments": [
                {
                    "color": color_map.get(level, "#36a64f"),
                    "title": title,
                    "text": message,
                    "footer": "Qhyx Inc. Notification System",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }

        # 추가 데이터가 있으면 필드로 추가
        if data:
            fields = []
            for key, value in data.items():
                fields.append({
                    "title": key,
                    "value": str(value),
                    "short": True
                })
            payload["attachments"][0]["fields"] = fields

        try:
            response = requests.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            if response.status_code == 200:
                logger.info(f"Slack 알림 전송 성공: {title}")
                return True
            else:
                logger.error(f"Slack 알림 실패: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Slack 알림 오류: {e}")
            return False

    def send_email(self, subject: str, body: str, data: Optional[Dict] = None) -> bool:
        """이메일 알림 전송"""
        config = NotificationConfig.get_email_config()

        if not all([config['smtp_host'], config['username'], config['password']]):
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = config['from_email'] or config['username']
            msg['To'] = config['username']  # 자신에게 발송
            msg['Subject'] = f"[Qhyx] {subject}"

            # HTML 본문 생성
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #333;">{subject}</h2>
                <p>{body}</p>
            """

            if data:
                html_body += """
                <table style="border-collapse: collapse; margin-top: 20px;">
                    <tr style="background-color: #f2f2f2;">
                        <th style="padding: 10px; border: 1px solid #ddd;">항목</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">값</th>
                    </tr>
                """
                for key, value in data.items():
                    html_body += f"""
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;">{key}</td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{value}</td>
                    </tr>
                    """
                html_body += "</table>"

            html_body += """
                <hr style="margin-top: 30px;">
                <p style="color: #666; font-size: 12px;">
                    Qhyx Inc. Notification System<br>
                    이 메일은 자동으로 발송되었습니다.
                </p>
            </body>
            </html>
            """

            msg.attach(MIMEText(html_body, 'html'))

            with smtplib.SMTP(config['smtp_host'], config['smtp_port']) as server:
                server.starttls()
                server.login(config['username'], config['password'])
                server.send_message(msg)

            logger.info(f"이메일 알림 전송 성공: {subject}")
            return True

        except Exception as e:
            logger.error(f"이메일 알림 오류: {e}")
            return False


class DiscoveryNotifier:
    """사업 발굴 전용 알림기"""

    def __init__(self):
        self.service = NotificationService()
        self.min_score = DiscoveryConfig.get_min_score()

    def notify_discovery_complete(self, results: Dict[str, Any]):
        """발굴 완료 알림"""
        analyzed = results.get('analyzed', 0)
        saved = results.get('saved', 0)
        batch_id = results.get('batch_id', 'unknown')

        if saved == 0:
            level = "warning"
            title = "사업 발굴 완료 - 저장된 아이디어 없음"
        else:
            level = "success"
            title = f"사업 발굴 완료 - {saved}개 저장"

        message = f"배치 ID: {batch_id}\n분석: {analyzed}개, 저장: {saved}개"

        data = {
            "분석된 아이디어": analyzed,
            "저장된 아이디어": saved,
            "최소 점수 기준": f"{self.min_score}점",
            "배치 ID": batch_id
        }

        # 저장된 아이디어 상세 정보 추가
        saved_ideas = [r for r in results.get('results', []) if r.get('saved')]
        if saved_ideas:
            ideas_summary = []
            for idea in saved_ideas[:5]:  # 최대 5개만 표시
                ideas_summary.append(f"- {idea.get('name', 'N/A')} ({idea.get('score', 0):.1f}점)")
            data["저장된 아이디어 목록"] = "\n".join(ideas_summary)

        return self.service.notify(title, message, level, data)

    def notify_high_score_idea(self, idea: Dict[str, Any]):
        """고득점 아이디어 알림"""
        name = idea.get('name', 'Unknown')
        score = idea.get('score', 0)
        market_score = idea.get('market_score', 0)
        revenue_score = idea.get('revenue_score', 0)

        if score >= DiscoveryConfig.DEFAULT_HIGH_SCORE_THRESHOLD:
            title = f"고득점 아이디어 발견: {name}"
            message = f"점수: {score:.1f}/100 (시장성: {market_score:.1f}, 수익성: {revenue_score:.1f})"

            data = {
                "사업명": name,
                "종합 점수": f"{score:.1f}/100",
                "시장성 점수": f"{market_score:.1f}/100",
                "수익성 점수": f"{revenue_score:.1f}/100",
                "우선순위": DiscoveryConfig.get_priority(score)
            }

            return self.service.notify(title, message, "success", data)

    def notify_error(self, error: str, context: Optional[Dict] = None):
        """오류 알림"""
        title = "사업 발굴 시스템 오류"
        message = f"오류 발생: {error}"

        data = context or {}
        data["오류 내용"] = error
        data["발생 시각"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return self.service.notify(title, message, "error", data)


# 싱글톤 인스턴스
_notification_service: Optional[NotificationService] = None
_discovery_notifier: Optional[DiscoveryNotifier] = None


def get_notification_service() -> NotificationService:
    """알림 서비스 싱글톤 반환"""
    global _notification_service
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service


def get_discovery_notifier() -> DiscoveryNotifier:
    """발굴 알림기 싱글톤 반환"""
    global _discovery_notifier
    if _discovery_notifier is None:
        _discovery_notifier = DiscoveryNotifier()
    return _discovery_notifier


# 편의 함수
def notify(title: str, message: str, level: str = "info", data: Optional[Dict] = None):
    """간편 알림 함수"""
    return get_notification_service().notify(title, message, level, data)


def notify_discovery_complete(results: Dict[str, Any]):
    """발굴 완료 알림 편의 함수"""
    return get_discovery_notifier().notify_discovery_complete(results)


def notify_high_score_idea(idea: Dict[str, Any]):
    """고득점 아이디어 알림 편의 함수"""
    return get_discovery_notifier().notify_high_score_idea(idea)


def notify_error(error: str, context: Optional[Dict] = None):
    """오류 알림 편의 함수"""
    return get_discovery_notifier().notify_error(error, context)
