FROM python:3.9-slim-buster

# set working directory
WORKDIR /app

# install system dependencies
RUN apt-get update \
  && apt-get clean

# add and install requirements
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
RUN pip3 install pymongo

# add app
COPY . .