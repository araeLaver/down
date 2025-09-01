# 🚀 Qhyx Inc. Koyeb 자동 배포 가이드

## 📋 Koyeb Git 연동 설정 방법

### 1. Koyeb 서비스 생성
1. Koyeb 콘솔 접속 (https://app.koyeb.com)
2. "Create Service" 클릭
3. "GitHub" 선택

### 2. Git 저장소 연결
```
Repository: https://github.com/araeLaver/down.git
Branch: master
```

### 3. 빌드 설정
```
Build Command: pip install -r requirements.txt
Start Command: python app.py
Port: 5000
Environment: Production
```

### 4. 환경 변수 설정
```
FLASK_ENV=production
DATABASE_URL=postgresql://unble:npg_1kjV0mhECxqs@ep-divine-bird-a1f4mly5.ap-southeast-1.pg.koyeb.app/unble
PORT=8000
```

### 5. 자동 배포 활성화
- ✅ Auto-deploy from Git: ON
- ✅ Auto-deploy on push: ON
- ✅ Health checks: ON

## 🌐 배포 후 접속 URL
배포 완료 시 Koyeb가 제공하는 URL을 통해 접속 가능:
- **메인 사이트**: https://[your-app-name].koyeb.app/
- **모니터링**: https://[your-app-name].koyeb.app/dashboard

## 📦 필요한 requirements.txt 파일
```txt
Flask==2.3.3
SQLAlchemy==2.0.21
psycopg2-binary==2.9.7
GitPython==3.1.32
schedule==1.2.0
```

## 🔄 자동 배포 플로우
1. **Git Push** → GitHub 저장소 업데이트
2. **Webhook** → Koyeb 자동 감지
3. **Build** → 의존성 설치 및 빌드
4. **Deploy** → 새 버전 배포
5. **Health Check** → 서비스 상태 확인

## ⚡ 즉시 활용 가능한 기능들
✅ 24/7 자동 비즈니스 운영 시스템
✅ 실시간 모니터링 대시보드  
✅ AI 직원 자율 회의 시스템
✅ 일일 사업 보고서 자동 생성
✅ 지속적 사업 확장 엔진

## 🎯 배포 완료 후 확인사항
1. 웹사이트 정상 접속 확인
2. 데이터베이스 연결 상태 확인  
3. 백그라운드 시스템 가동 확인
4. API 엔드포인트 정상 동작 확인

**Qhyx Inc.가 전세계 어디서나 접속 가능한 라이브 서비스가 됩니다!** 🌍