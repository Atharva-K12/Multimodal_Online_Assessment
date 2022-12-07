import os
import bson.json_util as json_util
from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
import moviepy.editor as mp
import random
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

client = MongoClient("mongodb+srv://test:test12345@fypdb.11jbtg4.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('fyp')
records= db.questionBank
list_of_questions = list(records.find())
q = Question(list_of_questions)

@app.route("/upload", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            # Saved file is mp4 file
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # video = mp.VideoFileClip(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # video.audio.write_audiofile(os.path.join(app.config['UPLOAD_FOLDER'], filename.split(".")[0] + ".wav"))
            # # grade function to be called here

            #Get answer from database
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