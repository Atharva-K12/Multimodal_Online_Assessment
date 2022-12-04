FROM ubuntu:18.04
RUN apt-get update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y cmake
RUN apt install -y libsm6
RUN apt install -y libxext6
RUN apt install -y libxrender1
RUN apt install -y libfontconfig1
RUN apt install -y git
RUN pip3 install --upgrade pip
RUN apt-get update && apt-get install -y git
RUN pip3 install git+https://github.com/openai/whisper.git setuptools-rust
RUN sudo apt update && sudo apt install ffmpeg
RUN pip3 install opencv-python
RUN pip3 install -U sentence-transformers
RUN pip3 install flask
RUN pip3 install flask_cors

# run the react app from frontend folder
RUN cd frontend && npm install && npm start
# run the flask app from backend folder

EXPOSE 5000
RUN cd backend && flask run







