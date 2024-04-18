import cv2
import mediapipe as mp
import time
import math


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


desired_fps = 10
cap = cv2.VideoCapture(0)
pTime = 0

constant_height_timer = 0
constant_height_threshold = 4
previous_height = 0


mppose = mp.solutions.pose
pose = mppose.Pose()
mpDraw = mp.solutions.drawing_utils

foot_detected = False
height = 0

while True:
    start_time = time.time()
    success, img = cap.read()
    imgRBG = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = pose.process(imgRBG)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mppose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape

            if results.pose_landmarks.landmark[29].visibility > 0.5:
                    if id == 32 or id == 31:
                        cx1, cy1 = int(lm.x * w), int(lm.y * h)
                        cv2.circle(img, (cx1, cy1), 10, (0, 0, 0), cv2.FILLED)

                        d = calculate_distance(cx1, cy1, cx2, cy2)
                        height = round(d * 0.5)

                    if id == 6:
                        cx2, cy2 = int(lm.x * w), int(lm.y * h)
                        cy2 += 20
                        cv2.circle(img, (cx2, cy2), 10, (0, 0, 0), cv2.FILLED)

                    cv2.putText(img, f'Height: {height} cm', (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)


        if h == previous_height:
            constant_height_timer += 1
        if constant_height_timer >= constant_height_threshold and h < 200:
            print(f'The aproximate height is {h}')
            constant_height_timer = 0  # Reset the timer
            
        else:
            constant_height_timer = 0  # Reset the timer if height changes
            previous_height = h
            
        

    
    CTime = time.time()
    fps = 1 - (CTime - pTime)
    pTime = CTime
    img = cv2.resize(img, (700, 500))
    cv2.putText(img, f'FPS: {fps}', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    cv2.imshow("image", img)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
