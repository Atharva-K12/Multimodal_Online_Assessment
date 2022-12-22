from functools import wraps
from flask import request, jsonify
import jwt
from app import app, db

def token_validation(func):
    @wraps(func)
    def validate(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = db.users.find_one({'public_id':data['public_id']})
            if not current_user:
                return jsonify({'message':'Token is invalid'}), 401
        except:
            return jsonify({'message':'Token is invalid'}), 401
        return func(current_user, *args, **kwargs)
    
    return validate