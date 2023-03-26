from pymongo import MongoClient
from flask import current_app
from flask import make_response, jsonify

class Teacher:
    def __init__(self):
        self.client = MongoClient(current_app.config['MONGO_URI'])
        self.db = self.client['fyp']
        self.collection = self.db['teachers']
    
    def get_teacher(self, student_id):
        return self.collection.find_one({'_id':student_id})
    
    def get_teacher(self, username):
        return self.collection.find_one({'username':username})
    
    def add_teacher(self, data):
        if self.collection.find_one({'username':data['username']}):
            return make_response(jsonify({'message': 'Username already exists'}, 401))
        data['approved'] = False
        self.collection.insert_one(data)
        return make_response(jsonify({'message': 'Student registered successfully'}), 200)
    
    def approve_teacher(self, username):
        self.collection.update_one({'username':username}, {'$set':{'approved':True}})
        return make_response(jsonify({'message': 'Teacher approved successfully'}), 200)
