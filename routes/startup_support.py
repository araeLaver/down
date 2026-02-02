from flask import Blueprint, render_template, jsonify, request

from startup_support_crawler import StartupSupportCrawler

startup_support_bp = Blueprint('startup_support', __name__)


@startup_support_bp.route('/startup-support')
def startup_support():
    """1인 창업 지원사업 탐색 페이지"""
    return render_template('startup_support.html')


@startup_support_bp.route('/startup-roadmap')
def startup_roadmap():
    """창업 로드맵 대시보드"""
    return render_template('startup_roadmap.html')


@startup_support_bp.route('/api/startup-support/programs')
def api_startup_support_programs():
    """모든 창업 지원사업 조회"""
    try:
        crawler = StartupSupportCrawler()
        programs = crawler.get_all_support_programs()
        return jsonify(programs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@startup_support_bp.route('/api/startup-support/recommend', methods=['POST'])
def api_startup_support_recommend():
    """사용자 맞춤 지원사업 추천"""
    try:
        user_profile = request.json
        crawler = StartupSupportCrawler()
        recommendations = crawler.get_recommended_programs(user_profile)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@startup_support_bp.route('/api/startup-support/search')
def api_startup_support_search():
    """지원사업 검색"""
    try:
        keyword = request.args.get('keyword')
        category = request.args.get('category')
        max_amount = request.args.get('max_amount')

        crawler = StartupSupportCrawler()
        results = crawler.search_programs(
            keyword=keyword,
            category=category,
            max_amount=max_amount
        )
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@startup_support_bp.route('/api/startup-roadmap/phases')
def api_roadmap_phases():
    """창업 로드맵 단계 조회"""
    phases = [
        {
            'id': 1,
            'title': '아이디어 검증',
            'description': '시장 조사 및 아이디어 검증 단계',
            'status': 'completed',
            'progress': 100,
            'tasks': [
                {'id': 1, 'title': '시장 조사 및 경쟁 분석', 'done': True},
                {'id': 2, 'title': '타겟 고객 정의', 'done': True},
                {'id': 3, 'title': '문제점/솔루션 가설 수립', 'done': True},
                {'id': 4, 'title': 'AI 사업 아이디어 발굴', 'done': True}
            ]
        },
        {
            'id': 2,
            'title': '사업 계획 수립',
            'description': '비즈니스 모델 및 사업계획서 작성',
            'status': 'in_progress',
            'progress': 40,
            'tasks': [
                {'id': 5, 'title': '비즈니스 모델 캔버스 작성', 'done': True},
                {'id': 6, 'title': '수익 모델 설계', 'done': True},
                {'id': 7, 'title': '사업계획서 작성', 'done': False},
                {'id': 8, 'title': '재무 계획 수립', 'done': False},
                {'id': 9, 'title': '창업 지원사업 신청', 'done': False}
            ]
        },
        {
            'id': 3,
            'title': '법인 설립 & 준비',
            'description': '사업자 등록 및 법인 설립',
            'status': 'pending',
            'progress': 0,
            'tasks': [
                {'id': 10, 'title': '사업자 등록 (개인/법인)', 'done': False},
                {'id': 11, 'title': '사업장 확보', 'done': False},
                {'id': 12, 'title': '통장/카드 개설', 'done': False},
                {'id': 13, 'title': '필요 인허가 취득', 'done': False}
            ]
        },
        {
            'id': 4,
            'title': 'MVP 개발',
            'description': '최소 기능 제품 개발 및 테스트',
            'status': 'pending',
            'progress': 0,
            'tasks': [
                {'id': 14, 'title': '핵심 기능 정의', 'done': False},
                {'id': 15, 'title': '프로토타입 개발', 'done': False},
                {'id': 16, 'title': '베타 테스트', 'done': False},
                {'id': 17, 'title': '피드백 반영', 'done': False}
            ]
        },
        {
            'id': 5,
            'title': '런칭 & 성장',
            'description': '제품 출시 및 성장 전략 실행',
            'status': 'pending',
            'progress': 0,
            'tasks': [
                {'id': 18, 'title': '마케팅 전략 실행', 'done': False},
                {'id': 19, 'title': '첫 고객 확보', 'done': False},
                {'id': 20, 'title': '피드백 수집 및 개선', 'done': False},
                {'id': 21, 'title': '스케일업 준비', 'done': False}
            ]
        }
    ]
    return jsonify(phases)


@startup_support_bp.route('/api/startup-roadmap/stats')
def api_roadmap_stats():
    """창업 로드맵 통계"""
    stats = {
        'current_phase': 2,
        'current_phase_name': '사업 계획 수립',
        'completed_tasks': 6,
        'total_tasks': 21,
        'overall_progress': 29,
        'days_elapsed': 15,
        'next_milestone': '사업계획서 작성 완료'
    }
    return jsonify(stats)


@startup_support_bp.route('/api/startup-roadmap/weekly-tasks')
def api_roadmap_weekly_tasks():
    """이번 주 할 일 목록"""
    tasks = [
        {'id': 1, 'title': '사업계획서 초안 작성', 'priority': 'high', 'done': False},
        {'id': 2, 'title': '창업지원센터 상담 예약', 'priority': 'high', 'done': False},
        {'id': 3, 'title': '시장 규모 조사', 'priority': 'medium', 'done': True},
        {'id': 4, 'title': '경쟁사 분석 자료 정리', 'priority': 'medium', 'done': False},
        {'id': 5, 'title': '예비창업패키지 지원 조건 확인', 'priority': 'low', 'done': False}
    ]
    return jsonify(tasks)


@startup_support_bp.route('/api/startup-roadmap/task/<int:task_id>', methods=['PUT'])
def api_roadmap_update_task(task_id):
    """태스크 상태 업데이트"""
    data = request.get_json()
    done = data.get('done', False)
    return jsonify({
        'success': True,
        'task_id': task_id,
        'done': done
    })
