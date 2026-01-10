# Qhyx Inc. 프로젝트 전체 소스 분석 종합 보고서

**작성일**: 2026-01-10
**분석 대상**: Qhyx AI 기반 자율 비즈니스 인텔리전스 플랫폼

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | Qhyx (Quantum Hope Youth eXcellence) |
| **프로젝트 유형** | AI 기반 자율 비즈니스 인텔리전스 플랫폼 |
| **총 코드 라인** | **~23,500줄** |
| **Python 파일** | 44개 (~18,000줄) |
| **HTML 템플릿** | 14개 (~5,500줄) |
| **주요 프레임워크** | Flask 2.3.3, SQLAlchemy 2.0, Chart.js |
| **데이터베이스** | PostgreSQL (Koyeb 클라우드) |
| **운영 방식** | 24/7 자율 운영 시스템 |

---

## 2. 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Qhyx Platform                                │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Frontend   │  │  Flask API  │  │  Background │  │  Database   │ │
│  │  (Jinja2)   │◄─┤  (35 APIs)  │◄─┤   Threads   │◄─┤ (PostgreSQL)│ │
│  │  14 HTML    │  │   app.py    │  │  Schedulers │  │  21 Tables  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
│         │                │                │                │        │
│         ▼                ▼                ▼                ▼        │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    Core Business Modules                        ││
│  ├─────────────┬─────────────┬─────────────┬─────────────┬────────┤│
│  │  Market     │  Business   │  Revenue    │  Action     │ Meeting││
│  │  Analyzer   │  Generator  │  Validator  │  Planner    │ System ││
│  │  (5 files)  │  (4 files)  │  (1 file)   │  (1 file)   │(4 files││
│  └─────────────┴─────────────┴─────────────┴─────────────┴────────┘│
│         │                │                │                │        │
│         ▼                ▼                ▼                ▼        │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    External Data Sources                        ││
│  │   크몽 API  │  네이버 검색  │  Google Trends  │  K-Startup      ││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. 모듈별 상세 분석

### 3.1 Flask 웹 서버 (app.py)

| 항목 | 내용 |
|------|------|
| **파일** | `app.py` (1,847줄) |
| **API 엔드포인트** | 35개 |
| **포트** | 5000 (기본), 환경변수 PORT |

**주요 API 그룹:**
```
GET  /api/discovered-businesses     # 발굴된 사업 목록
GET  /api/trigger-discovery         # 수동 발굴 실행
GET  /api/meetings                  # 회의록 목록
GET  /api/suggestions               # 직원 제안
GET  /api/startup-support/programs  # 창업 지원사업
GET  /api/stats                     # 시스템 통계
GET  /api/status                    # 운영 상태
POST /api/sync/control              # 동기화 제어
```

---

### 3.2 시장 분석 모듈

| 파일명 | 줄수 | 핵심 기능 |
|--------|------|----------|
| `market_analyzer.py` | 875 | 통합 시장 분석 엔진 |
| `kmong_analyzer.py` | 423 | 크몽 프리랜서 마켓 분석 |
| `naver_search_analyzer.py` | 312 | 네이버 검색 트렌드 분석 |
| `google_trends_analyzer.py` | 287 | Google Trends 분석 |
| `lightweight_market_analyzer.py` | 445 | 경량 시장 분석 (API 최소화) |
| **합계** | **2,342줄** | |

**시장 점수 산정 공식:**
```python
market_score = (
    naver_score * 0.35 +      # 네이버 검색량
    kmong_score * 0.35 +      # 크몽 수요/공급
    google_score * 0.20 +     # 글로벌 트렌드
    competition_score * 0.10  # 경쟁 강도
)
```

---

### 3.3 사업 발굴 모듈

| 파일명 | 줄수 | 핵심 기능 |
|--------|------|----------|
| `realistic_business_generator.py` | 954 | AI 사업 아이디어 생성 |
| `continuous_business_discovery.py` | 648 | 연속 발굴 시스템 |
| `revenue_validator.py` | 446 | 수익성 검증 엔진 |
| `action_plan_generator.py` | 432 | 4주 실행 계획 생성 |
| **합계** | **2,480줄** | |

**사업 생성 파이프라인:**
```
1. 트렌드 키워드 수집 (5개 생성)
     ↓
2. 시장 분석 (Market Score 산정)
     ↓
3. 수익성 검증 (Revenue Score 산정)
     ↓
4. 종합 점수 계산 (Total Score)
     ↓
5. 점수별 분류 저장
   - 80+ : 우수 사업 (즉시 실행)
   - 60-79 : 검토 필요
   - 60- : 부적합 (히스토리 기록)
```

---

### 3.4 자동화/운영 모듈

| 파일명 | 줄수 | 핵심 기능 |
|--------|------|----------|
| `autonomous_business_system.py` | 810 | 24/7 자율 운영 시스템 |
| `continuous_meeting_generator.py` | 231 | 30분 간격 회의 생성 |
| `meeting_report_system.py` | 383 | 일일 종합 보고서 |
| `hourly_meeting_daemon.py` | 157 | 매시간 데몬 |
| **합계** | **1,581줄** | |

**12명 AI 직원 구성:**
```python
employees = [
    {'id': 'CEO_001', 'name': '알렉스 김', 'role': 'CEO'},
    {'id': 'CFO_001', 'name': '에밀리 박', 'role': 'CFO'},
    {'id': 'CTO_001', 'name': '데이비드 이', 'role': 'CTO'},
    {'id': 'CMO_001', 'name': '소피아 최', 'role': 'CMO'},
    {'id': 'COO_001', 'name': '마이클 정', 'role': 'COO'},
    {'id': 'CPO_001', 'name': '올리비아 강', 'role': 'CPO'},
    # ... 6명 추가 (CSO, CHRO, CLO, CDO, CIO, CCO)
]
```

**6가지 회의 유형 (매시간 순환):**
1. 일일 스탠드업
2. 전략 회의
3. 기술 리뷰
4. 재무 검토
5. 마케팅 회의
6. 운영 검토

---

### 3.5 데이터베이스 모델

| 파일명 | 줄수 | 테이블 수 |
|--------|------|----------|
| `database_setup.py` | 423 | 16개 |
| `business_discovery_history.py` | 612 | 5개 |
| **합계** | **1,035줄** | **21개** |

**주요 테이블 구조:**

```sql
-- 스키마: qhyx_growth

-- 핵심 테이블
Employee (id, name, role, email, department, status)
BusinessPlan (id, name, description, market_score, revenue_score, total_score)
BusinessMeeting (id, title, date, participants, summary, action_items)
EmployeeSuggestion (id, employee_id, title, status, priority)

-- 히스토리 테이블
BusinessDiscoveryHistory (id, business_name, scores, created_at)
BusinessAnalysisSnapshot (id, time_of_day, statistics)
BusinessInsight (id, insight_type, content, importance)
LowScoreBusiness (id, business_name, failure_reason, scores)
```

**데이터베이스 연결:**
```python
SCHEMA_NAME = 'qhyx_growth'
engine = create_engine(
    connection_string,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)
```

---

### 3.6 유틸리티/헬퍼 모듈

| 파일명 | 줄수 | 핵심 기능 |
|--------|------|----------|
| `daily_report_system.py` | 658 | 12개 섹션 일일 보고서 |
| `startup_support_crawler.py` | 401 | 창업 지원사업 크롤러 |
| `business_monitor.py` | 172 | 실시간 모니터링 |
| `verify_data.py` | 131 | DB 무결성 검증 |
| `run_discovery.py` | 49 | Cron Job 실행 스크립트 |
| `check_status.py` | 41 | 발굴 상태 확인 |
| **합계** | **1,452줄** | |

**일일 보고서 12개 섹션:**
```python
sections = [
    "헤더",              # 회사명, 날짜
    "경영진 요약",        # 핵심 지표
    "사업 발굴 현황",     # 오늘 발굴 사업
    "시장 트렌드",        # 키워드 분석
    "수익성 분석",        # 매출/비용 예측
    "회의 요약",          # 오늘 회의록
    "직원 제안",          # 건의사항 현황
    "실행 계획",          # 주간 할일
    "리스크 분석",        # 위험 요소
    "경쟁사 동향",        # 시장 경쟁
    "권장 사항",          # AI 추천
    "푸터"               # 연락처
]
```

---

### 3.7 프론트엔드 템플릿

| 카테고리 | 파일 수 | 총 줄수 |
|----------|---------|---------|
| 공통 컴포넌트 | 1 | 216 |
| 메인 페이지 | 3 | 1,605 |
| 사업 발굴 | 6 | 2,751 |
| 회의/제안 | 2 | 1,291 |
| 창업 지원 | 1 | 602 |
| **합계** | **14** | **~5,500줄** |

**디자인 시스템:**
```css
/* Primary Theme */
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--success-color: #10b981;
--warning-color: #f59e0b;
--danger-color: #ef4444;

/* Card Style */
border-radius: 15px;
box-shadow: 0 10px 40px rgba(0,0,0,0.1);
transition: transform 0.3s;
```

**실시간 업데이트:**
```javascript
setInterval(updateStats, 5000);   // 5초
setInterval(updateLogs, 10000);   // 10초
setInterval(updateChart, 60000);  // 1분
```

---

## 4. 핵심 비즈니스 로직

### 4.1 사업 발굴 알고리즘

```python
def discover_business():
    # 1. 트렌드 키워드 5개 생성
    keywords = generate_trend_keywords()

    for keyword in keywords:
        # 2. 시장 분석
        market_score = analyze_market(keyword)
        # - 네이버 검색량 (35%)
        # - 크몽 수요/공급 (35%)
        # - Google Trends (20%)
        # - 경쟁 강도 (10%)

        # 3. 수익성 검증
        revenue_score = validate_revenue(keyword)
        # - 초기 투자 비용
        # - 월 운영 비용
        # - 예상 월 매출
        # - ROI 계산 (3개 시나리오)

        # 4. 종합 점수
        total_score = (market_score * 0.5) + (revenue_score * 0.5)

        # 5. 분류 저장
        if total_score >= 80:
            save_to_excellent(business)    # 즉시 실행
        elif total_score >= 60:
            save_to_review(business)       # 검토 필요
        else:
            save_to_history(business)      # 히스토리 기록
```

### 4.2 스케줄링 시스템

```python
# 8시간 주기 자동 발굴
schedule.every().day.at("01:00").do(run_discovery)  # 새벽
schedule.every().day.at("09:00").do(run_discovery)  # 오전
schedule.every().day.at("17:00").do(run_discovery)  # 오후

# 매시간 회의 생성
schedule.every().hour.at(":00").do(generate_meeting)

# 일일 보고서
schedule.every().day.at("09:00").do(send_morning_report)
schedule.every().day.at("14:00").do(send_afternoon_report)
schedule.every().day.at("18:00").do(send_evening_report)
```

### 4.3 점수 기준 체계

| 점수 범위 | 분류 | 의미 | 액션 |
|-----------|------|------|------|
| 80-100 | 우수 | 높은 시장성 + 수익성 | 즉시 실행 계획 생성 |
| 60-79 | 검토 | 잠재력 있음 | 추가 분석 필요 |
| 0-59 | 부적합 | 낮은 점수 | 히스토리 기록만 |

---

## 5. 기술 스택 종합

### 5.1 백엔드

| 기술 | 버전 | 용도 |
|------|------|------|
| Python | 3.10+ | 메인 언어 |
| Flask | 2.3.3 | 웹 프레임워크 |
| SQLAlchemy | 2.0 | ORM |
| PostgreSQL | - | 데이터베이스 |
| schedule | - | 스케줄링 |
| requests | - | HTTP 클라이언트 |
| BeautifulSoup | - | 웹 스크래핑 |

### 5.2 프론트엔드

| 기술 | 버전 | 용도 |
|------|------|------|
| HTML5 | - | 마크업 |
| CSS3 | - | 스타일링 |
| JavaScript | ES6+ | 인터랙션 |
| Jinja2 | - | 템플릿 엔진 |
| Bootstrap | 5.x | UI 프레임워크 |
| Chart.js | 4.x | 차트 시각화 |
| Font Awesome | 6.0 | 아이콘 |

### 5.3 인프라

| 서비스 | 용도 |
|--------|------|
| Koyeb | PostgreSQL 호스팅 |
| 환경변수 | DATABASE_URL, PORT |

---

## 6. 코드 통계

### 6.1 파일별 분포

```
Python 모듈 (44개 파일)
├── 서버/API        : 1,847줄 (app.py)
├── 시장 분석       : 2,342줄 (5개 파일)
├── 사업 발굴       : 2,480줄 (4개 파일)
├── 자동화/운영     : 1,581줄 (4개 파일)
├── 데이터베이스    : 1,035줄 (2개 파일)
├── 유틸리티        : 1,452줄 (6개 파일)
└── 기타            : ~7,000줄 (22개 파일)
                     ────────
                     ~18,000줄

HTML 템플릿 (14개 파일)
├── 공통 컴포넌트   : 216줄
├── 메인 페이지     : 1,605줄
├── 사업 발굴       : 2,751줄
├── 회의/제안       : 1,291줄
└── 창업 지원       : 602줄
                     ────────
                     ~5,500줄

총계: ~23,500줄
```

### 6.2 모듈별 복잡도

| 모듈 | 파일 수 | 줄수 | 복잡도 |
|------|---------|------|--------|
| 시장 분석 | 5 | 2,342 | 높음 |
| 사업 발굴 | 4 | 2,480 | 높음 |
| Flask 서버 | 1 | 1,847 | 중간 |
| 자동화 | 4 | 1,581 | 중간 |
| 유틸리티 | 6 | 1,452 | 낮음 |
| 데이터베이스 | 2 | 1,035 | 낮음 |

---

## 7. API 엔드포인트 종합

### 7.1 사업 발굴 API (10개)

```
GET  /api/discovered-businesses       # 우수 사업 목록
GET  /api/discovered-businesses/:id   # 사업 상세
GET  /api/trigger-discovery           # 수동 발굴
GET  /api/business-history            # 발굴 히스토리
GET  /api/low-score-businesses/list   # 부적합 사업
GET  /api/business-stats              # 사업 통계
GET  /api/business-insights           # 인사이트
GET  /api/analysis-snapshots          # 분석 스냅샷
POST /api/business/:id/action-plan    # 실행계획 생성
POST /api/business/:id/approve        # 사업 승인
```

### 7.2 회의/제안 API (8개)

```
GET  /api/meetings                    # 회의록 목록
GET  /api/meetings/:id                # 회의 상세
POST /api/meetings                    # 회의 생성
GET  /api/suggestions                 # 제안 목록
GET  /api/suggestions/:id             # 제안 상세
POST /api/suggestions                 # 제안 생성
PUT  /api/suggestions/:id/status      # 상태 변경
POST /api/suggestions/:id/feedback    # 피드백 추가
```

### 7.3 시스템 API (10개)

```
GET  /api/stats                       # 시스템 통계
GET  /api/status                      # 운영 상태
GET  /api/logs                        # 로그 조회
GET  /api/metrics                     # 메트릭
GET  /api/dashboard-data              # 대시보드 데이터
POST /api/sync/control                # 동기화 제어
GET  /api/employees                   # 직원 목록
GET  /api/startup-support/programs    # 지원사업 목록
POST /api/startup-support/recommend   # 맞춤 추천
GET  /health                          # 헬스체크
```

---

## 8. 운영 시나리오

### 8.1 일반 운영 흐름

```
00:00 ─────────────────────────────────────────────────── 24:00
  │                                                         │
  ├─ 01:00 [자동 발굴] 5개 사업 분석                         │
  │                                                         │
  ├─ 매시간 [AI 회의] 6가지 유형 순환                        │
  │   ├─ 00분: 스탠드업                                     │
  │   ├─ 01분: 전략 회의                                    │
  │   ├─ 02분: 기술 리뷰                                    │
  │   ├─ 03분: 재무 검토                                    │
  │   ├─ 04분: 마케팅 회의                                  │
  │   └─ 05분: 운영 검토                                    │
  │                                                         │
  ├─ 09:00 [자동 발굴] + [오전 보고서]                       │
  │                                                         │
  ├─ 14:00 [오후 보고서]                                    │
  │                                                         │
  ├─ 17:00 [자동 발굴]                                      │
  │                                                         │
  └─ 18:00 [저녁 보고서]                                    │
```

### 8.2 사업 발굴 파이프라인

```
┌─────────────────┐
│ 트렌드 키워드    │
│ 5개 생성        │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 시장 분석       │
│ (4개 데이터 소스)│
└────────┬────────┘
         ▼
┌─────────────────┐
│ 수익성 검증     │
│ (3개 시나리오)  │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 종합 점수 산정   │
│ Market 50%      │
│ Revenue 50%     │
└────────┬────────┘
         ▼
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│ 80+   │ │ 60-79 │ │ 60-   │
│ 우수   │ │ 검토  │ │ 부적합 │
└───────┘ └───────┘ └───────┘
```

---

## 9. 보안 및 설정

### 9.1 환경변수

```bash
DATABASE_URL=postgresql://user:pass@host:port/db
PORT=5000
FLASK_ENV=production
```

### 9.2 데이터베이스 보안

- Connection Pooling (pool_size=10, max_overflow=20)
- pool_pre_ping=True (연결 상태 확인)
- 스키마 분리 (qhyx_growth)

---

## 10. 프로젝트 강점

### 10.1 기술적 강점

| 영역 | 강점 |
|------|------|
| **자동화** | 24/7 무인 운영, 스케줄 기반 자동 발굴 |
| **분석력** | 다중 데이터 소스 통합 (크몽, 네이버, Google) |
| **확장성** | 모듈화된 구조, ORM 기반 DB 추상화 |
| **시각화** | Chart.js 기반 실시간 대시보드 |
| **반응형** | 모바일/데스크톱 완벽 지원 |

### 10.2 비즈니스 강점

| 영역 | 강점 |
|------|------|
| **효율성** | 하루 최대 15개 사업 자동 분석 |
| **객관성** | 점수 기반 사업 평가 시스템 |
| **추적성** | 모든 분석 결과 히스토리 보존 |
| **실행력** | 4주 단위 구체적 실행 계획 자동 생성 |

---

## 11. 개선 가능 영역

### 11.1 기술적 개선

| 영역 | 현재 상태 | 개선 방향 |
|------|----------|----------|
| 인증 | 미구현 | JWT/OAuth2 추가 |
| 캐싱 | 미구현 | Redis 캐시 레이어 |
| 테스트 | 미확인 | 단위/통합 테스트 추가 |
| 로깅 | 기본 | 구조화된 로깅 (ELK) |
| API 문서 | 미구현 | Swagger/OpenAPI |

### 11.2 아키텍처 개선

| 영역 | 현재 상태 | 개선 방향 |
|------|----------|----------|
| 배포 | 단일 서버 | 컨테이너화 (Docker) |
| 스케일링 | 수직 확장 | 수평 확장 (Kubernetes) |
| 메시징 | 동기 처리 | 비동기 큐 (Celery/RabbitMQ) |

---

## 12. 결론

### 12.1 프로젝트 평가

| 평가 항목 | 점수 | 비고 |
|-----------|------|------|
| 코드 품질 | ★★★★☆ | 모듈화, 명확한 구조 |
| 기능 완성도 | ★★★★★ | 핵심 기능 완전 구현 |
| UI/UX | ★★★★☆ | 일관된 디자인, 반응형 |
| 확장성 | ★★★★☆ | 모듈 분리, ORM 사용 |
| 문서화 | ★★★☆☆ | 코드 주석 존재, 별도 문서 미확인 |

### 12.2 핵심 수치 요약

```
┌────────────────────────────────────────────────────────┐
│                    Qhyx 프로젝트 요약                   │
├────────────────────────────────────────────────────────┤
│  총 코드 라인        │  ~23,500줄                      │
│  Python 파일         │  44개                           │
│  HTML 템플릿         │  14개                           │
│  API 엔드포인트      │  35개                           │
│  데이터베이스 테이블  │  21개                           │
│  AI 직원             │  12명                           │
│  회의 유형           │  6가지                          │
│  일일 사업 발굴      │  최대 15개                      │
│  운영 시간           │  24/7 자율 운영                 │
└────────────────────────────────────────────────────────┘
```

---

## 부록: 파일 목록

### Python 파일 (주요)

```
app.py                              # Flask 서버 (1,847줄)
market_analyzer.py                  # 시장 분석 (875줄)
realistic_business_generator.py     # 사업 생성 (954줄)
autonomous_business_system.py       # 자율 운영 (810줄)
continuous_business_discovery.py    # 연속 발굴 (648줄)
daily_report_system.py              # 일일 보고 (658줄)
business_discovery_history.py       # 히스토리 (612줄)
revenue_validator.py                # 수익 검증 (446줄)
lightweight_market_analyzer.py      # 경량 분석 (445줄)
action_plan_generator.py            # 실행 계획 (432줄)
database_setup.py                   # DB 설정 (423줄)
kmong_analyzer.py                   # 크몽 분석 (423줄)
startup_support_crawler.py          # 지원사업 (401줄)
meeting_report_system.py            # 회의 보고 (383줄)
naver_search_analyzer.py            # 네이버 (312줄)
google_trends_analyzer.py           # 구글 (287줄)
continuous_meeting_generator.py     # 회의 생성 (231줄)
business_monitor.py                 # 모니터링 (172줄)
hourly_meeting_daemon.py            # 시간별 (157줄)
verify_data.py                      # 검증 (131줄)
run_discovery.py                    # 실행 (49줄)
check_status.py                     # 상태 (41줄)
```

### HTML 템플릿

```
templates/
├── navbar.html                     # 공통 네비게이션 (216줄)
├── index.html                      # 메인 랜딩 (272줄)
├── qhyx_main.html                  # 마케팅 페이지 (847줄)
├── dashboard.html                  # 대시보드 (486줄)
├── business_discovery.html         # 우수 사업 (800+줄)
├── business_review.html            # 검토 사업 (~500줄)
├── business_rejected.html          # 부적합 사업 (498줄)
├── business_landing.html           # 사업 랜딩 (214줄)
├── business_history.html           # 히스토리 (~400줄)
├── trigger_discovery.html          # 수동 발굴 (339줄)
├── meetings.html                   # 회의록 (~600줄)
├── suggestions.html                # 건의사항 (691줄)
└── startup_support.html            # 창업지원 (602줄)
```

---

**보고서 작성 완료**

*본 보고서는 Qhyx Inc. 프로젝트의 전체 소스 코드를 분석한 종합 보고서입니다.*
*작성일: 2026-01-10*
