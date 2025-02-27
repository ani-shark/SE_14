from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from ai_agent import db
from ai_agent.models import User, RoleEnum, Course, UserCourse, Week


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
                return jsonify(msg=str(e)), 401

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
    import random
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
    new_weeks = []

    for course_data in course_list:
        new_course = Course(**course_data)
        db.session.add(new_course)
        new_courses.append(new_course)

    db.session.commit()

    for course in new_courses:
        for i in range(12):
            new_week = Week(name=f'Week {i+1}', course_id=course.id)
            new_weeks.append(new_week)

    db.session.add_all(new_weeks)
    db.session.commit()
