# TODO : UPDATE this for devnew branch
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import pandas as pd

def sentence_encoding(sentence):
    model = SentenceTransformer('stsb-roberta-large')
    #model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')    
    embedding = model.encode(sentence, convert_to_tensor=True)
    return embedding

def questionUpload():
    client = MongoClient('mongodb://Sahil_Purohit:#Pass4mongodb@ac-hifbqdl-shard-00-00.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-01.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-02.11jbtg4.mongodb.net:27017/?ssl=true&replicaSet=atlas-bzogsd-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client['fyp']
    collection = db['questionBank']
    # upload questions from Question Bank.csv using pandas
    df = pd.read_csv('Question Bank.csv')
    for index, row in df.iterrows():
        questions = row['question']
        answers = row['Answer']
        collection.insert_one({'question': questions, 'answer': answers, 'vector': sentence_encoding(questions).tolist()})
        
if __name__ == '__main__':
    questionUpload()