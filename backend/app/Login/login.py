from flask import Blueprint, request,current_app, make_response, jsonify
import bcrypt,jwt
from Models.student import Student
from Models.teacher import Teacher
from Models.admin import Admin

login = Blueprint('login', __name__)


@login.route('/student-register', methods=['POST'])
def student_register():
    if request.method == 'POST':
        data = request.get_json()
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        return Student().add_student(data)
    


@login.route('/teacher-register', methods=['POST'])
def teacher_register():
    if request.method == 'POST':
        data = request.get_json()
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        return Teacher().add_teacher(data)



@login.route('/student-login', methods=['POST'])
def student_login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = Student().get_student(username)
        if user:
            # check password with hashed password
            if bcrypt.hashpw(password.encode('utf-8'), user['password']) == user['password']:
                token = jwt.encode({'username': username, 'role': 'student'}, current_app.config['SECRET_KEY'])
                return make_response(jsonify({'token':token, 'username':username, 'roll_no': user['roll_no']}), 200)
            else:
                return make_response(jsonify({'message': 'Invalid password'}), 401)
        else:
            return make_response(jsonify({'message': 'Invalid username'}), 401)


@login.route('/teacher-login', methods=['POST'])
def teacher_login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = Teacher().find_one({'username': username})
        if user:
            if bcrypt.hashpw(password.encode('utf-8'), user['password']) == user['password']:
                token = jwt.encode({'username': username, 'role': 'teacher'}, current_app.config['SECRET_KEY'])
                return make_response(jsonify({'token':token, 'username': username}), 200)
            else:
                return make_response(jsonify({'message': 'Invalid password'}), 401)
        else:
            return make_response(jsonify({'message': 'Invalid username'}), 401)


@login.route('/admin-login', methods=['POST'])
def admin_login():
    # Code to login teacher
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = Admin().find_one({'username': username})
        if user:
            if bcrypt.hashpw(password.encode('utf-8'), user['password']) == user['password']:
                token = jwt.encode({'username': username, 'role': 'admin'}, current_app.config['SECRET_KEY'])
                return make_response(jsonify({'token':token, 'username': username}), 200)
            else:
                return make_response(jsonify({'message': 'Invalid password'}), 401)
        else:
            return make_response(jsonify({'message': 'Invalid username'}), 401)