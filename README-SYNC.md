# 지속적 동기화 시스템

이 저장소는 GitHub와 자동으로 동기화되도록 설정되었습니다.

## 🚀 빠른 시작

### 동기화 데몬 시작
```bash
./sync-control.sh start
```

### 동기화 상태 확인
```bash
./sync-control.sh status
```

### 즉시 수동 동기화
```bash
./sync-control.sh sync
```

## 📂 구성 요소

### 1. **auto-sync.sh**
- 단일 동기화 작업 수행
- 원격 변경사항 가져오기 (pull)
- 로컬 변경사항 푸시 (push)
- 충돌 시 rebase 사용

### 2. **continuous-sync.sh**
- 백그라운드 데몬 프로세스
- 60초마다 자동 동기화
- 네트워크 상태 확인
- 자동 충돌 감지

### 3. **sync-control.sh**
- 데몬 제어 스크립트
- 시작/중지/재시작/상태 확인
- 로그 보기 기능

### 4. **Git Hooks**
- `post-commit`: 커밋 후 자동 푸시
- `pre-push`: 푸시 전 원격 상태 확인

## 📋 사용 가능한 명령어

```bash
# 데몬 시작
./sync-control.sh start

# 데몬 중지
./sync-control.sh stop

# 데몬 재시작
./sync-control.sh restart

# 상태 확인
./sync-control.sh status

# 로그 보기
./sync-control.sh logs

# 즉시 동기화
./sync-control.sh sync
```

## 📊 로그 파일

모든 동기화 활동은 `sync.log` 파일에 기록됩니다:
```bash
tail -f sync.log
```

## ⚙️ 설정 변경

### 동기화 간격 변경
`continuous-sync.sh` 파일의 `SYNC_INTERVAL` 변수 수정:
```bash
SYNC_INTERVAL=60  # 초 단위
```

### 자동 커밋 활성화
`continuous-sync.sh`에서 자동 커밋 부분의 주석 해제:
```bash
# git add -A
# git commit -m "자동 저장: $(date '+%Y-%m-%d %H:%M:%S')"
# git push origin "$CURRENT_BRANCH"
```

## 🔧 문제 해결

### 충돌 발생 시
1. 데몬 중지: `./sync-control.sh stop`
2. 수동으로 충돌 해결
3. 데몬 재시작: `./sync-control.sh start`

### 데몬이 시작되지 않을 때
```bash
# PID 파일 확인 및 삭제
rm -f .sync-daemon.pid
# 데몬 재시작
./sync-control.sh start
```

## 📝 주의사항

- 데몬은 60초마다 동기화를 수행합니다
- 네트워크 연결이 없으면 동기화를 건너뜁니다
- 충돌 발생 시 로그에 경고가 기록되며 수동 개입이 필요합니다
- 시스템 재부팅 후에는 데몬을 다시 시작해야 합니다

## 🔐 보안

- Git hooks는 로컬에서만 작동합니다
- 인증은 기존 Git 설정을 사용합니다
- 민감한 정보는 커밋하지 마세요