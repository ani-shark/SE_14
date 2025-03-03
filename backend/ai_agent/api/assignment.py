from flask import Blueprint, request, jsonify
from flask.views import MethodView
from ai_agent import db
from ai_agent.models import (
    ProgrammingAssignment, ProgrammingTestCase, McqAssignment,
    McqQuestion, McqOption, McqScores, ProgrammingScores, Lectures,
    User, RoleEnum
)
from ai_agent.utils import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity
import subprocess


assignment_bp = Blueprint('assignment', __name__)

# ---------------- Admin CRUD for MCQ Assignments ---------------- #

class McqAssignmentAPI(MethodView):
    @jwt_required()
    def get(self, assignment_id=None):
        """
        Get MCQ assignment(s)
        If assignment_id is provided, return that specific assignment
        Otherwise, return all MCQ assignments
        """
        if assignment_id:
            assignment = McqAssignment.query.get(assignment_id)
            if not assignment:
                return jsonify({"error": "Assignment not found"}), 404
            return jsonify(assignment.to_dict()), 200
        else:
            assignments = McqAssignment.query.all()
            return jsonify([assignment.to_dict() for assignment in assignments]), 200

    @admin_required
    def post(self):
        """Create a new MCQ assignment with questions and options (Admin only)."""
        data = request.json

        # Validate required fields
        week_id = data.get('week_id')
        title = data.get('title')
        description = data.get('description')
        questions = data.get('questions', [])

        if not week_id or not title or not questions:
            return jsonify({"error": "week_id, title, and at least one question are required"}), 400

        # Create the MCQ assignment
        new_mcq = McqAssignment(
            title=title,
            description=description,
            week_id=week_id
        )
        db.session.add(new_mcq)
        db.session.commit()

        # Add questions and options
        for question_data in questions:
            new_question = McqQuestion(
                text=question_data['text'],
                correct_option=question_data['correct_option'],
                assignment_id=new_mcq.id
            )
            db.session.add(new_question)
            db.session.commit()

            for option_text in question_data['options']:
                print(option_text)
                new_option = McqOption(
                    text=option_text['text'],
                    question_id=new_question.id
                )
                db.session.add(new_option)

        db.session.commit()

        # Return the full assignment with questions and options
        return jsonify(new_mcq.to_dict()), 201



    @admin_required
    def put(self, assignment_id):
        """Update an existing MCQ assignment (Admin only)."""
        assignment = McqAssignment.query.get(assignment_id)
        if not assignment:
            return jsonify({"error": "Assignment not found"}), 404

        data = request.json
        assignment.title = data.get('title', assignment.title)
        assignment.description = data.get('description', assignment.description)
        db.session.commit()

        return jsonify(assignment.to_dict()), 200

    @admin_required
    def delete(self, assignment_id):
        """Delete an MCQ assignment (Admin only)."""
        assignment = McqAssignment.query.get(assignment_id)
        if not assignment:
            return jsonify({"error": "Assignment not found"}), 404

        db.session.delete(assignment)
        db.session.commit()
        return jsonify({"message": "Assignment deleted"}), 200


# ---------------- Admin CRUD for Programming Assignments ---------------- #

