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
            print("INFO | Coords (x,y) = " + "(" + str(fx) + "," + str(fy) +")")

        else:
            print("INFO | Pas de visage")
            xAxisRotate.mid() # Stepper à 0
            yAxisRotate.mid() # Stepper à 0
except KeyboardInterrupt:
    xAxisRotate.mid()
    yAxisRotate.mid()
    print("\nServo réinitialisés\nProgramme quittée (Ctrl+C)")
