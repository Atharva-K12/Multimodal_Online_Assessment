from flask import current_app
from functools import wraps
import jwt
from flask import request, jsonify
from Models.student import Student

# Token validation wrapper function
def token_validation(func):
    @wraps(func)
    def validate(*args, **kwargs):
        print("Inside token validation")
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message':'Token is missing'}), 401

        try:
            print("Inside try block")
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = Student().get_student(data['username'])
            if not current_user:
                return jsonify({'message':'Token is invalid'}), 401
        except:
            return jsonify({'message':'Token is invalid'}), 401
        print("user is valid")
        return func(*args, **kwargs)
    
    return validate
