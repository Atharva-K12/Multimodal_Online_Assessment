import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Models.gazeTracker.gaze_tracking import GazeTracking
import cv2

class VideoEyeTracker:
    def __init__(self, videopath):
        self.videopath = videopath
        self.classify_stream = []
        self.number_of_frames = 0
        self.threshold = 10
        self.eyeTrack()
        self.plagpercent=self.countPlagiarism()
        
    def eyeTrack(self):
        gazer = GazeTracking()
        video = cv2.VideoCapture(self.videopath)
        while True:
            _, frame = video.read()
            if frame is None:
                break
            gazer.refresh(frame)
            frame = gazer.annotated_frame()
            if gazer.is_blinking():
                self.classify_stream.append('0')
            elif gazer.is_right():
                self.classify_stream.append('1')
            elif gazer.is_left():
                self.classify_stream.append('1')
            elif gazer.is_center():
                self.classify_stream.append('0')
            self.number_of_frames += 1
    
    def countPlagiarism(self):
        count = 0
        countList = []
        for i in range(len(self.classify_stream)):
            if self.classify_stream[i] == '1':
                count += 1
            else:
                if count > self.threshold:
                    countList.append(count)
                count = 0
        if count != 0 and count > self.threshold:
            countList.append(count)
        
        self.plagpercent = (sum(countList)/self.number_of_frames)
        
        



