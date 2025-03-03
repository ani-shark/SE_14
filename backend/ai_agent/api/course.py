from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from ai_agent.models import Course, RoleEnum, User, Week
from ai_agent import db
from ai_agent.utils import admin_required
from ai_agent.validation import validate_course

course_bp = Blueprint('course', __name__)


class CourseAPI(MethodView):
    
    @admin_required
    def get(self,id):
                
        course = Course.query.get(id)
        if not course:
            return jsonify(error="course not found"), 404
        
        return jsonify(course.to_dict()), 200
    
    @admin_required
    def post(self):
        
        data = request.get_json()
        
        try:
            validate_course(data)
            
            course = Course(
                name=data.get('name'),
                intro=data.get('intro')
            )
            db.session.add(course)
            db.session.commit()
            
            new_weeks = []
            for i in range(12):
                new_weeks.append(Week(name=f'Week {i+1}',course_id=course.id))
            
            db.session.add_all(new_weeks)
            db.session.commit()
                
            return jsonify(message="course created successfully",**course.to_dict()), 201
        
        except Exception as e:
            return jsonify(error = str(e)), 400
    
    @admin_required
    def put(self, id):
        
        course = Course.query.get(id)
        if not course:
            return jsonify(error="course not found"), 404
        

        data = request.get_json()
        try:
            validate_course(data)
            
            course.name = data.get('name', course.name)
            course.intro = data.get('intro', course.intro)
            
            db.session.commit()
            
            return jsonify(message="course updated successfully",**course.to_dict()), 200
        
        except Exception as e:
            return jsonify(error = str(e)), 400
    
    @admin_required
    def delete(self, id):
        
        course = Course.query.get(id)
        if not course:
            return jsonify(error="course not found"), 404
        
        db.session.delete(course)
        db.session.commit()
        return jsonify(message="course deleted successfully"), 200


course_api = CourseAPI.as_view('course_api')


course_bp.add_url_rule('/create', view_func=course_api, methods=['POST'])
course_bp.add_url_rule('/<int:id>', view_func=course_api, methods=['GET','PUT', 'DELETE'])


@course_bp.route('/all',methods=['GET'])
@admin_required
def all_courses():
    all_courses = [course.to_dict() for course in Course.query.all()]
    return jsonify(all_courses),200

