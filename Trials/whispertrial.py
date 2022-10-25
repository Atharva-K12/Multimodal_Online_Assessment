import whisper
import cv2
import wave
import numpy as np
import torchtext.data.metrics as metrics


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
    print(result)
    return result['text']

def getTextfromFile(filePath):
    with open(filePath) as f:
        text = f.read().split(" .,\'\"")
    return text

def compareTexts(text1,text2):
    #compare BLEU Score



if __name__ == "__main__":
    





    