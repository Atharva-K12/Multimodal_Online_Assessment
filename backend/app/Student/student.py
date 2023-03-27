from flask import Blueprint, request, current_app, make_response, jsonify
from ..Functionalities.recommendationSystem import Recommendation
from ..Functionalities.sentenceMatch import sentence_match
from ..Functionalities.whisper import audioToText
from ..Models.test import Test
from ..Models.enrollment import Enrollment
from ..Models.student import Student
from ..Models.test import Test
from ..Models.score import Score
from ..Models.questionBank import QuestionBank
from ..middelware import token_validation
import os
import threading as th
import queue

student = Blueprint('student', __name__)

@student.route('/get-student-enrollments', methods=['GET'])
@token_validation
def get_student_enrollments(username):
    if request.method == 'GET':
        return make_response(jsonify({'enrollments': Enrollment().get_enrollments(username)}), 200)
    

@student.route('/get-all-test', methods=['GET'])
@token_validation
def get_all_test(username):
    if request.method == 'GET':
        test = Test().get_tests()
        enrollment = Enrollment().get_enrollments(username)
        for i in enrollment:
            test.remove(i)
        return make_response(jsonify({'tests': test}), 200)
    

@student.route('/enroll', methods=['POST'])
@token_validation
def enroll(username):
    if request.method == 'POST':
        data = request.get_json()
        data['student_name'] = username
        return Enrollment().enroll(data)
    

@student.route('/create-test', methods=['POST'])
def create_test():
    if request.method == 'POST':
        data = request.get_json()
        return Test().create_test(data)
    
    
@student.route('/recommend', methods=['POST'])
@token_validation
def recommend(username):
    if request.method == 'POST':
        # Header parameters
        data = request.get_json()
        student_id = Student().get_student_id(data['studentName'])
        test_id = Test().get_test_id(data['testName'])
        if not Enrollment().check_enrollment(student_id, test_id):
            return make_response(jsonify({'message': 'You are not enrolled in this test'}), 401)  
        question = Recommendation().recommend(student_id, test_id, None)  
        return make_response(jsonify({'question': question['question'], 'questionNumber': 1}),200)


def recommendQue(student_id, test_id, queue, question):
    queue.put(Recommendation().recommend(student_id, test_id, question))


def audioAnalysis(username, testName, question, question_number, file):
    filename = username + '_' + testName + '_' + str(question_number) + '.mp3'
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    modalQuestion = QuestionBank().get_question(question)
    sentence_cosine_score = sentence_match(modalQuestion['answer'], audioToText(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)))
    Score().add_score(username, testName, question, question_number, sentence_cosine_score)


@student.route('/upload-answer', method=['POST'])
@token_validation
def upload_answer(username):
    if request.method == 'POST':
        if 'file' not in request.files:
            return make_response(jsonify({'message': 'No file found'}), 400)
        file = request.files['file']
        if file:
            student_id = Student().get_student_id(username)
            test_id = Test().get_test_id(data['testName'])
            if not Enrollment().check_enrollment(student_id, test_id):
                return make_response(jsonify({'message': 'You are not enrolled in this test'}), 401)
            data = request.get_json()
            audio_thread = th.Thread(target=audioAnalysis, args=(username, data['testName'], data['question'], data['questionNumber'], file))
            audio_thread.start()
            output_queue = queue.Queue()
            if data['questionNumber'] == Test().get_max_question(Test().get_test_id(data['testName'])):
                if 'question' in data:
                    recommend_thread = th.Thread(target=recommendQue, args=(student_id, test_id, output_queue, data['question']))
                else:
                    recommend_thread = th.Thread(target=recommendQue, args=(student_id, test_id, output_queue, None))
                recommend_thread.start()
                audio_thread.join()
                recommend_thread.join()
                nextQuestion = output_queue.get()
                return make_response(jsonify({'question': nextQuestion['question'], 'questionNumber':data['questionNumber']+1}), 200)
            else:
                audio_thread.join()
                return make_response(jsonify({'message': 'End of Test'}), 200)
