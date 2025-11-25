#!/usr/bin/env python3
"""
시간마다 비즈니스 회의를 자동 생성하고 결과를 출력하는 데몬
"""

import os
import sys
import time
from datetime import datetime, timedelta
from realistic_business_generator import RealisticBusinessGenerator
import threading

# Windows 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

class HourlyMeetingDaemon:
    def __init__(self):
        self.generator = RealisticBusinessGenerator()
        self.meeting_count = 0
        self.running = True

    def generate_meeting_now(self):
        """즉시 회의 생성하고 결과 출력"""
        self.meeting_count += 1
        timestamp = datetime.now()

        print("\n" + "="*80)
        print(f"비즈니스 회의 #{self.meeting_count} - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)

        # 회의 데이터 생성
        meeting_data = self.generator.generate_business_meeting_agenda()

        # 콘솔에 요약 출력
        print("\n회의 안건:")
        for i, agenda in enumerate(meeting_data['agenda'], 1):
            print(f"  {i}. {agenda}")

        print("\n주요 결정사항:")
        for i, decision in enumerate(meeting_data['key_decisions'][:3], 1):  # 상위 3개만
            print(f"  {i}. {decision}")

        print("\n즉시 실행 항목:")
        for i, action in enumerate(meeting_data['action_items'][:3], 1):  # 상위 3개만
            print(f"  {i}. {action}")

        # 사업 기회 요약
        opportunities = meeting_data['opportunities']
        print(f"\n사업 기회 총 {len(opportunities)}개 발굴:")

        # 우선순위별 분류
        high_priority = [o for o in opportunities if o['priority'] == '매우 높음']
        medium_priority = [o for o in opportunities if o['priority'] == '높음']

        print("\n최우선 사업 기회 (매우 높음):")
        for opp in high_priority[:5]:  # 상위 5개
            business = opp['business']
            name = business.get('name', 'N/A')
            cost = business.get('startup_cost', business.get('초기 비용', 'N/A'))
            revenue = business.get('monthly_revenue', business.get('revenue_potential', 'N/A'))
            print(f"  - {name}")
            print(f"    초기비용: {cost}")
            print(f"    예상수익: {revenue}")

        print(f"\n우선순위 분포:")
        print(f"  - 매우 높음: {len(high_priority)}개")
        print(f"  - 높음: {len([o for o in opportunities if o['priority'] == '높음'])}개")
        print(f"  - 보통: {len([o for o in opportunities if o['priority'] == '보통'])}개")

        # 파일로 저장
        filename = f"meeting_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"=== 비즈니스 회의 #{self.meeting_count} ===\n")
            f.write(f"생성 시간: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"회의 유형: {meeting_data['meeting_type']}\n\n")

            f.write("[LIST] 회의 안건:\n")
            for agenda in meeting_data['agenda']:
                f.write(f"  • {agenda}\n")

            f.write("\n[IDEA] 결정사항:\n")
            for decision in meeting_data['key_decisions']:
                f.write(f"  • {decision}\n")

            f.write("\n⚡ 실행 항목:\n")
            for action in meeting_data['action_items']:
                f.write(f"  • {action}\n")

            f.write(f"\n\n=== 사업 기회 {len(opportunities)}개 ===\n")
            for i, opp in enumerate(opportunities, 1):
                f.write(f"\n[{i}] {opp['type']} - {opp['priority']}\n")
                business = opp['business']
                f.write(f"  사업명: {business.get('name', 'N/A')}\n")
                if 'description' in business:
                    f.write(f"  설명: {business['description']}\n")
                if 'startup_cost' in business:
                    f.write(f"  초기비용: {business['startup_cost']}\n")
                if 'monthly_revenue' in business:
                    f.write(f"  월수익: {business['monthly_revenue']}\n")
                elif 'revenue_potential' in business:
                    f.write(f"  수익잠재력: {business['revenue_potential']}\n")

        print(f"\n파일 저장: {filename}")
        print(f"다음 회의: {(timestamp + timedelta(hours=1)).strftime('%H:%M:%S')}")
        print("="*80)

        return filename

    def run_daemon(self):
        """데몬 모드로 실행 - 매시간 자동 생성"""
        print("\n시간별 비즈니스 회의 생성 데몬 시작")
        print("매시간 정각에 회의를 자동 생성합니다.")
        print("종료하려면 Ctrl+C를 누르세요.\n")

        # 첫 회의 즉시 생성
        self.generate_meeting_now()

        while self.running:
            try:
                # 다음 정시까지 대기
                now = datetime.now()
                next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                wait_seconds = (next_hour - now).total_seconds()

                print(f"\n⏳ 다음 회의까지 {int(wait_seconds//60)}분 {int(wait_seconds%60)}초 대기...")

                # 대기 (10초마다 체크)
                while wait_seconds > 0 and self.running:
                    time.sleep(min(10, wait_seconds))
                    wait_seconds -= 10

                if self.running:
                    self.generate_meeting_now()

            except KeyboardInterrupt:
                self.running = False
                print("\n\n[OK] 회의 생성 데몬 종료")
                print(f"총 {self.meeting_count}개 회의 생성 완료")
                break
            except Exception as e:
                print(f"\n[X] 오류 발생: {e}")
                time.sleep(60)  # 오류 시 1분 대기

def main():
    daemon = HourlyMeetingDaemon()

    # 명령줄 인자 확인
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # 한 번만 실행
        daemon.generate_meeting_now()
    else:
        # 데몬 모드 실행
        daemon.run_daemon()

if __name__ == "__main__":
    main()