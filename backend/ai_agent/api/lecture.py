from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from ai_agent.models import Course, Week, Lectures, User, RoleEnum
from ai_agent import db
from ai_agent.utils import admin_required

lecture_bp = Blueprint('lecture', __name__)

class LectureAPI(MethodView):

    def get(self, week_id=None):
        if week_id:
            lectures = Lectures.query.filter_by(week_id=week_id).all()
            return jsonify([lecture.to_dict() for lecture in lectures]), 200
        return jsonify(error="Week ID required"), 400

    @admin_required
    def post(self):
        data = request.get_json()
        week = Week.query.get(data.get('week_id'))
        if not week:
            return jsonify(error="Week not found"), 404
        
        lecture = Lectures(name=data.get('name'), week_id=week.id)
        db.session.add(lecture)
        db.session.commit()
        
        return jsonify(message="Lecture added successfully", **lecture.to_dict()), 201

    @admin_required
    def delete(self, id):
        lecture = Lectures.query.get(id)
        if not lecture:
            return jsonify(error="Lecture not found"), 404
        
        db.session.delete(lecture)
        db.session.commit()
        
        return jsonify(message="Lecture deleted successfully"), 200

lecture_api = LectureAPI.as_view('lecture_api')

lecture_bp.add_url_rule('/<int:week_id>', view_func=lecture_api, methods=['GET'])
lecture_bp.add_url_rule('/create', view_func=lecture_api, methods=['POST'])
lecture_bp.add_url_rule('/delete/<int:id>', view_func=lecture_api, methods=['DELETE'])

