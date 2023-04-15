from pymongo import MongoClient
from flask import current_app

class QuestionBank:
    def __init__(self):
        self.client = MongoClient(current_app.config['MONGO_URI'])
        self.db = self.client['fyp']
        self.collection = self.db['questionBank']

    def get_all_questions(self):
        return self.collection.find()
    
    def get_question_with_id(self, que_id):
        return self.collection.find({'_id':que_id})

    def get_question(self, question):
        return self.collection.find({'question':question})