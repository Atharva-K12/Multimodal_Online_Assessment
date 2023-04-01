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
RUN pip install dlib
RUN pip install pymongo

# add app
COPY . .