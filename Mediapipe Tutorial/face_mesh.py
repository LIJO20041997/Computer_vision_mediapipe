import cv2 
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
pTime = 0

while True:
    success, img = cap.read()
    CTime = time.time()
    fps = 1-(CTime-pTime)
    pTime = CTime
    cv2.imshow("image",img)
    cv2.waitKey(1) 
