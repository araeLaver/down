import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

NAVY = '#1B2A4A'
BLUE = '#2E86AB'
LIGHT_BLUE = '#E8F4F8'
GREEN = '#28A745'
LIGHT_GREEN = '#E8F5E9'
ORANGE = '#F5A623'
LIGHT_ORANGE = '#FFF3E0'
PURPLE = '#6C5CE7'
LIGHT_PURPLE = '#F0EDFF'
GRAY = '#F5F5F5'
DARK_GRAY = '#555555'
WHITE = '#FFFFFF'

# ================================================================
# IMAGE 1: 서비스 흐름도
# ================================================================
fig, ax = plt.subplots(1, 1, figsize=(20, 14), dpi=250)
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')
fig.patch.set_facecolor('#FFFFFF')

ax.text(10, 13.3, '렌트미 (RentMe) 서비스 흐름도', fontsize=26, fontweight='bold',
        ha='center', va='center', color=NAVY)
ax.text(10, 12.8, '"좋은 세입자임을 증명하면 보증금이 달라집니다"', fontsize=14,
        ha='center', va='center', color=DARK_GRAY, style='italic')

# STEP 1
box1 = FancyBboxPatch((0.5, 8.5), 4.2, 3.8, boxstyle='round,pad=0.15',
                       facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=2)
ax.add_patch(box1)
ax.text(2.6, 11.8, 'STEP 1', fontsize=11, fontweight='bold', ha='center', color=BLUE)
ax.text(2.6, 11.3, '프로필 생성', fontsize=16, fontweight='bold', ha='center', color=NAVY)
ax.plot([1.2, 4.0], [11.05, 11.05], color=BLUE, linewidth=1.5)
for i, item in enumerate(['기본정보 (나이, 가구형태)', '라이프스타일 (흡연, 반려동물)',
                           'LLM AI 자기소개서 자동 생성', '희망 지역 / 예산 설정']):
    ax.text(2.6, 10.5 - i*0.5, item, fontsize=10, ha='center', va='center', color=DARK_GRAY)

ax.annotate('', xy=(5.3, 10.4), xytext=(4.9, 10.4),
            arrowprops=dict(arrowstyle='->', color=NAVY, lw=2.5))

# STEP 2
box2 = FancyBboxPatch((5.5, 8.5), 4.2, 3.8, boxstyle='round,pad=0.15',
                       facecolor=LIGHT_GREEN, edgecolor=GREEN, linewidth=2)
ax.add_patch(box2)
ax.text(7.6, 11.8, 'STEP 2', fontsize=11, fontweight='bold', ha='center', color=GREEN)
ax.text(7.6, 11.3, '마이데이터 신뢰 인증', fontsize=15, fontweight='bold', ha='center', color=NAVY)
ax.plot([6.2, 9.0], [11.05, 11.05], color=GREEN, linewidth=1.5)
for i, item in enumerate(['재직 인증 (건강보험공단)    +25점',
                           '소득 인증 (국세청)             +25점',
                           '신용 인증 (CB사)                +20점',
                           '기본 점수                            +20점']):
    ax.text(7.6, 10.5 - i*0.5, item, fontsize=10, ha='center', va='center', color=DARK_GRAY)

ax.annotate('', xy=(10.3, 10.4), xytext=(9.9, 10.4),
            arrowprops=dict(arrowstyle='->', color=NAVY, lw=2.5))

# STEP 3
box3 = FancyBboxPatch((10.5, 8.5), 4.2, 3.8, boxstyle='round,pad=0.15',
                       facecolor=LIGHT_ORANGE, edgecolor=ORANGE, linewidth=2)
ax.add_patch(box3)
ax.text(12.6, 11.8, 'STEP 3', fontsize=11, fontweight='bold', ha='center', color=ORANGE)
ax.text(12.6, 11.3, '집주인 레퍼런스', fontsize=16, fontweight='bold', ha='center', color=NAVY)
ax.plot([11.2, 14.0], [11.05, 11.05], color=ORANGE, linewidth=1.5)
ax.text(12.6, 10.85, '  한국 최초  ', fontsize=9, fontweight='bold', ha='center',
        color=WHITE, bbox=dict(boxstyle='round,pad=0.2', facecolor=ORANGE, edgecolor='none'))
for i, item in enumerate(['고유코드로 이전 집주인에게 요청',
                           '월세 납부 성실도 평가',
                           '시설 관리 상태 평가',
                           '레퍼런스 점수                +30점']):
    ax.text(12.6, 10.3 - i*0.5, item, fontsize=10, ha='center', va='center', color=DARK_GRAY)

