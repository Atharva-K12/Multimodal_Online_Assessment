FROM ubuntu:18.04
RUN apt-get update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y cmake
RUN apt install -y libsm6
RUN apt install -y libxext6
RUN apt install -y libxrender1
RUN apt install -y libfontconfig1
RUN pip3 install --upgrade pip
RUN pip3 install git+https://github.com/openai/whisper.git setuptools-rust
RUN sudo apt update && sudo apt install ffmpeg
RUN pip3 install opencv-python
RUN pip3 install -U sentence-transformers
RUN pip3 install flask
RUN pip3 install flask_cors
RUN git submodule add https://github.com/antoinelame/GazeTracking.git Models/GazeTracking
RUN git submodule update --init --recursive
RUN pip3 install -r Models/GazeTracking/requirements.txt

# run the react app from frontend folder
RUN cd frontend && npm install && npm start
# run the flask app from backend folder

EXPOSE 5000
RUN cd backend && flask run







