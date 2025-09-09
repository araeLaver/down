"""
Qhyx Inc. 일일 비즈니스 데몬
매일 정해진 시간에 자동으로 회의를 진행하고 기록하는 시스템
"""

import schedule
import time
from datetime import datetime
from autonomous_business_system import DailyBusinessOperations
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('qhyx_business.log'),
        logging.StreamHandler()
    ]
)

class QhyxDailyDaemon:
    def __init__(self):
        self.daily_ops = DailyBusinessOperations()
        logging.info("Qhyx Inc. 일일 비즈니스 데몬 초기화 완료")
    
    def morning_meeting_job(self):
        """아침 9시 정기 회의"""
        try:
            logging.info("아침 전략 회의 시작")
            meeting_id = self.daily_ops.conduct_daily_morning_meeting()
            logging.info(f"아침 회의 완료 (Meeting ID: {meeting_id})")
        except Exception as e:
            logging.error(f"아침 회의 오류: {e}")
    
    def afternoon_update_job(self):
        """오후 2시 지표 업데이트"""
        try:
            logging.info("오후 지표 업데이트 시작")
            self.daily_ops.update_company_metrics()
            logging.info("지표 업데이트 완료")
        except Exception as e:
            logging.error(f"지표 업데이트 오류: {e}")
    
    def evening_review_job(self):
        """저녁 6시 일일 리뷰"""
        try:
            logging.info("저녁 리뷰 및 계획 수립 시작")
            self.daily_ops.evening_review_and_planning()
            logging.info("저녁 리뷰 완료")
        except Exception as e:
            logging.error(f"저녁 리뷰 오류: {e}")
    
    def hourly_metrics_job(self):
        """매시 정각 간단 지표 업데이트"""
        try:
            self.daily_ops.update_company_metrics()
            current_time = datetime.now().strftime("%H:%M")
            logging.info(f"[{current_time}] 시간별 지표 업데이트 완료")
        except Exception as e:
            logging.error(f"시간별 업데이트 오류: {e}")
    
    def start_daemon(self):
        """데몬 시작"""
        # 스케줄 설정
        schedule.every().day.at("09:00").do(self.morning_meeting_job)
        schedule.every().day.at("14:00").do(self.afternoon_update_job)
        schedule.every().day.at("18:00").do(self.evening_review_job)
        schedule.every().hour.at(":00").do(self.hourly_metrics_job)
        
        logging.info("스케줄 설정 완료:")
        logging.info("  - 09:00: 일일 전략 회의")
        logging.info("  - 14:00: 오후 지표 업데이트")
        logging.info("  - 18:00: 저녁 리뷰")
        logging.info("  - 매시 정각: 지표 업데이트")
        
        # 즉시 첫 회의 진행
        logging.info("첫 회의를 즉시 진행합니다...")
        self.morning_meeting_job()
        
        logging.info("24/7 자동 운영을 시작합니다. 잠들어도 회사는 계속 성장합니다!")
        
        # 무한 루프로 스케줄 실행
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크

if __name__ == "__main__":
    daemon = QhyxDailyDaemon()
    daemon.start_daemon()