FROM python:3.9-slim-buster

# set working directory
WORKDIR /app

# install system dependencies
RUN apt-get update \
  && apt-get clean

# add and install requirements
RUN apt install -y cmake
RUN apt install -y libsm6
RUN apt install -y libxext6
RUN apt install -y libxrender1
RUN apt install -y libfontconfig1
RUN apt install -y git
RUN pip install --upgrade pip
RUN apt install -y ffmpeg
RUN pip install git+https://github.com/openai/whisper.git setuptools-rust
RUN pip install opencv-python
RUN pip install -U sentence-transformers
RUN pip install flask
RUN pip install flask_cors

RUN apt install -y build-essential cmake
RUN apt install -y libopenblas-dev liblapack-dev 
RUN apt install -y  libx11-dev libgtk-3-dev
RUN apt install -y  python3-dev python3-pip python3-setuptools
RUN pip install dlib
RUN pip install pymongo
RUN pip install bcrypt
RUN pip install pyjwt
RUN pip install git+https://github.com/hukkelas/DSFD-Pytorch-Inference.git
RUN pip install mediapipe
# add app
COPY . .