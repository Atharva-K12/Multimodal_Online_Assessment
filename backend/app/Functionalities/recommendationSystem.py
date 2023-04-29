from ..Functionalities.sentenceMatch import sentence_match
from ..Models.cluster import Cluster
from ..Models.askedQue import AskedQue
import random
import numpy as np
from pymongo import MongoClient
from flask import current_app

class Recommendation:
    def __init__(self):
        self.cluster = Cluster()
        self.askedQue = AskedQue()
        self.client = MongoClient(current_app.config['MONGO_URI'])
        self.db = self.client['fyp']
        self.QuestionCollection = self.db['questionBank']

    def recommend(self, student_id, test_id, question = None, answer = None):
        if question == None and answer == None:	    
            cluster_ids = self.cluster.get_cluster_list()
            randCluster = random.choice(list(cluster_ids))
            randClusterData = self.cluster.get_cluster(randCluster['_id'])
            randQue = random.choice(randClusterData['que_list'])
            self.askedQue.addQue(student_id, test_id, randQue, False)
            return {'question': self.QuestionCollection.find_one({'_id': randQue})['question']}
        else:
            Question = self.QuestionCollection.find_one({'question': question})
            asked_que_ids = self.askedQue.getQueIds(student_id, test_id)
            cluster_ids = self.cluster.get_cluster_id(Question['_id'])
            distances = []
            i=0
            for cluster_id in cluster_ids:
                median = self.cluster.getMedian(cluster_id)
                distance = sentence_match(answer, self.QuestionCollection.find_one({'_id': median})['question'])
                distances.append({'distance':distance, 'index': cluster_id})
                i+=1
            distances.sort(key=lambda x: x['distance'])
            for i in range(len(distances)):
                cluster_id = distances[i]['index']
                cluster = self.cluster.get_cluster(cluster_id)
                que_list = cluster['que_list']
                for que in que_list:
                    if que in asked_que_ids:
                        que_list.remove(que)
                if len(que_list) > 0:
                    randQue = random.choice(que_list)
                    self.askedQue.addQue(student_id, test_id, randQue, True)
                    return {'question' : self.QuestionCollection.find_one({'_id': que})['question']}
        all_cluster_ids = list(self.cluster.get_cluster_list())
        for cluster_id in cluster_ids:
            if cluster_id in all_cluster_ids:
                all_cluster_ids.remove(cluster_id)
        randCluster = random.choice(all_cluster_ids)
        randClusterData = self.cluster.get_cluster(randCluster['_id'])
        randQue = random.choice(randClusterData['que_list'])
        self.askedQue.addQue(student_id, test_id, randQue, True)
        return {'question' : self.QuestionCollection.find_one({'_id': randQue})['question']}
    

        


