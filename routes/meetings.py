from flask import Blueprint, render_template, jsonify
import json

from services.db import Session
from database_setup import BusinessMeeting

meetings_bp = Blueprint('meetings', __name__)


@meetings_bp.route('/meetings')
def meetings():
    """회의 보고서 페이지"""
    return render_template('meetings.html')


@meetings_bp.route('/api/meetings')
def api_meetings():
    """회의 보고서 API"""
    session = Session()
    try:
        meetings = session.query(BusinessMeeting).order_by(
            BusinessMeeting.meeting_date.desc()
        ).limit(10).all()

        meeting_list = []
        for meeting in meetings:
            agenda_data = []
            if meeting.agenda:
                try:
                    agenda_data = json.loads(meeting.agenda)
                except json.JSONDecodeError:
                    if ')' in meeting.agenda:
                        agenda_data = [item.strip() for item in meeting.agenda.replace(') ', ')\n').split('\n') if item.strip()]
                    else:
                        agenda_data = [meeting.agenda]

            participants_data = _parse_participants(meeting.participants)

            meeting_notes_data = {}
            if meeting.meeting_notes:
                try:
                    meeting_notes_data = json.loads(meeting.meeting_notes)
                except:
                    pass

            meeting_data = {
                'id': meeting.id,
                'title': meeting.title,
                'meeting_type': meeting.meeting_type,
                'date': meeting.meeting_date.strftime('%Y-%m-%d %H:%M') if meeting.meeting_date else None,
                'status': meeting.status,
                'agenda': agenda_data,
                'key_decisions': meeting.key_decisions if meeting.key_decisions else [],
                'action_items': meeting.action_items if meeting.action_items else [],
                'participants': participants_data,
                'meeting_notes': meeting_notes_data
            }
            meeting_list.append(meeting_data)

        return jsonify({
            'meetings': meeting_list,
            'total_count': len(meeting_list)
        })
    finally:
        session.close()


@meetings_bp.route('/api/meetings/<int:meeting_id>')
def api_meeting_detail(meeting_id):
    """특정 회의 상세 정보 API"""
    session = Session()
    try:
        meeting = session.query(BusinessMeeting).filter_by(id=meeting_id).first()
        if not meeting:
            return jsonify({'error': 'Meeting not found'}), 404

        meeting_notes = {}
        if meeting.meeting_notes:
            try:
                meeting_notes = json.loads(meeting.meeting_notes)
            except:
                pass

        agenda_data = []
        if meeting.agenda:
            try:
                agenda_data = json.loads(meeting.agenda)
            except json.JSONDecodeError:
                if ')' in meeting.agenda:
                    agenda_data = [item.strip() for item in meeting.agenda.replace(') ', ')\n').split('\n') if item.strip()]
                else:
                    agenda_data = [meeting.agenda]

        participants_data = _parse_participants(meeting.participants)

        meeting_detail = {
            'id': meeting.id,
            'title': meeting.title,
            'meeting_type': meeting.meeting_type,
            'date': meeting.meeting_date.strftime('%Y-%m-%d %H:%M') if meeting.meeting_date else None,
            'status': meeting.status,
            'agenda': agenda_data,
            'key_decisions': meeting.key_decisions if meeting.key_decisions else [],
            'action_items': meeting.action_items if meeting.action_items else [],
            'participants': participants_data,
            'meeting_notes': meeting_notes
        }

        return jsonify(meeting_detail)
    finally:
        session.close()


def _parse_participants(participants):
    """참가자 데이터 파싱 헬퍼"""
    participants_data = []
    if participants:
        if isinstance(participants, list):
            participants_data = participants
        elif isinstance(participants, str):
            try:
                participants_data = json.loads(participants)
            except json.JSONDecodeError:
                if ',' in participants:
                    participants_data = [p.strip() for p in participants.split(',')]
                else:
                    participants_data = [participants]
    return participants_data
