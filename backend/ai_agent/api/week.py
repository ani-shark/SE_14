
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from ai_agent.models import Course, RoleEnum, User, Week, UserCourse
from ai_agent import db
from ai_agent.utils import admin_required
from ai_agent.validation import validate_week


week_bp = Blueprint('week', __name__)

class WeekAPI(MethodView):
    
    def get(self, id):
        
        week = Week.query.get(id)
        if not week:
            return jsonify(error="week not found"), 404
        
        return jsonify(week.to_dict()), 200
    
    @admin_required
    def post(self):
        
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != RoleEnum.ADMIN:
            return jsonify(error="unauthorized"), 403
        
        data = request.get_json()
        try:
            validate_week(data)
            
            week = Week(
                name=data.get('name'),
                course_id=data.get('course_id')
            )
            db.session.add(week)
            db.session.commit()
            
            return jsonify(message="week created successfully",**week.to_dict()), 201
        
        except Exception as e:
            return jsonify(error = str(e)), 400
    
    @admin_required
    def put(self, id):
        
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != RoleEnum.ADMIN:
            return jsonify(error="unauthorized"), 403
        
        week = Week.query.get(id)
        if not week:
            return jsonify(error="week not found"), 404
        
        data = request.get_json()
        try:
            validate_week(data)    
            week.name = data.get('name', week.name)
            week.course_id = data.get('course_id',week.course_id)
            
            db.session.commit()
            
            return jsonify(message="week updated successfully",**week.to_dict()), 200
        
        except Exception as e:
            return jsonify(error = str(e)), 400
    
    
    @admin_required
    def delete(self, id):
        
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != RoleEnum.ADMIN:
            return jsonify(error="unauthorized"), 403
        
        
        week = Week.query.get(id)
        if not week:
            return jsonify(error="week not found"), 404
        
        db.session.delete(week)
        db.session.commit()
        
        return jsonify(message="week deleted successfully"), 200

    

week_api = WeekAPI.as_view('week_api')

week_bp.add_url_rule('/create', view_func=week_api, methods=['POST'])
week_bp.add_url_rule('/<int:id>', view_func=week_api, methods=['GET','PUT', 'DELETE'])

@week_bp.route('/all', methods=['GET'])
#@jwt_required()
def get_weeks():
    course_id = request.args.get("course_id")

    if not course_id:
        return jsonify(error="Missing course_id"), 400

    weeks = Week.query.filter_by(course_id=course_id).all()

    if not weeks:
        return jsonify(error="No weeks found for this course"), 404

    return jsonify([week.to_dict() for week in weeks]), 200



@week_bp.route('/user/courses', methods=['GET'])
@jwt_required()
def get_user_courses():
    user_id = get_jwt_identity()  

    if not user_id:
        return jsonify(error="User ID is required"), 400

    registered_courses = UserCourse.query.filter_by(user_id=user_id).all()

    if not registered_courses:
        return jsonify(error="No courses found for this user"), 404

    courses = Course.query.filter(Course.id.in_([course.course_id for course in registered_courses])).all()

    return jsonify([{"id": course.id, "name": course.name, "intro": course.intro} for course in courses]), 200
