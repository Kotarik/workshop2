# USAGE
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat
# SOURCE
# https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/

from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from math import sqrt, acos, degrees
import datetime
import argparse
import imutils
import time
import dlib
import cv2
import requests
import json

with open('config.json') as f:
    config = json.load(f)

# Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
    help="Path to facial landmark predictor")
ap.add_argument("-n", "--no-request", action='store_true',
    help="No request action")
ap.add_argument("-f", "--face", action='store_true',
    help="Print face !")
args = vars(ap.parse_args())

# Initialize facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# Initialize the video stream
print("[INFO] camera sensor warming up...")
vs = VideoStream().start()
time.sleep(1.0)

# Part face
face = config['face']

# Pila number
pila_nb = config['pila_nb']

# Ratio eyebrow / nose
RATIO_EYE = config['ratio']['eye']
RATIO_EYEBROW_SURPRISE = config['ratio']['eyebrow_surprise']
RATIO_EYEBROW_FOCUS = config['ratio']['eyebrow_focus']

# Frame count
FRAME_NB = config['frame_nb']

# Degrees for head turn
TURN_HEAD = config['turn_head']

URL = config['url']

FONT = cv2.FONT_HERSHEY_SIMPLEX

# Eye part
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Counter for surprise
time_alarm_surpris = 0
time_alarm_turn = 0
time_alarm_focus = 0

request_surpris = True 
request_turn = False
request_focus = False

def eye_aspect_ratio(eye):
    # Distances between vertical eye landmarks
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Distance between horizontal eye landmark
    C = dist.euclidean(eye[0], eye[3])

    # Eye aspect ratio
    ear = (A + B) / (2.0 * C)

    return ear

def measure_angle(pts_a, pts_b, pts_c):
    a = dist.euclidean(pts_a, pts_b)
    b = dist.euclidean(pts_b, pts_c)
    c = dist.euclidean(pts_c, pts_a)
    return degrees(acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)))

def cal_ear():
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    return round((leftEAR + rightEAR) / 2.0, 3)

def center_ligne(pt1, pt2):
    pt1 = face['right_eyebrow']['barycentre']
    pt2 = face['left_eyebrow']['barycentre']
    center_x = int(round((pt1[0] + pt2[0]) / 2))
    center_y = int(round((pt1[1] + pt2[1]) / 2))
    return (center_x, center_y)

