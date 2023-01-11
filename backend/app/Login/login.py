from flask import Blueprint, request,current_app, make_response, jsonify
import bcrypt,jwt

login = Blueprint('login', __name__)
db = current_app.config['db']

@login.route('/student-reister', methods=['POST'])
def student_register():
    # Code to register student
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.student.find_one({'username': username})
        if user:
            return make_response(jsonify({'message': 'Username already exists'}), 401)
        else:
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            db.student.insert_one({'username': username, 'password': password, 'email': request.form['email'], 'name': request.form['name']})
            return make_response(jsonify({'message': 'Student registered successfully'}), 200)


@login.route('/teacher-reister', methods=['POST'])
def teacher_register():
    # Code to register teacher
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.teacher.find_one({'username': username})
        if user:
            return make_response(jsonify({'message': 'Username already exists'}), 401)
        else:
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            db.student.insert_one({'username': username, 'password': password, 'email': request.form['email'], 'name': request.form['name'], 'status':'pending' })
            return make_response(jsonify({'message': 'Teacher registered successfully and status pending'}), 200)



@login.route('/student-login', methods=['POST'])
def student_login():
    # Code to login student
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.student.find_one({'username': username})
        if user:
            if bcrypt.hashpw(password.encode('utf-8'), user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                token = jwt.encode({'username': username, 'role': 'student'}, current_app.config['SECRET_KEY'])
                return make_response(jsonify({'token':token}), 200)
            else:
                return make_response(jsonify({'message': 'Invalid password'}), 401)
        else:
            return make_response(jsonify({'message': 'Invalid username'}), 401)


@login.route('/teacher-login', methods=['POST'])
def teacher_login():
    # Code to login teacher
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.teacher.find_one({'username': username})
        if user:
            if bcrypt.hashpw(password.encode('utf-8'), user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                token = jwt.encode({'username': username, 'role': 'teacher'}, current_app.config['SECRET_KEY'])
                return make_response(jsonify({'token':token}), 200)
            else:
                return make_response(jsonify({'message': 'Invalid password'}), 401)
        else:
            return make_response(jsonify({'message': 'Invalid username'}), 401)


@login.route('/admin-login', methods=['POST'])
def admin_login():
    # Code to login teacher
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.admin.find_one({'username': username})
        if user:
            if bcrypt.hashpw(password.encode('utf-8'), user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                token = jwt.encode({'username': username, 'role': 'admin'}, current_app.config['SECRET_KEY'])
                return make_response(jsonify({'token':token}), 200)
            else:
                return make_response(jsonify({'message': 'Invalid password'}), 401)
        else:
            return make_response(jsonify({'message': 'Invalid username'}), 401)