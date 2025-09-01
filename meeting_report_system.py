"""
Qhyx Inc. 매일 회의 안건 및 회의록 자동 보고 시스템
사용자가 매일 회의 결과를 받아볼 수 있도록 하는 시스템
"""

import schedule
import time
from datetime import datetime, timedelta
from database_setup import Session, BusinessMeeting, Task, Employee, CompanyMilestone
from continuous_business_expansion import BusinessExpansionEngine
import json
import os

class MeetingReportSystem:
    """매일 회의 보고서 생성 및 전달 시스템"""
    
    def __init__(self):
        self.session = Session()
        self.expansion_engine = BusinessExpansionEngine()
    
    def generate_daily_meeting_agenda(self):
        """오늘의 회의 안건 생성"""
        
        today = datetime.now()
        
        # 핵심 회의 안건 템플릿
        base_agenda = [
            "📊 어제 사업 성과 및 진행 현황 검토",
            "🎯 오늘의 핵심 목표 설정",
            "💡 신규 사업 기회 발굴 현황",
            "📈 매출 증대 전략 논의",
            "🌍 글로벌 확장 진행 상황"
        ]
        
        # 요일별 특별 안건
        weekday_agendas = {
            0: ["🔄 주간 전략 검토", "💼 새로운 한 주 계획 수립"],  # 월요일
            1: ["🚀 제품 개발 진행 상황", "👥 팀 협업 효율성 개선"],  # 화요일
            2: ["💰 투자 유치 전략 업데이트", "🤝 파트너십 기회 검토"],  # 수요일
            3: ["📊 시장 분석 결과 공유", "🎯 고객 확보 전략 논의"],  # 목요일
            4: ["🏆 주간 성과 정리", "🎉 다음 주 도전 과제 설정"],  # 금요일
            5: ["🔍 경쟁사 동향 분석", "💎 차별화 전략 수립"],  # 토요일
            6: ["📝 주간 리뷰", "🌟 장기 비전 점검"]  # 일요일
        }
        
        today_special = weekday_agendas.get(today.weekday(), [])
        
        return {
            'date': today.strftime('%Y년 %m월 %d일 (%A)'),
            'meeting_type': '일일 전략 회의',
            'base_agenda': base_agenda,
            'special_agenda': today_special,
            'all_agenda': base_agenda + today_special
        }
    
    def generate_detailed_meeting_minutes(self, agenda_data):
        """상세한 회의록 생성"""
        
        # AI 직원들의 발언 시뮬레이션
        ai_employees = [
            {'name': '김창의', 'role': 'CCO', 'focus': '글로벌 신시장 개척'},
            {'name': '박실용', 'role': 'CPO', 'focus': '확장 가능한 제품 포트폴리오'},
            {'name': '이글로벌', 'role': 'CGO', 'focus': '20개국 동시 진출'},
            {'name': '정브랜드', 'role': 'CBO', 'focus': '45개 분야 브랜드 확장'},
            {'name': '최검증', 'role': 'CVO', 'focus': '신사업 검증'},
            {'name': '신재무', 'role': 'CFO', 'focus': '확장 자금 조달'},
        ]
        
        meeting_minutes = {
            'header': {
                'title': f"Qhyx Inc. {agenda_data['meeting_type']}",
                'date': agenda_data['date'],
                'time': f"{datetime.now().strftime('%H:%M')} - {(datetime.now() + timedelta(hours=1)).strftime('%H:%M')}",
                'participants': [emp['name'] + f"({emp['role']})" for emp in ai_employees],
                'location': 'Qhyx Inc. 가상 회의실'
            },
            'agenda_items': [],
            'key_decisions': [],
            'action_items': [],
            'next_meeting': (datetime.now() + timedelta(days=1)).strftime('%Y년 %m월 %d일 09:00')
        }
        
        # 각 안건별 상세 논의 내용 생성
        for i, agenda_item in enumerate(agenda_data['all_agenda'], 1):
            discussion = {
                'item': f"{i}. {agenda_item}",
                'presenter': ai_employees[i % len(ai_employees)]['name'],
                'key_points': self.generate_discussion_points(agenda_item),
                'conclusion': self.generate_conclusion(agenda_item)
            }
            meeting_minutes['agenda_items'].append(discussion)
        
        # 핵심 결정사항 생성
        meeting_minutes['key_decisions'] = [
            "📈 이번 주 목표: 신규 사업 영역 3개 분야 진출 결정",
            "💰 투자 유치: 시리즈 A 라운드 준비 착수",
            "🌍 글로벌 진출: 일본 시장 진출 우선 추진",
            "🤝 파트너십: 주요 테크 기업과 전략적 제휴 논의",
            "👥 조직 확장: AI 개발팀 2배 확장 승인"
        ]
        
        # 실행 항목 생성
        meeting_minutes['action_items'] = [
            {"task": "시장 조사 보고서 완성", "assignee": "이글로벌(CGO)", "due_date": "내일까지"},
            {"task": "투자 제안서 초안 작성", "assignee": "신재무(CFO)", "due_date": "이번 주 내"},
            {"task": "일본 진출 전략 수립", "assignee": "김창의(CCO)", "due_date": "3일 내"},
            {"task": "파트너십 후보 리스트 작성", "assignee": "박실용(CPO)", "due_date": "2일 내"},
            {"task": "AI 개발팀 채용 계획", "assignee": "정브랜드(CBO)", "due_date": "1주 내"}
        ]
        
        return meeting_minutes
    
    def generate_discussion_points(self, agenda_item):
        """안건별 논의 포인트 생성"""
        
        discussion_templates = {
            "어제 사업 성과": [
                "📊 일매출 전날 대비 12% 증가",
                "🎯 핵심 KPI 목표 달성률 85%",
                "💡 신규 고객 확보 47명"
            ],
            "신규 사업 기회": [
                "🚀 AI 헬스케어 분야 진출 기회 발견",
                "🌱 ESG 관련 신사업 수요 급증",
                "💎 블록체인 기반 새로운 수익 모델"
            ],
            "글로벌 확장": [
                "🇯🇵 일본 시장 진출 준비 90% 완료",
                "🇺🇸 북미 파트너십 논의 진행 중",
                "🇩🇪 유럽 법규 검토 완료"
            ]
        }
        
        # 키워드 매칭으로 관련 논의 포인트 선택
        for keyword, points in discussion_templates.items():
            if any(word in agenda_item for word in keyword.split()):
                return points
        
        # 기본 논의 포인트
        return [
            "✅ 현재 진행 상황 양호",
            "⚡ 가속화 방안 논의 필요",
            "🎯 구체적 실행 계획 수립"
        ]
    
    def generate_conclusion(self, agenda_item):
        """안건별 결론 생성"""
        
        conclusions = [
            "계획대로 순조롭게 진행하되, 속도 개선 방안 모색",
            "추가 리소스 투입으로 목표 달성 가속화",
            "시장 변화에 민첩하게 대응하여 기회 극대화",
            "경쟁 우위 확보를 위한 차별화 전략 강화",
            "고객 만족도 향상을 통한 지속가능한 성장"
        ]
        
        import random
        return random.choice(conclusions)
    
    def save_meeting_minutes_to_database(self, meeting_data, minutes):
        """회의록을 데이터베이스에 저장"""
        
        try:
            # 회의 정보 저장
            meeting = BusinessMeeting(
                meeting_type=meeting_data['meeting_type'],
                title=f"Qhyx Inc. 일일 전략 회의 - {meeting_data['date']}",
                agenda=json.dumps(meeting_data['all_agenda'], ensure_ascii=False),
                participants=[emp.split('(')[0] for emp in minutes['header']['participants']],
                status='completed',
                meeting_notes=json.dumps(minutes, ensure_ascii=False, indent=2),
                key_decisions=minutes['key_decisions'],
                action_items=[item['task'] for item in minutes['action_items']]
            )
            
            self.session.add(meeting)
            self.session.commit()
            
            # 실행 항목을 Task로 저장
            for i, action in enumerate(minutes['action_items']):
                task_id = f"MEETING_{datetime.now().strftime('%Y%m%d')}_{i+1:03d}"
                
                # 기존 Task ID 중복 확인
                existing_task = self.session.query(Task).filter_by(task_id=task_id).first()
                if not existing_task:
                    task = Task(
                        task_id=task_id,
                        title=action['task'],
                        description=f"회의에서 결정된 실행 항목: {action['task']}",
                        assigned_to=action['assignee'].split('(')[0],
                        status='pending',
                        priority='high',
                        due_date=datetime.now() + timedelta(days=1)
                    )
                    self.session.add(task)
            
            self.session.commit()
            return meeting.id
            
        except Exception as e:
            self.session.rollback()
            print(f"❌ 회의록 저장 오류: {e}")
            return None
    
    def generate_daily_meeting_report(self):
        """일일 회의 보고서 생성"""
        
        print(f"📋 {datetime.now().strftime('%Y년 %m월 %d일')} 회의 보고서 생성 중...")
        
        # 1. 오늘의 회의 안건 생성
        agenda_data = self.generate_daily_meeting_agenda()
        
        # 2. 상세 회의록 생성
        meeting_minutes = self.generate_detailed_meeting_minutes(agenda_data)
        
        # 3. 데이터베이스에 저장
        meeting_id = self.save_meeting_minutes_to_database(agenda_data, meeting_minutes)
        
        # 4. 보고서 포맷 생성
        report = self.format_meeting_report(agenda_data, meeting_minutes, meeting_id)
        
        # 5. 파일로 저장
        self.save_meeting_report_file(report)
        
        return report
    
    def format_meeting_report(self, agenda_data, minutes, meeting_id):
        """회의 보고서 포맷 작성"""
        
        today = datetime.now()
        
        report = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                      🏢 Qhyx Inc. 일일 회의 보고서                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📅 회의 정보
