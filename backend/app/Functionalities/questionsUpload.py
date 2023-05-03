# TODO : UPDATE this for devnew branch
from pymongo import MongoClient
import pandas as pd


def questionUpload(filepath):
    client = MongoClient('mongodb://Sahil_Purohit:#Pass4mongodb@ac-hifbqdl-shard-00-00.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-01.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-02.11jbtg4.mongodb.net:27017/?ssl=true&replicaSet=atlas-bzogsd-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client['fyp']
    collection = db['questionBank']
    # upload questions from Question Bank.csv using pandas
    df = pd.read_csv(filepath)
    for index, row in df.iterrows():
        questions = row['question']
        answers = row['Answer']
        collection.insert_one({'question': questions, 'answer': answers})
        