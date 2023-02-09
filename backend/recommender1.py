import random
import pandas as pd
from sentenceMatch import sentence_encoding
import numpy as np
import spacy
import tracemalloc

nlp = spacy.load('en_core_web_sm')
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

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
        self.k = 5
        self.distance_metric = self.euclidean_distance
        self.recommend()
    
    def euclidean_distance(self, vector1, vector2):
        return np.linalg.norm(vector1 - vector2)
    
    def cosine_similarity(self, vector1, vector2):
        return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

    def recommend(self, question=None):
        if question is None:
            question = self.vectorized_questions[np.random.randint(0, len(self.vectorized_questions))]
            self.recommended_questions.append(question)
            # print(self.recommended_questions[-1])
            return 
        nearest_neighbours = self.find_nearest_neighbours(question)
        flag = True
        while(flag):
            for neighbour in nearest_neighbours:
                if np.random.random() > 0.5 and neighbour not in self.recommended_questions:
                    self.recommended_questions.append(neighbour)
                    flag = False
                    break
        return self.recommended_questions[-1]
    

    def find_nearest_neighbours(self, question):
        distances = []
        for vectorized_question in self.vectorized_questions:
            distance = self.distance_metric(vectorized_question['vector'], question['vector'])
            distances.append({'question':vectorized_question['question'],'vector':vectorized_question['vector'], 'distance':distance})
        distances.sort(key=lambda x: x['distance'])
        # threshold = 0.3
        # value = 0
        # for distance in distances:
        #     if distance['distance'] < threshold:
        #         value +=1
        # recall = self.k/value
        # f1 = 2*1*recall/(1+recall)
        # print("recall = " + str(f1) + "\t" + str(recall))
        # remove 'distaknce' key from the list
        for distance in distances:
            del distance['distance']
        return distances[10:self.k+10]


class  RecommenderCluster:
    def __init__(self, question_list):
        self.question_list = question_list
        self.vectorized_questions = Vectorize_Questions(self.question_list).vectorized_questions
        self.recommended_questions = []
        # self.recommend()
        self.k = 5
        self.distance_metric = self.cosine_similarity
        self.threshold = 1.0
        self.recommend()
    
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
    
    def recommend(self, question = None):
        if question is None:
            question = self.vectorized_questions[np.random.randint(0, len(self.vectorized_questions))]
            self.recommended_questions.append(question)
            return
        clusters = self.cluster()
        cluster_medians = []
        for cluster in clusters:
            cluster_medians.append(self.find_median(cluster))
        distances = []
        for i,cluster_median in enumerate(cluster_medians):
            distance = self.distance_metric(cluster_median['vector'], question['vector'])
            distances.append({'question':cluster_median['question'],'vector': cluster_median['vector'], 'distance':distance,'index':i})
        distances.sort(key=lambda x: x['distance'])
        index = distances[0]['index']
        flag = True
        while(flag):
            for member in clusters[index]:
                if member not in self.recommended_questions:
                    self.recommended_questions.append(member)
                    flag = False
                    break
        return self.recommended_questions[-1]
    
    def find_median(self, cluster):
        distances = []
        for vectorized_question in cluster:
            distance = self.distance_metric(cluster[0]['vector'], vectorized_question['vector'])
            distances.append({'question':vectorized_question['question'],'vector': vectorized_question['vector'], 'distance':distance})
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
    
class  RecommenderCluster2:
    def __init__(self, question_list):
        self.question_list = question_list
        self.vectorized_questions = Vectorize_Questions(self.question_list).vectorized_questions
        self.recommended_questions = []
        self.k = 5
        self.distance_metric = self.cosine_similarity
        self.threshold = 0.7
        self.recommend()
    
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
                    if self.distance_metric(cluster[0]['vector'], vectorized_question['vector']) > self.threshold:
                        cluster.append(vectorized_question)
                        break
                else:
                    clusters.append([vectorized_question])
        return clusters
    
    def recommend(self, question = None):
        if question is None:
            question = self.vectorized_questions[np.random.randint(0, len(self.vectorized_questions))]
            self.recommended_questions.append(question)
            return
        clusters = self.cluster()
        cluster_medians = []
        for cluster in clusters:
            cluster_medians.append(self.find_median(cluster))
        distances = []
        question = [{'question': question}]
        question1 = Vectorize_Questions(question).vectorized_questions[0]
        for i,cluster_median in enumerate(cluster_medians):
            distance = self.distance_metric(cluster_median['vector'], question1['vector'])
            distances.append({'question':cluster_median['question'],'vector': cluster_median['vector'], 'distance':distance,'index':i})
        distances.sort(key=lambda x: x['distance'])
        index = distances[0]['index']
        flag = True
        while(flag):
            for member in clusters[index]:
                if member not in self.recommended_questions:
                    self.recommended_questions.append(member)
                    flag = False
                    break
        return self.recommended_questions[-1]
    
    def find_median(self, cluster):
        distances = []
        for vectorized_question in cluster:
            distance = self.distance_metric(cluster[0]['vector'], vectorized_question['vector'])
            distances.append({'question':vectorized_question['question'],'vector': vectorized_question['vector'], 'distance':distance})
        distances.sort(key=lambda x: x['distance'])
        return distances[len(distances)//2]
    
    

def RecomTest():
    #read questions from database
    tracemalloc.start()
    questions= pd.read_csv('../Trials/Question Bank.csv')
    questions=questions.to_dict('records')
    c2=RecommenderCluster2(questions)
    query_question =c2.recommended_questions[0]
    print("Memory Usage: ",tracemalloc.get_traced_memory()[0]/10**6,"MB")
    print('query_question')
    print(query_question['question'])
    for i in range(4):
        answer = input('Enter answer: ')
        query_question = c2.recommend(answer)
        print('query_question')
        print(query_question['question'])
    # q = {'question':'What is a virtual function?'}
    # c2.recommended_questions.append({'question':q['question'],'vector':Vectorize_Questions([q]).vectorized_questions[0]['vector']})
    # ans = 'A virtual function is a member function of a class, and its functionality can be overridden in its derived class. This function can be implemented by using a keyword called virtual, and it can be given during function declaration'
    # print(c2.recommend(ans))   

def NERTest():
    questions= pd.read_csv('../Trials/Question Bank.csv')
    questions=questions.to_dict('records')
    for question in questions:
        print(question['question'])
        words = word_tokenize(question['question'])
        stopword = set(stopwords.words('english'))
        words = [word for word in words if word not in stopword]
        fdist = FreqDist(words)
        print(fdist.most_common(2))

        document = nlp(question['question'])
        entities = [entity.text for entity in document.ents]
        print(entities)

if __name__ == "__main__":
    RecomTest()
    # NERTest()
        
