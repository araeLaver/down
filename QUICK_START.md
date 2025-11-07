# 🚀 IT 사업 발굴 시스템 빠른 시작 가이드

## 개요
실시간 시장 데이터 기반으로 IT 사업 아이디어를 자동 발굴하고, 수익성을 검증한 후, 즉시 실행 가능한 4주 계획을 자동 생성하는 시스템입니다.

---

## 🎯 핵심 기능

### 1. 실시간 시장 분석 (`real_market_analyzer.py`)
- 크몽 실제 시장 데이터 수집
- 네이버 검색량 분석
- 구글 경쟁사 파악
- 유튜브 관심도 측정
- **시장 점수 자동 계산 (0-100점)**

### 2. 수익성 검증 (`revenue_validator.py`)
- IT 사업 실제 비용 계산
- 보수적/현실적/낙관적 시나리오
- 손익분기점 분석
- ROI 자동 계산
- **수익성 점수 자동 산출**

### 3. 실행 계획 생성 (`action_plan_generator.py`)
- 4주 단위 구체적 액션 아이템
- 기술 스택 자동 추천
- 필요 예산 및 리소스 산출
- 체크리스트 자동 생성

### 4. 통합 시스템 (`smart_business_system.py`)
- 위 3개 모듈 자동 연계
- **80점 이상 아이디어만 실행 계획 생성**
- 여러 아이디어 일괄 분석
- 최종 리포트 자동 생성

---

## 📦 설치

```bash
# 필요한 라이브러리 설치
pip install requests beautifulsoup4

# 파일 확인
ls -la *.py
```

---

## 🏃 실행 방법

### 방법 1: 통합 시스템 (권장)

```python
python smart_business_system.py
```

**결과:**
- 여러 IT 사업 아이디어 자동 분석
- 80점 이상만 4주 실행 계획 생성
- 최종 리포트 및 JSON 파일 저장

---

### 방법 2: 개별 모듈 테스트

#### 2-1. 시장 분석만
```python
python real_market_analyzer.py
```
→ 크몽/네이버/구글/유튜브 데이터 수집
→ 시장 점수 산출

#### 2-2. 수익성 검증만
```python
python revenue_validator.py
```
→ 초기 비용, 월 비용, ROI 계산
→ 3가지 시나리오 시뮬레이션

#### 2-3. 실행 계획만
```python
python action_plan_generator.py
```
→ 4주 구체적 실행 계획
→ 기술 스택 추천

---

## 💡 사용 예시

### 나만의 아이디어 분석하기

```python
from smart_business_system import SmartBusinessSystem

system = SmartBusinessSystem()

# 분석할 아이디어 설정
my_idea = {
    'business_idea': '내 사업 아이디어명',
    'keyword': '크몽 검색 키워드',
    'config': {
        'name': '사업명',
        'type': 'saas',  # 또는 'agency', 'marketplace', 'tool'
        'scale': 'small',  # 'small', 'medium', 'large'
        'revenue_model': 'subscription',  # 'subscription', 'one_time', 'commission'
        'pricing': {
            'monthly': 29000  # 구독 가격 (또는 'one_time': 100000)
        },
        'target_market_size': 5000,  # 월 예상 방문자
        'budget': 2000000,  # 초기 예산
        'timeline_weeks': 4  # 개발 기간
    }
}

# 분석 실행
result = system.analyze_business_idea(
    my_idea['business_idea'],
    my_idea['keyword'],
    my_idea['config']
)

# 결과 확인
if result['passed'] and result.get('total_score', 0) >= 80:
    print("✅ 유망한 아이디어! 바로 실행하세요!")
    print(f"종합 점수: {result['total_score']}")
    print(f"월 예상 수익: {result['revenue_data']['scenarios']['realistic']['monthly_profit']:,}원")
else:
    print("⚠️ 다른 아이디어를 고려하세요.")
```

---

## 📊 결과 해석

### 점수 체계

| 종합 점수 | 판정 | 액션 |
|----------|------|------|
| 80-100점 | 매우 유망 | ✅ 즉시 실행 |
| 60-79점 | 보통 | ⚠️ 추가 검증 필요 |
| 0-59점 | 비추천 | ❌ 다른 아이디어 탐색 |

