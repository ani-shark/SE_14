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
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.STUDENT)

    # Many-to-Many with Course
    courses = db.relationship('Course', secondary = "user_course", 
                              backref=db.backref('users', lazy='dynamic'))

    # One-to-Many with Scores
    mcq_scores = db.relationship('McqScores', backref='user', cascade='all, delete-orphan')
    programming_scores = db.relationship('ProgrammingScores', backref='user', cascade='all, delete-orphan')

    def __init__(self, email, name, role=RoleEnum.STUDENT):
        self.email = email
        self.name = name
        self.role = role
        
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role.value,
            "courses": [(course.id, course.name) for course in self.courses]
        }


class Course(db.Model):
    __tablename__ = 'course'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)

    # One-to-Many with Week
    weeks = db.relationship('Week', backref='course', cascade="all, delete-orphan")

    def __init__(self, name, intro):
        self.name = name
        self.intro = intro
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "intro": self.intro,
            "weeks": [week.to_dict() for week in self.weeks]
        }


class Week(db.Model):
    __tablename__ = 'week'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    # One-to-Many with Assignments and Lectures
    mcq = db.relationship('McqAssignment', backref='week', cascade="all, delete-orphan")
    programming = db.relationship('ProgrammingAssignment', backref='week', cascade="all, delete-orphan")
    lectures = db.relationship('Lectures', backref='week', cascade="all, delete-orphan")

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


class McqAssignment(db.Model):
    __tablename__ = 'mcq_assignment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey('week.id'), nullable=False)

    def __init__(self, name, week_id):
        self.name = name
        self.week_id = week_id
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class ProgrammingAssignment(db.Model):
    __tablename__ = 'programming_assignment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey('week.id'), nullable=False)

    def __init__(self, name, week_id):
        self.name = name
        self.week_id = week_id
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
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
            "link":self.link
        }


class UserCourse(db.Model):
    __tablename__ = 'user_course'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    status = db.Column(db.Integer,nullable = False)
    
    def __init__(self,user_id,course_id, status='pending'):
        self.user_id = user_id
        self.course_id = course_id
        self.status = status

class McqScores(db.Model):
    __tablename__ = 'mcq_scores'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    mcq_id = db.Column(db.Integer, db.ForeignKey('mcq_assignment.id'), primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, mcq_id, score):
        self.user_id = user_id
        self.mcq_id = mcq_id
        self.score = score
    
    def to_dict(self):
        return {
            "id": self.mcq_id,
            "name": self.mcq.name,
            "score": self.score
        }


class ProgrammingScores(db.Model):
    __tablename__ = 'programming_scores'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    programming_id = db.Column(db.Integer, db.ForeignKey('programming_assignment.id'), primary_key=True)
    score = db.Column(db.Integer, nullable=False)


    def __init__(self, user_id, programming_id, score):
        self.user_id = user_id
        self.programming_id = programming_id
        self.score = score
    
    def to_dict(self):
        return {
            "id": self.programming_id,
            "name": self.programming.name,
            "score": self.score
        }



 


        
 

    