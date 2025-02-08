from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from backend.models import Course, Message, db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return jsonify({'message': 'Welcome to Group 25 SE Project!'})

@main_bp.route('/status')
def status():
    return jsonify({'status': 'API operational'})

@main_bp.route('/classes', methods=['GET', 'POST'])
@login_required
def manage_classes():
    if request.method == 'GET':
        courses = Course.query.all()
        return jsonify([{
            'id': c.id,
            'code': c.course_code,
            'name': c.course_name
        } for c in courses])
        
    elif request.method == 'POST':
        data = request.json
        course = Course.query.get(data['course_id'])
        if course:
            current_user.registered_courses.append(course)
            db.session.commit()
            return jsonify({"message": "Course registered successfully"})
        return jsonify({"error": "Course not found"}), 404

@main_bp.route('/ai-message', methods=['POST'])
@login_required
def ai_message():
    data = request.json
    message = Message(content=data['message'], user_id=current_user.id)
    message.response = "AI agent to be initialized soon"
    db.session.add(message)
    db.session.commit()
    return jsonify({
        "message": message.content,
        "response": message.response,
        "timestamp": message.timestamp.isoformat()
    })

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return jsonify({
        "user": current_user.username,
        "courses": [{
            "code": c.course_code,
            "name": c.course_name
        } for c in current_user.registered_courses]
    })