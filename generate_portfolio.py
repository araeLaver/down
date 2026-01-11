"""
포트폴리오 PDF 생성기
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

class PortfolioGenerator:
    def __init__(self):
        self.width, self.height = A4
        self.filename = "Portfolio.pdf"

        # 한글 폰트 등록 (Windows 기본 폰트)
        try:
            pdfmetrics.registerFont(TTFont('malgun', 'malgun.ttf'))
            self.font_name = 'malgun'
        except:
            try:
                pdfmetrics.registerFont(TTFont('gulim', 'gulim.ttc'))
                self.font_name = 'gulim'
            except:
                self.font_name = 'Helvetica'

    def create_styles(self):
        """커스텀 스타일 생성"""
        styles = getSampleStyleSheet()

        # 제목 스타일
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontName=self.font_name,
            fontSize=28,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            bold=True
        ))

        # 부제목 스타일
        styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=styles['Heading1'],
            fontName=self.font_name,
            fontSize=20,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12,
            bold=True
        ))

        # 섹션 제목
        styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=styles['Heading2'],
            fontName=self.font_name,
            fontSize=16,
            textColor=colors.HexColor('#3f51b5'),
            spaceAfter=10,
            spaceBefore=10,
            bold=True
        ))

        # 본문
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['BodyText'],
            fontName=self.font_name,
            fontSize=11,
            textColor=colors.HexColor('#212121'),
            spaceAfter=8,
            leading=16
        ))

        # 강조 텍스트
        styles.add(ParagraphStyle(
            name='Highlight',
            parent=styles['BodyText'],
            fontName=self.font_name,
            fontSize=12,
            textColor=colors.HexColor('#d32f2f'),
            spaceAfter=8,
            bold=True
        ))

        return styles

    def create_header_footer(self, canvas, doc):
        """헤더/푸터 추가"""
        canvas.saveState()

        # 푸터
        canvas.setFont(self.font_name, 9)
        canvas.setFillColor(colors.grey)
        canvas.drawString(inch, 0.5 * inch,
                         f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        canvas.drawRightString(self.width - inch, 0.5 * inch,
                              f"Page {doc.page}")

        canvas.restoreState()

    def generate(self):
        """포트폴리오 PDF 생성"""
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )

        styles = self.create_styles()
        story = []

        # === 표지 ===
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph("AI 기반 비즈니스 자동화 시스템", styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph("Down AI Portfolio", styles['CustomHeading1']))
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(
            "실시간 시장 분석 및 자동 사업 발굴 플랫폼",
            styles['CustomBody']
        ))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(
            f"작성일: {datetime.now().strftime('%Y년 %m월 %d일')}",
            styles['CustomBody']
        ))

        story.append(PageBreak())

        # === 프로젝트 개요 ===
        story.append(Paragraph("📋 프로젝트 개요", styles['CustomHeading1']))
        story.append(Spacer(1, 0.2*inch))

        overview_data = [
            ['항목', '내용'],
            ['프로젝트명', 'Down AI - 자동 비즈니스 발굴 시스템'],
            ['개발 기간', '2025년 1월 ~ 현재'],
            ['기술 스택', 'Python, Flask, PostgreSQL, SQLAlchemy, BeautifulSoup4'],
            ['배포 환경', 'Koyeb Cloud Platform'],
            ['데이터베이스', 'PostgreSQL (Koyeb Managed DB)'],
            ['주요 기능', '실시간 시장 분석, 자동 사업 발굴, 비즈니스 평가'],
        ]

        overview_table = Table(overview_data, colWidths=[2*inch, 4*inch])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), self.font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        story.append(overview_table)
        story.append(Spacer(1, 0.3*inch))

        # === 핵심 기능 ===
        story.append(Paragraph("⚙️ 핵심 기능", styles['CustomHeading1']))
        story.append(Spacer(1, 0.2*inch))

        story.append(Paragraph("1. 다중 플랫폼 실시간 시장 분석", styles['CustomHeading2']))
        story.append(Paragraph(
            "• <b>10개 주요 플랫폼</b> 실시간 데이터 수집 및 분석",
            styles['CustomBody']
        ))
        story.append(Paragraph(
            "• 크몽, 위시켓, 숨고, 탈잉, 쿠팡, 네이버, 구글, 유튜브, 블로그, 인스타그램",
            styles['CustomBody']
        ))
        story.append(Paragraph(
            "• 시장 수요, 경쟁 강도, 가격 분석을 통한 종합 점수 산출 (100점 만점)",
            styles['CustomBody']
        ))
        story.append(Spacer(1, 0.15*inch))

        story.append(Paragraph("2. 자동 비즈니스 발굴 시스템", styles['CustomHeading2']))
        story.append(Paragraph(
            "• <b>시간당 자동 실행</b>되는 비즈니스 아이디어 발굴",
            styles['CustomBody']
        ))
        story.append(Paragraph(
            "• Google Trends, 정부 창업 지원 사업, 시장 트렌드 기반 아이디어 생성",
            styles['CustomBody']
        ))
        story.append(Paragraph(
            "• 실시간 시장 분석 후 점수 60점 이상만 자동 저장",
            styles['CustomBody']
        ))
        story.append(Spacer(1, 0.15*inch))

        story.append(Paragraph("3. 비즈니스 평가 및 히스토리 관리", styles['CustomHeading2']))
        story.append(Paragraph(
            "• 발굴된 비즈니스에 대한 상세 분석 데이터 저장",
            styles['CustomBody']
        ))
        story.append(Paragraph(
            "• 승인/거부 이력 및 거부 사유 관리",
            styles['CustomBody']
        ))
        story.append(Paragraph(
            "• 시간대별 분석 결과 및 인사이트 저장",
            styles['CustomBody']
        ))
        story.append(Spacer(1, 0.15*inch))

        story.append(Paragraph("4. 정부 창업 지원 사업 정보 크롤링", styles['CustomHeading2']))
        story.append(Paragraph(
            "• K-Startup, 중소벤처기업부 등 정부 지원사업 자동 수집",
            styles['CustomBody']
        ))
        story.append(Paragraph(
            "• 지원금, 신청 기간, 대상 등 상세 정보 제공",
            styles['CustomBody']
        ))
        story.append(Spacer(1, 0.3*inch))

        # === 기술 아키텍처 ===
        story.append(PageBreak())
        story.append(Paragraph("🏗️ 기술 아키텍처", styles['CustomHeading1']))
        story.append(Spacer(1, 0.2*inch))

        tech_data = [
            ['레이어', '기술', '설명'],
            ['Frontend', 'HTML5, CSS3, JavaScript', '반응형 웹 인터페이스'],
            ['Backend', 'Flask (Python 3.13)', 'RESTful API 서버'],
            ['Database', 'PostgreSQL + SQLAlchemy', 'ORM 기반 데이터 관리'],
            ['Web Scraping', 'BeautifulSoup4, Requests', '실시간 시장 데이터 수집'],
            ['Scheduler', 'Threading, Time', '시간당 자동 실행 스케줄러'],
            ['Deployment', 'Koyeb Cloud', '자동 배포 및 확장'],
            ['Version Control', 'Git, GitHub', '소스 코드 버전 관리'],
        ]

        tech_table = Table(tech_data, colWidths=[1.5*inch, 2*inch, 2.5*inch])
        tech_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#283593')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), self.font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        story.append(tech_table)
        story.append(Spacer(1, 0.3*inch))

        # === 데이터베이스 스키마 ===
        story.append(Paragraph("🗄️ 데이터베이스 구조", styles['CustomHeading1']))
        story.append(Spacer(1, 0.2*inch))

        db_data = [
            ['테이블명', '용도', '주요 필드'],
            ['BusinessDiscoveryHistory', '발굴된 비즈니스 저장', 'business_idea, market_score, created_at'],
            ['BusinessAnalysisSnapshot', '상세 분석 데이터', 'analysis_data (JSON), platforms'],
            ['BusinessInsight', '비즈니스 인사이트', 'insight_type, content, confidence'],
            ['LowScoreBusiness', '저점수 비즈니스', 'reason, score'],
            ['StartupSupportProgram', '정부 지원사업', 'title, budget, deadline'],
            ['BusinessMeeting', '비즈니스 회의록', 'attendees, decisions, action_items'],
        ]

        db_table = Table(db_data, colWidths=[2*inch, 2*inch, 2*inch])
        db_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        story.append(db_table)
        story.append(Spacer(1, 0.3*inch))

        # === 주요 성과 ===
        story.append(Paragraph("📊 주요 성과", styles['CustomHeading1']))
        story.append(Spacer(1, 0.2*inch))

        achievements = [
            "✅ <b>시간당 자동 실행</b>으로 24시간 무중단 비즈니스 발굴",
            "✅ <b>10개 플랫폼 통합 분석</b>으로 정확도 향상",
            "✅ <b>실시간 시장 데이터</b> 기반 객관적 평가 시스템",
            "✅ <b>PostgreSQL 기반</b> 확장 가능한 데이터 관리",
            "✅ <b>Koyeb Cloud</b> 자동 배포 및 스케일링",
            "✅ <b>Git 연동</b> 코드 푸시 시 자동 재배포",
        ]

        for achievement in achievements:
            story.append(Paragraph(achievement, styles['CustomBody']))
            story.append(Spacer(1, 0.1*inch))

        story.append(Spacer(1, 0.3*inch))

        # === API 엔드포인트 ===
        story.append(PageBreak())
        story.append(Paragraph("🌐 API 엔드포인트", styles['CustomHeading1']))
        story.append(Spacer(1, 0.2*inch))

        api_data = [
            ['Method', 'Endpoint', '설명'],
            ['GET', '/', '메인 대시보드'],
            ['GET', '/business-discovery', '비즈니스 발굴 현황'],
            ['GET', '/business-history', '발굴 히스토리'],
            ['GET', '/business-review', '비즈니스 평가'],
            ['GET', '/startup-support', '정부 지원사업 정보'],
            ['GET', '/meetings', '비즈니스 회의록'],
            ['POST', '/trigger-discovery', '수동 비즈니스 발굴'],
            ['POST', '/approve-business/<id>', '비즈니스 승인'],
            ['POST', '/reject-business/<id>', '비즈니스 거부'],
            ['GET', '/api/business-stats', '통계 데이터 (JSON)'],
        ]

        api_table = Table(api_data, colWidths=[1*inch, 2.5*inch, 2.5*inch])
        api_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d32f2f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        story.append(api_table)
        story.append(Spacer(1, 0.3*inch))

        # === 향후 계획 ===
        story.append(Paragraph("🚀 향후 개선 계획", styles['CustomHeading1']))
        story.append(Spacer(1, 0.2*inch))

        future_plans = [
            "<b>1. 머신러닝 기반 예측 모델</b>",
            "   - 과거 데이터 학습을 통한 성공 가능성 예측",
            "   - 시장 트렌드 예측 알고리즘 개발",
            "",
            "<b>2. 실시간 알림 시스템</b>",
            "   - 유망 비즈니스 발견 시 이메일/SMS 알림",
            "   - Slack, Discord 웹훅 연동",
            "",
            "<b>3. 상세 재무 분석 기능</b>",
            "   - 예상 매출, 비용, 손익분기점 자동 계산",
            "   - 투자 회수 기간(ROI) 분석",
            "",
            "<b>4. 경쟁사 분석 강화</b>",
            "   - 경쟁사 가격, 리뷰, 마케팅 전략 분석",
            "   - SWOT 분석 자동 생성",
        ]

        for plan in future_plans:
            story.append(Paragraph(plan, styles['CustomBody']))
            story.append(Spacer(1, 0.08*inch))

        story.append(Spacer(1, 0.3*inch))

        # === 결론 ===
        story.append(Paragraph("💡 결론", styles['CustomHeading1']))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(
            "본 프로젝트는 <b>실시간 시장 데이터 분석</b>과 <b>자동화 시스템</b>을 결합하여 "
            "효율적인 비즈니스 발굴 프로세스를 구축했습니다. "
            "10개의 주요 플랫폼 데이터를 통합 분석하여 객관적이고 정확한 시장 평가를 제공하며, "
            "시간당 자동 실행으로 24시간 비즈니스 기회를 탐색합니다.",
            styles['CustomBody']
        ))
        story.append(Spacer(1, 0.15*inch))
        story.append(Paragraph(
            "향후 머신러닝 기반 예측 모델과 실시간 알림 시스템을 추가하여 "
            "더욱 정교하고 실용적인 플랫폼으로 발전시킬 계획입니다.",
            styles['CustomBody']
        ))

        # PDF 생성
        doc.build(story, onFirstPage=self.create_header_footer,
                 onLaterPages=self.create_header_footer)

        return self.filename

if __name__ == "__main__":
    generator = PortfolioGenerator()
    filename = generator.generate()
    print(f"\nPortfolio PDF generated: {filename}")
    print(f"File path: {os.path.abspath(filename)}")