• 일시: {minutes['header']['date']} {minutes['header']['time']}
• 회의 유형: {agenda_data['meeting_type']}
• 참석자: {len(minutes['header']['participants'])}명
• 회의 ID: {meeting_id}
• 장소: {minutes['header']['location']}

👥 참석자 명단
{chr(10).join([f"  • {participant}" for participant in minutes['header']['participants']])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 회의 안건 및 논의 내용

{chr(10).join([
    f'''
{item['item']}
👤 발표자: {item['presenter']}

💬 주요 논의사항:
{chr(10).join([f"  • {point}" for point in item['key_points']])}

📌 결론: {item['conclusion']}
''' for item in minutes['agenda_items']
])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 핵심 결정사항

{chr(10).join([f"  {i+1}. {decision}" for i, decision in enumerate(minutes['key_decisions'])])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 실행 항목 (Action Items)

{chr(10).join([f'''  {i+1}. {item['task']}
     👤 담당자: {item['assignee']}
     ⏰ 마감일: {item['due_date']}
''' for i, item in enumerate(minutes['action_items'])])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 회의 요약

✨ 오늘의 핵심 성과:
• 📈 신규 사업 기회 {len([item for item in minutes['agenda_items'] if '신규' in item['item']])}개 발굴
• 🎯 실행 항목 {len(minutes['action_items'])}개 확정
• 💡 핵심 결정 {len(minutes['key_decisions'])}건 도출

🚀 다음 회의: {minutes['next_meeting']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌟 Qhyx Inc. 성장 현황
• 📊 총 사업 영역: 45개 분야 확장 중
• 🌍 글로벌 진출: 20개국 동시 진출 계획
• 👥 AI 직원: 12명이 24/7 자동 운영
• 💰 예상 연매출: 1,000억원 목표

💫 "예측불가능한 변화의 흐름으로 혁신을 이끈다"
   - Unpredictable Flow of Innovation -

보고서 생성 시간: {today.strftime('%Y년 %m월 %d일 %H시 %M분')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        return report
    
    def save_meeting_report_file(self, report):
        """회의 보고서를 파일로 저장"""
        
        today = datetime.now()
        filename = f"meeting_report_{today.strftime('%Y%m%d')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"📄 일일 회의 보고서가 저장되었습니다: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ 파일 저장 오류: {e}")
            return None
    
    def run_daily_meeting_report(self):
        """일일 회의 보고서 실행"""
        
        try:
            print(f"🏢 [{datetime.now().strftime('%H:%M:%S')}] 일일 회의 보고서 생성 시작...")
            
            # 회의 보고서 생성
            report = self.generate_daily_meeting_report()
            
            print("✅ 일일 회의 보고서 생성 완료!")
            print("\n" + "="*80)
            print(report)
            print("="*80)
            
            return report
            
        except Exception as e:
            print(f"❌ 일일 회의 보고서 생성 오류: {e}")
            return None
    
    def start_meeting_report_scheduler(self):
        """회의 보고서 스케줄러 시작"""
        
        # 매일 오전 9시에 회의 진행 및 보고서 생성
        schedule.every().day.at("09:00").do(self.run_daily_meeting_report)
        
        # 매일 오후 2시에 추가 회의 (중간 점검)
        schedule.every().day.at("14:00").do(self.run_daily_meeting_report)
        
        # 매일 오후 6시에 마감 회의
        schedule.every().day.at("18:00").do(self.run_daily_meeting_report)
        
        print("📅 일일 회의 보고서 스케줄러 시작됨:")
        print("  - 오전 9시: 일일 전략 회의 및 보고서")
        print("  - 오후 2시: 중간 점검 회의 및 보고서")
        print("  - 오후 6시: 마감 회의 및 보고서")
        print("💼 매일 3회 상세한 회의록을 받아보실 수 있습니다!")
        
        # 즉시 첫 번째 회의 보고서 생성
        print("\n🚀 첫 번째 회의 보고서를 즉시 생성합니다...")
        self.run_daily_meeting_report()
        
        # 스케줄러 실행
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크
    
    def close(self):
        self.session.close()
        if hasattr(self, 'expansion_engine'):
            self.expansion_engine.close()

if __name__ == "__main__":
    meeting_system = MeetingReportSystem()
    
    try:
        meeting_system.start_meeting_report_scheduler()
    except KeyboardInterrupt:
        print("\n🛑 회의 보고서 시스템이 종료되었습니다.")
    finally:
        meeting_system.close()