import os
import bson.json_util as json_util
from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
import moviepy.editor as mp
import random
from useWhisper import audioToText
from videoEyeTrack import VideoEyeTracker
from pymongo import MongoClient
from sentenceMatch import sentence_match , sentence_scoring_metric

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            client = MongoClient("mongodb+srv://test:test12345@fypdb.11jbtg4.mongodb.net/?retryWrites=true&w=majority")
            db = client.get_database('fyp')
            records= db.questionBank
            qid = request.form['qid']
            question = records.find({"_id":qid})
            answer = json_util.dumps(question)['answer']

            # Audio to text conversion and sentence matching
            app.config['FILE_PATH'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            sentence_cosine_score = sentence_match(audioToText(app.config['FILE_PATH']),answer)
            text_score = sentence_scoring_metric(sentence_cosine_score)
            # Video analysis function to be called here
            video_score = VideoEyeTracker(app.config['FILE_PATH'])
            # Final score to be calculated here
            # final_score = ADD_FINAL_SCORE_FUNCTION_HERE(text_score,video_score)

            # RETURN FINAL SCORE DATA AND OTHER ANALYSIS DATA 
            
            return "File uploaded successfully"

@app.route("/get-question", methods=['GET'])
def get_question():
    client = MongoClient("mongodb+srv://test:test12345@fypdb.11jbtg4.mongodb.net/?retryWrites=true&w=majority")
    db = client.get_database('fyp')
    records= db.questionBank
    list_of_questions = list(records.find())
    ret_question = random.choice(list_of_questions)
    json_return_object = json_util.dumps(ret_question)
    return json_return_object