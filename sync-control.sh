#!/bin/bash

# 동기화 데몬 제어 스크립트

REPO_DIR="/Users/down/Dev/D/Down"
LOG_FILE="$REPO_DIR/sync.log"
PID_FILE="$REPO_DIR/.sync-daemon.pid"
DAEMON_SCRIPT="$REPO_DIR/continuous-sync.sh"

# 색상 코드
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 상태 확인 함수
status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC} 동기화 데몬 실행 중 (PID: $PID)"
            return 0
        else
            echo -e "${RED}✗${NC} 동기화 데몬이 실행되지 않음 (오래된 PID 파일 발견)"
            rm -f "$PID_FILE"
            return 1
        fi
    else
        echo -e "${YELLOW}○${NC} 동기화 데몬이 실행되지 않음"
        return 1
    fi
}

# 시작 함수
start() {
    if status > /dev/null 2>&1; then
        echo -e "${YELLOW}!${NC} 동기화 데몬이 이미 실행 중입니다"
        return 1
    fi
    
    echo -e "${GREEN}▶${NC} 동기화 데몬 시작 중..."
    nohup "$DAEMON_SCRIPT" > /dev/null 2>&1 &
    sleep 2
    
    if status > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} 동기화 데몬이 성공적으로 시작되었습니다"
    else
        echo -e "${RED}✗${NC} 동기화 데몬 시작 실패"
        return 1
    fi
}

# 중지 함수
stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo -e "${YELLOW}■${NC} 동기화 데몬 중지 중..."
            kill "$PID"
            sleep 2
            
            if ps -p "$PID" > /dev/null 2>&1; then
                echo -e "${YELLOW}!${NC} 강제 종료 시도..."
                kill -9 "$PID"
            fi
            
            rm -f "$PID_FILE"
            echo -e "${GREEN}✓${NC} 동기화 데몬이 중지되었습니다"
        else
            echo -e "${YELLOW}!${NC} 프로세스를 찾을 수 없음 (PID 파일 정리)"
            rm -f "$PID_FILE"
        fi
    else
        echo -e "${YELLOW}○${NC} 동기화 데몬이 실행되지 않음"
    fi
}

# 재시작 함수
restart() {
    echo -e "${YELLOW}↻${NC} 동기화 데몬 재시작 중..."
    stop
    sleep 1
    start
}

# 로그 보기 함수
logs() {
    if [ -f "$LOG_FILE" ]; then
        echo -e "${GREEN}📋${NC} 최근 로그 (마지막 20줄):"
        echo "----------------------------------------"
        tail -n 20 "$LOG_FILE"
    else
        echo -e "${YELLOW}!${NC} 로그 파일이 없습니다"
    fi
}

# 수동 동기화 함수
sync_now() {
    echo -e "${GREEN}🔄${NC} 즉시 동기화 실행 중..."
    cd "$REPO_DIR" || exit 1
    "$REPO_DIR/auto-sync.sh"
    echo -e "${GREEN}✓${NC} 동기화 완료"
}

# 도움말 함수
usage() {
    echo "사용법: $0 {start|stop|restart|status|logs|sync|help}"
    echo ""
    echo "명령어:"
    echo "  start    - 동기화 데몬 시작"
    echo "  stop     - 동기화 데몬 중지"
    echo "  restart  - 동기화 데몬 재시작"
    echo "  status   - 동기화 데몬 상태 확인"
    echo "  logs     - 최근 동기화 로그 보기"
    echo "  sync     - 즉시 수동 동기화 실행"
    echo "  help     - 이 도움말 표시"
}

# 메인 처리
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    sync)
        sync_now
        ;;
    help)
        usage
        ;;
    *)
        usage
        exit 1
        ;;
esac