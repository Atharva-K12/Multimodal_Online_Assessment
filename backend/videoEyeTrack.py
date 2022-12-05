import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Models.gazeTracker.gaze_tracking import GazeTracking
import cv2
import numpy as np

def videoEyeTrack(videopath):
    counts = {'left':0, 'right':0, 'center':0,'blink':0}
    gazer = GazeTracking()
    video = cv2.VideoCapture(videopath)
    while True:
        _, frame = video.read()
        gazer.refresh(frame)
        frame = gazer.annotated_frame()
        text = ""
        if gazer.is_blinking():
            counts['blink'] += 1
        elif gazer.is_right():
            counts['right'] += 1
        elif gazer.is_left():
            counts['left'] += 1
        elif gazer.is_center():
            counts['center'] += 1

    return counts