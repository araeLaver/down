from flask import Blueprint, jsonify, request
from flask import render_template
from datetime import datetime

from services.db import Session
from database_setup import EmployeeSuggestion, SuggestionFeedback, Employee

suggestions_bp = Blueprint('suggestions', __name__)


@suggestions_bp.route('/suggestions')
def suggestions():
    """직원 건의사항 페이지"""
    return render_template('suggestions.html')


@suggestions_bp.route('/api/suggestions')
def api_suggestions():
    """건의사항 목록 API"""
    session = Session()
    try:
        suggestions = session.query(EmployeeSuggestion).order_by(
            EmployeeSuggestion.created_at.desc()
        ).limit(20).all()

        employee_ids = list(set(s.employee_id for s in suggestions))
        employees_dict = {e.employee_id: e for e in session.query(Employee).filter(
            Employee.employee_id.in_(employee_ids)
        ).all()} if employee_ids else {}

        suggestion_list = []
        for suggestion in suggestions:
            employee = employees_dict.get(suggestion.employee_id)
            employee_name = employee.name if employee else suggestion.employee_id

            suggestion_data = {
                'id': suggestion.id,
                'suggestion_id': suggestion.suggestion_id,
                'employee_id': suggestion.employee_id,
                'employee_name': employee_name,
                'category': suggestion.category,
                'priority': suggestion.priority,
                'title': suggestion.title,
                'description': suggestion.description,
                'suggested_solution': suggestion.suggested_solution,
                'expected_benefit': suggestion.expected_benefit,
                'implementation_difficulty': suggestion.implementation_difficulty,
                'status': suggestion.status,
                'created_at': suggestion.created_at.strftime('%Y-%m-%d %H:%M') if suggestion.created_at else None,
                'reviewed_at': suggestion.reviewed_at.strftime('%Y-%m-%d %H:%M') if suggestion.reviewed_at else None,
                'estimated_impact': suggestion.estimated_impact,
                'tags': suggestion.tags if suggestion.tags else []
            }
            suggestion_list.append(suggestion_data)

        stats = {
            'total': len(suggestion_list),
            'submitted': len([s for s in suggestion_list if s['status'] == 'submitted']),
            'reviewing': len([s for s in suggestion_list if s['status'] == 'reviewing']),
            'approved': len([s for s in suggestion_list if s['status'] == 'approved']),
            'implemented': len([s for s in suggestion_list if s['status'] == 'implemented'])
        }

        return jsonify({
            'suggestions': suggestion_list,
            'stats': stats
        })
    finally:
        session.close()


@suggestions_bp.route('/api/suggestions/<int:suggestion_id>')
def api_suggestion_detail(suggestion_id):
    """특정 건의사항 상세 정보 API"""
    session = Session()
    try:
        suggestion = session.query(EmployeeSuggestion).filter_by(id=suggestion_id).first()
        if not suggestion:
            return jsonify({'error': 'Suggestion not found'}), 404

        employee = session.query(Employee).filter_by(employee_id=suggestion.employee_id).first()

        feedbacks = session.query(SuggestionFeedback).filter_by(
            suggestion_id=suggestion.suggestion_id
        ).order_by(SuggestionFeedback.created_at.desc()).all()

        feedback_list = []
        for feedback in feedbacks:
            feedback_list.append({
                'id': feedback.id,
                'feedback_type': feedback.feedback_type,
                'feedback_text': feedback.feedback_text,
                'created_by': feedback.created_by,
                'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M'),
                'is_internal': feedback.is_internal
            })

        suggestion_detail = {
            'id': suggestion.id,
            'suggestion_id': suggestion.suggestion_id,
            'employee_id': suggestion.employee_id,
            'employee_name': employee.name if employee else suggestion.employee_id,
            'employee_role': employee.role if employee else '',
            'category': suggestion.category,
            'priority': suggestion.priority,
            'title': suggestion.title,
            'description': suggestion.description,
            'suggested_solution': suggestion.suggested_solution,
            'expected_benefit': suggestion.expected_benefit,
            'implementation_difficulty': suggestion.implementation_difficulty,
            'status': suggestion.status,
            'created_at': suggestion.created_at.strftime('%Y-%m-%d %H:%M') if suggestion.created_at else None,
            'reviewed_at': suggestion.reviewed_at.strftime('%Y-%m-%d %H:%M') if suggestion.reviewed_at else None,
            'implemented_at': suggestion.implemented_at.strftime('%Y-%m-%d %H:%M') if suggestion.implemented_at else None,
            'reviewer_notes': suggestion.reviewer_notes,
            'implementation_cost': suggestion.implementation_cost,
            'estimated_impact': suggestion.estimated_impact,
            'tags': suggestion.tags if suggestion.tags else [],
            'feedbacks': feedback_list
        }

        return jsonify(suggestion_detail)
    finally:
        session.close()


@suggestions_bp.route('/api/suggestions', methods=['POST'])
def api_create_suggestion():
    """새 건의사항 생성 API"""
    data = request.json

    session = Session()
    try:
        today = datetime.now()
        suggestion_id = f"SUG_{today.strftime('%Y%m%d')}_{session.query(EmployeeSuggestion).count() + 1:03d}"

        suggestion = EmployeeSuggestion(
            suggestion_id=suggestion_id,
            employee_id=data.get('employee_id'),
            category=data.get('category'),
            priority=data.get('priority', 'medium'),
            title=data.get('title'),
            description=data.get('description'),
            suggested_solution=data.get('suggested_solution'),
            expected_benefit=data.get('expected_benefit'),
            implementation_difficulty=data.get('implementation_difficulty', 'medium'),
            estimated_impact=data.get('estimated_impact'),
            tags=data.get('tags', [])
        )

        session.add(suggestion)
        session.commit()

        return jsonify({
            'success': True,
            'suggestion_id': suggestion_id,
            'id': suggestion.id
        })
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@suggestions_bp.route('/api/suggestions/<int:suggestion_id>/feedback', methods=['POST'])
def api_add_suggestion_feedback(suggestion_id):
    """건의사항에 피드백 추가 API"""
    data = request.json

    session = Session()
    try:
        suggestion = session.query(EmployeeSuggestion).filter_by(id=suggestion_id).first()
        if not suggestion:
            return jsonify({'error': 'Suggestion not found'}), 404

        feedback = SuggestionFeedback(
            suggestion_id=suggestion.suggestion_id,
            feedback_type=data.get('feedback_type', 'comment'),
            feedback_text=data.get('feedback_text'),
            created_by=data.get('created_by', 'System'),
            is_internal=data.get('is_internal', False)
        )

        session.add(feedback)
        session.commit()

        return jsonify({'success': True, 'id': feedback.id})
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@suggestions_bp.route('/api/suggestions/<int:suggestion_id>/status', methods=['PUT'])
def api_update_suggestion_status(suggestion_id):
    """건의사항 상태 업데이트 API"""
    data = request.json

    session = Session()
    try:
        suggestion = session.query(EmployeeSuggestion).filter_by(id=suggestion_id).first()
        if not suggestion:
            return jsonify({'error': 'Suggestion not found'}), 404

        old_status = suggestion.status
        suggestion.status = data.get('status')
        suggestion.reviewer_notes = data.get('reviewer_notes')

        if suggestion.status in ['approved', 'rejected'] and old_status == 'submitted':
            suggestion.reviewed_at = datetime.utcnow()
        elif suggestion.status == 'implemented':
            suggestion.implemented_at = datetime.utcnow()
            suggestion.implementation_cost = data.get('implementation_cost')

        session.commit()

        return jsonify({'success': True})
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
