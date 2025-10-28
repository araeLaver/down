#!/usr/bin/env python3
"""
안정적인 매시간 사업 발굴 회의 생성 시스템
DB 연결 문제 자동 복구
"""

import time
import json
import os
import sys
from datetime import datetime, timedelta
from database_setup import Session, BusinessMeeting
from realistic_business_generator import RealisticBusinessGenerator
import logging

if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# 로깅 설정
logging.basicConfig(
    filename='meeting_generator.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

class StableHourlyMeeting:
    def __init__(self):
        self.business_generator = RealisticBusinessGenerator()
        self.employees = [
            '알렉스 김', '에밀리 박', '마이클 이', '소피아 최',
            '다니엘 정', '올리비아 한', '라이언 조', '그레이스 윤',
            '벤자민 강', '사만사 임', '조슈아 서', '나탈리 류'
        ]
        self.session = None
        self.reconnect_db()

    def reconnect_db(self):
        """DB 재연결"""
        try:
            if self.session:
                self.session.close()
        except:
            pass

        self.session = Session()
        logging.info("Database connected successfully")

    def conduct_hourly_meeting(self):
        """매시간 사업 발굴 회의 진행"""
        now = datetime.now()
        logging.info(f"Starting meeting at {now}")

        # 실제 스타트업에서 일어날 법한 회의 주제 (날짜와 시간 기반)
        meeting_types = [
            ("주간 매출 리뷰 및 목표 달성률 점검", "매출 데이터 분석 및 개선"),
            ("긴급 CS 이슈 대응 회의", "고객 불만 처리 및 즉시 개선"),
            ("신규 기능 출시 전 최종 점검", "출시 준비 상태 확인"),
            ("월간 KPI 리뷰 및 개선안", "핵심 지표 분석 및 액션플랜"),
            ("고객 이탈 방지 대책 회의", "Churn Rate 감소 전략"),
            ("주간 스프린트 회고", "개발 생산성 및 이슈 점검"),
            ("경쟁사 신제품 분석 긴급 회의", "시장 대응 전략 수립"),
            ("파트너사 계약 조건 협상", "Win-Win 협력 모델 설계"),
            ("투자자 미팅 준비", "IR 자료 점검 및 시연 리허설"),
            ("비용 절감 및 효율화 방안", "운영비 최적화 전략"),
            ("인력 채용 및 조직 확대 회의", "채용 우선순위 및 인터뷰 계획"),
            ("서버 장애 사후 분석 및 재발 방지", "시스템 안정성 개선"),
            ("마케팅 ROI 분석 및 채널 최적화", "광고비 효율 극대화"),
            ("제품 로드맵 우선순위 조정", "고객 요청 vs 기술 부채 균형"),
            ("B2B 세일즈 파이프라인 리뷰", "영업 기회 및 전환율 점검"),
            ("사용자 행동 데이터 분석", "핵심 기능 개선 포인트 도출")
        ]

        # 날짜와 시간을 조합하여 다양한 회의 선택
        index = (now.day * 24 + now.hour) % len(meeting_types)
        selected_type, theme = meeting_types[index]

        print(f"\n{'='*80}")
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {selected_type} ({theme})")
        print(f"{'='*80}")

        try:
            opportunities = self.business_generator.generate_monthly_opportunities()
            high_viability = self.business_generator.generate_high_viability_themes()
        except Exception as e:
            logging.error(f"Failed to generate opportunities: {e}")
            opportunities = []
            high_viability = []

        # 현실적인 회의 안건 (실제 스타트업 시나리오)
        all_agendas = {
            "주간 매출 리뷰 및 목표 달성률 점검": [
                "이번 주 매출 실적: 목표 대비 달성률 분석",
                "주요 상품별/채널별 매출 비중 및 트렌드",
                "미달성 원인 분석 및 즉시 개선 가능한 항목",
                "다음 주 매출 목표 및 액션플랜 수립"
            ],
            "긴급 CS 이슈 대응 회의": [
                "주요 고객 불만 사항 TOP 3 공유",
                "긴급 대응이 필요한 케이스 우선순위 결정",
                "CS 팀 리소스 재배치 및 에스컬레이션 프로세스",
                "재발 방지를 위한 시스템/프로세스 개선안"
            ],
            "신규 기능 출시 전 최종 점검": [
                "QA 완료 상태 및 Critical Bug 여부 확인",
                "출시 일정, 배포 시간, 롤백 계획 점검",
                "고객 공지 메시지 및 가이드 자료 준비 상태",
                "출시 후 모니터링 지표 및 담당자 배정"
            ],
            "월간 KPI 리뷰 및 개선안": [
                "MAU, DAU, Retention Rate 등 핵심 지표 분석",
                "전월 대비 증감 원인 및 인사이트 도출",
                "목표 미달 지표에 대한 개선 액션플랜",
                "다음 달 KPI 목표 설정 및 책임자 지정"
            ],
            "고객 이탈 방지 대책 회의": [
                "최근 1개월 Churn Rate 분석 및 이탈 패턴 파악",
                "이탈 고객 인터뷰 결과 및 주요 불만 사항",
                "리텐션 개선을 위한 기능/서비스 우선순위",
                "재활성화 캠페인 기획 및 예상 효과 시뮬레이션"
            ],
            "주간 스프린트 회고": [
                "지난 스프린트에서 완료된 태스크 및 성과",
                "미완료 항목 및 블로커 원인 분석",
                "팀 협업, 커뮤니케이션에서 개선할 점",
                "다음 스프린트 우선순위 및 용량 계획"
            ],
            "경쟁사 신제품 분석 긴급 회의": [
                "경쟁사 신제품 주요 기능 및 차별화 포인트",
                "우리 제품 대비 강점/약점 비교 분석",
                "시장 반응 및 고객 이탈 위험도 평가",
                "대응 전략: 빠른 Follow-up vs 차별화 강화"
            ],
            "파트너사 계약 조건 협상": [
                "파트너사 제안 조건 검토 (수수료, 계약 기간 등)",
                "우리 측 요구사항 및 협상 가능한 범위 설정",
                "Win-Win 모델 설계 및 예상 수익 시뮬레이션",
                "최종 계약서 검토 및 리스크 체크리스트"
            ],
            "투자자 미팅 준비": [
                "IR 피칭 자료 최종 검토 (비전, 시장, 성과, 계획)",
                "예상 질문 Q&A 리스트 및 답변 시나리오",
                "제품 데모 시연 리허설 및 피드백",
                "투자 조건 및 협상 전략 사전 조율"
            ],
            "비용 절감 및 효율화 방안": [
                "부서별 운영비 현황 및 불필요한 지출 항목 점검",
                "SaaS 구독 서비스 사용률 분석 및 통폐합",
                "인력 효율화: 업무 자동화 및 아웃소싱 검토",
                "절감 목표 금액 설정 및 실행 계획 수립"
            ],
            "인력 채용 및 조직 확대 회의": [
                "긴급 채용 포지션 및 우선순위 결정",
                "채용 공고 문구 검토 및 채널 선정",
                "지원자 스크리닝 기준 및 인터뷰 일정 조율",
                "온보딩 프로세스 점검 및 멘토 배정 계획"
            ],
            "서버 장애 사후 분석 및 재발 방지": [
                "장애 발생 시간대, 원인, 영향 범위 정리",
                "대응 과정 타임라인 및 초동 조치 평가",
                "근본 원인 분석 (Root Cause Analysis)",
                "재발 방지 대책: 모니터링 강화, 이중화 등"
            ],
            "마케팅 ROI 분석 및 채널 최적화": [
                "채널별 광고비 집행 현황 및 전환율 분석",
                "CAC(고객 획득 비용) vs LTV(생애 가치) 비교",
                "성과 높은 채널 예산 확대 및 저성과 채널 축소",
                "A/B 테스트 결과 기반 크리에이티브 최적화"
            ],
            "제품 로드맵 우선순위 조정": [
                "고객 요청 기능 TOP 10 및 Impact 분석",
                "기술 부채 항목 및 시급도 평가",
                "리소스 제약 고려한 분기별 우선순위 재조정",
                "로드맵 변경 시 이해관계자 커뮤니케이션 계획"
            ],
            "B2B 세일즈 파이프라인 리뷰": [
                "영업 단계별 딜 현황 (Discovery, Proposal, Negotiation)",
                "Close 예정 딜 및 주요 장애물 점검",
                "전환율 낮은 단계 원인 분석 및 개선 방안",
                "다음 분기 영업 목표 및 전략 수립"
            ],
            "사용자 행동 데이터 분석": [
                "주요 기능별 사용률 및 이탈 구간 분석",
                "사용자 여정(User Journey) 병목 지점 파악",
                "A/B 테스트 결과 및 인사이트 도출",
                "우선 개선 기능 선정 및 개발 착수"
            ]
        }

        agendas = all_agendas.get(selected_type, [
            "전날 진행사항 검토",
            "오늘의 우선순위 설정",
            "이슈 및 해결방안 논의",
            "다음 단계 계획 수립"
        ])

        # 회의 유형별 현실적인 결정사항 및 실행항목 생성
        import random
        random.seed(now.day * 100 + now.hour)

        # 회의 타입별 결정사항과 실행항목
        decisions_and_actions = {
            "주간 매출 리뷰 및 목표 달성률 점검": {
                "business_topics": [
                    f"신규 수익 모델: {random.choice(['B2B 엔터프라이즈 플랜 출시', '프리미엄 애드온 기능 판매', '화이트라벨 솔루션 제공'])}",
                    f"확장 채널: {random.choice(['대기업 파트너십', '리셀러 프로그램', '해외 진출 (동남아)'])}",
                    f"교차 판매 기회: {random.choice(['기존 고객 업셀링', '번들 상품 패키지', '추천 프로그램 강화'])}"
                ],
                "decisions": [
                    f"이번 주 매출: 목표 대비 {random.randint(85, 115)}% 달성",
                    f"주요 히트 상품: {random.choice(['프리미엄 구독', 'API 이용권', '프로 플랜'])} - 전주 대비 {random.randint(10, 40)}% 증가",
                    f"개선 필요 채널: {random.choice(['온라인 광고', 'SNS 마케팅', '제휴 판매'])} 전환율 {random.randint(1, 3)}% 미달",
                    f"다음 주 매출 목표: {random.randint(5000, 8000)}만원 (전주 대비 {random.randint(10, 20)}% 상향)"
                ],
                "actions": [
                    "매출 부진 채널 긴급 개선안 수립 및 실행 (2일 내)",
                    "히트 상품 추가 프로모션 기획 및 집행 (3일 내)",
                    "고객 구매 패턴 분석 리포트 작성 (5일 내)",
                    "영업팀 일일 목표 달성률 모니터링 강화"
                ]
            },
            "긴급 CS 이슈 대응 회의": {
                "business_topics": [
                    f"CS 자동화: AI 챗봇 도입으로 반복 문의 80% 자동 처리",
                    f"프리미엄 지원 서비스: VIP 고객 전담 팀 운영 (추가 요금제)",
                    f"셀프 서비스 강화: FAQ, 튜토리얼 비디오 확충",
                ],
                "decisions": [
                    f"금일 접수된 긴급 이슈 {random.randint(3, 8)}건 중 {random.randint(2, 4)}건 즉시 처리 완료",
                    f"주요 불만: {random.choice(['결제 오류', '로그인 실패', '느린 응답 속도'])} - 시스템 개선 필요",
                    "CS 응대 시간 단축 목표: 평균 2시간 → 1시간 이내",
                    f"VIP 고객 {random.randint(2, 5)}명 직접 응대 및 보상 제공 결정"
                ],
                "actions": [
                    "주요 이슈 원인 파악 및 핫픽스 배포 (당일 18시까지)",
                    "고객 사과 문자 및 보상 쿠폰 발송 (내일 10시)",
                    "CS 매뉴얼 업데이트 및 팀 공유 (2일 내)",
                    "재발 방지 시스템 점검 및 모니터링 강화"
                ]
            },
            "신규 기능 출시 전 최종 점검": {
                "business_topics": [
                    f"신규 기능: {random.choice(['AI 추천 엔진', '실시간 협업 기능', '고급 분석 대시보드'])}",
                    f"프리미엄 Tier 출시: 고급 기능을 유료화하여 ARPU 증대",
                    f"얼리어댑터 프로그램: 베타 테스터를 유료 고객으로 전환",
                ],
                "decisions": [
                    f"출시 예정일: {(now + timedelta(days=random.randint(1, 3))).strftime('%m월 %d일 %H시')}",
                    f"QA 통과율: {random.randint(92, 100)}% (Critical Bug {random.randint(0, 2)}건 해결 완료)",
                    f"베타 테스터 피드백 반영: {random.randint(8, 15)}개 항목 중 {random.randint(5, 12)}개 적용",
                    "출시 후 24시간 집중 모니터링 체계 가동"
                ],
                "actions": [
                    "남은 버그 최종 수정 및 재테스트 (출시 2시간 전)",
                    "고객 공지 이메일/푸시 발송 (출시 1시간 전)",
                    "출시 당일 온콜 엔지니어 배치 및 대기",
                    "사용자 피드백 수집 채널 오픈 및 모니터링"
                ]
            },
            "월간 KPI 리뷰 및 개선안": {
                "business_topics": [
                    f"성장 가속: {random.choice(['바이럴 마케팅', '레퍼럴 프로그램', '인플루언서 협업'])}",
                    f"신규 시장 진출: {random.choice(['교육 기관', '정부 기관', '중소기업'])} 타겟팅",
                    f"수익화 강화: 무료→유료 전환율 개선 전략",
                ],
                "decisions": [
                    f"MAU: {random.randint(15000, 25000)}명 (전월 대비 {random.randint(-10, 20):+d}%)",
                    f"Retention Rate (D7): {random.randint(35, 60)}% (목표 {random.randint(40, 50)}%)",
                    f"전환율: {random.uniform(2.5, 5.5):.1f}% (업계 평균 {random.uniform(3.0, 4.5):.1f}%)",
                    f"목표 미달 지표: {random.choice(['신규 가입', '재방문율', '구매 전환'])} - 집중 개선 필요"
                ],
                "actions": [
                    "Retention 개선 캠페인 기획 (7일 내)",
                    "전환율 향상 A/B 테스트 설계 및 실행 (10일 내)",
                    "이탈 사용자 인터뷰 진행 (5일 내, 20명 목표)",
                    "다음 달 KPI 목표 재설정 및 전사 공유"
                ]
            },
            "고객 이탈 방지 대책 회의": {
                "business_topics": [
                    f"로열티 프로그램: 장기 고객 리워드 시스템 도입",
                    f"맞춤형 리텐션: 이탈 위험 고객 자동 감지 및 개인화 혜택",
                    f"커뮤니티 구축: 사용자 커뮤니티로 Lock-in 효과 강화",
                ],
                "decisions": [
                    f"이번 달 Churn Rate: {random.uniform(5, 15):.1f}% (전월 대비 {random.uniform(-2, 3):+.1f}%p)",
                    f"주요 이탈 원인: {random.choice(['가격 부담', '기능 부족', '사용 불편'])} ({random.randint(30, 50)}%)",
                    f"재활성화 대상 고객: {random.randint(500, 1500)}명 선정",
                    "이탈 방지 예산 증액: 월 500만원 → 800만원"
                ],
                "actions": [
                    "이탈 예정 고객 타겟 푸시/이메일 발송 (3일 내)",
                    "특별 할인 쿠폰 제공 캠페인 시작 (즉시)",
                    "이탈 사용자 서베이 실시 및 분석 (7일 내)",
                    "핵심 기능 개선 로드맵 수립 (10일 내)"
                ]
            },
            "주간 스프린트 회고": {
                "business_topics": [
                    f"개발 생산성 툴: {random.choice(['CI/CD 파이프라인 개선', 'Low-code 도입', 'AI 코딩 어시스턴트'])}",
                    f"기술 스택 현대화: 레거시 시스템 마이그레이션",
                    f"오픈소스 기여: 자사 도구 오픈소스화로 브랜딩",
                ],
                "decisions": [
                    f"완료된 스토리 포인트: {random.randint(25, 45)}/{random.randint(40, 50)} ({random.randint(60, 100)}% 달성)",
                    f"주요 블로커: {random.choice(['API 연동 지연', '디자인 리소스 부족', '요구사항 변경'])}",
                    f"팀 만족도: {random.randint(3, 5)}/5 (전주 대비 {random.choice(['유지', '상승', '하락'])})",
                    "다음 스프린트 목표: 기술 부채 해소 20% + 신규 기능 3개"
                ],
                "actions": [
                    "미완료 태스크 재평가 및 백로그 이동",
                    "블로커 해결 방안 즉시 실행 (2일 내)",
                    "다음 스프린트 계획 회의 소집 (내일 10시)",
                    "팀 프로세스 개선안 Wiki 문서화"
                ]
            },
            "경쟁사 신제품 분석 긴급 회의": {
                "business_topics": [
                    f"차별화 포인트 강화: {random.choice(['독보적 AI 기술', '업계 최고 보안', '최저 가격 보장'])}",
                    f"블루오션 전략: 경쟁사가 놓친 니치 시장 공략",
                    f"파트너십 강화: 경쟁사 대신 우리와 제휴하도록 유도",
                ],
                "decisions": [
                    f"경쟁사: {random.choice(['A사', 'B사', 'C사'])} 신제품 출시 ({now.strftime('%m월 %d일')})",
                    f"주요 차별화: {random.choice(['AI 기능 탑재', '가격 30% 인하', '모바일 최적화'])}",
                    f"예상 고객 이탈 위험도: {random.choice(['낮음', '보통', '높음'])}",
                    f"대응 전략: {random.choice(['빠른 Follow-up', '차별화 강화', '가격 경쟁력 확보'])}"
                ],
                "actions": [
                    "경쟁사 제품 상세 분석 리포트 작성 (3일 내)",
                    "우리 제품 강점 마케팅 캠페인 즉시 시작",
                    "고객 이탈 방지 특별 프로모션 기획 (5일 내)",
                    "차별화 기능 개발 착수 (긴급 스프린트 편성)"
                ]
            },
            "파트너사 계약 조건 협상": {
                "business_topics": [
                    f"전략적 제휴: {random.choice(['대기업과 공동 마케팅', '유통망 확보', '기술 크로스 라이선싱'])}",
                    f"수익 다각화: 파트너 네트워크 통한 간접 매출 창출",
                    f"Win-Win 모델: 리셀러 프로그램으로 시장 확대",
                ],
                "decisions": [
                    f"제안 수수료율: {random.randint(10, 30)}% → 최종 {random.randint(15, 25)}%로 합의",
                    f"계약 기간: {random.choice(['1년', '2년', '3년'])} + 자동 연장 조항 포함",
                    f"예상 월 수익: {random.randint(500, 2000)}만원 (MG: {random.randint(200, 800)}만원)",
                    "계약 체결 목표일: 이번 주 금요일까지"
                ],
                "actions": [
                    "법무팀 계약서 최종 검토 요청 (2일 내)",
                    "파트너사 담당자와 세부 조율 미팅 (내일)",
                    "내부 승인 프로세스 진행 (임원 결재)",
                    "계약 체결 후 킥오프 미팅 일정 조율"
                ]
            },
            "투자자 미팅 준비": {
                "business_topics": [
                    f"투자 활용 계획: {random.choice(['해외 진출 자금', '인력 확충', 'R&D 투자'])}",
                    f"엑싯 시나리오: {random.choice(['IPO', 'M&A', '전략적 인수'])} 로드맵 제시",
                    f"성장 스토리: 시장 규모 X 우리 점유율 X 수익성 입증",
                ],
                "decisions": [
                    f"미팅 일정: {(now + timedelta(days=random.randint(3, 10))).strftime('%m월 %d일 %H시')}",
                    f"목표 투자 유치액: {random.randint(10, 50)}억원 (Valuation: {random.randint(100, 500)}억원)",
                    f"IR 피칭 시간: {random.randint(15, 30)}분 + Q&A {random.randint(15, 30)}분",
                    "핵심 메시지: 시장 성장성 + 우리만의 기술력 + 트랙션"
                ],
                "actions": [
                    "IR 자료 최종 수정 및 인쇄 (미팅 1일 전)",
                    "데모 시연 리허설 3회 실시 (내일부터)",
                    "예상 질문 50개 준비 및 답변 스크립트 작성",
                    "투자자 배경 조사 및 관심사 파악"
                ]
            },
            "비용 절감 및 효율화 방안": {
                "business_topics": [
                    f"자동화 투자: RPA로 반복 업무 제거하여 인건비 절감",
                    f"클라우드 최적화: 서버 비용 30% 절감 (Reserved Instance, Spot)",
                    f"아웃소싱 전환: 비핵심 업무 외주화로 고정비 변동비화",
                ],
                "decisions": [
                    f"이번 달 총 운영비: {random.randint(3000, 8000)}만원 (예산 대비 {random.randint(-10, 20):+d}%)",
                    f"절감 가능 항목: {random.randint(5, 15)}개 발굴 (예상 절감액: {random.randint(300, 800)}만원/월)",
                    f"미사용 SaaS: {random.randint(3, 8)}개 해지 결정",
                    "목표 절감률: 다음 분기 15% 비용 감축"
                ],
                "actions": [
                    "부서별 불필요 지출 항목 정리 및 보고 (3일 내)",
                    "SaaS 계약 재협상 또는 해지 진행 (7일 내)",
                    "업무 자동화 도구 도입 검토 (10일 내)",
                    "월간 비용 리포트 자동화 시스템 구축"
                ]
            },
            "인력 채용 및 조직 확대 회의": {
                "business_topics": [
                    f"인재 영입 전략: {random.choice(['주식 옵션 제공', '원격 근무 허용', '경력 개발 지원'])}",
                    f"조직 문화: 강점화로 인재 유치 및 retention",
                    f"글로벌 채용: 해외 우수 인력 원격 채용",
                ],
                "decisions": [
                    f"긴급 채용 포지션: {random.choice(['백엔드 개발자', '프론트엔드 개발자', '마케터', 'CS 매니저'])} {random.randint(1, 3)}명",
                    f"채용 예산: 1인당 연봉 {random.randint(4000, 7000)}만원 (총 {random.randint(5000, 15000)}만원)",
                    "채용 목표일: 이번 달 말까지 최소 1명 확정",
                    f"온보딩 기간: {random.randint(2, 4)}주 (멘토: 팀장급 배정)"
                ],
                "actions": [
                    "채용 공고 작성 및 잡플랫폼 게시 (2일 내)",
                    "헤드헌터 의뢰 및 추천 후보 검토",
                    "지원자 서류 스크리닝 기준 정리 (내일)",
                    "1차 인터뷰 일정 조율 (다음 주부터)"
                ]
            },
            "서버 장애 사후 분석 및 재발 방지": {
                "business_topics": [
                    f"인프라 사업: 안정성 노하우를 B2B 클라우드 서비스로 상품화",
                    f"SLA 보장 상품: 가용성 99.99% 보장 프리미엄 플랜",
                    f"재해 복구 서비스: DR(Disaster Recovery) 솔루션 판매",
                ],
                "decisions": [
                    f"장애 발생 시간: {(now - timedelta(hours=random.randint(12, 48))).strftime('%m월 %d일 %H시')} (총 {random.randint(15, 180)}분)",
                    f"원인: {random.choice(['DB 과부하', 'API Rate Limit 초과', '메모리 누수', 'CDN 장애'])}",
                    f"영향 범위: 전체 사용자의 {random.randint(10, 100)}% ({random.randint(1000, 10000)}명)",
                    "재발 방지 대책: 모니터링 강화 + 이중화 + Auto-scaling"
                ],
                "actions": [
                    "Root Cause Analysis 상세 보고서 작성 (2일 내)",
                    "모니터링 Alert 임계값 재조정 (즉시)",
                    "DB 성능 최적화 및 인덱스 추가 (3일 내)",
                    "장애 대응 매뉴얼 업데이트 및 훈련"
                ]
            },
            "마케팅 ROI 분석 및 채널 최적화": {
                "business_topics": [
                    f"퍼포먼스 마케팅 강화: 데이터 기반 실시간 최적화",
                    f"브랜드 마케팅: 장기적 브랜드 가치 구축 투자",
                    f"바이럴 콘텐츠: 자발적 공유 유도하여 CAC 절감",
                ],
                "decisions": [
                    f"총 광고비: {random.randint(1000, 5000)}만원 (ROI: {random.uniform(1.5, 4.0):.1f}x)",
                    f"최고 성과 채널: {random.choice(['Google Ads', 'Facebook', 'Instagram', '카카오'])} (ROI {random.uniform(3.0, 5.0):.1f}x)",
                    f"CAC: {random.randint(5000, 20000)}원 / LTV: {random.randint(50000, 150000)}원",
                    f"예산 재배분: 고성과 채널 +{random.randint(30, 50)}%, 저성과 채널 -{random.randint(30, 50)}%"
                ],
                "actions": [
                    "고성과 채널 예산 즉시 증액 및 캠페인 확대",
                    "저성과 채널 크리에이티브 A/B 테스트 (5일 내)",
                    "신규 채널 테스트 예산 배정 (월 200만원)",
                    "주간 ROI 리포트 자동화 대시보드 구축"
                ]
            },
            "제품 로드맵 우선순위 조정": {
                "business_topics": [
                    f"신제품 라인: {random.choice(['모바일 앱 출시', 'API 플랫폼', '화이트라벨 솔루션'])}",
                    f"수직 통합: 연관 제품군 인수하여 생태계 구축",
                    f"플랫폼화: 써드파티 개발자 유치하여 확장",
                ],
                "decisions": [
                    f"고객 요청 기능 TOP 3: {random.choice(['다크모드', '엑셀 내보내기', '알림 커스터마이징'])}",
                    f"기술 부채 긴급도: {random.choice(['높음', '보통'])} - 리팩토링 시간 {random.randint(2, 4)}주 필요",
                    "이번 분기 우선순위: 고객 요청 60% + 기술 부채 40%",
                    f"다음 릴리즈: {(now + timedelta(weeks=random.randint(2, 6))).strftime('%m월 %d일')}"
                ],
                "actions": [
                    "로드맵 수정안 작성 및 이해관계자 공유 (3일 내)",
                    "우선순위 변경에 따른 리소스 재배치",
                    "고객 대상 로드맵 공개 및 피드백 수집",
                    "분기별 릴리즈 일정 확정 및 공지"
                ]
            },
            "B2B 세일즈 파이프라인 리뷰": {
                "business_topics": [
                    f"엔터프라이즈 영업: 대기업 전담 세일즈 팀 신설",
                    f"채널 파트너: 리셀러, SI 파트너 네트워크 구축",
                    f"인바운드 강화: 콘텐츠 마케팅으로 리드 자동 생성",
                ],
                "decisions": [
                    f"현재 파이프라인 딜: {random.randint(10, 30)}개 (총액 {random.randint(5, 20)}억원)",
                    f"Close 예정: {random.randint(2, 5)}개 (이번 달 내, 예상 계약액 {random.randint(1, 5)}억원)",
                    f"전환율: Discovery→Proposal {random.randint(30, 60)}%, Proposal→Close {random.randint(20, 40)}%",
                    "주요 장애물: 가격 협상 + 의사결정 지연"
                ],
                "actions": [
                    "Close 예정 딜 집중 팔로업 (매일 1회 이상)",
                    "가격 협상 가이드라인 재정비 (3일 내)",
                    "저전환율 구간 세일즈 스크립트 개선",
                    "다음 분기 영업 목표 및 인센티브 설계"
                ]
            },
            "사용자 행동 데이터 분석": {
                "business_topics": [
                    f"데이터 기반 신사업: 사용자 데이터 분석 인사이트를 컨설팅 상품화",
                    f"개인화 서비스: AI 추천으로 사용자 경험 극대화",
                    f"프로덕트 애널리틱스: 분석 도구 자체를 B2B 제품으로 판매",
                ],
                "decisions": [
                    f"핵심 기능 사용률: {random.choice(['검색', '필터', '대시보드', '리포트'])} {random.randint(60, 90)}%",
                    f"이탈 구간: {random.choice(['온보딩 2단계', '결제 페이지', '설정 화면'])} ({random.randint(30, 60)}% 이탈)",
                    f"A/B 테스트 결과: 버전 B가 전환율 {random.randint(10, 40)}% 높음",
                    "우선 개선 기능: 이탈율 높은 구간 UX 개선"
                ],
                "actions": [
                    "이탈 구간 UX 개선안 설계 (5일 내)",
                    "A/B 테스트 승자 버전 100% 배포 (즉시)",
                    "사용자 인터뷰 10명 진행 (7일 내)",
                    "주요 기능 튜토리얼 강화 (10일 내)"
                ]
            }
        }

        # 현재 회의 타입에 맞는 내용 가져오기
        meeting_data = decisions_and_actions.get(selected_type)

        if meeting_data:
            key_decisions = [
                f"[{now.strftime('%Y-%m-%d %H:%M')}] {selected_type} 결과"
            ] + meeting_data["decisions"]

            action_items = meeting_data["actions"]

            print(f"\n[결정] {len(key_decisions)}개 핵심 결정사항")
            print(f"[실행] {len(action_items)}개 액션 아이템")
        else:
            key_decisions = [
                f"{now.strftime('%Y년 %m월 %d일')} {selected_type} 결과",
                "현황 분석 완료",
                "개선 방향 설정",
                "실행 계획 수립"
            ]
            action_items = [
                f"현재 진행 중인 프로젝트 상태 점검 ({now.strftime('%m월 %d일')})",
                "팀별 주간 보고서 제출 요청 (2일 내)",
                "다음 분기 계획 초안 작성 (7일 내)"
            ]

        meeting = BusinessMeeting(
            meeting_type=selected_type,
            title=f"Qhyx Inc. {selected_type} - {now.strftime('%Y-%m-%d')}",
            agenda=json.dumps(agendas, ensure_ascii=False),
            participants=json.dumps(self.employees, ensure_ascii=False),
            key_decisions=key_decisions,
            action_items=action_items,
            status='completed',
            meeting_notes=json.dumps({
                'meeting_theme': theme,
                'meeting_duration': '45분',
                'participants_count': len(self.employees),
                'agenda_items': len(agendas),
                'decisions_count': len(key_decisions),
                'action_items_count': len(action_items),
                'business_topics': meeting_data.get('business_topics', []) if meeting_data else []
            }, ensure_ascii=False)
        )

        # DB 저장 시도 (재시도 로직 포함)
        for attempt in range(3):
            try:
                self.session.add(meeting)
                self.session.commit()
                print(f"\n[OK] 회의 완료 - DB 저장 완료")
                logging.info(f"Meeting saved successfully: {meeting.title}")
                break
            except Exception as e:
                logging.error(f"DB save attempt {attempt+1} failed: {e}")
                print(f"\n[ERROR] DB 저장 실패 (시도 {attempt+1}/3): {e}")

                try:
                    self.session.rollback()
                except:
                    pass

                self.reconnect_db()

                if attempt == 2:
                    print("[FINAL ERROR] DB 저장 최종 실패")
                    logging.error("Failed to save meeting after 3 attempts")

        print(f"   결정사항: {len(key_decisions)}개")
        print(f"   실행항목: {len(action_items)}개")
        print(f"{'='*80}\n")

    def run_hourly(self):
        """매시간 정각에 실행"""
        print("[START] 안정적인 매시간 사업 발굴 회의 시스템")
        print("[TIME] 매시간 정각에 자동으로 회의 생성")
        print("[LOG] meeting_generator.log 파일에 로그 기록")
        print("[STOP] Ctrl+C로 종료\n")

        logging.info("System started")

        last_hour = -1
        consecutive_errors = 0

        while True:
            try:
                now = datetime.now()
                current_hour = now.hour
                current_minute = now.minute

                # 매시간 00분에 실행
                if current_minute == 0 and current_hour != last_hour:
                    self.conduct_hourly_meeting()
                    last_hour = current_hour
                    consecutive_errors = 0
                    time.sleep(60)
                else:
                    # 30초마다 체크
                    time.sleep(30)

            except KeyboardInterrupt:
                print("\n\n시스템 종료")
                logging.info("System stopped by user")
                break
            except Exception as e:
                consecutive_errors += 1
                print(f"[ERROR] 시스템 오류: {e}")
                logging.error(f"System error: {e}")

                if consecutive_errors > 10:
                    print("[CRITICAL] 연속 오류 10회 초과 - 재시작 필요")
                    logging.critical("Too many consecutive errors - restart needed")
                    time.sleep(300)  # 5분 대기
                else:
                    time.sleep(60)

if __name__ == "__main__":
    system = StableHourlyMeeting()

    # 시작하자마자 한번 실행
    try:
        system.conduct_hourly_meeting()
    except Exception as e:
        print(f"Initial meeting failed: {e}")
        logging.error(f"Initial meeting failed: {e}")

    # 매시간 실행
    system.run_hourly()