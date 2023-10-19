import cv2
from cvzone.FaceDetectionModule import FaceDetector
import numpy as np
from gpiozero import Servo
from time import sleep


cap = cv2.VideoCapture(0)
ws, hs = 1920,1080
cap.set(3, ws)
cap.set(4, hs)

if not cap.isOpened():
    print("FATAL | Camera non détecté")
    exit()

xAxisRotate = Servo(5)
yAxisRotate = Servo(6)

x = np.array([0, 1920])
interpX_l = np.array([1, -1])

y = np.array([0, 1080])
interpY_l = np.array([1, -1])

detector = FaceDetector()
try:
    while True:
        success, img = cap.read()
        img, bboxs = detector.findFaces(img, draw=False)

        if bboxs:
            # Recupérer les coordonées

            fx, fy = bboxs[0]["center"][0], bboxs[0]["center"][1]
            pos = [fx, fy]
            xAxisRotate.value = np.interp(fx, (x.min(), x.max()), interpX_l) # Transforme les coordonées prop>
            yAxisRotate.value = np.interp(fy, (y.min(), y.max()), interpY_l) # Transforme les coordonées prop>
            print("INFO | Coords (x,y) = " + "(" + str(xAxisRotate.value) + "," + str(yAxisRotate.value) +")")
            cv2.circle(img, (fx, fy), 80, (0, 0, 255), 2)
            cv2.putText(img, str(pos), (fx+15, fy-15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2 )
            cv2.line(img, (0, fy), (ws, fy), (0, 0, 0), 2)  # x line
            cv2.line(img, (fx, hs), (fx, 0), (0, 0, 0), 2)  # y line
            cv2.circle(img, (fx, fy), 15, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, "SUIVI", (850, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            sleep(0.1)

        else:
            print("INFO | Pas de visage")
            xAxisRotate.mid() # Stepper à 0
            yAxisRotate.mid() # Stepper à 0

            cv2.putText(img, "R.A.S.", (880, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            cv2.circle(img, (640, 360), 80, (0, 0, 255), 2)
            cv2.circle(img, (640, 360), 15, (0, 0, 255), cv2.FILLED)

            cv2.line(img, (0, 360), (ws, 360), (0, 0, 0), 2)  # x line
            cv2.line(img, (640, hs), (640, 0), (0, 0, 0), 2)  # y line

    cv2.imshow("TETE DE ROBOT - Tracking", img)
    print("INFO | Window updated")
    cv2.waitKey()
except KeyboardInterrupt:
    xAxisRotate.mid()
    yAxisRotate.mid()
    print("\nProgramme quittée (Ctrl+C)")
