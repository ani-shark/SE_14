from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from ai_agent import db
from ai_agent.models import User, RoleEnum, Course, UserCourse, Week, Lectures, McqAssignment, McqQuestion, McqOption, ProgrammingAssignment, ProgrammingTestCase
import random
import csv
import os

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user = User.query.get(get_jwt_identity())

                if not current_user.role == permission:
                    raise Exception("insufficient permissions.")
                else:
                    return f(*args, **kwargs)
            except Exception as e:
                return jsonify(error=str(e)), 401

        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(RoleEnum.ADMIN)(f)


def add_users():
    user_list = [
        {"email": "student1@example.com",
         "name": "Student One", "role": RoleEnum.STUDENT},
        {"email": "student2@example.com",
         "name": "Student Two", "role": RoleEnum.STUDENT},
        {"email": "student3@example.com",
         "name": "Student Three", "role": RoleEnum.STUDENT},
        {"email": "admin@example.com",
         "name": "Admin User", "role": RoleEnum.ADMIN},
    ]
    course_list = Course.query.all()
   
    for user_data in user_list:
        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()
        register_courses = random.sample(course_list, random.randint(1, 4))

        new_enrolled_course = []
        for item in register_courses:
            new_enrolled_course.append(UserCourse(
                user_id=new_user.id, course_id=item.id))

        db.session.add_all(new_enrolled_course)
        db.session.commit()


def add_courses():
    courses = {}
    weeks = {}

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'lecture_list.csv')
    with open(csv_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            course_name = row['course']
            week_name = row['week']
            lecture_name = row['lecture']

            # Add course if it doesn't exist
            if course_name not in courses:
                new_course = Course(name=course_name, intro=f"Introduction to {course_name}")
                db.session.add(new_course)
                db.session.commit()
                courses[course_name] = new_course

            course = courses[course_name]

            # Add week if it doesn't exist for this course
            if (course.id, week_name) not in weeks:
                new_week = Week(name=week_name, course_id=course.id)
                db.session.add(new_week)
                db.session.commit()
                weeks[(course.id, week_name)] = new_week

            week = weeks[(course.id, week_name)]

            # Add lecture
            new_lecture = Lectures(name=lecture_name, week_id=week.id, link='https://youtu.be/81BaOIrfvJA')
            db.session.add(new_lecture)

    db.session.commit()

def add_mcq():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'English_II_Week_6_Graded_Assignment.csv')
    with open(csv_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        new_mcq = McqAssignment(
            title="English II Week 6 Graded Assignment",
            description="Test your knowledge on English language concepts.",
            week_id=27  # week_id=27 is for English II Week 6
        )
        db.session.add(new_mcq)
        db.session.commit()

        for row in csv_reader:
            new_question = McqQuestion(
                text=row['question'],
                correct_option=row['correct_answer'],
                assignment_id=new_mcq.id
            )
            db.session.add(new_question)
            db.session.commit()

            options = [row['option1'], row['option2'], row['option3'], row['option4']]
            for option_text in options:
                if option_text:
                    new_option = McqOption(
                        text=option_text,
                        question_id=new_question.id
                    )
                    db.session.add(new_option)

        db.session.commit()

    print("MCQ assignment from CSV added successfully.")

def add_programming():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'PDSA_Week_7_Graded_Programming_Assignment.csv')
    with open(csv_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            new_programming = ProgrammingAssignment(
                title="PDSA Week 7 Graded Programming Assignment",
                description=row['question'],
                week_id=11  # week_id=11 is for PDSA Week 7
            )
            db.session.add(new_programming)
            db.session.commit()

            new_test_case = ProgrammingTestCase(
                input=row['sample_input'],
                expected_output=row['sample_output'],
                assignment_id=new_programming.id
            )
            db.session.add(new_test_case)
            db.session.commit()

    print("Programming assignments from CSV added successfully.")