#!/bin/bash

# 자동 동기화 스크립트
# 지속적으로 최신 변경사항을 가져오고 로컬 변경사항을 푸시

REPO_DIR="/Users/down/Dev/D/Down"
LOG_FILE="$REPO_DIR/sync.log"

# 로그 함수
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 저장소로 이동
cd "$REPO_DIR" || exit 1

# 동기화 함수
sync_repo() {
    # 원격 변경사항 가져오기
    log_message "원격 저장소에서 최신 변경사항 가져오기 시작"
    
    # fetch 수행
    git fetch origin
    
    # 현재 브랜치 확인
    CURRENT_BRANCH=$(git branch --show-current)
    
    # 로컬 변경사항 확인
    if [[ -n $(git status --porcelain) ]]; then
        log_message "로컬 변경사항 발견, 커밋 준비"
        
        # 모든 변경사항 스테이징
        git add -A
        
        # 자동 커밋
        COMMIT_MSG="자동 동기화: $(date '+%Y-%m-%d %H:%M:%S')"
        git commit -m "$COMMIT_MSG"
        log_message "커밋 완료: $COMMIT_MSG"
    fi
    
    # pull with rebase to avoid merge commits
    log_message "원격 변경사항 병합 중"
    git pull --rebase origin "$CURRENT_BRANCH"
    
    # push 로컬 변경사항
    if git status | grep -q "Your branch is ahead"; then
        log_message "로컬 변경사항 푸시 중"
        git push origin "$CURRENT_BRANCH"
        log_message "푸시 완료"
    fi
    
    log_message "동기화 완료"
}

# 메인 실행
log_message "===== 자동 동기화 시작 ====="
sync_repo
log_message "===== 자동 동기화 종료 ====="