class ProgrammingAssignmentAPI(MethodView):
    @jwt_required()
    def get(self, assignment_id=None):
        """
        Get Programming assignment(s)
        If assignment_id is provided, return that specific assignment
        Otherwise, return all Programming assignments
        """
        if assignment_id:
            assignment = ProgrammingAssignment.query.get(assignment_id)
            if not assignment:
                return jsonify({"error": "Assignment not found"}), 404
            return jsonify(assignment.to_dict()), 200
        else:
            assignments = ProgrammingAssignment.query.all()
            return jsonify([assignment.to_dict() for assignment in assignments]), 200
    @admin_required
    def post(self):
        """Create a new Programming assignment (Admin only)."""
        data = request.json
        week_id = data['week_id']
        title = data['title']
        description = data['description']
        test_cases = data['test_cases']

        new_assignment = ProgrammingAssignment(title=title, description=description, week_id=week_id)
        db.session.add(new_assignment)
        db.session.commit()

        for test_case in test_cases:
            new_test_case = ProgrammingTestCase(
                assignment_id=new_assignment.id,
                input=test_case['input'],
                expected_output=test_case['expected_output']
            )
            db.session.add(new_test_case)

        db.session.commit()

        return jsonify(new_assignment.to_dict()), 201

    @admin_required
    def put(self, assignment_id):
        """Update a Programming assignment (Admin only)."""
        assignment = ProgrammingAssignment.query.get(assignment_id)
        if not assignment:
            return jsonify({"error": "Assignment not found"}), 404

        data = request.json
        assignment.title = data.get('title', assignment.title)
        assignment.description = data.get('description', assignment.description)

        if 'test_cases' in data:
            ProgrammingTestCase.query.filter_by(assignment_id=assignment_id).delete()

            for test_case in data['test_cases']:
                new_test_case = ProgrammingTestCase(
                    assignment_id=assignment_id,
                    input=test_case['input'],
                    expected_output=test_case['expected_output']
                )
                db.session.add(new_test_case)

        db.session.commit()

        return jsonify(assignment.to_dict()), 200

    @admin_required
    def delete(self, assignment_id):
        """Delete a Programming assignment (Admin only)."""
        assignment = ProgrammingAssignment.query.get(assignment_id)
        if not assignment:
            return jsonify({"error": "Assignment not found"}), 404

        db.session.delete(assignment)
        db.session.commit()
        return jsonify({"message": "Assignment deleted"}), 200


# ---------------- User: Read and Submit Operations ---------------- #

class McqSubmitAPI(MethodView):
    @jwt_required()
    def get(self, assignment_id=None):
        """
        Get user's MCQ submissions/scores
        If assignment_id is provided, return scores for that specific assignment
        Otherwise, return all MCQ scores for the user
        """
        user_id = get_jwt_identity()
        
        if assignment_id:
            scores = McqScores.query.filter_by(user_id=user_id, assignment_id=assignment_id).all()
            if not scores:
                return jsonify({"message": "No submissions found for this assignment"}), 404
        else:
            scores = McqScores.query.filter_by(user_id=user_id).all()
            if not scores:
                return jsonify({"message": "No MCQ submissions found"}), 404
        
        result = []
        for score in scores:
            assignment = McqAssignment.query.get(score.assignment_id)
            result.append({
                "score_id": score.id,
                "assignment_id": score.assignment_id,
                "assignment_title": assignment.title if assignment else "Unknown",
                "score": score.score
            })
        
        return jsonify(result), 200
    @jwt_required()
    def post(self):
        """User submits MCQ assignment."""
        data = request.json
        user_id = get_jwt_identity()
        assignment_id = data['assignment_id']
        answers = data['answers']  # { question_id: selected_option_id }

        assignment = McqAssignment.query.get(assignment_id)
        if not assignment:
            return jsonify({"error": "Assignment not found"}), 404

        # Remove previous submissions
        McqScores.query.filter_by(user_id=user_id, assignment_id=assignment_id).delete()

        score = 0
        for question in assignment.questions:
            correct_option = question.correct_option
            if str(answers.get(str(question.id))) == str(correct_option):
                score += 1

        mcq_score = McqScores(user_id=user_id, assignment_id=assignment_id, score=score)
        db.session.add(mcq_score)
        db.session.commit()

        return jsonify({"message": "MCQ submitted successfully", "score": score}), 200



