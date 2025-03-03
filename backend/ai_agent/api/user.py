from flask import request, jsonify, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from ai_agent import db
from ai_agent.models import Course, McqScores, ProgrammingScores, User, RoleEnum, UserCourse
from ai_agent.validation import validate_user

user_bp = Blueprint('user', __name__)


class UserAPI(MethodView):
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict()), 200
        
        return jsonify(error="user not found"), 404

    def post(self):
        data = request.get_json()
        
        try:
            validate_user(data)
            user = User(
                email=data.get('email'),
                name=data.get('name'),
                role=RoleEnum.STUDENT
            )
            db.session.add(user)
            db.session.commit()
            
            register_courses = data.get('register_courses')
            new_enrolled_courses = []
            
            for course_id,course_name in register_courses:
                course = Course.query.get(course_id)
                if course:
                    new_enrolled_courses.append(UserCourse(user_id = user.id, course_id=course.id))
                    
            db.session.add_all(new_enrolled_courses)
            db.session.commit()
                    
            return jsonify(message="user registered successfully", **user.to_dict()), 201
        
        except Exception as e:
            return jsonify(error = str(e)), 400
    
    
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify(error="user not found"), 404
        
        data = request.get_json()
        try:
            
            validate_user(data,is_update=True)
            user.email = data.get('email')
            user.name = data.get('name')
            db.session.commit()
        
            register_courses = data.get('register_courses')
        
            user_courses = {uc.course_id: uc for uc in UserCourse.query.filter_by(user_id=user_id, status='pending').all()}
        
        # Remove courses that are not in registered_courses
            for course_id, user_course in list(user_courses.items()):
                if user_course.status == 'pending' and course_id not in [item[0] for item in register_courses]:
                    db.session.delete(user_course)
                    db.session.commit()
    
        # Add new courses from registered_courses that are not in user_courses
            for course_id,course_name in register_courses:
                if course_id not in user_courses:
                    new_course = UserCourse(user_id=user_id, course_id=course_id, status='pending')
                    db.session.add(new_course)
                    db.session.commit()
            
            return jsonify({"message": "user data updated successfully", **user.to_dict()}),200
        
        except Exception as e:
            return jsonify(error = str(e)), 400
    

class UserCoursesAPI(MethodView):
    
    @jwt_required()
    def get(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify(error="user not found"), 404
       
        
        course_check = Course.query.get(course_id)
        if not course_check:
            return jsonify(error="course not found"), 404
            
            
        course_content = course_check.to_dict()
        is_enrolled = UserCourse.query.filter_by(user_id=user.id,course_id=course_check.id).first()
        
        if not is_enrolled:
            return jsonify(error="user not enrolled in this course"), 401
            
        resp = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role.value,
            "course_content":course_content,
            "mcq_scores":[],
            "programming_scores":[]
        }
        
        for week in course_content['weeks']:
            for mcq in week['mcq']:
                case = McqScores.query.filter_by(user_id = user.user_id, mcq_id = mcq['id']).first()
                if case:
                    resp['mcq_scores'].append(case.to_dict())
            
            for prog in week['programming']:
                case = ProgrammingScores.query.filter_by(user_id = user.user_id, programming_id = prog['id']).first()
                if case:
                    resp['programming_scores'].append(case.to_dict())
                            
        
        return jsonify(resp), 200

     





user_api = UserAPI.as_view('user_api')
usercourses_api = UserCoursesAPI.as_view('usercourses_api')


user_bp.add_url_rule('/get', view_func=user_api, methods=['GET'])
user_bp.add_url_rule('/register', view_func=user_api, methods=['POST'])
user_bp.add_url_rule('/edit', view_func=user_api, methods=['PUT'])

user_bp.add_url_rule('/courses/<int:course_id>', view_func=usercourses_api, methods=['GET'])


