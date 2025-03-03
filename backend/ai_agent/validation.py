from ai_agent.models import RoleEnum,Course,User, Week
import re


def validate_length(string,min=1,max=None):    
    if min<=len(string)<=max:
        return True

    return False


def validate_email(email):
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    if not re.match(email_pattern, email):
        return False

    return True


def validate_user(user, is_update=False):
    assert user['email'] and isinstance(user['email'], str) and validate_length(user['email'], max=100) and \
        validate_email(user['email']), "invalid or missing email"
    
    if not is_update:
        assert not User.query.filter_by(email=user['email']).first(), "email already exists"
    
    assert user['name'] and isinstance(user['name'], str) and \
        validate_length(user['name'], max=100), "invalid or missing name"
    
    assert user['role'] and isinstance(user['role'], str) and \
        (user['role'] == RoleEnum.ADMIN.value or user['role'] == RoleEnum.STUDENT.value), \
    "invalid role"


def validate_course(course):
    assert course['name'] and isinstance(course['name'], str) and validate_length(course['name'], max=100), \
        "invalid or missing course name"
    
    assert course['intro'] and isinstance(course['intro'], str) and validate_length(course['intro'], max=300), \
        "invalid or missing course intro"

    
def validate_week(week):
    assert week['name'] and isinstance(week['name'], str) and validate_length(week['name'], max=100), \
        "invalid or missing week name"
    
    assert week['course_id'] and isinstance(week['course_id'], int) and\
    Course.query.get(week['course_id']), "invalid or missing course ID"


def validate_lecture(lecture):
    assert lecture['name'] and isinstance(lecture['name'], str) and validate_length(lecture['name'], max=100), \
        "invalid or missing lecture name"
    
    assert lecture['week_id'] and isinstance(lecture['week_id'], int) and \
        Week.query.get(lecture['week_id']), "invalid or missing week ID"
        
    assert lecture['link'] and isinstance(lecture['link'], str), "invalid or missing link"

def validate_mcq_assignment(mcq):
    assert mcq['name'] and isinstance(mcq['name'], str) and validate_length(mcq['name'], max=100), \
        "invalid or missing MCQ assignment name"
    
    assert mcq['week_id'] and isinstance(mcq['week_id'], int) and \
        Week.query.get(mcq['week_id']), "invalid or missing week ID"


def validate_programming_assignment(programming):
    assert programming['name'] and isinstance(programming['name'], str) and\
        validate_length(programming['name'], max=100), \
        "invalid or missing programming assignment name"
    
    assert programming['week_id']  and isinstance(programming['week_id'], int) \
        and Week.query.get(programming['week_id']) , "invalid or missing week ID"

