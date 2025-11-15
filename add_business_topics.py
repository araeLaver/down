#!/usr/bin/env python3
"""모든 회의 타입에 사업 주제 추가"""

import re

# 각 회의 타입별 사업 주제
business_topics_map = {
    "긴급 CS 이슈 대응 회의": [
        "CS 자동화: AI 챗봇 도입으로 반복 문의 80% 자동 처리",
        "프리미엄 지원 서비스: VIP 고객 전담 팀 운영 (추가 요금제)",
        "셀프 서비스 강화: FAQ, 튜토리얼 비디오 확충"
    ],
    "신규 기능 출시 전 최종 점검": [
        "신규 기능: {random.choice(['AI 추천 엔진', '실시간 협업 기능', '고급 분석 대시보드'])}",
        "프리미엄 Tier 출시: 고급 기능을 유료화하여 ARPU 증대",
        "얼리어댑터 프로그램: 베타 테스터를 유료 고객으로 전환"
    ],
    "월간 KPI 리뷰 및 개선안": [
        "성장 가속: {random.choice(['바이럴 마케팅', '레퍼럴 프로그램', '인플루언서 협업'])}",
        "신규 시장 진출: {random.choice(['교육 기관', '정부 기관', '중소기업'])} 타겟팅",
        "수익화 강화: 무료→유료 전환율 개선 전략"
    ],
    "고객 이탈 방지 대책 회의": [
        "로열티 프로그램: 장기 고객 리워드 시스템 도입",
        "맞춤형 리텐션: 이탈 위험 고객 자동 감지 및 개인화 혜택",
        "커뮤니티 구축: 사용자 커뮤니티로 Lock-in 효과 강화"
    ],
    "주간 스프린트 회고": [
        "개발 생산성 툴: {random.choice(['CI/CD 파이프라인 개선', 'Low-code 도입', 'AI 코딩 어시스턴트'])}",
        "기술 스택 현대화: 레거시 시스템 마이그레이션",
        "오픈소스 기여: 자사 도구 오픈소스화로 브랜딩"
    ],
    "경쟁사 신제품 분석 긴급 회의": [
        "차별화 포인트 강화: {random.choice(['독보적 AI 기술', '업계 최고 보안', '최저 가격 보장'])}",
        "블루오션 전략: 경쟁사가 놓친 니치 시장 공략",
        "파트너십 강화: 경쟁사 대신 우리와 제휴하도록 유도"
    ],
    "파트너사 계약 조건 협상": [
        "전략적 제휴: {random.choice(['대기업과 공동 마케팅', '유통망 확보', '기술 크로스 라이선싱'])}",
        "수익 다각화: 파트너 네트워크 통한 간접 매출 창출",
        "Win-Win 모델: 리셀러 프로그램으로 시장 확대"
    ],
    "투자자 미팅 준비": [
        "투자 활용 계획: {random.choice(['해외 진출 자금', '인력 확충', 'R&D 투자'])}",
        "엑싯 시나리오: {random.choice(['IPO', 'M&A', '전략적 인수'])} 로드맵 제시",
        "성장 스토리: 시장 규모 X 우리 점유율 X 수익성 입증"
    ],
    "비용 절감 및 효율화 방안": [
        "자동화 투자: RPA로 반복 업무 제거하여 인건비 절감",
        "클라우드 최적화: 서버 비용 30% 절감 (Reserved Instance, Spot)",
        "아웃소싱 전환: 비핵심 업무 외주화로 고정비 변동비화"
    ],
    "인력 채용 및 조직 확대 회의": [
        "인재 영입 전략: {random.choice(['주식 옵션 제공', '원격 근무 허용', '경력 개발 지원'])}",
        "조직 문화: 강점화로 인재 유치 및 retention",
        "글로벌 채용: 해외 우수 인력 원격 채용"
    ],
    "서버 장애 사후 분석 및 재발 방지": [
        "인프라 사업: 안정성 노하우를 B2B 클라우드 서비스로 상품화",
        "SLA 보장 상품: 가용성 99.99% 보장 프리미엄 플랜",
        "재해 복구 서비스: DR(Disaster Recovery) 솔루션 판매"
    ],
    "마케팅 ROI 분석 및 채널 최적화": [
        "퍼포먼스 마케팅 강화: 데이터 기반 실시간 최적화",
        "브랜드 마케팅: 장기적 브랜드 가치 구축 투자",
        "바이럴 콘텐츠: 자발적 공유 유도하여 CAC 절감"
    ],
    "제품 로드맵 우선순위 조정": [
        "신제품 라인: {random.choice(['모바일 앱 출시', 'API 플랫폼', '화이트라벨 솔루션'])}",
        "수직 통합: 연관 제품군 인수하여 생태계 구축",
        "플랫폼화: 써드파티 개발자 유치하여 확장"
    ],
    "B2B 세일즈 파이프라인 리뷰": [
        "엔터프라이즈 영업: 대기업 전담 세일즈 팀 신설",
        "채널 파트너: 리셀러, SI 파트너 네트워크 구축",
        "인바운드 강화: 콘텐츠 마케팅으로 리드 자동 생성"
    ],
    "사용자 행동 데이터 분석": [
        "데이터 기반 신사업: 사용자 데이터 분석 인사이트를 컨설팅 상품화",
        "개인화 서비스: AI 추천으로 사용자 경험 극대화",
        "프로덕트 애널리틱스: 분석 도구 자체를 B2B 제품으로 판매"
    ]
}

# 파일 읽기
with open('stable_hourly_meeting.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 각 회의 타입에 business_topics 추가
for meeting_type, topics in business_topics_map.items():
    # "meeting_type": { 패턴 찾기
    pattern = f'"{meeting_type}": {{\\s+"decisions":'
    replacement = f'"{meeting_type}": {{\n                "business_topics": [\n'
    for topic in topics:
        replacement += f'                    f"{topic}",\n'
    replacement += '                ],\n                "decisions":'

    content = re.sub(pattern, replacement, content)

# meeting_notes에 business_topics 추가 부분 수정
old_notes_pattern = r"meeting_notes=json\.dumps\(\{[\s\S]*?\}, ensure_ascii=False\)"
new_notes = """meeting_notes=json.dumps({
                'meeting_theme': theme,
                'meeting_duration': '45분',
                'participants_count': len(self.employees),
                'agenda_items': len(agendas),
                'decisions_count': len(key_decisions),
                'action_items_count': len(action_items),
                'business_topics': meeting_data.get('business_topics', []) if meeting_data else []
            }, ensure_ascii=False)"""

content = re.sub(old_notes_pattern, new_notes, content)

# 파일 쓰기
with open('stable_hourly_meeting.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Business topics added successfully!")
