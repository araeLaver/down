"""
독립 실행형 비즈니스 발굴 스크립트
Koyeb Cron Job 또는 외부 스케줄러에서 호출
"""
import sys
import os

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv()

# 인코딩 설정
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from continuous_business_discovery import ContinuousBusinessDiscovery
from datetime import datetime

def main():
    """단일 발굴 실행"""
    print(f"\n{'='*80}")
    print(f"[RUN] Business Discovery - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")

    try:
        discovery = ContinuousBusinessDiscovery()
        results = discovery.run_hourly_discovery()

        print(f"\n{'='*80}")
        print(f"[RESULTS] Completed")
        print(f"{'='*80}")
        print(f"Analyzed: {results.get('analyzed', 0)}")
        print(f"Saved (60+): {results.get('saved', 0)}")
        print(f"Rejected (<60): {results.get('rejected', 0)}")

        if results['saved'] > 0:
            print(f"\n[MEETING] Generating discovery meeting...")
            discovery.generate_discovery_meeting(results)

        print(f"\n[DONE] Discovery completed successfully!\n")
        return 0

    except Exception as e:
        print(f"\n[ERROR] Discovery failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
