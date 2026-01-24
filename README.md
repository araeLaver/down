# Fryndo

> AI 기반 실시간 여행 동행 매칭 플랫폼

**안전한 여행 동반자를 찾고, 여행의 추억을 디지털 자산으로 기록하세요.**

[![Deploy](https://img.shields.io/badge/Deploy-Koyeb-blue)](https://various-belva-untab-1a59bee2.koyeb.app)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 서비스 소개

Fryndo는 **혼자 여행하기 망설이는 사람들**을 위한 여행 동행 매칭 서비스입니다.

### 핵심 기능

| 기능 | 설명 |
|------|------|
| **AI 매칭** | 여행 스타일, 관심사, 일정 기반 동행자 추천 |
| **실시간 채팅** | WebSocket 기반 그룹 채팅 (이미지/위치 공유) |
| **안전 시스템** | 신분증 인증, 긴급 SOS, 동행 후 리뷰 |
| **NFT 수집** | GPS 기반 방문 인증 NFT 발행 (Polygon) |
| **여행 커뮤니티** | 여행 후기, 장소 리뷰, 팁 공유 |

### 차별점

```
┌──────────────────┬──────────────────┬──────────────────┐
│   안전 최우선     │   여행 특화 매칭   │    지역 집중      │
├──────────────────┼──────────────────┼──────────────────┤
│ • 신분증 필수     │ • 데이팅 앱 X     │ • 제주 → 부산     │
│ • 긴급 SOS       │ • 여행 스타일 기반 │ • → 서울 확장     │
│ • 위치 공유      │ • 일정 기반 그룹   │ • 높은 매칭 밀도   │
│ • 리뷰 시스템    │ • 동행 후기       │                  │
└──────────────────┴──────────────────┴──────────────────┘
```

---

## 기술 스택

### Backend
- **Framework**: Flask 2.3
- **Database**: PostgreSQL + SQLAlchemy
- **Cache**: Redis
- **Auth**: OAuth 2.0 (카카오, 구글)

### Frontend
- **Template**: Jinja2
- **Style**: Tailwind CSS
- **Realtime**: WebSocket

### Infrastructure
- **Deploy**: Koyeb (PaaS)
- **CI/CD**: GitHub Actions
- **Monitoring**: Built-in logging

### Blockchain (Optional)
- **Network**: Polygon
- **Standard**: ERC-721 NFT

---

## 설치 및 실행

### 1. 환경 설정

```bash
# 저장소 클론
git clone https://github.com/araeLaver/down.git
cd down

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수

```bash
cp .env.example .env
# .env 파일 수정
```

주요 환경 변수:
```
DATABASE_URL=postgresql://user:pass@localhost/fryndo
SECRET_KEY=your-secret-key
KAKAO_CLIENT_ID=your-kakao-key
GOOGLE_CLIENT_ID=your-google-key
```

### 3. 실행

```bash
# 개발 서버
flask run

# 프로덕션
gunicorn app:app
```

---

## 프로젝트 구조

```
├── app.py                    # 메인 애플리케이션
├── auth.py                   # 인증 모듈
├── config.py                 # 설정
├── database_setup.py         # DB 스키마
├── requirements.txt          # 의존성
├── templates/                # HTML 템플릿
├── docs/                     # 문서
│   ├── Fryndo_사업계획서.md
│   ├── Fryndo_예비창업패키지_사업계획서.md
│   └── legal/                # 법적 문서
└── .github/workflows/        # CI/CD
```

---

## 스크린샷

> 스크린샷은 `docs/images/` 폴더에 추가 예정

| 메인 화면 | 매칭 화면 | 채팅 화면 |
|-----------|-----------|-----------|
| ![메인](docs/images/01_landing.png) | ![매칭](docs/images/04_groups.png) | ![채팅](docs/images/05_chat.png) |

---

## 로드맵

- [x] MVP 개발 완료
- [x] 카카오/구글 소셜 로그인
- [x] 실시간 채팅
- [x] 여행 그룹 매칭
- [ ] NFT 민팅 기능
- [ ] AR 안경 연동 (Meta SDK)
- [ ] iOS/Android 앱

---

## 라이선스

MIT License

---

## 링크

- **서비스**: https://various-belva-untab-1a59bee2.koyeb.app
- **문서**: [docs/README.md](docs/README.md)

---

*Last updated: 2026-01-22*