ax.annotate('', xy=(15.3, 10.4), xytext=(14.9, 10.4),
            arrowprops=dict(arrowstyle='->', color=NAVY, lw=2.5))

# STEP 4
box4 = FancyBboxPatch((15.5, 8.5), 4.0, 3.8, boxstyle='round,pad=0.15',
                       facecolor=LIGHT_PURPLE, edgecolor=PURPLE, linewidth=2)
ax.add_patch(box4)
ax.text(17.5, 11.8, 'STEP 4', fontsize=11, fontweight='bold', ha='center', color=PURPLE)
ax.text(17.5, 11.3, '신뢰점수 완성', fontsize=16, fontweight='bold', ha='center', color=NAVY)
ax.plot([16.2, 18.8], [11.05, 11.05], color=PURPLE, linewidth=1.5)
circle = plt.Circle((17.5, 10.0), 0.7, facecolor=PURPLE, edgecolor='none', alpha=0.15)
ax.add_patch(circle)
ax.text(17.5, 10.15, '87', fontsize=28, fontweight='bold', ha='center', va='center', color=PURPLE)
ax.text(17.5, 9.5, '/ 100점', fontsize=10, ha='center', va='center', color=PURPLE)
ax.text(17.5, 8.95, '프로필 카드 완성', fontsize=10, ha='center', va='center',
        color=DARK_GRAY, fontweight='bold')

# Big arrow down
ax.annotate('', xy=(10, 7.8), xytext=(10, 8.3),
            arrowprops=dict(arrowstyle='->', color=NAVY, lw=3))

# Bottom: 세입자 혜택
box_t = FancyBboxPatch((0.5, 4.2), 5.8, 3.3, boxstyle='round,pad=0.15',
                        facecolor='#E3F2FD', edgecolor=BLUE, linewidth=2)
ax.add_patch(box_t)
ax.text(3.4, 7.1, '세입자 혜택', fontsize=16, fontweight='bold', ha='center', color=NAVY)
ax.plot([1.2, 5.6], [6.85, 6.85], color=BLUE, linewidth=1.5)
for i, (t, d) in enumerate([('보증금 협상력 확보', '신뢰점수로 객관적 증명'),
                              ('우선 노출', '프리미엄 프로필 상위 노출'),
                              ('AI 자기소개서', '집주인 관점 최적화 생성'),
                              ('레퍼런스 축적', '이사할 때마다 신뢰 자산화')]):
    y = 6.4 - i * 0.55
    ax.text(1.3, y, '  ' + t, fontsize=11, fontweight='bold', va='center', color=BLUE)
    ax.text(4.2, y, d, fontsize=9.5, va='center', color=DARK_GRAY)

# Bottom: 집주인 혜택
box_l = FancyBboxPatch((7.1, 4.2), 5.8, 3.3, boxstyle='round,pad=0.15',
                        facecolor=LIGHT_GREEN, edgecolor=GREEN, linewidth=2)
ax.add_patch(box_l)
ax.text(10.0, 7.1, '집주인 혜택', fontsize=16, fontweight='bold', ha='center', color=NAVY)
ax.plot([7.8, 12.2], [6.85, 6.85], color=GREEN, linewidth=1.5)
for i, (t, d) in enumerate([('검증된 세입자', '재직/소득/신용 사전 확인'),
                              ('리스크 사전 파악', '이전 집주인 평가 확인'),
                              ('공실 최소화', '조건 매칭으로 빠른 입주'),
                              ('라이프스타일 매칭', '반려동물, 흡연 등 확인')]):
    y = 6.4 - i * 0.55
    ax.text(7.9, y, '  ' + t, fontsize=11, fontweight='bold', va='center', color=GREEN)
    ax.text(10.8, y, d, fontsize=9.5, va='center', color=DARK_GRAY)

# Bottom: 수익 구조 (보증보험 -> 수익 모델로 변경)
box_i = FancyBboxPatch((13.7, 4.2), 5.8, 3.3, boxstyle='round,pad=0.15',
                        facecolor=LIGHT_ORANGE, edgecolor=ORANGE, linewidth=2)
ax.add_patch(box_i)
ax.text(16.6, 7.1, '수익 구조', fontsize=16, fontweight='bold', ha='center', color=NAVY)
ax.plot([14.4, 18.8], [6.85, 6.85], color=ORANGE, linewidth=1.5)
for i, (t, d) in enumerate([('세입자 프리미엄', '9,900원/월 (40%)'),
                              ('집주인 열람', '3,900원/건 (30%)'),
                              ('집주인 구독', '29,900원/월 (30%)'),
                              ('BEP', '유료 ~500명 (2027 하반기)')]):
    y = 6.4 - i * 0.55
    ax.text(14.5, y, t, fontsize=11, fontweight='bold', va='center', color=ORANGE)
    ax.text(17.2, y, d, fontsize=9.5, va='center', color=DARK_GRAY)

