from pymongo import MongoClient
from flask import current_app

class Score:
    def __init__(self):
        self.client = MongoClient(current_app.config['MONGO_URI'])
        self.db = self.client['fyp']
        self.collection = self.db['score']

    def get_score(self, student_id, test_id):
        return self.collection.find_one({'student_id':student_id, 'test_id':test_id})['total_score']
    
    def add_score(self, student_id, test_id, question_number,score):
        if question_number == 0:
            return self.collection.insert_one({'student_id':student_id, 'test_id':test_id, 'total_score':score, 'score_list':[score]})
        else:
            data = self.collection.find_one({'student_id':student_id, 'test_id':test_id})
            data['total_score'] += score
            data['score_list'].append(score)
            return self.collection.update_one({'_id':data['_id']}, {'$set': {'total_score': data['total_score'], 'score_list': data['score_list']}})