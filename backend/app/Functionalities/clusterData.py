from pymongo import MongoClient
from .sentenceMatch import sentence_match
import numpy as np

class Cluster:
    def __init__(self):
        self.client = MongoClient('mongodb://Sahil_Purohit:#Pass4mongodb@ac-hifbqdl-shard-00-00.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-01.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-02.11jbtg4.mongodb.net:27017/?ssl=true&replicaSet=atlas-bzogsd-shard-0&authSource=admin&retryWrites=true&w=majority')
        self.db = self.client['fyp']
        self.collection = self.db['cluster']

    def get_cluster(self, cluster_id):
        return self.collection.find_one({'_id':cluster_id})
    
    def create_new_cluster(self, que_id):
        que_list = [que_id]
        return self.collection.insert_one({'median': que_id, 'que_list':que_list})

    def add_que_to_cluster(self, que_id, cluster_id):
        cluster = self.get_cluster(cluster_id)
        cluster['que_list'].append(que_id)
        return self.collection.update_one({'_id':cluster_id}, {'$set': {'que_list': cluster['que_list']}})
    
    # check whether question is part of any cluster or not
    def check_que_in_cluster(self, que_id):
        cluster = self.collection.find()
        for c in cluster:
            if que_id in c['que_list']:
                return True
        return False
    
    def get_cluster_id(self, que_id):
        cluster = self.collection.find()
        cluster_list = []
        for c in cluster:
            if que_id in c['que_list']:
                cluster_list.append(c['_id'])
        return cluster_list
    
    def getMedian(self, cluster_id):
        cluster = self.collection.find_one({'_id': cluster_id})
        return cluster['median']
        
    def get_cluster_list(self):
        return self.collection.find()


class ClusterData:
    def __init__(self):
        self.client = MongoClient('mongodb://Sahil_Purohit:#Pass4mongodb@ac-hifbqdl-shard-00-00.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-01.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-02.11jbtg4.mongodb.net:27017/?ssl=true&replicaSet=atlas-bzogsd-shard-0&authSource=admin&retryWrites=true&w=majority')
        self.db = self.client['fyp']
        self.ClusterCollection = self.db['cluster']
        self.QuestionCollection = self.db['questionBank'] 
        self.threshold = 0.6

    def createCluster(self):
        questions = self.QuestionCollection.find()
        cluster = Cluster()
        Flag = False
        for question in questions:
            if cluster.check_que_in_cluster(question['_id']):
                continue
            clusters_db = self.ClusterCollection.find()
            if self.ClusterCollection.count_documents({}) == 0:
                cluster.create_new_cluster(question['_id'])
            else:
                flag = True
                for cluster_db in clusters_db:
                    medianQ = self.QuestionCollection.find_one({'_id': cluster_db['median']})
                    if sentence_match(question['question'], medianQ['question']) > self.threshold:
                        cluster.add_que_to_cluster(question['_id'], cluster_db['_id'])
                        flag = False
                if flag:
                    cluster.create_new_cluster(question['_id'])
