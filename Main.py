import cv2
import mediapipe as mp
import time
import math


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


desired_fps = 10
cap = cv2.VideoCapture(0)
pTime = 0


mppose = mp.solutions.pose
pose = mppose.Pose()
mpDraw = mp.solutions.drawing_utils



while True:

    start_time = time.time()

    success, img = cap.read()
    imgRBG = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = pose.process(imgRBG)
    if results.pose_landmarks:
            mpDraw.draw_landmarks(img,results.pose_landmarks, mppose.POSE_CONNECTIONS)
            for id , lm in enumerate(results.pose_landmarks.landmark):
                  h, w, c = img.shape
                  if id == 32 or id == 31:
                        cx1, cy1 = int(lm.x*w), int(lm.y*h)
                        cv2.circle(img,(cx1,cy1),10,(0,0,0),cv2.FILLED)

                        d = calculate_distance(cx1, cy1, cx2, cy2)
                        h = round(d*0.5)
                        
                  if id == 6:
                        cx2, cy2 = int(lm.x*w), int(lm.y*h)
                        cy2 += 20
                        cv2.circle(img,(cx2,cy2),10,(0,0,0),cv2.FILLED)



    CTime = time.time()
    fps = 1-(CTime-pTime)
    pTime = CTime
    img = cv2.resize(img , (700,500))   
    cv2.putText(img, f'Height: {h} cm',(10,70),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
    cv2.putText(img,f'FPS: {fps}',(10,40),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)               
    cv2.imshow("image",img)
    if cv2.waitKey(1) == ord("q"):
        break



cap.release()
cv2.destroyAllWindows()