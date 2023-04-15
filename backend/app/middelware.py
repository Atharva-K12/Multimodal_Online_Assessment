from flask import current_app
from functools import wraps
import jwt
from flask import request, jsonify
from .Models.student import Student
from .Models.teacher import Teacher
from .Models.admin import Admin

# Token validation wrapper function
def token_validation(func):
    @wraps(func)
    def validate(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message':'Token is missing'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            role = data['role']
            if role == 'student':
                current_user = Student().get_student(data['username'])
            elif role == 'teacher':
                current_user = Teacher().get_teacher(data['username'])
            elif role == 'admin':
                current_user = Admin().get_teacher(data['username'])
            else:
                return jsonify({'message':'Token is invalid'}), 401
            if not current_user:
                return jsonify({'message':'Token is invalid'}), 401
        except:
            return jsonify({'message':'Token is invalid'}), 401
        return func(data['username'],*args, **kwargs)
    
    return validate
