from pymongo import MongoClient
from flask import current_app
from flask import make_response, jsonify

class Test:
    def __init__(self):
        self.client = MongoClient(current_app.config['MONGO_URI'])
        self.db = self.client['fyp']
        self.collection = self.db['tests']
    
    def create_test(self, data):
        if self.collection.find_one({'Name':data['Name']}):
            return make_response(jsonify({'message': 'Test already exists'}), 401)
        self.collection.insert_one(data)
        return make_response(jsonify({'message': 'Test created successfully'}), 200)
    
    def get_test(self, test_id):
        print(test_id)
        return self.collection.find_one({'_id':test_id})['Name']
    
    def get_test_id(self, test_name):
        return self.collection.find_one({'Name':test_name})['_id']
    
    def get_tests(self):
        tests = self.collection.find()
        test_list = []
        for test in tests:
            test_list.append(test['Name'])
        return test_list
    