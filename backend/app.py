import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
from useWhisper import audioToText
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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # grade function to be called here
            sentence_cosine_score = sentence_match(audioToText(app.config['AUDIO_FILE']),"ADD RETRIEVED TEXT HERE")
            text_score = sentence_scoring_metric(sentence_cosine_score)
            # Video analysis function to be called here
            video_score = ADD_VIDEO_ANALYSIS_FUNCTION_HERE()
            # Final score to be calculated here
            final_score = ADD_FINAL_SCORE_FUNCTION_HERE(text_score,video_score)

            # RETURN FINAL SCORE DATA AND OTHER ANALYSIS DATA 
            
            return "File uploaded successfully"