while True:
    # Get frame
    frame = vs.read()
    frame = imutils.resize(frame, 1300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    rects = detector(gray, 0)
    
    # Loop over the face detections
    for rect in rects:
        # Facial landmarks FACS
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        if args['face']:
            frame = face_utils.visualize_facial_landmarks(frame, shape)
        else:
            pass

        for (i, name) in enumerate(face.keys()):
            # For all points in face

            if name in ['eyebrow']:
                # if part face in list, continue
                continue

            # All points in part face
            (j, k) = face[name]['pts']
            for i in range(j, k):
                face[name]['pts_list'][i + 1] = shape[i]

            # Calcule barycenter part face
            if name in ['right_eyebrow', 'left_eyebrow', 'nose', 'right_eye', 'left_eye']:
                nb_pts = len(face[name]['pts_list'])
                x = 0
                y = 0
                for v in face[name]['pts_list'].values():
                    x += v[0]
                    y += v[1]
                x = int(round(x / nb_pts))
                y = int(round(y / nb_pts))
                face[name]['barycentre'] = (x, y)
                font = cv2.FONT_HERSHEY_PLAIN
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

            # Print all points in face
            for k,v in face[name]['pts_list'].items():
                (x, y) = v
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                font = cv2.FONT_HERSHEY_PLAIN
                cv2.putText(frame, str(k), (x, y), font, 1, (255,255,255), 1)
        
        # Center between eyebrow line
        face['eyebrow']['centre'] = center_ligne(face['right_eyebrow']['barycentre'], face['left_eyebrow']['barycentre'])
        cv2.circle(frame, face['eyebrow']['centre'], 1, (0, 255, 0), -1)

        dist_nose = dist.euclidean(face['nose']['barycentre'], face['eyebrow']['centre'])
        dist_eyebrow = dist.euclidean(face['right_eyebrow']['barycentre'], face['left_eyebrow']['barycentre'])
        ratio_eyebrow = round(dist_nose / dist_eyebrow, 5)
        cv2.putText(frame, "Ratio Eyebrow : %s " % str(ratio_eyebrow), (10, 30), FONT, 0.7, (0, 0, 0), 2)

        # Calculate EAR
        ear = cal_ear()
        cv2.putText(frame, "EAR : %s" % ear, (10, 60), FONT, 0.7, (0, 0, 0), 2)

        dist2829 = round(dist.euclidean(shape[28],shape[29]))
        dist2028 = round(dist.euclidean(shape[20], shape[28]))
        # Calculate ratio
        ratio20 = round(dist2028 / dist2829, 5)
        cv2.putText(frame, "Ratio eyebrow / nose : %s" % str(ratio20), (10, 90), FONT, 0.7, (0, 0, 0), 2)

        # Alert when surprise
        if ratio_eyebrow >= RATIO_EYEBROW_SURPRISE and ear >= RATIO_EYE:
            time_alarm_surpris += 1
            if time_alarm_surpris >= FRAME_NB:
                cv2.putText(frame, "Surprise !", (10, 300), FONT, 0.7, (0, 0, 255), 2)
                if request_surpris:
                    request_surpris = False
                    if args['no_request']:
                        print('===============================')
                        print('No request !')
                        print('Emotion : supris')
                        print('Pila : %s' % pila_nb)
                        print('===============================')
                    else:
                        data = {
                            'emotion': 'surpris',
                            'pila': pila_nb
                        }
                        print('=============================')
                        print('Request : %s' % URL)
                        print('Data : %s' % data)
                        print('=============================')
                        requests.post('%s/emotion' % URL, data=data)
        else:
            time_alarm_surpris = 0
            request_surpris = True

        # Calculate angle for turn head
        angle = round(measure_angle(face['left_eyebrow']['barycentre'], face['eyebrow']['centre'], face['nose']['barycentre']), 1)
        cv2.putText(frame, "Angle : %s" % angle, (10, 210), FONT, 0.7, (0, 0, 0), 2)

        # Alert when head turn
        if angle < 90 - TURN_HEAD or angle > 90 + TURN_HEAD:
            time_alarm_turn += 1
            if time_alarm_turn >= 5:
                cv2.putText(frame, "Head turn !", (10, 330), FONT, 0.7, (0, 0, 255), 2)
                if request_turn:
                    request_turn = False
                    if args['no_request']:
                        print('===============================')
                        print('No request !')
                        print('Emotion : headturn')
                        print('Pila : %s' % pila_nb)
                        print('===============================')
                    else:
                        data = {
                            'emotion': 'headturn',
                            'pila': pila_nb
                        }
                        print('=============================')
                        print('Request : %s' % URL)
                        print('Data : %s' % data)
                        print('=============================')
                        requests.post('%s/emotion' % URL, data=data)
            else:
                pass
        else:
            time_alarm_turn = 0
            request_turn = True


        # Alert when concentre
        if ratio20 < RATIO_EYEBROW_FOCUS:
            time_alarm_focus += 1
            if time_alarm_focus >= 5:
                cv2.putText(frame, "Concentre !", (10, 360), FONT, 0.7, (0, 0, 255), 2)
                if request_focus:
                    request_focus = False
                    if args['no_request']:
                        print('===============================')
                        print('No request !')
                        print('Emotion : concentre')
                        print('Pila : %s' % pila_nb)
                        print('===============================')
                    else:
                        data = {
                            'emotion': 'concentre',
                            'pila': pila_nb
                        }
                        print('=============================')
                        print('Request : %s' % URL)
                        print('Data : %s' % data)
                        print('=============================')
                        requests.post('%s/emotion' % URL, data=data)
            else:
                pass
        else:
            time_alarm_focus = 0
            request_focus = True
        
        cv2.putText(frame, "Count surpris : %s" % time_alarm_surpris, (10, 120), FONT, 0.7, (0, 0, 0), 2)
        cv2.putText(frame, "Count head turn : %s" % time_alarm_turn, (10, 150), FONT, 0.7, (0, 0, 0), 2)
        cv2.putText(frame, "Count concentre : %s" % time_alarm_focus, (10, 180), FONT, 0.7, (0, 0, 0), 2)


    # Show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
 
    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
 
# Cleanup
cv2.destroyAllWindows()
vs.stop()
