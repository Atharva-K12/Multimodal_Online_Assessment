from flask import Blueprint, request, current_app, make_response, jsonify
from ..Functionalities.recommendationSystem import Recommendation
from ..Functionalities.sentenceMatch import sentence_match
from ..Functionalities.Whisper import audioToText
from ..Functionalities.video import video_analysis
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
import datetime
import concurrent.futures as cf

executor = cf.ThreadPoolExecutor()
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
        data = request.form
        data['student_name'] = username
        return Enrollment().enroll(data)
    

@student.route('/start-test', methods=['GET'])
@token_validation
def start_test(username):
    if request.method == 'GET':
        test_id = request.args.get('test_id')
        test = Test().get_test(test_id)
        if test['last_date'] < datetime.datetime.now():
            return make_response(jsonify({'message': 'Test expired'}), 401)
        else :
            return make_response(jsonify({'message': 'Test started'}), 200)

    
@student.route('/recommend', methods=['POST'])
@token_validation
def recommend(username):
    if request.method == 'POST':
        # Header parameters
        data = request.form
        student_id = Student().get_student_id(data['studentName'])
        test_id = Test().get_test_id(data['testName'])
        if not Enrollment().check_enrollment(student_id, test_id):
            return make_response(jsonify({'message': 'You are not enrolled in this test'}), 401)  
        question = Recommendation().recommend(student_id, test_id, None, None)  
        return make_response(jsonify({'question': question['question'], 'questionNumber': 1}),200)


def recommendQue(student_id, test_id, question, answer):
    print('here')
    return Recommendation().recommend(student_id, test_id, question, answer)


def audioAnalysis(student_id, test_id, question, questionNumber, candidate_answer):
    print('here')
    qb = QuestionBank()
    modalQuestion = qb.get_question(question)
    print(modalQuestion)
    # modalQuestion = QuestionBank().get_question(question)
    sentence_cosine_score = sentence_match(modalQuestion,candidate_answer)
    print(sentence_cosine_score)
    scobj = Score()
    scobj.add_score(student_id, test_id, questionNumber, sentence_cosine_score)

@student.route('/upload-answer', methods=['POST'])
@token_validation
def upload_answer(username):
    print(request.files)
    print(request.form)
    if request.method == 'POST':
        if 'file' not in request.files:
            print("Not file")
            data = request.form
            student_id = Student().get_student_id(username)
            test_id = Test().get_test_id(data['testName'])
            if not Enrollment().check_enrollment(student_id, test_id):
                return make_response(jsonify({'message': 'You are not enrolled in this test'}), 401)  
            question = Recommendation().recommend(student_id, test_id, None, None)  
            return make_response(jsonify({'question': question['question'], 'questionNumber': 1}),200)
        # data = request.form
        # student_id = Student().get_student_id(username)
        # test_id = Test().get_test_id(data['testName'])
        # if not Enrollment().check_enrollment(student_id, test_id):
        #     return make_response(jsonify({'message': 'You are not enrolled in this test'}), 401)  
        # question = Recommendation().recommend(student_id, test_id, None, None) 
        # print(question)
        # return make_response(jsonify({'question': question['question'], 'questionNumber': int(data['questionNumber']) + 1}),200)
        file = request.files['file']
        if file:
            data = request.form
            student_id = Student().get_student_id(username)
            test_id = Test().get_test_id(data['testName'])
            if not Enrollment().check_enrollment(student_id, test_id):
                return make_response(jsonify({'message': 'You are not enrolled in this test'}), 401)
            filename = username + '_' + data['testName'] + '_' + str(data['questionNumber']) + '.mp3'
            file.save(os.path.join(current_app.config['AUDIO_FOLDER'], username ,filename))
            candidate_answer = audioToText(os.path.join(current_app.config['AUDIO_FOLDER'], username, filename))
            print(candidate_answer)
            # audio_thread = th.Thread(target=audioAnalysis, args=(student_id, test_id, data['question'], data['questionNumber'], candidate_answer))
            # audio_thread.start()
            audioAnalysis(student_id, test_id, data['question'], data['questionNumber'], candidate_answer)
            test_id=Test().get_test_id(data['testName'])
            print(test_id)
            max_question = Test().get_max_question(test_id)
            print(max_question)
            if int(data['questionNumber']) < max_question:
                print('here if')
                # output_queue = queue.Queue()
                # recommend_thread = th.Thread(target=recommendQue, args=(student_id, test_id, output_queue, data['question'], candidate_answer))
                # recommend_thread.start()
                # audio_thread.join()
                # recommend_thread.join()
                nextQuestion=recommendQue(student_id, test_id, data['question'], candidate_answer)
                # nextQuestion = output_queue.get()
                print(nextQuestion)
                return make_response(jsonify({'question': nextQuestion['question'], 'questionNumber':int(data['questionNumber'])+1}), 200)
            else:
                # audio_thread.join()
                return make_response(jsonify({'message': 'End of Test'}), 200)


@student.route('/video-upload', methods=['POST'])
@token_validation
def video_upload(username):
    if request.method == 'POST':
        if 'file' not in request.files:
            print(request.form['testName'])
            return make_response(jsonify({'message': 'No file found'}), 400)
        file = request.files['file']
        if file:
            data = request.form
            student_id = Student().get_student_id(username)
            test_id = Test().get_test_id(data['testName'])
            if not Enrollment().check_enrollment(student_id, test_id):
                return make_response(jsonify({'message': 'You are not enrolled in this test'}), 401)
            filename = username + '_' + data['testName'] + '.mp4'
            file.save(os.path.join(current_app.config['VIDEO_FOLDER'], filename))
            video_path = os.path.join(current_app.config['VIDEO_FOLDER'], filename)
            executor.submit(video_analysis_function, video_path, username, test_id)
            return make_response(jsonify({'message': 'File uploaded'}), 200)

# Pass argument to fucntion using executor.submit(video_analysis)
def video_analysis_function(video_path, username, test_id):
    scores = video_analysis(video_path)
    student_id = Student().get_student_id(username)
    Score().update_negative_score(student_id, test_id, scores)

