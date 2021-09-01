import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm


pTime = 0  # previous
cTime = 0  # current
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img,draw=False)
    lmList = detector.findPosition(img, draw=False)
    if lmList:
        print(lmList)
    # fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 27:  # esc로 종료
        break