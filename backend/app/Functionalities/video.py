import cv2
import face_detection
# import dlib
# from .gaze_tracking import GazeTracking
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
            if len(detections) > 1:
                frame_count += 1
        i += 1
    cam.release()
    return frame_count/i
        

def headpose_detect(video_path):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(video_path)
    result = dict()
    for key in ['left', 'right', 'centre', 'down', 'up']:
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

    centre_count = result['centre']
    ret = 0
    for result_key in result.keys():
        ret += result[result_key] / centre_count
    return ret-1
        

# def gaze_tracking(video_path):
#     gaze = GazeTracking()
#     webcam = cv2.VideoCapture(video_path)
#     result = dict()
#     fps = webcam.get(cv2.CAP_PROP_FPS)
#     for key in ['left', 'right', 'center', 'blink']:
#         result[key] = 0
    
#     while webcam.isOpened():
#         _, frame = webcam.read()

#         gaze.refresh(frame)

#         frame = gaze.annotated_frame()

#         if gaze.is_blinking():
#             result['blink'] += 1
#         elif gaze.is_right():
#             result['right'] += 1
#         elif gaze.is_left():
#             result['left'] += 1
#         elif gaze.is_center():
#             result['center'] += 1
 
#     webcam.release()
#     centre_count = result['center']
#     ret = 0
#     for result_key in result.keys():
#         if result_key == 'blink':
#             ret_blink = float(result[result_key] == 0)
#         else:
#             ret += result[result_key] / centre_count
#     return ret-1
            

# Perform all malpractice checks for video analysis
def video_analysis(video_path):
    scores = dict()
    keys = ['face', 'blink', 'headpose', 'gaze']
    for key in keys:
        scores[key] = None
    scores['face'] = face_detect(video_path)
    #scores['blink'] = eye_blink_detect(video_path)
    # scores['gaze'] = gaze_tracking(video_path)
    scores['headpose'] = headpose_detect(video_path)
    total = 0
    for key in scores.keys():
        if scores[key] is not None:
            total += scores[key]
    return total
        
        
# video_analysis('APlusBsquare.mp4')