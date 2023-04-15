from pymongo import MongoClient
# from flask import current_app
from .sentenceMatch import sentence_encoding as vectorise
# from flask import make_response, jsonify, Blueprint

# db = Blueprint('db', __name__)

# @db.route('/vectorise-db', methods=['GET'])
def vectorise_db():
    client = MongoClient('mongodb://Sahil_Purohit:#Pass4mongodb@ac-hifbqdl-shard-00-00.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-01.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-02.11jbtg4.mongodb.net:27017/?ssl=true&replicaSet=atlas-bzogsd-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client['fyp']
    collection = db['questionBank']
    questions = collection.find()
    for question in questions:
        print(question['question'])
        question['vector'] = vectorise(question['question']).tolist()
        collection.update_one({'_id':question['_id']}, {'$set':question})
        print(question['vector'])
    # return make_response(jsonify({'message': 'Vectorised successfully'}), 200)


