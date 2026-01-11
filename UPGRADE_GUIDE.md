# Koyeb 유료 플랜 전환 가이드

Koyeb 유료 플랜 전환 시 외부 API를 사용한 실시간 시장 분석을 활성화하는 방법입니다.

## 현재 상태

| 항목 | 현재 (무료 티어) | 전환 후 (유료 플랜) |
|-----|----------------|------------------|
| 메모리 | 512MB | 1GB+ |
| 시장 분석 | 경량 모드 (사전 정의 데이터) | 전체 모드 (실시간 API) |
| 데이터 소스 | 내부 추정치 | 크몽, 네이버, 구글, 유튜브 등 10개+ |

## 전환 절차

### 1단계: Koyeb 유료 플랜 업그레이드

1. [Koyeb Dashboard](https://app.koyeb.com) 접속
2. Settings > Billing 이동
3. Starter 또는 Pro 플랜 선택
4. 인스턴스 사양 업그레이드: **최소 1GB RAM 권장**

### 2단계: 환경변수 설정

Koyeb 대시보드에서 서비스의 환경변수를 설정합니다:

```
MARKET_ANALYSIS_MODE=full
```

**설정 방법:**
1. Koyeb Dashboard > Services > 해당 서비스 선택
2. Settings > Environment variables
3. 새 환경변수 추가:
   - Key: `MARKET_ANALYSIS_MODE`
   - Value: `full`
4. Save & Redeploy

### 3단계: 확인

배포 완료 후 API로 설정 상태를 확인합니다:

```bash
curl https://your-app.koyeb.app/api/market-config
```

**응답 예시 (전체 모드):**
```json
{
  "success": true,
  "config": {
    "mode": "full",
    "mode_description": "전체 모드 (외부 API 사용)",
    "is_lightweight": false,
    "api_timeout": 10,
    "api_delay": 2
  }
}
```

## 환경변수 옵션

| 환경변수 | 값 | 설명 |
|---------|---|------|
| `MARKET_ANALYSIS_MODE` | `lightweight` (기본값) | 경량 모드 - 외부 API 미사용 |
| `MARKET_ANALYSIS_MODE` | `full` | 전체 모드 - 외부 API 사용 |
| `MARKET_API_TIMEOUT` | `10` (기본값) | API 요청 타임아웃 (초) |
| `MARKET_API_DELAY` | `2` (기본값) | API 호출 간 대기 시간 (초) |

## 전체 모드에서 사용하는 데이터 소스

전체 모드 활성화 시 다음 플랫폼에서 실시간 데이터를 수집합니다:

| 플랫폼 | 수집 데이터 | 점수 비중 |
|-------|-----------|---------|
| 크몽 | 서비스 수, 평균 가격, 리뷰 수, 경쟁 강도 | 20점 |
| 네이버 검색 | 검색량, 자동완성, 인기도 | 15점 |
| 위시켓 | 프로젝트 수, 평균 예산, 수요 수준 | 15점 |
| 구글 검색 | 검색 결과 수, 광고 경쟁 | 10점 |
| 숨고 | 전문가 수, 리뷰 수, 경쟁 강도 | 10점 |
| 쿠팡 | 상품 수, 평균 가격, 이커머스 잠재력 | 10점 |
| 유튜브 | 관심도 지표, 콘텐츠 양 | 5점 |
| 네이버 블로그 | 포스트 수, 트렌드 지표 | 5점 |
| 탈잉 | 클래스 수, 교육 시장 규모 | 5점 |
| 인스타그램 | SNS 활성도, 마케팅 잠재력 | 5점 |

**블록체인/Web3 관련 키워드 추가 분석:**
- CoinMarketCap, 업비트, OpenSea, GitHub, 사람인 채용시장

## 롤백 방법

문제 발생 시 경량 모드로 즉시 롤백:

```
MARKET_ANALYSIS_MODE=lightweight
```

또는 환경변수를 삭제하면 기본값(경량 모드)으로 동작합니다.

## 예상 비용

| 사양 | 월 예상 비용 |
|-----|------------|
| 1GB RAM, 0.5 vCPU | ~$10-15/월 |
| 2GB RAM, 1 vCPU | ~$20-30/월 |

## 관련 파일

- `market_config.py` - 설정 모듈
- `smart_business_system.py` - 모드 전환 로직
- `real_market_analyzer.py` - 외부 API 분석기
- `lightweight_market_analyzer.py` - 경량 분석기

## 문의

설정 상태 확인: `GET /api/market-config`
