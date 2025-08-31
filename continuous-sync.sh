#!/bin/bash

# 지속적 동기화 데몬 스크립트
# 백그라운드에서 실행되며 주기적으로 동기화 수행

REPO_DIR="/Users/down/Dev/D/Down"
LOG_FILE="$REPO_DIR/sync.log"
PID_FILE="$REPO_DIR/.sync-daemon.pid"
SYNC_INTERVAL=60  # 동기화 간격 (초)

# 로그 함수
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [DAEMON] $1" >> "$LOG_FILE"
}

# 종료 시그널 핸들러
cleanup() {
    log_message "동기화 데몬 종료 중..."
    rm -f "$PID_FILE"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 이미 실행 중인지 확인
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "동기화 데몬이 이미 실행 중입니다 (PID: $OLD_PID)"
        exit 1
    else
        rm -f "$PID_FILE"
    fi
fi

# PID 저장
echo $$ > "$PID_FILE"

# 저장소로 이동
cd "$REPO_DIR" || exit 1

log_message "===== 지속적 동기화 데몬 시작 ====="
log_message "동기화 간격: ${SYNC_INTERVAL}초"

# 메인 루프
while true; do
    # 네트워크 연결 확인
    if ping -c 1 github.com > /dev/null 2>&1; then
        log_message "동기화 시작"
        
        # fetch 최신 변경사항
        git fetch origin 2>&1 | while read line; do
            [ -n "$line" ] && log_message "FETCH: $line"
        done
        
        # 현재 브랜치
        CURRENT_BRANCH=$(git branch --show-current)
        
        # 원격과 로컬 상태 비교
        LOCAL=$(git rev-parse @)
        REMOTE=$(git rev-parse @{u} 2>/dev/null)
        BASE=$(git merge-base @ @{u} 2>/dev/null)
        
        if [ "$LOCAL" != "$REMOTE" ]; then
            if [ "$LOCAL" = "$BASE" ]; then
                # 원격이 앞서 있음 - pull 필요
                log_message "원격 변경사항 발견, pull 수행"
                git pull --rebase origin "$CURRENT_BRANCH" 2>&1 | while read line; do
                    [ -n "$line" ] && log_message "PULL: $line"
                done
            elif [ "$REMOTE" = "$BASE" ]; then
                # 로컬이 앞서 있음 - push 필요
                log_message "로컬 변경사항 푸시"
                git push origin "$CURRENT_BRANCH" 2>&1 | while read line; do
                    [ -n "$line" ] && log_message "PUSH: $line"
                done
            else
                # 분기 발생
                log_message "경고: 원격과 로컬이 분기됨 - 수동 병합 필요"
            fi
        else
            # 로컬 변경사항 확인
            if [[ -n $(git status --porcelain) ]]; then
                log_message "추적되지 않은 로컬 변경사항 발견"
                
                # 자동 커밋 옵션 (필요시 활성화)
                # git add -A
                # git commit -m "자동 저장: $(date '+%Y-%m-%d %H:%M:%S')"
                # git push origin "$CURRENT_BRANCH"
            fi
        fi
        
        log_message "동기화 완료"
    else
        log_message "네트워크 연결 실패 - 동기화 건너뜀"
    fi
    
    # 대기
    sleep "$SYNC_INTERVAL"
done