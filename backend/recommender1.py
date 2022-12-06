import random

class Question:
    def __init__(self, question_list):
        self.question_list = question_list
        self.asked_questions = {}
        self.easy = [d for d in self.question_list if d['difficulty'] == 'easy']
        self.medium = [d for d in self.question_list if d['difficulty'] == 'medium']
        self.hard = [d for d in self.question_list if d['difficulty'] == 'hard']

    def evaluate_answer(self, answer):
        return answer == self.question
    
    def first_question(self):
        q1 = random.choice(self.easy)
        self.asked_questions[q1] = 'easy'
        return q1
    
    def choose_question(self, next_level, label):
        q = random.choice(next_level)
        while q in self.asked_questions:
            q = random.choice(next_level)
        next_ques = q
        self.asked_questions[q] = label
        
        return next_ques 
    
    def next_question(self, current_question, current_score):
        next_ques = ""
        if current_score >= 0.7:
            if self.asked_questions[current_question] == 'easy':
                next_ques = self.choose_question(self.medium, 'medium')
            else:
                next_ques = self.choose_question(self.hard, 'hard')
        elif current_score >= 0.4 and current_score < 0.7:
            if self.asked_questions[current_question] == 'easy':
                next_ques = self.choose_question(self.easy, 'easy')
            elif self.asked_questions[current_question] == 'medium':
                next_ques = self.choose_question(self.medium, 'medium')
            else:
                next_ques = self.choose_question(self.hard, 'hard')
        else:
            if self.asked_questions[current_question] == 'easy' or self.asked_questions[current_question] == 'medium':
                next_ques = self.choose_question(self.easy, 'easy')
            else:
                next_ques = self.choose_question(self.medium, 'medium')
                
        return next_ques
                
                
        