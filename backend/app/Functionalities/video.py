import cv2
import matplotlib.pyplot as plt
import face_detection
from scipy.spatial import distance as dist
import dlib
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import imutils

def face_detect(video_path):
    cam = cv2.VideoCapture(video_path)
    fps = cam.get(cv2.CAP_PROP_FPS)
    i = 0
    detector = face_detection.build_detector("RetinaNetResNet50", confidence_threshold=.5, nms_iou_threshold=.3)
    frame_count = 0
    while True:
        if i % fps == 0:
            ret, frame = cam.read()
            if not ret:
                break
            detections = detector.detect(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if len(detections) > 0:
                frame_count += 1
        i += 1
    cam.release()
    return frame_count
        

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])
	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)
	# return the eye aspect ratio
	return ear

def eye_blink_detect(filepath):
    # define two constants, one for the eye aspect ratio to indicate
    # blink and then a second constant for the number of consecutive
    # frames the eye must be below the threshold
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 3
    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0
    blink = 0
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    
    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    
    vs = FileVideoStream(filepath).start()
    fileStream = True
    
    while True:
        if fileStream and not vs.more():
            break
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        
        if len(rects) != 1:
            return -1
        else:
            shape = predictor(gray, rects)
            shape = face_utils.shape_to_np(shape)
            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0
            
            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:
                COUNTER += 1
                blink += 1
            # otherwise, the eye aspect ratio is not below the blink
            # threshold
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1
                    blink -= COUNTER
                # reset the eye frame counter
                COUNTER = 0
    return blink

def headpose_detect(img):
    return 0

def gaze_tracking(img):
    return 0

# Perform all malpractice checks for video analysis
def video_analysis(video_path):
    scores = dict()
    keys = ['face', 'blink', 'headpose', 'gaze']
    for key in keys:
        scores[key] = None
    scores['face'] = face_detect(video_path)
    scores['blink'] = eye_blink_detect(video_path)

    return scores
        
        
video_analysis('APlusBsquare.mp4')