class ProgrammingSubmitAPI(MethodView):
    @jwt_required()
    def get(self, assignment_id=None):
        """
        Get user's Programming submissions/scores
        If assignment_id is provided, return scores for that specific assignment
        Otherwise, return all Programming scores for the user
        """
        user_id = get_jwt_identity()
        
        if assignment_id:
            scores = ProgrammingScores.query.filter_by(user_id=user_id, assignment_id=assignment_id).all()
            if not scores:
                return jsonify({"message": "No submissions found for this assignment"}), 404
        else:
            scores = ProgrammingScores.query.filter_by(user_id=user_id).all()
            if not scores:
                return jsonify({"message": "No programming submissions found"}), 404
        
        result = []
        for score in scores:
            assignment = ProgrammingAssignment.query.get(score.assignment_id)
            result.append({
                "score_id": score.id,
                "assignment_id": score.assignment_id,
                "assignment_title": assignment.title if assignment else "Unknown",
                "score": score.score
            })
        
        return jsonify(result), 200
    @jwt_required()
    def post(self):
        """User submits Programming assignment."""
        data = request.json
        user_id = get_jwt_identity()
        assignment_id = data['assignment_id']
        code = data['code']
        print("Submitted code:", code)

        assignment = ProgrammingAssignment.query.get(assignment_id)
        if not assignment:
            return jsonify({"error": "Assignment not found"}), 404

        # Remove previous submissions
        ProgrammingScores.query.filter_by(user_id=user_id, assignment_id=assignment_id).delete()

        score = 0
        test_cases = assignment.test_cases

        try:
            for test_case in test_cases:
                result = subprocess.run(
                    ['python', '-c', code],
                    input=test_case.input + '\n',
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                output = result.stdout.strip()
                print(f"Input: {test_case.input} | Expected: {test_case.expected_output} | Got: {output}")

                if output == test_case.expected_output.strip():
                    score += 1

        except subprocess.TimeoutExpired:
            return jsonify({"error": "Code execution timed out"}), 400
        except subprocess.CalledProcessError as e:
            return jsonify({"error": "Code execution failed", "details": e.stderr}), 400

        programming_score = ProgrammingScores(user_id=user_id, assignment_id=assignment_id, score=score)
        db.session.add(programming_score)
        db.session.commit()

        return jsonify({"message": "Programming assignment submitted successfully", "score": score}), 200






# ---------------- Register Routes ---------------- #

# Admin routes
assignment_bp.add_url_rule('/mcq', view_func=McqAssignmentAPI.as_view('create_mcq'), methods=['POST'])
assignment_bp.add_url_rule('/mcq/<int:assignment_id>', view_func=McqAssignmentAPI.as_view('update_mcq'), methods=['PUT'])
assignment_bp.add_url_rule('/mcq/<int:assignment_id>', view_func=McqAssignmentAPI.as_view('delete_mcq'), methods=['DELETE'])

assignment_bp.add_url_rule('/programming', view_func=ProgrammingAssignmentAPI.as_view('create_programming'), methods=['POST'])
assignment_bp.add_url_rule('/programming/<int:assignment_id>', view_func=ProgrammingAssignmentAPI.as_view('update_programming'), methods=['PUT'])
assignment_bp.add_url_rule('/programming/<int:assignment_id>', view_func=ProgrammingAssignmentAPI.as_view('delete_programming'), methods=['DELETE'])

# User routes
assignment_bp.add_url_rule('/submit/mcq', view_func=McqSubmitAPI.as_view('submit_mcq'), methods=['POST'])
assignment_bp.add_url_rule('/submit/programming', view_func=ProgrammingSubmitAPI.as_view('submit_programming'), methods=['POST'])

# GET routes for assignments
assignment_bp.add_url_rule('/mcq', view_func=McqAssignmentAPI.as_view('get_all_mcq'), methods=['GET'])
assignment_bp.add_url_rule('/mcq/<int:assignment_id>', view_func=McqAssignmentAPI.as_view('get_mcq'), methods=['GET'])
assignment_bp.add_url_rule('/programming', view_func=ProgrammingAssignmentAPI.as_view('get_all_programming'), methods=['GET'])
assignment_bp.add_url_rule('/programming/<int:assignment_id>', view_func=ProgrammingAssignmentAPI.as_view('get_programming'), methods=['GET'])

# GET routes for user submissions
assignment_bp.add_url_rule('/submit/mcq', view_func=McqSubmitAPI.as_view('get_all_mcq_scores'), methods=['GET'])
assignment_bp.add_url_rule('/submit/mcq/<int:assignment_id>', view_func=McqSubmitAPI.as_view('get_mcq_scores'), methods=['GET'])
assignment_bp.add_url_rule('/submit/programming', view_func=ProgrammingSubmitAPI.as_view('get_all_programming_scores'), methods=['GET'])
assignment_bp.add_url_rule('/submit/programming/<int:assignment_id>', view_func=ProgrammingSubmitAPI.as_view('get_programming_scores'), methods=['GET'])