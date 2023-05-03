from pymongo import MongoClient
from flask import current_app

class AskedQue:
    def __init__(self):
        self.client = MongoClient(current_app.config['MONGO_URI'])
        self.db = self.client['fyp']
        self.collection = self.db['askedQue']

    def getQueIds(self, student_id, test_id):
        que_ids = []
        ques = self.collection.find({'student_id':student_id, 'test_id':test_id})
        for que in ques:
            que_ids.append(que['que_ids'])
        return que_ids

    def addQue(self, student_id, test_id, que_id, exist):
        if exist:
            data = self.getQueIds(student_id, test_id)
            data['que_ids'].append(que_id)
            self.collection.update_one({'_id':data['_id']}, {'$set': {'que_ids': data['que_ids']}})
        else:
            self.collection.insert_one({'student_id':student_id, 'test_id':test_id, 'que_ids':[que_id]})