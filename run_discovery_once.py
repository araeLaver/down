"""한 번만 사업 발굴 실행 (테스트 데이터 생성용)"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from continuous_business_discovery import ContinuousBusinessDiscovery
from datetime import datetime

print("=" * 80)
print("🔍 테스트 사업 발굴 실행 중...")
print("=" * 80)

discovery = ContinuousBusinessDiscovery()

try:
    results = discovery.run_hourly_discovery()
    
    print(f"\n✅ 완료!")
    print(f"   분석: {results['analyzed']}개")
    print(f"   저장: {results['saved']}개")
    print(f"\n💡 이제 /business 페이지에서 확인하세요!")
    
except Exception as e:
    print(f"\n❌ 에러: {e}")

finally:
    discovery.close()