# Bottom: 시장 진입 로드맵
box_s = FancyBboxPatch((0.5, 0.3), 19.0, 3.5, boxstyle='round,pad=0.15',
                        facecolor=GRAY, edgecolor='#CCCCCC', linewidth=1.5)
ax.add_patch(box_s)
ax.text(10, 3.4, '시장 진입 로드맵', fontsize=16, fontweight='bold', ha='center', color=NAVY)
ax.plot([3, 17], [3.15, 3.15], color='#CCCCCC', linewidth=1.5)

stages = [
    ('1단계', '셰어하우스\n코리빙 B2B', 'M1~M6', BLUE, '500명'),
    ('2단계', '대학가\n원룸', 'M4~M9', GREEN, '3,000명'),
    ('3단계', '신축\n오피스텔', 'M7~M12', ORANGE, '10,000명'),
    ('4단계', '일반\n월세 시장', 'M12+', PURPLE, '50,000명+'),
]
for i, (stage, desc, period, color, target) in enumerate(stages):
    x = 2.5 + i * 4.2
    box = FancyBboxPatch((x-1.5, 0.6), 3.2, 2.2, boxstyle='round,pad=0.1',
                          facecolor=WHITE, edgecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(x+0.1, 2.5, stage, fontsize=11, fontweight='bold', ha='center', color=color)
    ax.text(x+0.1, 1.9, desc, fontsize=11, ha='center', va='center', color=NAVY, fontweight='bold')
    ax.text(x+0.1, 1.15, period, fontsize=9, ha='center', color=DARK_GRAY)
    ax.text(x+0.1, 0.8, target, fontsize=10, fontweight='bold', ha='center', color=color)
    if i < 3:
        ax.annotate('', xy=(x+1.9, 1.7), xytext=(x+1.6, 1.7),
                    arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))

plt.tight_layout(pad=0.5)
plt.savefig('docs/예비창업패키지/렌트미_서비스흐름도.png', dpi=250, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print('Image 1 done')


# ================================================================
# IMAGE 2: 비즈니스 모델 + 시장규모
# ================================================================
fig, ax = plt.subplots(1, 1, figsize=(20, 15), dpi=250)
ax.set_xlim(0, 20)
ax.set_ylim(0, 15)
ax.axis('off')
fig.patch.set_facecolor('#FFFFFF')

ax.text(10, 14.3, '렌트미 (RentMe) 비즈니스 모델', fontsize=26, fontweight='bold',
        ha='center', va='center', color=NAVY)
ax.text(10, 13.8, '세입자 신뢰 프로필 플랫폼 | 수익 구조 및 시장 분석', fontsize=14,
        ha='center', va='center', color=DARK_GRAY)

# ── LEFT: 시장 규모 ──
box_market = FancyBboxPatch((0.5, 9.5), 6.0, 3.8, boxstyle='round,pad=0.15',
                             facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=2)
ax.add_patch(box_market)
ax.text(3.5, 12.9, '시장 규모', fontsize=18, fontweight='bold', ha='center', color=NAVY)
ax.plot([1.2, 5.8], [12.6, 12.6], color=BLUE, linewidth=1.5)

markets = [
    ('TAM', '약 2조원', '임차 가구 900만, 연 200만 건 거래', 2.0),
    ('SAM', '약 6,000억원', '1인 가구 월세 120만 건/년', 1.4),
    ('SOM', '약 30억원', '수도권 1인 월세, 점유율 5% (3년)', 0.8),
]
for i, (label, size, basis, radius) in enumerate(markets):
    cx, cy = 2.5, 11.2
    circle = plt.Circle((cx, cy), radius, facecolor=BLUE, edgecolor='none',
                         alpha=0.08 + i*0.06)
    ax.add_patch(circle)

ax.text(2.5, 11.8, 'TAM 약 2조원', fontsize=13, fontweight='bold', ha='center', color=BLUE)
ax.text(2.5, 11.4, 'SAM 약 6,000억원', fontsize=11, fontweight='bold', ha='center', color=BLUE)
ax.text(2.5, 11.0, 'SOM 약 30억원', fontsize=10, fontweight='bold', ha='center', color=NAVY)

ax.text(5.0, 11.9, '임차 900만 가구', fontsize=9, va='center', color=DARK_GRAY)
ax.text(5.0, 11.4, '1인 월세 120만건/년', fontsize=9, va='center', color=DARK_GRAY)
ax.text(5.0, 10.9, '수도권 점유 5%', fontsize=9, va='center', color=DARK_GRAY)

ax.text(3.5, 10.2, '월세 비중 60.2%  |  1인 가구 804만', fontsize=10,
        ha='center', color=DARK_GRAY, fontweight='bold')
ax.text(3.5, 9.8, '전세사기 2.5만명 피해 > 신뢰 니즈 폭발', fontsize=10,
        ha='center', color='#D32F2F', fontweight='bold')

# ── RIGHT: 경쟁 포지셔닝 ──
box_comp = FancyBboxPatch((7.0, 9.5), 6.0, 3.8, boxstyle='round,pad=0.15',
                           facecolor=LIGHT_GREEN, edgecolor=GREEN, linewidth=2)
ax.add_patch(box_comp)
ax.text(10.0, 12.9, '경쟁 포지셔닝', fontsize=18, fontweight='bold', ha='center', color=NAVY)
ax.plot([7.7, 12.3], [12.6, 12.6], color=GREEN, linewidth=1.5)

comps = [
    ('직방/다방', '매물 검색', '세입자 인증 없음', '#999999'),
    ('피터팬', '직거래 커뮤니티', '신뢰 보장 없음', '#999999'),
    ('렌트미', '세입자 신뢰 프로필', '한국 유일', GREEN),
]
for i, (name, pos, gap, color) in enumerate(comps):
    y = 12.0 - i * 0.85
    is_us = (name == '렌트미')
    ax.text(8.0, y, name, fontsize=12, fontweight='bold', va='center',
            color=WHITE if is_us else DARK_GRAY,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=color if is_us else '#EEEEEE',
                      edgecolor='none'))
    ax.text(9.8, y, pos, fontsize=10, va='center', color=NAVY if is_us else DARK_GRAY,
            fontweight='bold' if is_us else 'normal')
    ax.text(11.5, y, gap, fontsize=9, va='center',
            color=GREEN if is_us else '#999999', fontweight='bold' if is_us else 'normal')

