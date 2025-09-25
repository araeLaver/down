#!/usr/bin/env python3
"""
간단한 시간별 회의 생성기
"""

import os
import sys
import time
from datetime import datetime, timedelta
from realistic_business_generator import RealisticBusinessGenerator

# Windows 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def generate_meeting():
    generator = RealisticBusinessGenerator()
    meeting_data = generator.generate_business_meeting_agenda()
    timestamp = datetime.now()

    print("\n" + "="*80)
    print(f"비즈니스 회의 - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    # 사업 기회 요약
    opportunities = meeting_data['opportunities']
    high_priority = [o for o in opportunities if o['priority'] == '매우 높음']

    print(f"\n사업 기회 총 {len(opportunities)}개 발굴")
    print(f"최우선 기회: {len(high_priority)}개")

    print("\n최우선 사업 기회:")
    for i, opp in enumerate(high_priority[:5], 1):
        business = opp['business']
        name = business.get('name', 'N/A')
        cost = business.get('startup_cost', business.get('초기 비용', 'N/A'))
        revenue = business.get('monthly_revenue', business.get('revenue_potential', 'N/A'))
        print(f"  {i}. {name}")
        print(f"     초기비용: {cost}")
        print(f"     예상수익: {revenue}")

    # 주요 결정사항
    print(f"\n주요 결정사항 {len(meeting_data['key_decisions'])}개:")
    for i, decision in enumerate(meeting_data['key_decisions'][:3], 1):
        print(f"  {i}. {decision}")

    # 실행 항목
    print(f"\n실행 항목 {len(meeting_data['action_items'])}개:")
    for i, action in enumerate(meeting_data['action_items'][:3], 1):
        print(f"  {i}. {action}")

    # 파일 저장
    filename = f"meeting_{timestamp.strftime('%Y%m%d_%H%M')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"=== 비즈니스 회의 ===\n")
        f.write(f"생성: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write(f"사업 기회: {len(opportunities)}개\n")
        f.write("="*50 + "\n")

        for i, opp in enumerate(opportunities, 1):
            f.write(f"\n{i}. {opp['type']} ({opp['priority']})\n")
            business = opp['business']
            f.write(f"   사업명: {business.get('name', 'N/A')}\n")
            if 'startup_cost' in business:
                f.write(f"   초기비용: {business['startup_cost']}\n")
            if 'monthly_revenue' in business:
                f.write(f"   월수익: {business['monthly_revenue']}\n")
            elif 'revenue_potential' in business:
                f.write(f"   수익: {business['revenue_potential']}\n")

        f.write(f"\n\n결정사항 {len(meeting_data['key_decisions'])}개:\n")
        for decision in meeting_data['key_decisions']:
            f.write(f"- {decision}\n")

        f.write(f"\n실행항목 {len(meeting_data['action_items'])}개:\n")
        for action in meeting_data['action_items']:
            f.write(f"- {action}\n")

    print(f"\n파일 저장: {filename}")
    print("="*80)
    return filename

def run_hourly():
    """시간마다 실행"""
    print("시간별 회의 생성기 시작")
    print("매시간 정각에 회의 생성")
    print("Ctrl+C로 종료\n")

    count = 0

    # 첫 회의 바로 생성
    generate_meeting()
    count += 1

    while True:
        try:
            # 다음 정시까지 대기
            now = datetime.now()
            next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            wait_seconds = (next_hour - now).total_seconds()

            print(f"\n다음 회의까지 {int(wait_seconds//60)}분 대기...")
            time.sleep(wait_seconds)

            generate_meeting()
            count += 1

        except KeyboardInterrupt:
            print(f"\n\n종료. 총 {count}개 회의 생성")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        generate_meeting()
    else:
        run_hourly()