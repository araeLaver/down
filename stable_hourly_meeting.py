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

        # 매일 다른 회의 주제 선택 (날짜와 시간 기반)
        meeting_types = [
            ("현실적 사업 발굴 회의", "새로운 수익원 창출"),
            ("일일 전략 회의", "오늘의 우선순위 결정"),
            ("시장 분석 회의", "시장 트렌드 및 기회 분석"),
            ("사업 확장 회의", "기존 사업 확장 전략"),
            ("제품 개발 회의", "신제품 개발 계획"),
            ("파트너십 검토 회의", "협력 기회 탐색"),
            ("고객 피드백 회의", "고객 의견 반영"),
            ("재무 현황 회의", "수익성 분석 및 개선"),
            ("마케팅 전략 회의", "홍보 및 브랜딩"),
            ("기술 혁신 회의", "AI 및 자동화 도입"),
            ("경쟁사 분석 회의", "시장 포지셔닝"),
            ("리스크 관리 회의", "위험 요소 대응")
        ]

        # 날짜와 시간을 조합하여 다양한 회의 선택
        index = (now.day * 24 + now.hour) % len(meeting_types)
        selected_type, theme = meeting_types[index]

        print(f"\n{'='*80}")
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {selected_type} ({theme})")
        print(f"{'='*80}")

        try:
            opportunities = self.business_generator.generate_monthly_opportunities()
            high_viability = self.business_generator.generate_high_viability_themes()
        except Exception as e:
            logging.error(f"Failed to generate opportunities: {e}")
            opportunities = []
            high_viability = []

        # 매일 다른 안건 생성 (회의 유형에 따라 변경)
        all_agendas = {
            "현실적 사업 발굴 회의": [
                "즉시 시작 가능한 사업 아이템 검토",
                "시장 검증된 비즈니스 모델 분석",
                "고수익 앱 개발 테마 분석",
                "최소 투자 고수익 모델 발굴"
            ],
            "일일 전략 회의": [
                "전날 진행사항 검토 및 피드백",
                "오늘의 최우선 과제 3가지 선정",
                "이슈 및 해결방안 즉시 논의",
                "내일 준비 사항 점검"
            ],
            "시장 분석 회의": [
                "경쟁사 동향 분석 (TOP 5)",
                "시장 트렌드 및 소비자 행동 변화",
                "신규 진입 기회 평가",
                "우리 포지셔닝 점검"
            ],
            "사업 확장 회의": [
                "기존 사업 성과 리뷰",
                "확장 가능 영역 탐색",
                "투자 대비 효과 시뮬레이션",
                "리스크 및 대응 방안"
            ],
            "제품 개발 회의": [
                "신제품 아이디어 브레인스토밍",
                "고객 니즈 검증 결과 분석",
                "MVP 개발 우선순위",
                "출시 일정 및 마일스톤"
            ],
            "파트너십 검토 회의": [
                "잠재 협력 파트너 리스트업",
                "상호 이익 모델 설계",
                "계약 조건 및 협상 포인트",
                "리스크 관리 방안"
            ],
            "고객 피드백 회의": [
                "이번 주 고객 의견 종합",
                "불만 사항 및 개선 요청",
                "긍정 피드백 및 강화 방안",
                "즉시 반영 가능한 항목"
            ],
            "재무 현황 회의": [
                "이번 주 매출 및 비용 분석",
                "수익성 개선 포인트 발굴",
                "불필요한 지출 절감 방안",
                "다음 달 예산 계획"
            ],
            "마케팅 전략 회의": [
                "캠페인 성과 리뷰 (ROI 중심)",
                "신규 채널 및 전략 검토",
                "브랜딩 강화 방안",
                "고객 획득 비용 최적화"
            ],
            "기술 혁신 회의": [
                "AI 및 자동화 도입 기회",
                "기술 스택 업그레이드 검토",
                "개발 생산성 향상 방안",
                "보안 및 성능 개선"
            ],
            "경쟁사 분석 회의": [
                "주요 경쟁사 전략 분석",
                "우리만의 차별화 포인트",
                "시장 점유율 확대 방안",
                "선제적 대응 전략"
            ],
            "리스크 관리 회의": [
                "현재 주요 리스크 요소 점검",
                "비상 대응 계획 수립",
                "법률 및 규제 검토",
                "위기 시나리오 및 대응"
            ]
        }

        agendas = all_agendas.get(selected_type, [
            "전날 진행사항 검토",
            "오늘의 우선순위 설정",
            "이슈 및 해결방안 논의",
            "다음 단계 계획 수립"
        ])

        # 회의 유형별 다양한 결정사항 및 실행항목 생성
        if opportunities:
            # 매일 다른 사업 아이템 선택 (랜덤하게)
            import random
            random.seed(now.day * 100 + now.hour)
            selected_opportunities = random.sample(opportunities, min(3, len(opportunities)))
            top_biz = selected_opportunities[0]['business']

            key_decisions = [
                f"{now.strftime('%Y년 %m월 %d일')} 회의 결과",
                f"최우선 검토 사업: {top_biz['name']} ({selected_opportunities[0]['priority']} 우선순위)",
                f"사업 카테고리: {selected_opportunities[0]['type']}",
                f"목표 초기 투자금: {top_biz.get('startup_cost', '미정')}",
                f"예상 월 수익: {top_biz.get('monthly_revenue', top_biz.get('revenue_potential', '미정'))}",
                f"추가 검토 사업 2가지 선정 완료"
            ]

            action_items = [
                f"【최우선】{top_biz['name']} 상세 시장 조사 (7일 내)",
                f"경쟁업체 TOP 5 분석 및 차별화 전략 수립 (5일 내)",
                f"최소 실행 가능 제품(MVP) 개발 계획 작성 (3일 내)",
                f"타겟 고객 50명 인터뷰 및 니즈 검증 (10일 내)",
                f"수익 모델 시뮬레이션 및 손익분기점 계산 (7일 내)",
                f"초기 자금 조달 방안 검토 (5일 내)",
                f"팀 구성 및 역할 분담 계획 (3일 내)",
                f"다음 회의일: {(now + timedelta(days=1)).strftime('%Y년 %m월 %d일 %H시')}"
            ]

            print(f"\n[TOP] 최우선 사업: {top_biz['name']}")
            print(f"   초기비용: {top_biz.get('startup_cost', 'N/A')}")
            print(f"   월수익: {top_biz.get('monthly_revenue', top_biz.get('revenue_potential', 'N/A'))}")
            print(f"\n[STATS] 총 발굴 사업 기회: {len(opportunities)}개")
            print(f"[HIGH] 고수익 테마: {len(high_viability)}개")
            print(f"[SELECTED] 오늘 선정된 검토 대상: {len(selected_opportunities)}개")
        else:
            key_decisions = [
                f"{now.strftime('%Y년 %m월 %d일')} {selected_type} 결과",
                "기존 사업 성과 분석 우선",
                "신규 투자 검토 보류",
                "내부 프로세스 개선 집중"
            ]
            action_items = [
                f"현재 진행 중인 프로젝트 상태 점검 ({now.strftime('%m월 %d일')})",
                "팀별 주간 보고서 제출 요청 (2일 내)",
                "다음 분기 계획 초안 작성 (7일 내)"
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