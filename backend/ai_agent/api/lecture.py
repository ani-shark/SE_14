from flask import Blueprint, jsonify, request
from flask.views import MethodView
from ai_agent.models import Week, Lectures
from ai_agent import db
from ai_agent.utils import admin_required
from ai_agent.validation import validate_lecture

lecture_bp = Blueprint('lecture', __name__)

class LectureAPI(MethodView):

    def get(self, id):
        
        lecture = Lectures.query.get(id)
        if not lecture:
            return jsonify(error="lecture not found"), 404
        
        return jsonify(lecture.to_dict()), 200
        


    @admin_required
    def post(self):
        
        data = request.get_json()
        try:
            validate_lecture(data)
        
            lecture = Lectures(name=data.get('name'), week_id=data.get('week_id'),link=data.get('link'))
            db.session.add(lecture)
            db.session.commit()
            
            return jsonify(message="lecture created successfully", **lecture.to_dict()), 201
        
        except Exception as e:
            return jsonify(error = str(e)), 400
        
    
    @admin_required
    def put(self,id):
        
        lecture = Lectures.query.get(id)
        if not lecture:
            return jsonify(error="lecture not found"), 404
        
        
        data = request.get_json()
        try:
            validate_lecture(data)
            
            lecture.name = data.get('name',lecture.name)
            lecture.week_id = data.get('week_id',lecture.week_id)
            lecture.link = data.get('link',lecture.link)
            
         
            db.session.commit()
            
            return jsonify(message="lecture updated successfully", **lecture.to_dict()), 201
        
        except Exception as e:
            return jsonify(error = str(e)), 400
        
            

    @admin_required
    def delete(self, id):
        
        lecture = Lectures.query.get(id)
        if not lecture:
            return jsonify(error="lecture not found"), 404
        
        db.session.delete(lecture)
        db.session.commit()
        
        return jsonify(message="lecture deleted successfully"), 200

lecture_api = LectureAPI.as_view('lecture_api')


lecture_bp.add_url_rule('/create', view_func=lecture_api, methods=['POST'])
lecture_bp.add_url_rule('/<int:id>', view_func=lecture_api, methods=['GET','DELETE','PUT'])



