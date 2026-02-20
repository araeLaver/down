"""
Fryndo 사업계획서 이미지 2장 - 심플 비즈니스 스타일
AI 티 안 나게 깔끔한 도표/인포그래픽 스타일
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 색상 (차분한 비즈니스 톤)
NAVY = '#1B3A5C'
BLUE = '#3B7DD8'
TEAL = '#2A9D8F'
ORANGE = '#E76F51'
GRAY = '#6B7280'
LGRAY = '#E5E7EB'
WHITE = '#FFFFFF'
BG = '#FFFFFF'


def rbox(ax, x, y, w, h, fc=WHITE, ec=LGRAY, lw=1.2, r=0.015):
    b = FancyBboxPatch((x - w/2, y - h/2), w, h,
                       boxstyle=f"round,pad={r}",
                       facecolor=fc, edgecolor=ec, lw=lw, zorder=2)
    ax.add_patch(b)


def arrow_right(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5), zorder=1)


# ═══════════════════════════════════════
# 이미지 1: 서비스 개요도
# ═══════════════════════════════════════

fig1, ax1 = plt.subplots(figsize=(13, 8.5))
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')
fig1.patch.set_facecolor(BG)

# 상단 타이틀 바
rbox(ax1, 0.5, 0.955, 0.96, 0.06, fc=NAVY, ec='none')
ax1.text(0.5, 0.955, 'Fryndo(프린도) 서비스 개요',
         ha='center', va='center', fontsize=16, color=WHITE, fontweight='bold')

# ── 왼쪽: 문제 정의 ──
ax1.text(0.03, 0.88, 'Problem', ha='left', fontsize=12, color=ORANGE, fontweight='bold')
ax1.plot([0.03, 0.45], [0.865, 0.865], color=ORANGE, lw=2)

problems = [
    ('동행 부재', '1인 여행 불편함 67%\n"동행 있으면 좋겠다" 72%'),
    ('안전 불안', '여성 78% "안전이 최대 걱정"\n안전 우려로 여행 취소 34%'),
    ('기록 휘발', '여행 기록 남기는 비율 23%\n방문 인증 체계 부재'),
]

for i, (t, d) in enumerate(problems):
    py = 0.81 - i * 0.095
    rbox(ax1, 0.24, py, 0.40, 0.075, ec=ORANGE, lw=1)
    ax1.text(0.06, py, t, ha='left', va='center', fontsize=10, color=ORANGE, fontweight='bold')
    ax1.text(0.16, py, d, ha='left', va='center', fontsize=8, color=GRAY, linespacing=1.3)

# ── 오른쪽: 솔루션 ──
ax1.text(0.55, 0.88, 'Solution', ha='left', fontsize=12, color=TEAL, fontweight='bold')
ax1.plot([0.55, 0.97], [0.865, 0.865], color=TEAL, lw=2)

solutions = [
    ('AI 동행 매칭', '여행스타일/일정/관심사 분석\n실명인증 + 신뢰점수'),
    ('안전 시스템', '실시간 위치공유, 긴급 SOS\n후기/평점, 신뢰 점수제'),
    ('NFT 수집', 'GPS 관광지 방문 인증\n지역 한정 디지털 수집품'),
]

for i, (t, d) in enumerate(solutions):
    py = 0.81 - i * 0.095
    rbox(ax1, 0.76, py, 0.40, 0.075, ec=TEAL, lw=1)
    ax1.text(0.58, py, t, ha='left', va='center', fontsize=10, color=TEAL, fontweight='bold')
    ax1.text(0.68, py, d, ha='left', va='center', fontsize=8, color=GRAY, linespacing=1.3)

# 화살표 (문제 → 솔루션)
arrow_right(ax1, 0.46, 0.72, 0.54, 0.72)

# ── 중간: 서비스 이용 흐름 ──
ax1.plot([0.03, 0.97], [0.575, 0.575], color=LGRAY, lw=1)
ax1.text(0.5, 0.56, '서비스 이용 흐름', ha='center', fontsize=11, color=NAVY, fontweight='bold',
         bbox=dict(facecolor=WHITE, edgecolor='none', pad=3))

flow_steps = [
    ('1. 가입', '카카오/구글\n소셜 로그인'),
    ('2. 프로필', '여행스타일\n일정 입력'),
    ('3. AI 매칭', '동행자\n추천'),
    ('4. 채팅', '실시간\n그룹 채팅'),
    ('5. 여행', 'GPS 위치공유\n안전 시스템'),
    ('6. NFT', '관광지 방문\n인증 수집'),
]

for i, (title, desc) in enumerate(flow_steps):
    fx = 0.09 + i * 0.15
    # 원형 넘버
    circle = plt.Circle((fx, 0.49), 0.022, facecolor=BLUE, edgecolor='none', zorder=3)
    ax1.add_patch(circle)
    ax1.text(fx, 0.49, str(i+1), ha='center', va='center',
             fontsize=10, color=WHITE, fontweight='bold', zorder=4)
    # 텍스트
    ax1.text(fx, 0.45, title.split('. ')[1], ha='center', va='center',
             fontsize=9, color=NAVY, fontweight='bold')
    ax1.text(fx, 0.41, desc, ha='center', va='center',
             fontsize=7.5, color=GRAY, linespacing=1.3)
    # 화살표
    if i < 5:
        arrow_right(ax1, fx + 0.04, 0.49, fx + 0.11, 0.49)

# ── 하단 왼쪽: 시장 규모 ──
ax1.plot([0.03, 0.97], [0.33, 0.33], color=LGRAY, lw=1)
ax1.text(0.25, 0.305, '시장 규모', ha='center', fontsize=11, color=NAVY, fontweight='bold',
         bbox=dict(facecolor=WHITE, edgecolor='none', pad=3))

# TAM-SAM-SOM 동심원 (심플)
for r, label, val, c in [(0.11, 'TAM', '7조원', LGRAY),
                          (0.075, 'SAM', '2.8조원', '#C5D5EA'),
                          (0.04, 'SOM', '28억원', BLUE)]:
    circle = plt.Circle((0.15, 0.19), r, facecolor=c, edgecolor=NAVY, lw=0.8, zorder=2 if r < 0.1 else 1, alpha=0.7)
    ax1.add_patch(circle)

ax1.text(0.15, 0.19, 'SOM\n28억', ha='center', va='center', fontsize=8, color=WHITE, fontweight='bold', zorder=4)
ax1.text(0.30, 0.26, 'TAM 7조원 (국내 1인 여행)', ha='left', fontsize=8, color=GRAY)
ax1.text(0.30, 0.23, 'SAM 2.8조원 (디지털 플랫폼)', ha='left', fontsize=8, color=GRAY)
ax1.text(0.30, 0.20, 'SOM 28억원 (초기 점유 0.1%)', ha='left', fontsize=8, color=NAVY, fontweight='bold')
ax1.text(0.30, 0.14, '글로벌 CAGR 14.3%', ha='left', fontsize=9, color=BLUE, fontweight='bold')
ax1.text(0.30, 0.11, '(Grand View Research, 2030)', ha='left', fontsize=7, color=GRAY)

# ── 하단 오른쪽: 수익 모델 ──
ax1.text(0.75, 0.305, '수익 모델 (BM)', ha='center', fontsize=11, color=NAVY, fontweight='bold',
         bbox=dict(facecolor=WHITE, edgecolor='none', pad=3))

bm = [
    ('B2C 구독', '55%', 'Plus 9,900/월, Pro 19,900/월', BLUE),
    ('B2B 제휴', '25%', '지자체 NFT 대행, 관광 데이터', TEAL),
    ('광고', '15%', '관광지/숙박 타겟 광고', GRAY),
    ('NFT', '5%', 'NFT 거래 수수료', ORANGE),
]

for i, (name, pct, desc, c) in enumerate(bm):
    by = 0.255 - i * 0.045
    # 바
    bar_w = float(pct.replace('%','')) / 100 * 0.30
    rbox(ax1, 0.57 + 0.15, by, 0.30, 0.032, fc=LGRAY, ec='none', r=0.005)
    bar = FancyBboxPatch((0.57, by - 0.016), bar_w, 0.032,
                         boxstyle="round,pad=0.005",
                         facecolor=c, edgecolor='none', alpha=0.8, zorder=3)
    ax1.add_patch(bar)
    ax1.text(0.56, by, name, ha='right', va='center', fontsize=8, color=NAVY, fontweight='bold')
    ax1.text(0.57 + 0.155, by, pct, ha='center', va='center', fontsize=7, color=WHITE, fontweight='bold', zorder=4)
    ax1.text(0.88, by, desc, ha='left', va='center', fontsize=7, color=GRAY)

# 하단 URL
ax1.text(0.5, 0.03, 'URL: https://various-belva-untab-1a59bee2.koyeb.app',
         ha='center', fontsize=8, color=GRAY)


out1 = os.path.join(os.path.dirname(__file__), 'Fryndo_서비스흐름도.png')
fig1.savefig(out1, dpi=180, bbox_inches='tight', facecolor=BG)
plt.close(fig1)
print(f'[1] {out1}')


# ═══════════════════════════════════════
# 이미지 2: 기술 구성 및 팀/일정
# ═══════════════════════════════════════

fig2, ax2 = plt.subplots(figsize=(13, 8.5))
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')
fig2.patch.set_facecolor(BG)

# 타이틀
rbox(ax2, 0.5, 0.955, 0.96, 0.06, fc=NAVY, ec='none')
ax2.text(0.5, 0.955, 'Fryndo(프린도) 기술 구성 및 사업 계획',
         ha='center', va='center', fontsize=16, color=WHITE, fontweight='bold')

# ── 기술 스택 (3 레이어) ──
ax2.text(0.03, 0.895, '기술 스택', ha='left', fontsize=12, color=NAVY, fontweight='bold')
ax2.plot([0.03, 0.97], [0.88, 0.88], color=NAVY, lw=1.5)

layers = [
    ('Frontend', 0.83, BLUE, [
        ('React', '반응형 웹'),
        ('React Native', '모바일 앱 (예정)'),
        ('Tailwind CSS', 'UI 스타일링'),
    ]),
    ('Backend', 0.73, TEAL, [
        ('Spring Boot', 'REST API'),
        ('Spring Security', 'JWT/OAuth'),
        ('WebSocket', '실시간 채팅'),
        ('OpenAI API', 'AI 매칭'),
    ]),
    ('Data/Infra', 0.63, ORANGE, [
        ('PostgreSQL', 'RDBMS'),
        ('Polygon', 'NFT/블록체인'),
        ('IPFS', '분산 저장'),
        ('Koyeb', '클라우드'),
    ]),
]

for layer_name, ly, lcolor, items in layers:
    # 레이어 라벨
    rbox(ax2, 0.08, ly, 0.10, 0.065, fc=lcolor, ec='none')
    ax2.text(0.08, ly, layer_name, ha='center', va='center',
             fontsize=8, color=WHITE, fontweight='bold', zorder=4)
    # 아이템들
    iw = 0.78 / len(items)
    for i, (name, desc) in enumerate(items):
        ix = 0.18 + iw/2 + i * iw
        rbox(ax2, ix, ly, iw - 0.01, 0.065, fc=WHITE, ec=lcolor, lw=1)
        ax2.text(ix, ly + 0.012, name, ha='center', va='center',
                 fontsize=9, color=NAVY, fontweight='bold', zorder=4)
        ax2.text(ix, ly - 0.015, desc, ha='center', va='center',
                 fontsize=7, color=GRAY, zorder=4)

# ── 팀 구성 ──
ax2.text(0.03, 0.555, '팀 구성 (선정 후)', ha='left', fontsize=12, color=NAVY, fontweight='bold')
ax2.plot([0.03, 0.97], [0.54, 0.54], color=NAVY, lw=1.5)

team = [
    ('대표 (김다운)', '기술 총괄\n백엔드/AI/블록체인', NAVY),
    ('기획/PM', '사업운영 전담\n일정관리/제휴', BLUE),
    ('앱 개발자', 'React Native\n모바일 앱', TEAL),
    ('블록체인 개발자', 'Solidity/Web3\nNFT 고도화', ORANGE),
    ('마케터', 'SNS/인플루언서\n커뮤니티', GRAY),
    ('디자이너 (외주)', 'UI/UX\n브랜딩', LGRAY),
]

for i, (role, desc, c) in enumerate(team):
    tx = 0.09 + i * 0.155
    tc = WHITE if c not in [LGRAY] else NAVY
    rbox(ax2, tx, 0.49, 0.14, 0.07, fc=c, ec='none')
    ax2.text(tx, 0.505, role, ha='center', va='center',
             fontsize=7.5, color=tc, fontweight='bold', zorder=4)
    ax2.text(tx, 0.475, desc, ha='center', va='center',
             fontsize=6.5, color=tc, alpha=0.85, zorder=4, linespacing=1.2)

# ── 간트 차트 (협약 7개월) ──
ax2.text(0.03, 0.415, '사업 추진 일정 (2026.5~11월)', ha='left', fontsize=12, color=NAVY, fontweight='bold')
ax2.plot([0.03, 0.97], [0.40, 0.40], color=NAVY, lw=1.5)

# 월 라벨
months = ['5월', '6월', '7월', '8월', '9월', '10월', '11월']
mx_start = 0.22
mx_w = 0.105

for i, m in enumerate(months):
    mx = mx_start + i * mx_w
    ax2.text(mx + mx_w/2, 0.385, m, ha='center', va='center', fontsize=8, color=NAVY, fontweight='bold')

# 간트 바
gantt_items = [
    ('기획/PM (전담)', [(0, 6)], BLUE),
    ('앱 개발', [(0, 3)], TEAL),
    ('블록체인', [(1, 2)], ORANGE),
    ('마케팅', [(4, 3)], '#8B5CF6'),
    ('디자인 (외주)', [(0, 2)], GRAY),
    ('베타 테스트', [(2, 2)], '#EC4899'),
]

for i, (label, spans, c) in enumerate(gantt_items):
    gy = 0.355 - i * 0.038
    ax2.text(0.20, gy, label, ha='right', va='center', fontsize=7.5, color=NAVY)
    for start, dur in spans:
        bx = mx_start + start * mx_w
        bw = dur * mx_w
        bar = FancyBboxPatch((bx, gy - 0.012), bw, 0.024,
                             boxstyle="round,pad=0.003",
                             facecolor=c, edgecolor='none', alpha=0.75, zorder=2)
        ax2.add_patch(bar)

# 마일스톤
milestones = [
    (0, 'M1: 법인설립\n팀 구성'),
    (2, 'M3: 앱 출시\n베타 테스트'),
    (4, 'M5: 마케팅\n본격 시작'),
    (6, 'M7: 성과 정리\nIR 준비'),
]
for mi, label in milestones:
    mx = mx_start + mi * mx_w
    ax2.plot([mx, mx], [0.13, 0.37], color=LGRAY, lw=0.8, ls='--', zorder=0)
    ax2.text(mx, 0.12, label, ha='center', va='center', fontsize=6.5, color=GRAY, linespacing=1.2)

# ── 하단: KPI 목표 ──
ax2.plot([0.03, 0.97], [0.08, 0.08], color=LGRAY, lw=1)
ax2.text(0.03, 0.055, 'KPI 목표:', ha='left', fontsize=9, color=NAVY, fontweight='bold')

kpis = [
    '고객 5,000명', '매출 700만원', '신규고용 4명',
    '앱 출시 1건', '아이템 검증 20회', '홍보 25건'
]
kpi_text = '    |    '.join(kpis)
ax2.text(0.17, 0.055, kpi_text, ha='left', fontsize=8, color=GRAY)


out2 = os.path.join(os.path.dirname(__file__), 'Fryndo_시스템아키텍처.png')
fig2.savefig(out2, dpi=180, bbox_inches='tight', facecolor=BG)
plt.close(fig2)
print(f'[2] {out2}')

print('완료')
