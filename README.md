# HandTracking
(computer vision) HandTracking Machine을 만들면서 opencv와 mediapipe를 사용해본다.  
참고 강의  
youtube   
Murtaze's Workshop - Robotics and AI 채널  
[Hand Tracking 30 FPS using CPU | OpenCV Python (2021) | Computer Vision]( https://www.youtube.com/watch?v=NZde8Xt78Iw&t=10s)
___

## 비디오 캡쳐
```python
import cv2

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 27:  # esc로 종료
      break
```
- cap = cv2.VideoCapture(0) : 비디오 캡쳐를 위한 객체를 생성 (0은 웹캠 번호)
- success, img = cap.read() : success는 비디오를 제대로 읽었는지 여부, img는 프레임

---
## mediapipe의 Hands
```python
mpHands = mp.solutions.hands
hands = mpHands.Hands()
```
- mediapipe의 Hands 솔루션을 사용 [참고](https://google.github.io/mediapipe/solutions/hands.html)
- 파라미터 : static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5
___
## 랜드마킹
```python
(...)
while True:
    success, img = cap.read()
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 27:  # esc로 종료
      break
```
- imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) : BGR이미지를 RGB이미지로 변환하여 변수에 저장
- results = hands.process(imgRGB) : 손을 탐지하여 랜드마킹한 결과를 반환
hands.py
> Processes an RGB image and returns the hand landmarks and handedness of each detected hand
```python
print(results.multi_hand_landmarks)
```
- 손 인식 여부를 확인 / results의 반환값 확인  
hands.py
> A NamedTuple object with two fields: a "multi_hand_landmarks" field that
      contains the hand landmarks on each detected hand and a "multi_handedness"
      field that contains the handedness (left v.s. right hand) of the detected
      hand.
___
## mediapipe의 drawing_utils
```python
mpDraw = mp.solutions.drawing_utils
```
mediapipe의 drawing_utils를 사용하기 위한 객체를 생성
```python
if results.multi_hand_landmarks:
    for handLms in results.multi_hand_landmarks:
        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
```
- results.multi_hand_landmarks의 랜드마크 정보를 img위에 그린다.  
- mpHands.HAND_CONNECTIONS : 기존의 점만 찍히던 img위에 연결선을 추가 할 수 있다.

<img src="https://user-images.githubusercontent.com/57162448/131523401-59ea8a2d-fee3-4ed5-a0c6-dab5625f3ccf.png" height="150" ><img height="150" src="https://user-images.githubusercontent.com/57162448/131523436-21c4100b-2f1a-4044-b725-a798dcee36e5.png"><img height="150" src="https://user-images.githubusercontent.com/57162448/131523460-a02aa764-49fb-4953-ab29-e07ba83bbe86.png">
___
## FPS (frames per second)
```python
(...)
pTime = 0  # previous
cTime = 0  # current
(...)
cTime = time.time()
fps = 1/(cTime-pTime)
pTime = cTime
cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3,
           (255,0,255),3)
(...)
```
cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)  
: [참고](https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/)
매개변수 순서대로 img, text, org, fontFace, fontScale, color, thickness, lineType, bottomLeftOrigin  
|매개변수|의미|
|---|---|
|org|bottom-left corner 위치|
|fontFace|font type. CV2.FONT_XXX|
|bottomLeftOrigin|org 옵션 True 좌측하단 False 좌측 상단|
___
## 각 랜드마크 값 가져오기
```python
(...)
if results.multi_hand_landmarks:
    h, w, c = img.shape
    for handLms in results.multi_hand_landmarks:
        for id, lm in enumerate(handLms.landmark):
            # print(id, lm)
            cx, cy = int(lm.x*w), int(lm.y*h)
            # print(id, cx, cy)
            if id == 4:  # 예시로 id값 4 (엄지손가락 끝)에 원을 그리도록 함
                cv2.circle(img, (cx,cy), 15, (255,0,255),cv2.FILLED)
        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
```
- for id, lm in enumerate(handLms.landmark): 각 마디의 landmark 정보를 하나씩 꺼낸다.
- h, w, c = img.shape : lm.x와 lm.y가 좌표를 화면 내의 비율 값으로 나타내므로 화면 너비 높이값이 필요하다.
- cx, cy = int(lm.x*w), int(lm.y*h) : 비율값이 아닌 x, y좌표 값을 수치로 변형하여 저장한다.
> 참고한 강의에서는 이중 for문 안에 h, w, c = img.shape 를 위치 하였으나 이 코드를 밖으로 빼내면 중복되는 계산을 제거할 수 있을것이라고 생각하여 수정하였다.

___
## 모듈화
___
## 결과
<img src="https://user-images.githubusercontent.com/57162448/131673513-3b10718f-7bb5-47fe-a435-b31a5c683fb1.gif" height="150" >
