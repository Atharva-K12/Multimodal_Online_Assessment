from flask import Blueprint, request, make_response, jsonify
from ..Models.test import Test
from ..Models.enrollment import Enrollment
from ..Functionalities.clusterData import ClusterData
from ..Functionalities.recommendationSystem import Recommendation
from ..Models.student import Student
from ..Models.test import Test
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
    
    
@student.route('/recommend', methods=['POST'])
def recommend():
    if request.method == 'POST':
        # Header parameters
        data = request.get_json()
        student_id = Student().get_student_id(data['studentName'])
        test_id = Test().get_test_id(data['testName'])
        if 'question' in data:
            question = data['question']
        else:
            question = None
        
        return make_response(Recommendation().recommend(student_id, test_id, question),200)