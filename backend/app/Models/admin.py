from pymongo import MongoClient
from flask import current_app
from flask import make_response, jsonify

class Admin:
    def __init__(self):
        self.client = MongoClient(current_app.config['MONGO_URI'])
        self.db = self.client['fyp']
        self.collection = self.db['admin']
    
    def get_admin(self, username):
        return self.collection.find_one({'username':username})
    