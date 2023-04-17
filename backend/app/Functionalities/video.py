import cv2
import matplotlib.pyplot as plt
import face_detection

def face_detect(img):
    detector = face_detection.build_detector("RetinaNetResNet50", confidence_threshold=.5, nms_iou_threshold=.3)
    detections = detector.detect(img)
    print("Number of faces detected: {}".format(len(detections)))
    
    return len(detections)

def eye_blink_detect(img):
    return 0

def headpose_detect(img):
    return 0

def gaze_tracking(img):
    return 0

# Perform all malpractice checks for video analysis
def video_analysis(video_path):
    cam = cv2.VideoCapture(video_path)
    fps = cam.get(cv2.CAP_PROP_FPS)
    i = 0
    scores = dict()
    keys = ['face', 'blink', 'headpose', 'gaze']
    for key in keys:
        scores[key] = None
        
    while True:
        if i % fps == 0:
            ret, frame = cam.read()
            if not ret:
                break
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            scores['face'] = face_detect(img_rgb)
            scores['blink'] = eye_blink_detect(img_rgb)
            scores['headpose'] = headpose_detect(img_rgb)
            scores['gaze'] = gaze_tracking(img_rgb) 
        i+=1
    cam.release()
    return scores
        
        
video_analysis('APlusBsquare.mp4')
        
        
