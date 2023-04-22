import cv2
import matplotlib.pyplot as plt
import face_detection
from scipy.spatial import distance as dist
import dlib
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import imutils
from gaze_tracking import GazeTracking
import mediapipe as mp
import numpy as np


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
        
'''
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
'''

def headpose_detect(video_path):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(video_path)
    result = dict()
    for key in ['left', 'right', 'center', 'down', 'up']:
        result[key] = 0

    while cap.isOpened():
        _, image = cap.read()

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        
        results = face_mesh.process(image)

        image.flags.writeable = True
        
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = image.shape
        face_3d = []
        face_2d = []

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        face_2d.append([x, y])

                        face_3d.append([x, y, lm.z])       
                
                face_2d = np.array(face_2d, dtype=np.float64)
                face_3d = np.array(face_3d, dtype=np.float64)

                focal_length = 1 * img_w

                cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                        [0, focal_length, img_w / 2],
                                        [0, 0, 1]])

                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                rmat, jac = cv2.Rodrigues(rot_vec)

                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                x = angles[0] * 360
                y = angles[1] * 360

                if y < -10:
                    result['left'] += 1
                elif y > 10:
                    result['right'] += 1
                elif x < -10:
                    result['down'] += 1
                else:
                    result['centre'] += 1
    cap.release()
    
    return 0

def gaze_tracking(video_path):
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(video_path)
    result = dict()
    
    for key in ['left', 'right', 'center', 'blink']:
        result[key] = 0

    while webcam.isOpened():
        _, frame = webcam.read()

        gaze.refresh(frame)

        frame = gaze.annotated_frame()

        if gaze.is_blinking():
            result['blink'] += 1
        elif gaze.is_right():
            result['right'] += 1
        elif gaze.is_left():
            result['left'] += 1
        elif gaze.is_center():
            result['center'] += 1
 
    webcam.release()     
    return result
            

# Perform all malpractice checks for video analysis
def video_analysis(video_path):
    scores = dict()
    keys = ['face', 'blink', 'headpose', 'gaze']
    for key in keys:
        scores[key] = None
    scores['face'] = face_detect(video_path)
    #scores['blink'] = eye_blink_detect(video_path)
    scores['gaze'] = gaze_tracking(video_path)
    scores['headpose'] = headpose_detect(video_path)

    return scores
        
        
video_analysis('APlusBsquare.mp4')