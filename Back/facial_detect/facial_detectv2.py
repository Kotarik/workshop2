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

# Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
    help="path to facial landmark predictor")
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
face = {
    "right_eyebrow": {
        "pts": (17, 22),
        "pts_list": {}
    },
    "left_eyebrow": {
        "pts": (22, 27),
        "pts_list": {}
    },
    "nose": {
        "pts": (27, 31),
        "pts_list": {}
    },
    "eyebrow": {
    },
    "right_eye": {
        "pts": (36, 42),
        "pts_list": {}
    },
    "left_eye": {
        "pts": (42, 48),
        "pts_list": {}
    },
}

#Pila number
pilanumber = 1

# Ratio eyebrow / nose
EYEBROW_RATIO = 0.52
# Ratio eye
EYE_RATIO = 0.31
FRAME_NB= 6
EYEBROW_RATIO_CONCENTRE = 2.8

dureeAlerteTete = 0
dureeAlerteConcentre = 0

# Eye part
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Counter for surprise
counter = 0

# Degrees for head turn
TURN_HEAD = 13

def eye_aspect_ratio(eye):
    # Distances between vertical eye landmarks
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Distance between horizontal eye landmark
    C = dist.euclidean(eye[0], eye[3])

    # Eye aspect ratio
    ear = (A + B) / (2.0 * C)

    return ear

def dist_points(pts_a, pts_b):
    # Calcul distance between two points
    return sqrt((pts_b[0] - pts_a[0]) ** 2 + (pts_b[1] - pts_a[1]) ** 2)

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

        # 
        dist2829= round(dist.euclidean(shape[28],shape[29]))
        dist2228= round(dist.euclidean(shape[22], shape[28]))
        dist2028= round(dist.euclidean(shape[20], shape[28]))

        # frame = face_utils.visualize_facial_landmarks(frame, shape)

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
                cv2.putText(frame, name, (x, y), font, 0.5, (255,255,255), 1)

            # Print all points in face
            for k,v in face[name]['pts_list'].items():
                (x, y) = v
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                font = cv2.FONT_HERSHEY_PLAIN
                cv2.putText(frame, str(k), (x, y), font, 1, (255,255,255), 1)

        # Trace line between barycenter eyebrow
        bc1 = face['right_eyebrow']['barycentre']
        bc2 = face['left_eyebrow']['barycentre']
        cv2.line(frame, bc1, bc2, (255, 0, 0), 1)
        
        # Center between eyebrow line
        pt1 = face['right_eyebrow']['barycentre']
        pt2 = face['left_eyebrow']['barycentre']
        x_eyebrow = int(round((pt1[0] + pt2[0]) / 2))
        y_eyebrow = int(round((pt1[1] + pt2[1]) / 2))
        face['eyebrow']['centre'] = (x_eyebrow, y_eyebrow)
        eyebrow = face['eyebrow']['centre']
        cv2.circle(frame, eyebrow, 1, (0, 255, 0), -1)
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(frame, 'eyebrow', eyebrow, font, 1, (255,255,255), 1)

        # Trace line between barycenter nose and center eyebrow line
        nose = face['nose']['barycentre']
        cv2.line(frame, nose, eyebrow, (255, 0, 0), 1)

        dist_nose = int(round(sqrt((nose[0] - eyebrow[0]) ** 2 + (nose[1] - eyebrow[1]) ** 2)))
        dist_eyebrow = int(round(sqrt((bc2[0] - bc1[0]) ** 2 + (bc2[1] - bc2[1]) ** 2)))
        ratio_eyebrow = round(dist_nose / dist_eyebrow, 5)
        cv2.putText(frame, "Distance nose : %s " % str(dist_nose), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Distance eyebrow : %s " % str(dist_eyebrow), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Ratio : %s " % str(ratio_eyebrow), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Distance 20/28 %s " % str(dist2028), (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Distance 22/28 %s " % str(dist2228), (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Distance 28/29 %s " % str(dist2829), (10, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


        # Calculate EAR
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Calculate ratio
        ratio20 = round(dist2028 / dist2829, 5)
        ratio22 = round(dist2228 / dist2829, 5)
        cv2.putText(frame, "ratio20 : %s" % str(ratio20), (10, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "ratio22 : %s" % str(ratio22), (10, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Alert when surprise
        if ratio_eyebrow >= EYEBROW_RATIO and ear >= EYE_RATIO:
            counter += 1
            if counter >= FRAME_NB:
                cv2.putText(frame, "Surprise !", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                # requests.post('http://127.0.0.1:5000/emotion', data={'emotion':'surpris', 'pila': pilanumber})
                print("{'emotion':'surpris', 'pila': pilanumber}")
        else:
            counter = 0

        # Print counter
        cv2.putText(frame, "Counter : %s" % counter, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Calculate angle for turn head
        a = dist_points(face['left_eyebrow']['barycentre'], face['eyebrow']['centre'])
        b = dist_points(face['eyebrow']['centre'], face['nose']['barycentre'])
        c = dist_points(face['nose']['barycentre'], face['left_eyebrow']['barycentre'])

        angle = degrees(acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)))
        cv2.putText(frame, "Angle : %s" % angle, (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Alert when head turn
        if angle < 90 - TURN_HEAD or angle > 90 + TURN_HEAD:
            dureeAlerteTete += 1
            cv2.putText(frame, "Head turn ! %s" % dureeAlerteTete, (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
        else:
            dureeAlerteTete = 0
        if dureeAlerteTete == 5:
            # requests.post('http://127.0.0.1:5000/emotion', data={'emotion':'headturn', 'pila': pilanumber})
            print("{'emotion':'headturn', 'pila': pilanumber}")

        # Alert when concentre
        if ratio20 < EYEBROW_RATIO_CONCENTRE:
            dureeAlerteConcentre += 1
            cv2.putText(frame, "Concentre ! %s" % dureeAlerteConcentre, (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
        else:
            dureeAlerteConcentre = 0
        if dureeAlerteConcentre == 5:
            # requests.post('http://127.0.0.1:5000/emotion', data={'emotion':'concentre', 'pila': pilanumber})
            print("{'emotion':'concentre', 'pila': pilanumber}")

    # Show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
 
    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
 
# Cleanup
cv2.destroyAllWindows()
vs.stop()
