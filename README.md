# HandTracking
(computer vision) HandTracking Machine을 만들면서 opencv 사용법을 알아간다.
___

## 비디오 캡쳐
```python
import cv2

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 27:
      break
```
- cap = cv2.VideoCapture(0) : 비디오 캡쳐를 위한 객체를 생성 (0은 웹캠 번호)
- success, img = cap.read() : success는 비디오를 제대로 읽었는지 여부, img는 프레임

