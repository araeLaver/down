from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# 프레젠테이션 생성
prs = Presentation()
prs.slide_width = Inches(16)
prs.slide_height = Inches(9)

# 색상 정의
PRIMARY_COLOR = RGBColor(41, 98, 255)  # 파란색
DARK_COLOR = RGBColor(33, 33, 33)
WHITE_COLOR = RGBColor(255, 255, 255)
ACCENT_COLOR = RGBColor(255, 87, 34)  # 주황색

def add_title_slide(prs, title, subtitle):
    """표지 슬라이드"""
    slide_layout = prs.slide_layouts[6]  # 빈 슬라이드
    slide = prs.slides.add_slide(slide_layout)

    # 배경 도형
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(16), Inches(9))
    shape.fill.solid()
    shape.fill.fore_color.rgb = PRIMARY_COLOR
    shape.line.fill.background()

    # 제목
    title_box = slide.shapes.add_textbox(Inches(1), Inches(3), Inches(14), Inches(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(60)
    p.font.bold = True
    p.font.color.rgb = WHITE_COLOR
    p.alignment = PP_ALIGN.CENTER

    # 부제목
    sub_box = slide.shapes.add_textbox(Inches(1), Inches(4.8), Inches(14), Inches(1))
    tf = sub_box.text_frame
    p = tf.paragraphs[0]
    p.text = subtitle
    p.font.size = Pt(28)
    p.font.color.rgb = WHITE_COLOR
    p.alignment = PP_ALIGN.CENTER

    return slide

def add_content_slide(prs, title, contents, highlight=None):
    """내용 슬라이드"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # 상단 바
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(16), Inches(1.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = PRIMARY_COLOR
    bar.line.fill.background()

    # 제목
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.3), Inches(14), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE_COLOR

    # 내용
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(14), Inches(6.5))
    tf = content_box.text_frame
    tf.word_wrap = True

    for i, content in enumerate(contents):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = content
        p.font.size = Pt(24)
        p.font.color.rgb = DARK_COLOR
        p.space_after = Pt(16)

        if highlight and content.startswith(highlight):
            p.font.bold = True
            p.font.color.rgb = PRIMARY_COLOR

    return slide

def add_two_column_slide(prs, title, left_title, left_items, right_title, right_items):
    """2단 비교 슬라이드"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # 상단 바
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(16), Inches(1.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = PRIMARY_COLOR
    bar.line.fill.background()

    # 제목
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.3), Inches(14), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE_COLOR

    # 왼쪽 컬럼
    left_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.5), Inches(6))
    tf = left_box.text_frame
    p = tf.paragraphs[0]
    p.text = left_title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = DARK_COLOR

    for item in left_items:
        p = tf.add_paragraph()
        p.text = f"• {item}"
        p.font.size = Pt(22)
        p.font.color.rgb = DARK_COLOR
        p.space_after = Pt(12)

    # 오른쪽 컬럼
    right_box = slide.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(6.5), Inches(6))
    tf = right_box.text_frame
    p = tf.paragraphs[0]
    p.text = right_title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR

    for item in right_items:
        p = tf.add_paragraph()
        p.text = f"✓ {item}"
        p.font.size = Pt(22)
        p.font.color.rgb = PRIMARY_COLOR
        p.space_after = Pt(12)

    return slide

