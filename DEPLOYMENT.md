# 회사 성장 추적 시스템 배포 가이드

## 시스템 개요
- **대시보드**: http://localhost:5000
- **데이터베이스**: Koyeb PostgreSQL (company_growth 스키마)
- **동기화**: GitHub 자동 동기화 (60초 간격)

## 구성 요소

### 1. 데이터베이스 (PostgreSQL)
```
Host: ep-divine-bird-a1f4mly5.ap-southeast-1.pg.koyeb.app
Schema: company_growth
Tables: 9개 (활동로그, 동기화로그, 메트릭, AI직원 등)
```

### 2. 웹 애플리케이션
- Flask 기반 REST API
- 실시간 대시보드
- Git 활동 추적
- 동기화 상태 모니터링

### 3. 자동 동기화
```bash
# 상태 확인
./sync-control.sh status

# 로그 보기
./sync-control.sh logs
```

## Koyeb 배포

### 1. GitHub 저장소 연결
Koyeb 대시보드에서 GitHub 저장소 연결

### 2. 환경 변수 설정
```
DATABASE_URL=postgresql://unble:npg_1kjV0mhECxqs@ep-divine-bird-a1f4mly5.ap-southeast-1.pg.koyeb.app/unble
```

### 3. 배포 명령
```bash
# Docker 이미지 빌드
docker build -t company-dashboard .

# Koyeb CLI로 배포
koyeb app init company-dashboard
koyeb service deploy company-dashboard --docker
```

## API 엔드포인트

- `GET /` - 대시보드
- `GET /api/stats` - 통계 정보
- `GET /api/logs` - 로그 조회
- `GET /api/metrics` - 성장 지표
- `POST /api/sync/control` - 동기화 제어
- `POST /api/record` - 활동 기록

## 로컬 테스트
```bash
# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 초기화
python database_setup.py

# 서버 실행
python app.py
```

## 모니터링
- 대시보드: http://localhost:5000
- API 상태: http://localhost:5000/api/stats
- 동기화 로그: tail -f sync.log