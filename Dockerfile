FROM python
# Path: Dockerfile

# Whisper installation
RUN pip3 install git+https://github.com/openai/whisper.git setuptools-rust torch torchvision torchaudio torchtext

RUN sudo apt update && sudo apt install ffmpeg





