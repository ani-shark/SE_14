from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from ai_agent import db
from ai_agent.models import User, RoleEnum, Course, UserCourse, Week, Lectures, McqAssignment, McqQuestion, McqOption, ProgrammingAssignment, ProgrammingTestCase
import random

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
    course_list = [
        {"name": "Programming, Data Structures and Algorithms using Python",
         "intro": "This course provides a deep dive into programming fundamentals, data structures, and algorithms using Python. Students will learn how to write efficient code, optimize performance, and solve complex computational problems."},
        {"name": "Tools in Data Science", "intro": "A comprehensive guide to essential tools in data science, including data wrangling, visualization, and machine learning frameworks. Learn how to leverage Python libraries like Pandas, NumPy, and TensorFlow."},
        {"name": "Programming in Python", "intro": "An introduction to Python programming covering syntax, control flow, functions, and object-oriented programming. This course is designed for beginners looking to build a strong foundation in Python."},
        {"name": "Statistics 2", "intro": "An advanced statistics course covering hypothesis testing, regression analysis, probability distributions, and inferential statistics. Ideal for students who want to deepen their understanding of statistical methods."}
    ]
    
    new_courses = []

    for course_data in course_list:
        new_course = Course(**course_data)
        db.session.add(new_course)
        new_courses.append(new_course)

    db.session.commit()

    for course in new_courses:
        
        for i in range(12):
            new_week = Week(name=f'Week {i+1}', course_id=course.id)
            db.session.add(new_week)
            db.session.commit()
        
            num_lectures = random.randint(1, 3)
            for i in range(num_lectures):
                new_lecture = Lectures(name=f"Lecture {i+1}",week_id=new_week.id,link='https://youtu.be/81BaOIrfvJA')
                db.session.add(new_lecture)
                db.session.commit()
            
    db.session.commit()

def add_mcq():
    mcq_list = [
        {
            "title": "Python Basics Quiz",
            "description": "Test your knowledge on basic Python concepts like variables, loops, and functions.",
            "week_id": 1,
            "questions": [
                {
                    "text": "What is the output of print(2 ** 3)?",
                    "correct_option": "8",
                    "options": ["5", "6", "8", "10"]
                },
                {
                    "text": "Which of these is a valid Python variable name?",
                    "correct_option": "variable_name",
                    "options": ["2_variable", "variable_name", "var-name", "variable name"]
                }
            ]
        }
    ]

    for mcq_data in mcq_list:
        new_mcq = McqAssignment(
            title=mcq_data["title"],
            description=mcq_data["description"],
            week_id=mcq_data["week_id"]
        )
        db.session.add(new_mcq)
        db.session.commit()

        for question_data in mcq_data["questions"]:
            new_question = McqQuestion(
                text=question_data["text"],
                correct_option=question_data["correct_option"],
                assignment_id=new_mcq.id
            )
            db.session.add(new_question)
            db.session.commit()

            for option_text in question_data["options"]:
                new_option = McqOption(
                    text=option_text,
                    question_id=new_question.id
                )
                db.session.add(new_option)

        db.session.commit()

    print("Sample MCQ assignments added successfully.")

def add_programming():
    programming_list = [
        {
            "title": "FizzBuzz Challenge",
            "description": "Write a program that prints numbers from 1 to 100, but for multiples of 3, print 'Fizz', for multiples of 5, print 'Buzz', and for multiples of both, print 'FizzBuzz'.",
            "week_id": 1,
            "test_cases": [
                {"input": "3", "expected_output": "Fizz"},
                {"input": "5", "expected_output": "Buzz"},
                {"input": "15", "expected_output": "FizzBuzz"},
                {"input": "7", "expected_output": "7"}
            ]
        }
    ]

    for prog_data in programming_list:
        new_programming = ProgrammingAssignment(
            title=prog_data["title"],
            description=prog_data["description"],
            week_id=prog_data["week_id"]
        )
        db.session.add(new_programming)
        db.session.commit()

        for test_case_data in prog_data["test_cases"]:
            new_test_case = ProgrammingTestCase(
                input=test_case_data["input"],
                expected_output=test_case_data["expected_output"],
                assignment_id=new_programming.id
            )
            db.session.add(new_test_case)

        db.session.commit()

    print("Sample programming assignments added successfully.")