import os
import bson.json_util as json_util
import bcrypt
from flask import Flask, request, session, make_response, jsonify
from flask_cors import CORS
import jwt
from functools import wraps
from useWhisper import audioToText
# from videoEyeTrack import VideoEyeTracker
from pymongo import MongoClient
from sentenceMatch import sentence_match , sentence_scoring_metric
from score import scoring_criteria
from recommender1 import Question

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
CORS(app)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Secret key to be decided
app.config['SECRET_KEY'] = 'secret key'

client = MongoClient("mongodb+srv://test:test12345@fypdb.11jbtg4.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('fyp')
records= db.questionBank
list_of_questions = list(records.find())
q = Question(list_of_questions)

####################### Middle-ware functions ############################

def token_validation(func):
    @wraps(func)
    def validate(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = db.users.find_one({'public_id':data['public_id']})
            if not current_user:
                return jsonify({'message':'Token is invalid'}), 401
        except:
            return jsonify({'message':'Token is invalid'}), 401
        return func(current_user, *args, **kwargs)
    
    return validate

################################################################################

@app.route("/SignUp", methods=['POST'])
def SignUp():
    # Check whether username exists in db
    # If exists, return error
    # Else, add user to db
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({'username':username})
        if user:
            return "Username already exists"
        else:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            db.users.insert_one({'username':username,'password':hashed,'email':request.form['email']})
            return "User created"


@app.route("/Login", methods=['POST'])
def Login():
    # Check whether username exists in db
    # If exists, check password
    # Else, return error
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({'username':username})
        if user:
            if bcrypt.hashpw(password.encode('utf-8'), user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['username'] = username
                token = jwt.encode({'public_id':user['public_id']}, app.config['SECRET_KEY'])
                return make_response(jsonify({'token':token}), 200)
            else:
                return "Incorrect password"
        else:   
            return "Username does not exist"


@app.route("/Logout", methods=['GET'])
@token_validation
def Logout(current_user):
    session.pop('username', None)
    return "Logout successful"

            
@app.route("/get-question", methods=['GET'])
def get_question():
    # client = MongoClient("mongodb+srv://test:test12345@fypdb.11jbtg4.mongodb.net/?retryWrites=true&w=majority")
    # db = client.get_database('fyp')
    # records= db.questionBank
    # list_of_questions = list(records.find())
    # q = Question(list_of_questions)
    
    # ret_question = random.choice(list_of_questions)
    ret_question = q.next_question()
    print(ret_question)
    json_return_object = json_util.dumps(ret_question)
    return json_return_object


# Multi user support
@app.route("/upload", methods=['POST'])
@token_validation()
def upload_file(current_user):
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            # Saved file is mp4 file
            username = current_user['username']
            qid = request.form['qid']
            filename = username + qid + ".mp3"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # video = mp.VideoFileClip(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # video.audio.write_audiofile(os.path.join(app.config['UPLOAD_FOLDER'], filename.split(".")[0] + ".wav"))

            #client = MongoClient("mongodb+srv://test:test12345@fypdb.11jbtg4.mongodb.net/?retryWrites=true&w=majority")
            #db = client.get_database('fyp')
            #records= db.questionBank
            question = request.form['question']
            question = records.find({"question":question})
            answer = json_util.dumps(question[0]["answer"])

            # Audio to text conversion and sentence matching
            app.config['FILE_PATH'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            sentence_cosine_score = sentence_match(audioToText(app.config['FILE_PATH']),answer)
            text_score = sentence_scoring_metric(sentence_cosine_score)
            # # Video analysis function to be called here
            video_score = 0
            # video_score = VideoEyeTracker(app.config['FILE_PATH']).plagpercent
            # Final score to be calculated here
            final_score = scoring_criteria(text_score,video_score)
            q.asked_questions.append({'Question':question[0], 'Score' :final_score})
            score = {"score":final_score,"text_score":text_score, "video_score":video_score}
            
            json_return_score = json_util.dumps(score)
            return json_return_score


# Video file upload
@app.route("/videoFile", methods = ['POST'])
@token_validation
def upload_video(current_user):
    if request.method == 'POST':
        if 'video-file' not in request.files:
            return "No file part"
        file = request.files['video-file']
        if file.filename == '':
            return "No selected file"
        if file:
            # Saved file is mp4 file
            username = current_user['username']
            filename = username + ".mp4"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "File uploaded successfully"