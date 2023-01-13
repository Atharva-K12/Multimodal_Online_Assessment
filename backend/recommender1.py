import random
from sentenceMatch import sentence_encoding
import numpy as np

class Question:
    def __init__(self, question_list):
        self.question_list = question_list
        self.asked_questions = []
        self.easy = [d for d in self.question_list if d['difficulty'] == 'easy']
        self.medium = [d for d in self.question_list if d['difficulty'] == 'medium']
        self.hard = [d for d in self.question_list if d['difficulty'] == 'hard']

    def first_question(self):
        q1 = random.choice(self.easy)
        return q1
    
    def choose_question(self, next_level):
        q = random.choice(next_level)
        while q in self.asked_questions:
            q = random.choice(next_level)
        next_ques = q        
        return next_ques 
    
    def next_question(self):
        next_ques = ""
        if len(self.asked_questions) == 0:
            return self.first_question()

        current_question = self.asked_questions[-1]['Question']["difficulty"]
        current_score = self.asked_questions[-1]['Score']
        
        if current_score >= 0.7:
            if current_question == 'easy':
                next_ques = self.choose_question(self.medium)
            else:
                next_ques = self.choose_question(self.hard)
        elif current_score >= 0.4 and current_score < 0.7:
            if current_question == 'easy':
                next_ques = self.choose_question(self.easy)
            elif current_question == 'medium':
                next_ques = self.choose_question(self.medium)
            else:
                next_ques = self.choose_question(self.hard)
        else:
            if current_question == 'easy' or current_question == 'medium':
                next_ques = self.choose_question(self.easy)
            else:
                next_ques = self.choose_question(self.medium)
                
        return next_ques


class Vectorize_Questions:
    def __init__(self, question_list):
        self.question_list = question_list
        self.vectorized_questions = []
        self.vectorize_questions()

    def vectorize_questions(self):
        for question in self.question_list:
            self.vectorized_questions.append({'question':question['question'], 'vector':self.vectorize(question['question'])})

    def vectorize(self, question):
        return sentence_encoding(question)

# KNN Algorithm
class RecommenderKNN:
    def __init__(self, question_list):
        self.question_list = question_list
        self.vectorized_questions = Vectorize_Questions(self.question_list).vectorized_questions
        self.recommended_questions = []
        self.recommend()
        self.k = 5
        self.distance_metric = self.euclidean_distance
    
    def euclidean_distance(self, vector1, vector2):
        return np.linalg.norm(vector1 - vector2)
    
    def cosine_similarity(self, vector1, vector2):
        return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

    def recommend(self, question):
        nearest_neighbours = self.find_nearest_neighbours(question)
        for neighbour in nearest_neighbours:
            if np.random.random() > 0.5:
                self.recommended_questions.append(neighbour['question'])
                break
        return self.recommended_questions[-1]
    

    def find_nearest_neighbours(self, question):
        distances = []
        for vectorized_question in self.vectorized_questions:
            distance = self.distance_metric(vectorized_question['vector'], question['vector'])
            distances.append({'question':vectorized_question['question'], 'distance':distance})
        distances.sort(key=lambda x: x['distance'])
        return distances[:self.k]


class  RecommenderCluster:
    def __init__(self, question_list):
        self.question_list = question_list
        self.vectorized_questions = Vectorize_Questions(self.question_list).vectorized_questions
        self.recommended_questions = []
        self.recommend()
        self.k = 5
        self.distance_metric = self.euclidean_distance
        self.threshold = 0.5
    
    def euclidean_distance(self, vector1, vector2):
        return np.linalg.norm(vector1 - vector2)
    
    def cosine_similarity(self, vector1, vector2):
        return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

    def cluster(self):
        clusters = []
        for vectorized_question in self.vectorized_questions:
            if len(clusters) == 0:
                clusters.append([vectorized_question])
            else:
                for cluster in clusters:
                    if self.distance_metric(cluster[0]['vector'], vectorized_question['vector']) < self.threshold:
                        cluster.append(vectorized_question)
                        break
                else:
                    clusters.append([vectorized_question])
        return clusters
    
    def recommend(self, question):
        clusters = self.cluster()
        cluster_medians = []
        for cluster in clusters:
            cluster_medians.append(self.find_median(cluster))
        distances = []
        for cluster_median in cluster_medians:
            distance = self.distance_metric(cluster_median['vector'], question['vector'])
            distances.append({'question':cluster_median['question'], 'distance':distance})
        distances.sort(key=lambda x: x['distance'])
        self.recommended_questions.append(distances[0]['question'])
        return self.recommended_questions[-1]
    
    def find_median(self, cluster):
        distances = []
        for vectorized_question in cluster:
            distance = self.distance_metric(cluster[0]['vector'], vectorized_question['vector'])
            distances.append({'question':vectorized_question['question'], 'distance':distance})
        distances.sort(key=lambda x: x['distance'])
        return distances[len(distances)//2]


class Recommender:

    def __init__(self, question_list, threshold=0.5):
        self.question_list = question_list
        self.vectorized_questions = Vectorize_Questions(self.question_list).vectorized_questions
        self.distance_metric = self.euclidean_distance
        self.threshold = threshold

    def vectorize(self, question):
        return sentence_encoding(question)
    
    def clusterize(self):
        # assign same id to questions with distance less than threshold
        clusters = []
        for question in self.vectorized_questions:
            if len(clusters) == 0:
                clusters.append([question])
            else:
                for cluster in clusters:
                    if self.distance_metric(cluster[0]['vector'], question['vector']) < self.threshold:
                        cluster.append(question)
                        break
                else:
                    clusters.append([question])
        self.clusters = clusters
    
    def distance_metric(self, vector1, vector2):
        return np.linalg.norm(vector1 - vector2)

class QuestionHandler:
    def __init__(self,questionsDB=None):
        if questionsDB is None:
            self.questions = []
        else:
            self.questions = questionsDB
        

    def add_question(self, question):
        self.questions.append(Vectorize_Questions([question]))
    
    
    

        
