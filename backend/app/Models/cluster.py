from pymongo import MongoClient
from flask import current_app

class Cluster:
    def __init__(self):
        self.client = MongoClient(current_app.config['MONGO_URI'])
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