def add_ending_slide(prs, title, subtitle):
    """마무리 슬라이드"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # 배경
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(16), Inches(9))
    shape.fill.solid()
    shape.fill.fore_color.rgb = PRIMARY_COLOR
    shape.line.fill.background()

    # 비전
    title_box = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(14), Inches(2))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = f'"{title}"'
    p.font.size = Pt(40)
    p.font.italic = True
    p.font.color.rgb = WHITE_COLOR
    p.alignment = PP_ALIGN.CENTER

    # 서비스명
    sub_box = slide.shapes.add_textbox(Inches(1), Inches(5), Inches(14), Inches(1))
    tf = sub_box.text_frame
    p = tf.paragraphs[0]
    p.text = subtitle
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = WHITE_COLOR
    p.alignment = PP_ALIGN.CENTER

    # 감사합니다
    thanks_box = slide.shapes.add_textbox(Inches(1), Inches(7), Inches(14), Inches(1))
    tf = thanks_box.text_frame
    p = tf.paragraphs[0]
    p.text = "감사합니다"
    p.font.size = Pt(32)
    p.font.color.rgb = WHITE_COLOR
    p.alignment = PP_ALIGN.CENTER

    return slide


# ========== 슬라이드 생성 ==========

# 1. 표지
add_title_slide(
    prs,
    "Fryndo AR Companion",
    "언어가 달라도 함께 여행하는 AR 동행 서비스"
)

# 2. 문제 정의
add_content_slide(
    prs,
    "해외여행, 이런 경험 있으시죠?",
    [
        "🗣️ 문제 1: 동행자와 말이 안 통해요",
        "     다국적 그룹 여행 시 소통 단절",
        "     기존 번역 앱은 1:1만 지원",
        "",
        "📍 문제 2: 만나기로 한 장소에서 못 찾아요",
        "     사람 많은 곳에서 서로 헤맴",
        "",
        "🗺️ 문제 3: 낯선 도시에서 길을 잃어요",
        "     지도 보느라 여행을 못 즐김",
    ]
)

# 3. 솔루션
add_content_slide(
    prs,
    "Fryndo AR Companion 솔루션",
    [
        "✅ 기능 1: 실시간 그룹 번역",
        "     3명 이상 다국어 동시 번역, 음성 → 자막 실시간 표시",
        "",
        "✅ 기능 2: AR 동행자 찾기",
        "     카메라로 주변 스캔, \"3시 방향 15m\" AR 표시",
        "",
        "✅ 기능 3: AR 길안내",
        "     화면에 화살표 오버레이, 지도 안 봐도 됨",
    ]
)

# 4. 데모 (플레이스홀더)
add_content_slide(
    prs,
    "데모 시연",
    [
        "",
        "",
        "              🎬 데모 영상 삽입 위치",
        "",
        "              (30초 ~ 1분 분량)",
        "",
        "",
        "     * 앱 실행 → 그룹 번역 → AR 동행자 찾기 시연",
    ]
)

# 5. 시장 분석
add_content_slide(
    prs,
    "시장 기회",
    [
        "🌍 TAM (전체 시장)",
        "     글로벌 여행자: 연간 15억 명",
        "",
        "🇰🇷 SAM (유효 시장)",
        "     한국 출국자 + 방한 외국인: 4,500만 명",
        "",
        "🎯 SOM (목표 시장)",
        "     다국적 그룹 여행자: 100만 명",
        "     1년차 목표: 1,000명 (0.1%)",
    ]
)

# 6. 비즈니스 모델
add_content_slide(
    prs,
    "비즈니스 모델",
    [
        "💰 수익 구조",
        "",
        "     무료 티어: 월 30분 번역 + 기본 AR",
        "",
        "     Plus 구독: ₩9,900/월",
        "     - 무제한 번역",
        "     - 전체 AR 기능",
        "",
        "📊 1년차 목표: 유료 전환 100명 → 월 99만원",
    ]
)

# 7. 경쟁력
add_two_column_slide(
    prs,
    "왜 Fryndo인가?",
    "기존 번역 앱",
    ["1:1 번역만 지원", "번역 기능만 제공", "일회성 사용", "범용 앱"],
    "Fryndo AR Companion",
    ["그룹 번역 지원", "동행 매칭 + 번역 + AR 통합", "커뮤니티 기반 재사용", "여행 특화"]
)

# 8. 팀 소개
add_content_slide(
    prs,
    "팀 소개",
    [
        "👤 대표 / 개발",
        "     • React Native, Node.js 풀스택 개발",
        "     • Fryndo MVP 단독 개발 완료",
        "",
        "🤝 협업 파트너",
        "     • AR 개발: 전문 외주 협업",
        "     • UI/UX 디자인: 크몽/숨고 활용",
        "",
        "💪 강점: 이미 검증된 MVP 보유, 빠른 실행력",
    ]
)

# 9. 로드맵 & 자금
add_content_slide(
    prs,
    "1년 로드맵 & 자금 계획",
    [
        "📅 로드맵",
        "     1~3월: 기반 구축 (AR 모듈, API 연동)",
        "     4~6월: MVP 개발 (핵심 3기능)",
        "     7~9월: 베타 테스트 (100명)",
        "     10~12월: 정식 출시 (1,000명 목표)",
        "",
        "💵 자금 사용 (1억원)",
        "     인건비 40% | 외주개발 25% | API 10% | 마케팅 15% | 운영 10%",
    ]
)

# 10. 마무리
add_ending_slide(
    prs,
    "언어가 달라도, 전 세계 누구와도 함께 여행하는 세상",
    "Fryndo AR Companion"
)

# 저장
output_path = r"C:\Develop\00.down\down\docs\Fryndo_AR_Companion_IR.pptx"
prs.save(output_path)
print(f"PPT 생성 완료: {output_path}")
