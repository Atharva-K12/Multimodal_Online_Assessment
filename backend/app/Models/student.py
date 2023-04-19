from pymongo import MongoClient
from flask import current_app
from flask import make_response, jsonify
import os

class Student:
    def __init__(self):
        self.client = MongoClient(current_app.config['MONGO_URI'])
        self.db = self.client['fyp']
        self.collection = self.db['students']
    
    def get_all_students(self):
        return self.collection.find()
    
    def get_student_id(self, username):
        return self.collection.find_one({'username':username})['_id']
    
    def get_student(self, student_id):
        return self.collection.find_one({'_id':student_id})
    
    def get_student(self, username):
        return self.collection.find_one({'username':username})
    
    def add_student(self, data):
        if self.collection.find_one({'username':data['username']}):
            return make_response(jsonify({'message': 'Username already exists'}, 401))
        self.collection.insert_one(data)
        os.mkdir(os.path.join(current_app.config['AUDIO_FILES'], data['username']))
        return make_response(jsonify({'message': 'Student registered successfully'}), 200)
