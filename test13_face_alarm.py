import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
from playsound import playsound
cap = cv2.VideoCapture(0)  # 0 for webcam, 0 for external camera
detector = FaceMeshDetector(maxFaces=1) # maxFaces=1 means only one face is detected, it will be faster.

# 初始化状态
face_detected = False

while True:

    # 检查目前帧数是否等于全部的帧数 保持视频不断地重复而不关闭
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    # 用cvzone中的detector对面部特定点进行定位
    img, faces = detector.findFaceMesh(img)
    # 如果检测到人脸
    if faces:
        # 如果之前没有检测到人脸，播放 alert.mp3
        if not face_detected:
            playsound("alert.mp3")
            face_detected = True
            sound_playing = True
    else:
        # 如果之前检测到人脸，停止播放
        if sound_playing:
            playsound("alert.mp3", False)  # 停止声音
            sound_playing = False
            face_detected = False
    # 视频太大的话 可以将视频resize成目标大小
    img = cv2.resize(img, (640, 360))
    cv2.imshow('image', img)
    # 按下'q'键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# 释放摄像头和关闭窗口
cap.release()
cv2.destroyAllWindows()