# ── FAR RIGHT: 핵심 차별화 ──
box_diff = FancyBboxPatch((13.5, 9.5), 6.0, 3.8, boxstyle='round,pad=0.15',
                           facecolor=LIGHT_PURPLE, edgecolor=PURPLE, linewidth=2)
ax.add_patch(box_diff)
ax.text(16.5, 12.9, '핵심 차별화', fontsize=18, fontweight='bold', ha='center', color=NAVY)
ax.plot([14.2, 18.8], [12.6, 12.6], color=PURPLE, linewidth=1.5)

diffs = [
    ('마이데이터 자동 인증', '재직/소득/신용 API 실시간 검증'),
    ('집주인 레퍼런스', '한국 최초, 임대 이력 증명'),
    ('LLM AI 자기소개서', '집주인 관점 맞춤 자동 생성'),
    ('다층 신뢰 스코어링', '인증+레퍼런스+프로필 종합'),
    ('세입자-집주인 매칭', '신뢰점수 기반 조건 맞춤 추천'),
]
for i, (title, desc) in enumerate(diffs):
    y = 12.1 - i * 0.55
    ax.text(14.3, y, title, fontsize=10, fontweight='bold', va='center', color=PURPLE)
    ax.text(16.5, y, desc, fontsize=9, va='center', color=DARK_GRAY)

# ── MIDDLE: 수익 모델 (3개 수익원) ──
box_rev = FancyBboxPatch((0.5, 4.8), 19.0, 4.2, boxstyle='round,pad=0.15',
                          facecolor='#FAFAFA', edgecolor=NAVY, linewidth=2)
ax.add_patch(box_rev)
ax.text(10, 8.6, '수익 모델 (Revenue Model)', fontsize=18, fontweight='bold',
        ha='center', color=NAVY)
ax.plot([3, 17], [8.3, 8.3], color=NAVY, linewidth=1)

# Revenue 1: 세입자 B2C
rev_box1 = FancyBboxPatch((1.0, 5.2), 5.5, 2.8, boxstyle='round,pad=0.1',
                           facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=1.5)
ax.add_patch(rev_box1)
ax.text(3.75, 7.7, '세입자 프리미엄 (B2C)', fontsize=13, fontweight='bold', ha='center', color=NAVY)
ax.text(3.75, 7.2, '40%', fontsize=24, fontweight='bold', ha='center', color=BLUE)
ax.text(3.75, 6.6, '9,900원/월', fontsize=14, fontweight='bold', ha='center', color=BLUE)
ax.text(3.75, 6.1, '우선 노출, 무제한 AI 자기소개,', fontsize=9, ha='center', color=DARK_GRAY)
ax.text(3.75, 5.7, '레퍼런스 무제한', fontsize=9, ha='center', color=DARK_GRAY)
ax.text(3.75, 5.3, 'LTV:CAC = 12:1', fontsize=10, fontweight='bold', ha='center', color=BLUE)

