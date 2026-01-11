#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""비즈니스 발굴 상태 확인"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from app import Session
from business_discovery_history import BusinessDiscoveryHistory
from datetime import datetime, timedelta

session = Session()

# 전체 통계
total = session.query(BusinessDiscoveryHistory).count()
print(f"전체 발굴된 비즈니스: {total}개\n")

# 최근 24시간
one_day_ago = datetime.utcnow() - timedelta(days=1)
recent_24h = session.query(BusinessDiscoveryHistory).filter(
    BusinessDiscoveryHistory.discovered_at >= one_day_ago
).count()
print(f"최근 24시간: {recent_24h}개")

# 최근 1시간
one_hour_ago = datetime.utcnow() - timedelta(hours=1)
recent_1h = session.query(BusinessDiscoveryHistory).filter(
    BusinessDiscoveryHistory.discovered_at >= one_hour_ago
).count()
print(f"최근 1시간: {recent_1h}개\n")

# 최신 5개
print("최신 5개:")
latest = session.query(BusinessDiscoveryHistory).order_by(
    BusinessDiscoveryHistory.discovered_at.desc()
).limit(5).all()

for i, b in enumerate(latest, 1):
    print(f"{i}. {b.business_name} ({b.total_score}점) - {b.discovered_at}")

session.close()
