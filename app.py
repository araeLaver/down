from flask import Flask
from flask_cors import CORS
import os
from threading import Thread

# 통합 로깅 시스템
from logging_config import init_logging

# 로깅 초기화
app_logger = init_logging()

# 데이터베이스 초기화
from database_setup import initialize_database
from business_discovery_history import initialize_history_tables

try:
    initialize_database()
    initialize_history_tables()
except Exception as e:
    print(f"Database initialization warning: {e}")

# Flask 앱 생성
app = Flask(__name__)
CORS(app, origins=["https://anonymous-kylen-untab-d30cd097.koyeb.app"])

# Blueprint 등록
from routes import register_blueprints
register_blueprints(app)

# 인증 라우트 등록
from auth import create_auth_routes
create_auth_routes(app)
print("[STARTUP] Auth routes registered")

# 백그라운드 스레드 시작 (non-blocking)
from services.background import start_background_threads
startup_thread = Thread(target=start_background_threads, daemon=True)
startup_thread.start()
print("[STARTUP] Background initialization thread started (non-blocking)")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