# Revenue 2: 집주인 열람
rev_box2 = FancyBboxPatch((7.25, 5.2), 5.5, 2.8, boxstyle='round,pad=0.1',
                           facecolor=LIGHT_GREEN, edgecolor=GREEN, linewidth=1.5)
ax.add_patch(rev_box2)
ax.text(10.0, 7.7, '집주인 열람 (B2B)', fontsize=13, fontweight='bold', ha='center', color=NAVY)
ax.text(10.0, 7.2, '30%', fontsize=24, fontweight='bold', ha='center', color=GREEN)
ax.text(10.0, 6.6, '3,900원/건', fontsize=14, fontweight='bold', ha='center', color=GREEN)
ax.text(10.0, 6.1, '검증된 세입자 프로필 열람,', fontsize=9, ha='center', color=DARK_GRAY)
ax.text(10.0, 5.7, '연락처 + 상세 프로필 제공', fontsize=9, ha='center', color=DARK_GRAY)

# Revenue 3: 집주인 구독
rev_box3 = FancyBboxPatch((13.5, 5.2), 5.5, 2.8, boxstyle='round,pad=0.1',
                           facecolor=LIGHT_ORANGE, edgecolor=ORANGE, linewidth=1.5)
ax.add_patch(rev_box3)
ax.text(16.25, 7.7, '집주인 구독 (B2B)', fontsize=13, fontweight='bold', ha='center', color=NAVY)
ax.text(16.25, 7.2, '30%', fontsize=24, fontweight='bold', ha='center', color=ORANGE)
ax.text(16.25, 6.6, '29,900원/월', fontsize=14, fontweight='bold', ha='center', color=ORANGE)
ax.text(16.25, 6.1, '무제한 열람, 매칭 알림,', fontsize=9, ha='center', color=DARK_GRAY)
ax.text(16.25, 5.7, '우선 지원', fontsize=9, ha='center', color=DARK_GRAY)
ax.text(16.25, 5.3, 'LTV:CAC = 9:1', fontsize=10, fontweight='bold', ha='center', color=ORANGE)

# ── BOTTOM: 3개년 목표 ──
box_goal = FancyBboxPatch((0.5, 0.3), 19.0, 4.0, boxstyle='round,pad=0.15',
                           facecolor=GRAY, edgecolor='#CCCCCC', linewidth=1.5)
ax.add_patch(box_goal)
ax.text(10, 3.9, '3개년 성장 목표', fontsize=16, fontweight='bold', ha='center', color=NAVY)
ax.plot([3, 17], [3.6, 3.6], color='#CCCCCC', linewidth=1.5)

# Year columns
years = [
    ('2026년 (5개월)', ['가입 3,000명', '유료 전환 8%', '월 매출 100만원', '고용 2명'], BLUE),
    ('2027년', ['가입 30,000명', '유료 전환 12%', '월 매출 2,000만원', '고용 4명'], GREEN),
    ('2028년', ['가입 150,000명', '유료 전환 18%', '월 매출 1.5억원', '고용 7명'], PURPLE),
]
for i, (year, items, color) in enumerate(years):
    x = 3.5 + i * 5.5
    box_y = FancyBboxPatch((x-2.2, 0.6), 4.8, 2.7, boxstyle='round,pad=0.1',
                            facecolor=WHITE, edgecolor=color, linewidth=2)
    ax.add_patch(box_y)
    ax.text(x+0.2, 3.0, year, fontsize=13, fontweight='bold', ha='center', color=color)
    for j, item in enumerate(items):
        ax.text(x+0.2, 2.4 - j*0.45, item, fontsize=11, ha='center', va='center',
                color=NAVY, fontweight='bold' if j == 2 else 'normal')
    if i < 2:
        ax.annotate('', xy=(x+2.9, 1.9), xytext=(x+2.5, 1.9),
                    arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))

# BEP annotation
ax.text(10, 0.45, '사업 전체 BEP: 유료 구독 ~500명 + 열람 300건/월 (2027 하반기 예상)',
        fontsize=10, ha='center', color=DARK_GRAY, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF9C4', edgecolor='#FFD54F'))

plt.tight_layout(pad=0.5)
plt.savefig('docs/예비창업패키지/렌트미_비즈니스모델.png', dpi=250, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print('Image 2 done')
print('All images generated successfully')
