from pymongo import MongoClient
from flask import current_app
from flask import make_response, jsonify
from ..Models.test import Test
from ..Models.student import Student

class Enrollment:
    def __init__(self):
        self.client = MongoClient(current_app.config['MONGO_URI'])
        self.db = self.client['fyp']
        self.collection = self.db['enrollments']

    def get_enrollments(self,student_name):
        student_id = Student().get_student_id(student_name)
        tests = self.collection.find({'student_id':student_id})
        if tests is None:
            return make_response(jsonify({'message': 'Not enrolled in any test'}), 404)
        test_list = []
        for test in tests:
            test_list.append(Test().get_test(test['test_id']))
        return test_list

    def enroll(self, data):
        test_id = Test().get_test_id(data['test_name'])
        student_id = Student().get_student_id(data['student_name'])
        if self.collection.find_one({'student_id':student_id, 'test_id':test_id}):
            return make_response(jsonify({'message': 'Already enrolled in test'}), 401)
        data['test_id'] = test_id
        data['student_id'] = student_id
        data.pop('student_name')
        data.pop('test_name')
        self.collection.insert_one(data)
        return make_response(jsonify({'message': 'Enrolled in test successfully'}), 200)