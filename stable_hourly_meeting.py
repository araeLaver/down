#!/usr/bin/env python3
"""
안정적인 매시간 사업 발굴 회의 생성 시스템
DB 연결 문제 자동 복구
"""

import time
import json
import os
import sys
from datetime import datetime, timedelta
from database_setup import Session, BusinessMeeting
from realistic_business_generator import RealisticBusinessGenerator
import logging

if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# 로깅 설정
logging.basicConfig(
    filename='meeting_generator.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

class StableHourlyMeeting:
    def __init__(self):
        self.business_generator = RealisticBusinessGenerator()
        self.employees = [
            '알렉스 김', '에밀리 박', '마이클 이', '소피아 최',
            '다니엘 정', '올리비아 한', '라이언 조', '그레이스 윤',
            '벤자민 강', '사만사 임', '조슈아 서', '나탈리 류'
        ]
        self.session = None
        self.reconnect_db()

    def reconnect_db(self):
        """DB 재연결"""
        try:
            if self.session:
                self.session.close()
        except:
            pass

        self.session = Session()
        logging.info("Database connected successfully")

    def conduct_hourly_meeting(self):
        """매시간 사업 발굴 회의 진행"""
        now = datetime.now()
        logging.info(f"Starting meeting at {now}")

        meeting_types = [
            "현실적 사업 발굴 회의",
            "일일 전략 회의",
            "시장 분석 회의",
            "사업 확장 회의",
            "제품 개발 회의",
            "파트너십 검토 회의"
        ]

        selected_type = meeting_types[now.hour % len(meeting_types)]

        print(f"\n{'='*80}")
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {selected_type} 시작")
        print(f"{'='*80}")

        try:
            opportunities = self.business_generator.generate_monthly_opportunities()
            high_viability = self.business_generator.generate_high_viability_themes()
        except Exception as e:
            logging.error(f"Failed to generate opportunities: {e}")
            opportunities = []
            high_viability = []

        agendas = [
            "전날 진행사항 검토",
            "오늘의 우선순위 설정",
            "이슈 및 해결방안 논의",
            "즉시 시작 가능한 사업 아이템 검토",
            "계절별 기회 사업 평가",
            "기술 활용 저비용 창업 방안",
            "시장 검증된 비즈니스 모델 분석"
        ]

        if opportunities:
            top_biz = opportunities[0]['business']

            key_decisions = [
                f"{top_biz['name']} 우선 검토 결정 (우선순위: {opportunities[0]['priority']})",
                f"사업 유형: {opportunities[0]['type']}",
                f"목표 초기 투자금: {top_biz.get('startup_cost', '미정')}",
                f"예상 월 수익: {top_biz.get('monthly_revenue', top_biz.get('revenue_potential', '미정'))}"
            ]

            action_items = [
                f"{top_biz['name']} 상세 시장 조사 실시",
                "경쟁업체 TOP 5 분석 및 차별화 포인트 도출",
                "최소 실행 가능 제품(MVP) 개발 계획 수립",
                "타겟 고객 100명 인터뷰 및 니즈 검증",
                "수익 모델 시뮬레이션 및 손익분기점 계산"
            ]

            print(f"\n[TOP] 최우선 사업: {top_biz['name']}")
            print(f"   초기비용: {top_biz.get('startup_cost', 'N/A')}")
            print(f"   월수익: {top_biz.get('monthly_revenue', top_biz.get('revenue_potential', 'N/A'))}")
            print(f"\n[STATS] 총 발굴 사업 기회: {len(opportunities)}개")
            print(f"[HIGH] 고수익 테마: {len(high_viability)}개")
        else:
            key_decisions = [
                "AI 자동화 컨설팅 우선 검토",
                "목표 초기 투자금: 50만원",
                "예상 월 수익: 200-500만원"
            ]
            action_items = [
                "AI 자동화 컨설팅 시장 조사",
                "경쟁사 분석",
                "MVP 개발 계획"
            ]

        meeting = BusinessMeeting(
            meeting_type=selected_type,
            title=f"Qhyx Inc. {selected_type} - {now.strftime('%Y-%m-%d')}",
            agenda=json.dumps(agendas, ensure_ascii=False),
            participants=json.dumps(self.employees, ensure_ascii=False),
            key_decisions=key_decisions,
            action_items=action_items,
            status='completed',
            meeting_notes=json.dumps({
                'total_opportunities': len(opportunities),
                'high_viability_count': len(high_viability),
                'meeting_duration': '45 minutes'
            }, ensure_ascii=False)
        )

        # DB 저장 시도 (재시도 로직 포함)
        for attempt in range(3):
            try:
                self.session.add(meeting)
                self.session.commit()
                print(f"\n[OK] 회의 완료 - DB 저장 완료")
                logging.info(f"Meeting saved successfully: {meeting.title}")
                break
            except Exception as e:
                logging.error(f"DB save attempt {attempt+1} failed: {e}")
                print(f"\n[ERROR] DB 저장 실패 (시도 {attempt+1}/3): {e}")

                try:
                    self.session.rollback()
                except:
                    pass

                self.reconnect_db()

                if attempt == 2:
                    print("[FINAL ERROR] DB 저장 최종 실패")
                    logging.error("Failed to save meeting after 3 attempts")

        print(f"   결정사항: {len(key_decisions)}개")
        print(f"   실행항목: {len(action_items)}개")
        print(f"{'='*80}\n")

    def run_hourly(self):
        """매시간 정각에 실행"""
        print("[START] 안정적인 매시간 사업 발굴 회의 시스템")
        print("[TIME] 매시간 정각에 자동으로 회의 생성")
        print("[LOG] meeting_generator.log 파일에 로그 기록")
        print("[STOP] Ctrl+C로 종료\n")

        logging.info("System started")

        last_hour = -1
        consecutive_errors = 0

        while True:
            try:
                now = datetime.now()
                current_hour = now.hour
                current_minute = now.minute

                # 매시간 00분에 실행
                if current_minute == 0 and current_hour != last_hour:
                    self.conduct_hourly_meeting()
                    last_hour = current_hour
                    consecutive_errors = 0
                    time.sleep(60)
                else:
                    # 30초마다 체크
                    time.sleep(30)

            except KeyboardInterrupt:
                print("\n\n시스템 종료")
                logging.info("System stopped by user")
                break
            except Exception as e:
                consecutive_errors += 1
                print(f"[ERROR] 시스템 오류: {e}")
                logging.error(f"System error: {e}")

                if consecutive_errors > 10:
                    print("[CRITICAL] 연속 오류 10회 초과 - 재시작 필요")
                    logging.critical("Too many consecutive errors - restart needed")
                    time.sleep(300)  # 5분 대기
                else:
                    time.sleep(60)

if __name__ == "__main__":
    system = StableHourlyMeeting()

    # 시작하자마자 한번 실행
    try:
        system.conduct_hourly_meeting()
    except Exception as e:
        print(f"Initial meeting failed: {e}")
        logging.error(f"Initial meeting failed: {e}")

    # 매시간 실행
    system.run_hourly()