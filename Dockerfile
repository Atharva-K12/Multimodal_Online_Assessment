FROM ubuntu:latest
RUN apt-get update
COPY . /app
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y cmake
RUN apt install -y libsm6
RUN apt install -y libxext6
RUN apt install -y libxrender1
RUN apt install -y libfontconfig1
RUN apt install -y git
RUN pip3 install --upgrade pip
RUN apt install -y ffmpeg
RUN pip3 install git+https://github.com/openai/whisper.git setuptools-rust
RUN pip3 install opencv-python
RUN pip3 install -U sentence-transformers
RUN pip3 install flask
RUN pip3 install flask_cors
RUN pip3 install dlib

WORKDIR /app
RUN git sumbodule init
RUN cd frontend && npm start
RUN cd backend && flask run

# RUN ls
# # run the react app from frontend folder
# RUN cd frontend && npm install && npm start
# # run the flask app from backend folder

# EXPOSE 5000
# RUN cd backend && flask run







