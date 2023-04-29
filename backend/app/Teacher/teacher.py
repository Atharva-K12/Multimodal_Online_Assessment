from flask import Blueprint, request, current_app, make_response, jsonify
from ..Models.test import Test
from ..Models.teacher import Teacher
from ..middelware import token_validation
from ..Functionalities.questionsUpload import questionUpload
from ..Functionalities.clusterData import ClusterData
import concurrent.futures as cf
import os

executor = cf.ThreadPoolExecutor()
teacher = Blueprint('teacher', __name__)

def test_file_upload(filepath):
    questionUpload(filepath)
    ClusterData().createCluster()
    

@teacher.route('/create-test', methods=['POST'])
@token_validation
def create_test(username):
    if request.method == 'POST':
        data = request.get_json()
        teacher = Teacher().get_teacher(username)
        data['teacher_id'] = teacher['teacher_id']
        return Test().create_test(data)
    

@teacher.route('/upload-test-file', methods=['POST'])
@token_validation
def upload_test_file(username):
    if request.method == 'POST':
        file = request.files['file']
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        executor.submit(test_file_upload, filepath)
        return make_response(jsonify({'message': 'File uploaded successfully'}), 200)
    

            


