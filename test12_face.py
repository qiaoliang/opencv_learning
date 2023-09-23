import cv2
from cvzone.FaceMeshModule import FaceMeshDetector

cap = cv2.VideoCapture(0)  # 0 for webcam, 0 for external camera
detector = FaceMeshDetector(maxFaces=1) # maxFaces=1 means only one face is detected, it will be faster.

while True:

    # 检查目前帧数是否等于全部的帧数 保持视频不断地重复而不关闭
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    # 用cvzone中的detector对面部特定点进行定位
    img, faces = detector.findFaceMesh(img)

    # 视频太大的话 可以将视频resize成目标大小
    # img = cv2.resize(img, (640, 360))
    cv2.imshow('image', img)
    key = cv2.waitKey(1)  # 每一帧的时间间隔。单位为毫秒。如果为零，则表示播放速度为最大值（每一帧之间没有间隔）。
        # 如果按下 'q' 键，退出程序
    if key == ord('q'):
        break

# 释放摄像头和关闭窗口
cap.release()
cv2.destroyAllWindows()