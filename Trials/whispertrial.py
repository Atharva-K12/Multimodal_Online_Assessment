import whisper
import cv2
import wave
import numpy as np
import torchtext.data.metrics as metrics
from torchtext.data import get_tokenizer


def getVideo(videoFilePath,applyFunction):
    cap = cv2.VideoCapture(videoFilePath)
    #convert frames to numpy array
    frames = []
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frames.append(frame)
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    applyFunction(np.array(frames))

def processVideo(videoArray):
    #process video array
    print(videoArray)


def useWhisper(audioFile):
    model = whisper.load_model("base")
    result = model.transcribe(audioFile,fp16=False)
    return result['text']

def getTextfromFile(filePath):
    with open(filePath) as f:
        text = f.read()
    return text.replace("\n"," ")

def compareTexts(text1,text2):
    tokenizer = get_tokenizer("basic_english")
    text1 = tokenizer(text1) # , and other punctuation are to be removed # TODO
    text2 = tokenizer(text2) 
    print(text1)
    print(text2)
    print(metrics.bleu_score(text1,text2)) # needs same number of tokens for the two texts

if __name__ == "__main__":
    #getVideo("C:\\Users\\user\\Desktop\\video.mp4",processVideo)
    audioFile = "D:\\fyp\\Multimodal_Online_Assessment\\Trials\\m1.wav"
    textFile = "D:\\fyp\\Multimodal_Online_Assessment\\Trials\\m1.txt"
    text1 = useWhisper(audioFile)
    print(text1)
    text2 = getTextfromFile(textFile)
    print(text2)
    compareTexts(text1,text2)
    





    