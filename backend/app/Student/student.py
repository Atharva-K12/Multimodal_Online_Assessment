from flask import Blueprint, request,current_app, make_response, jsonify
from ..Models.test import Test
from ..Models.enrollment import Enrollment
from ..middelware import token_validation

student = Blueprint('student', __name__)

@student.route('/get-student-enrollments', methods=['GET'])
@token_validation
def get_student_enrollments(username):
    if request.method == 'GET':
        return make_response(jsonify({'enrollments': Enrollment().get_enrollments(username)}), 200)
    

@student.route('/get-all-test', methods=['GET'])
@token_validation
def get_all_test(username):
    if request.method == 'GET':
        test = Test().get_tests()
        enrollment = Enrollment().get_enrollments(username)
        for i in enrollment:
            test.remove(i)
        return make_response(jsonify({'tests': test}), 200)
    

@student.route('/enroll', methods=['POST'])
@token_validation
def enroll(username):
    if request.method == 'POST':
        data = request.get_json()
        data['student_name'] = username
        return Enrollment().enroll(data)
    

@student.route('/create-test', methods=['POST'])
def create_test():
    if request.method == 'POST':
        data = request.get_json()
        return Test().create_test(data)