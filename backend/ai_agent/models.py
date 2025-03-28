from ai_agent import db
from enum import Enum


class RoleEnum(Enum):
    STUDENT = 'student'
    ADMIN = 'admin'


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False,
                     default=RoleEnum.STUDENT)

    # Many-to-Many with Course
    courses = db.relationship('Course', secondary="user_course",
                              backref=db.backref('users', lazy='dynamic'))

    # One-to-Many with Scores
    mcq_scores = db.relationship(
        'McqScores', backref='user', cascade='all, delete-orphan')
    programming_scores = db.relationship(
        'ProgrammingScores', backref='user', cascade='all, delete-orphan')

    def __init__(self, email, name, role=RoleEnum.STUDENT):
        self.email = email
        self.name = name
        self.role = role

    def to_dict(self):
        user_details = {
            'course_details': []
        }
        for course in self.courses:
            course_detail = {
                'id': course.id,
                'name': course.name,
                'mcq_scores': [],
                'programming_scores': []
            }
            for week in course.to_dict()['weeks']:
                for mcq in week['mcq']:
                    case = McqScores.query.filter_by(
                        user_id=self.id, assignment_id=mcq['id']).first()
                    if case:
                        course_detail['mcq_scores'].append(case.to_dict())

                for prog in week['programming']:
                    case = ProgrammingScores.query.filter_by(
                        user_id=self.id, assignment_id=prog['id']).first()
                    if case:
                        course_detail['programming_scores'].append(
                            case.to_dict())

            user_details['course_details'].append(course_detail)

        user_details['id'] = self.id
        user_details['email'] = self.email
        user_details['name'] = self.name
        user_details['role'] = self.role.value

        return user_details


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)

    # One-to-Many with Week
    weeks = db.relationship('Week', backref='course',
                            cascade="all, delete-orphan")

    def __init__(self, name, intro):
        self.name = name
        self.intro = intro

    def to_dict(self):
        
        week_0 = {'id': 0, 'course_intro': [{'content_type': 'intro', 'intro': self.intro}]}
        ans = {
            "id": self.id,
            "name": self.name,
            "weeks": [week_0] + [week.to_dict() for week in self.weeks]
            }
        
        return ans
class Week(db.Model):
    __tablename__ = 'week'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id'), nullable=False)

    # One-to-Many with Assignments and Lectures
    mcq = db.relationship('McqAssignment', backref='week',
                          cascade="all, delete-orphan")
    programming = db.relationship(
        'ProgrammingAssignment', backref='week', cascade="all, delete-orphan")
    lectures = db.relationship(
        'Lectures', backref='week', cascade="all, delete-orphan")

    def __init__(self, name, course_id):
        self.name = name
        self.course_id = course_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "mcq": [mcq.to_dict() for mcq in self.mcq],
            "programming": [prog.to_dict() for prog in self.programming],
            "lectures": [lec.to_dict() for lec in self.lectures]
        }


class Lectures(db.Model):
    __tablename__ = 'lectures'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey('week.id'), nullable=False)
    link = db.Column(db.String(150), nullable=False)

    def __init__(self, name, week_id, link):
        self.name = name
        self.week_id = week_id
        self.link = link

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "content_type": "lectures"
        }


class UserCourse(db.Model):
    __tablename__ = 'user_course'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'course.id'), primary_key=True)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, course_id, status='pending'):
        self.user_id = user_id
        self.course_id = course_id
        self.status = status

# MCQ Assignment model


class McqAssignment(db.Model):
    __tablename__ = 'mcq_assignment'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey('week.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # One-to-Many with Questions
    questions = db.relationship(
        'McqQuestion', backref='mcq_assignment', cascade="all, delete-orphan")

    def __init__(self, title, week_id, description):
        self.title = title
        self.week_id = week_id
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "questions": [question.to_dict() for question in self.questions],
            "description": self.description,
            "content_type": "mcq"
        }


# MCQ Question model
class McqQuestion(db.Model):
    __tablename__ = 'mcq_question'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    correct_option = db.Column(db.String(100), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey(
        'mcq_assignment.id'), nullable=False)

    # One-to-Many with Options
    options = db.relationship(
        'McqOption', backref='mcq_question', cascade="all, delete-orphan")

    def __init__(self, text, correct_option, assignment_id):
        self.text = text
        self.correct_option = correct_option
        self.assignment_id = assignment_id

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "correct_option": self.correct_option,
            "options": [option.text for option in self.options]
        }


# MCQ Options model
class McqOption(db.Model):
    __tablename__ = 'mcq_option'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'mcq_question.id'), nullable=False)

    def __init__(self, text, question_id):
        self.text = text
        self.question_id = question_id

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text
        }


class ProgrammingTestCase(db.Model):
    __tablename__ = 'programming_test_case'

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey(
        'programming_assignment.id', ondelete='CASCADE'), nullable=False)
    input = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text, nullable=False)

    def __init__(self, assignment_id, input, expected_output):
        self.assignment_id = assignment_id
        self.input = input
        self.expected_output = expected_output

    def to_dict(self):
        return {
            "id": self.id,
            "input": self.input,
            "expected_output": self.expected_output,
        }


class ProgrammingAssignment(db.Model):
    __tablename__ = 'programming_assignment'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey('week.id'), nullable=False)

    # One-to-Many relationship with test cases
    test_cases = db.relationship(
        'ProgrammingTestCase', backref='assignment', cascade='all, delete-orphan')

    def __init__(self, title, description, week_id):
        self.title = title
        self.description = description
        self.week_id = week_id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "test_cases": [test_case.to_dict() for test_case in self.test_cases],
            "content_type": "programming"
        }


# Scores models
class McqScores(db.Model):
    __tablename__ = 'mcq_scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey(
        'mcq_assignment.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        assignment = McqAssignment.query.get(self.assignment_id).first()
        week = Week.query.get(assignment.week_id).first()
        return {
            "id": self.id,
            "assignment_id": self.assignment_id,
            "assignment_title": assignment.title,
            "week_name": week.name,
            "score": self.score
        }


class ProgrammingScores(db.Model):
    __tablename__ = 'programming_scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey(
        'programming_assignment.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        assignment = ProgrammingAssignment.query.get(
            self.assignment_id).first()
        week = Week.query.get(assignment.week_id).first()
        return {
            "id": self.id,
            "assignment_id": self.assignment_id,
            "assignment_title": assignment.title,
            "week_name": week.name,
            "score": self.score
        }
