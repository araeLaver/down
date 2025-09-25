#!/usr/bin/env python3
"""
Quick Business Meeting Generator
Generates a single business meeting immediately and saves it to a file
"""

import os
import sys
from datetime import datetime
from realistic_business_generator import RealisticBusinessGenerator

# Set encoding for Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def generate_meeting():
    generator = RealisticBusinessGenerator()
    meeting_data = generator.generate_business_meeting_agenda()

    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"business_meeting_{timestamp}.txt"

    # Write meeting to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write(f"비즈니스 회의: {meeting_data['meeting_type']}\n")
        f.write(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")

        f.write("회의 안건:\n")
        f.write("-"*40 + "\n")
        for i, agenda in enumerate(meeting_data['agenda'], 1):
            f.write(f"{i}. {agenda}\n")
        f.write("\n")

        f.write("주요 결정사항:\n")
        f.write("-"*40 + "\n")
        for i, decision in enumerate(meeting_data['key_decisions'], 1):
            f.write(f"{i}. {decision}\n")
        f.write("\n")

        f.write("실행 항목:\n")
        f.write("-"*40 + "\n")
        for i, action in enumerate(meeting_data['action_items'], 1):
            f.write(f"{i}. {action}\n")
        f.write("\n")

        f.write("="*80 + "\n")
        f.write(f"생성된 사업 기회: {len(meeting_data['opportunities'])}개\n")
        f.write("="*80 + "\n\n")

        # Write all business opportunities
        for i, opp in enumerate(meeting_data['opportunities'], 1):
            f.write(f"\n--- 사업 기회 #{i} ---\n")
            f.write(f"유형: {opp['type']}\n")
            f.write(f"카테고리: {opp.get('category', 'N/A')}\n")

            business = opp['business']
            f.write(f"사업명: {business.get('name', 'N/A')}\n")

            if 'description' in business:
                f.write(f"설명: {business['description']}\n")

            if 'startup_cost' in business:
                f.write(f"초기 비용: {business['startup_cost']}\n")

            if 'monthly_revenue' in business:
                f.write(f"월 예상 수익: {business['monthly_revenue']}\n")
            elif 'revenue_potential' in business:
                f.write(f"수익 잠재력: {business['revenue_potential']}\n")

            if 'timeline' in business:
                f.write(f"시작 시점: {business['timeline']}\n")
            elif 'development_time' in business:
                f.write(f"개발 기간: {business['development_time']}\n")

            if 'difficulty' in business:
                f.write(f"난이도: {business['difficulty']}\n")

            if 'viability' in business:
                f.write(f"사업성: {business['viability']}\n")

            f.write(f"우선순위: {opp['priority']}\n")

    print(f"회의 파일 생성 완료: {filename}")
    print(f"총 사업 기회: {len(meeting_data['opportunities'])}개")
    print(f"주요 결정사항: {len(meeting_data['key_decisions'])}개")
    print(f"실행 항목: {len(meeting_data['action_items'])}개")

    # Priority distribution
    priority_counts = {}
    for opp in meeting_data['opportunities']:
        priority = opp['priority']
        priority_counts[priority] = priority_counts.get(priority, 0) + 1

    print("\n우선순위 분포:")
    for priority, count in sorted(priority_counts.items()):
        print(f"  {priority}: {count}개")

    return filename

if __name__ == "__main__":
    print("빠른 비즈니스 회의 생성기")
    print("-" * 40)
    generate_meeting()