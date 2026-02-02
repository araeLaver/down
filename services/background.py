import time
import logging
from datetime import datetime
from threading import Thread

from config import DiscoveryConfig


def background_sync_parser():
    """백그라운드에서 주기적으로 sync.log 파싱"""
    from services.git_utils import parse_sync_log
    while True:
        try:
            parse_sync_log()
        except Exception as e:
            print(f"Background parser error: {e}")
        time.sleep(30)


def background_meeting_generator():
    """백그라운드에서 매시간 회의 생성"""
    from stable_hourly_meeting import StableHourlyMeeting

    logging.info("[BACKGROUND] Starting hourly meeting generator...")
    print("[BACKGROUND] Starting hourly meeting generator...")

    system = StableHourlyMeeting()
    last_hour = -1

    while True:
        try:
            now = datetime.now()
            current_hour = now.hour
            current_minute = now.minute

            if current_minute == 0 and current_hour != last_hour:
                logging.info(f"[MEETING] Generating meeting at {now}")
                print(f"[MEETING] Generating meeting at {now}")
                system.conduct_hourly_meeting()
                last_hour = current_hour
                time.sleep(60)
            else:
                time.sleep(30)
        except Exception as e:
            logging.error(f"Meeting generator error: {e}")
            print(f"Meeting generator error: {e}")
            time.sleep(60)


def background_business_discovery():
    """백그라운드에서 8시간마다 사업 발굴 (설정 기반 스케줄)"""
    from continuous_business_discovery import ContinuousBusinessDiscovery
    from services.db import engine

    scheduled_hours = DiscoveryConfig.get_schedule_hours()

    logging.info(f"[BACKGROUND] Starting business discovery (schedule: {scheduled_hours})...")
    print(f"[BACKGROUND] Starting business discovery (schedule: {scheduled_hours})...")

    discovery = None
    last_run_hour = -1
    error_count = 0

    while True:
        try:
            now = datetime.now()
            current_hour = now.hour
            current_minute = now.minute

            if current_hour in scheduled_hours and current_minute <= 2 and current_hour != last_run_hour:
                logging.info(f"[DISCOVERY] Running scheduled discovery at {now}")
                print(f"\n" + "="*80)
                print(f"[DISCOVERY] Running discovery at {now.strftime('%Y-%m-%d %H:%M:%S')}")
                print("="*80)

                try:
                    discovery = ContinuousBusinessDiscovery()
                    results = discovery.run_hourly_discovery()

                    logging.info(f"[DISCOVERY] Results: analyzed={results.get('analyzed', 0)}, saved={results.get('saved', 0)}")
                    print(f"\n[RESULTS] Analyzed: {results.get('analyzed', 0)}, Saved: {results.get('saved', 0)}")

                    if results['saved'] > 0:
                        discovery.generate_discovery_meeting(results)

                    error_count = 0
                except Exception as inner_e:
                    print(f"[DISCOVERY] Inner error: {inner_e}")
                    error_count += 1
                    try:
                        engine.dispose()
                    except:
                        pass

                last_run_hour = current_hour

                next_hours = [h for h in scheduled_hours if h > current_hour]
                next_hour = next_hours[0] if next_hours else scheduled_hours[0]
                print(f"[NEXT] Next discovery at {next_hour:02d}:00")
                print("="*80 + "\n")

                time.sleep(180)
            else:
                time.sleep(30)

        except Exception as e:
            logging.error(f"Discovery error: {e}")
            print(f"\n[ERROR] Discovery error: {e}\n")
            error_count += 1
            wait_time = min(300, 60 * error_count)
            print(f"[WAIT] Waiting {wait_time}s before retry (error count: {error_count})")
            time.sleep(wait_time)


def start_background_threads():
    """백그라운드 스레드 시작"""
    print("[STARTUP] Waiting 30 seconds...")
    time.sleep(30)
    print("[STARTUP] Starting background threads now...")

    parser_thread = Thread(target=background_sync_parser, daemon=True)
    parser_thread.start()
    print("[STARTUP] Background sync parser started")

    meeting_thread = Thread(target=background_meeting_generator, daemon=True)
    meeting_thread.start()
    print("[STARTUP] Background meeting generator started")

    discovery_thread = Thread(target=background_business_discovery, daemon=True)
    discovery_thread.start()
    schedule = DiscoveryConfig.get_schedule_hours()
    print(f"[STARTUP] Background business discovery ENABLED - Schedule: {schedule} (KST)")