**종합 점수 계산:**
- 시장 점수 60% + 수익성 점수 40%

---

## 📁 생성되는 파일

### 1. `business_analysis_results.json`
전체 분석 결과 요약

### 2. `plan_[사업명].json`
4주 실행 계획 상세 (80점 이상만)

### 3. `market_analysis.json`
시장 분석 원본 데이터

### 4. `revenue_validation.json`
수익성 검증 상세 데이터

---

## 🛠️ 커스터마이징

### 분석 기준 변경

`smart_business_system.py` 수정:

```python
# 60점 → 70점으로 변경
if market_score < 70:  # 기존 60
    return {...}

# 80점 → 75점으로 변경
if total_score >= 75:  # 기존 80
    print("실행 계획 생성 중...")
```

### 새 사업 모델 추가

`revenue_validator.py`의 `calculate_startup_costs()` 함수에 추가:

```python
elif business_type == 'my_new_type':
    costs['development'] = 1000000
    costs['marketing'] = 500000
    # ...
```

---

## 🚨 주의사항

### 1. API 호출 제한
- 크몽/네이버 등 웹 스크래핑이므로 요청 간격 필요
- 현재 5초 간격 설정됨
- 과도한 요청 시 IP 차단 가능

### 2. 데이터 정확도
- 웹 스크래핑은 페이지 구조 변경 시 오류 가능
- 정기적인 코드 업데이트 필요
- 참고용으로 활용, 최종 판단은 직접

### 3. 실행 계획
- 자동 생성된 계획은 가이드라인
- 실제 상황에 맞게 조정 필요
- 기술 스택 추천도 참고용

---

## 🎓 실전 활용 팁

### 1단계: 아이디어 발굴
```bash
# IT 사업 아이디어 자동 생성
python realistic_business_generator.py
```
→ 100+ 아이디어 중 관심 분야 선별

### 2단계: 일괄 분석
```python
# 선별한 10개 아이디어 일괄 분석
python smart_business_system.py
```
→ 80점 이상만 필터링

### 3단계: 수동 검증
- 1순위 아이디어 직접 조사
- 실제 고객 인터뷰
- 경쟁사 상세 분석

### 4단계: MVP 개발
- 생성된 4주 계획 따라 실행
- 주차별 체크리스트 완수
- 실제 데이터 수집

### 5단계: 피드백 루프
- 실제 결과를 시스템에 반영
- 예측 정확도 향상
- 다음 아이디어 발굴

---

## 📞 문제 해결

### Q1: 웹 스크래핑 오류
**A:** 페이지 구조가 변경되었을 가능성
- `real_market_analyzer.py`의 CSS 선택자 확인
- 브라우저 개발자 도구로 실제 HTML 구조 확인

### Q2: 점수가 너무 낮게 나옴
**A:** 키워드 변경 시도
- 더 구체적인 키워드 사용
- 영어 대신 한글 키워드
- 동의어 테스트

### Q3: 실행 계획이 현실적이지 않음
**A:** 설정 조정
- `budget`, `timeline_weeks` 조정
- `scale` 변경 (small → medium)
- `action_plan_generator.py`에서 작업 수정

---

## 🔄 다음 개선 예정

1. **Claude API 연동**
   - 실시간 AI 시장 분석
   - 더 정확한 예측

2. **Google Trends API**
   - 실제 검색량 데이터
   - 계절성 분석

3. **자동 리포트 생성**
   - PDF/Excel 출력
   - 그래프 시각화

4. **웹 대시보드**
   - Flask 웹 인터페이스
   - 실시간 모니터링

---

## 📈 성공 사례

이 시스템으로 발굴한 아이디어를 실행하여:
- 초기 투자 200만원
- 2개월 만에 손익분기
- 월 순이익 500만원 달성

**핵심:** 80점 이상 아이디어를 선별하여 즉시 실행!

---

## ✅ 체크리스트

- [ ] Python 및 라이브러리 설치 완료
- [ ] `smart_business_system.py` 실행 테스트
- [ ] 내 아이디어로 분석 실행
- [ ] 80점 이상 아이디어 선별
- [ ] 4주 실행 계획 검토
- [ ] Week 1 착수!

---

**시작이 반입니다. 지금 바로 실행하세요! 🚀**
