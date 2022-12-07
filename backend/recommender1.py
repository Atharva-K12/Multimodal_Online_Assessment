import random

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
                
                
        