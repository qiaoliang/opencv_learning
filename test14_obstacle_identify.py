import cv2 as cv

# 定义结构元素(内核矩阵)的形状和大小
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))

# 打开摄像头
capture = cv.VideoCapture(0)

# 初始化摄像头读取状态和帧
ok, frame = capture.read()

# 定义颜色范围（HSV颜色空间）用于绿色颜色物体的识别
# 你可以使用任何你喜欢的颜色,但是要确保HSV颜色空间的值正确,
# hsv.png 展示了HSV颜色空间的值
# 你可以使用工具HSV Color Picker来获取正确的值, 例如: https://colorpicker.me/
lower_b = (35, 43, 46)  # 绿色最低颜色值
upper_b = (77, 255, 255)  # 绿色最高颜色值

# 获取图像的高度和宽度
height, width = frame.shape[0:2]

# 计算屏幕中心位置和偏移量
screen_center = width / 2
offset = 50

while ok:
    # 将图像转换为HSV颜色空间
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # 基于颜色的物体提取
    mask = cv.inRange(hsv_frame, lower_b, upper_b) # 用于创建二进制掩码图像。它创建一个二进制图像，其中像素值在指定范围内的部分被设为白色（255），而不在范围内的部分被设为黑色（0）
    # 下面两个操作经常一起使用，以便在处理二值图像时平衡去噪和连接物体的需求。首先，开运算去除小噪声和分离物体，然后闭运算连接对象并填充空洞，以便更好地识别和分析目标物体的形状和结构。
    mask2 = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask3 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernel)

    # 找到图中所有的轮廓list
    contours, _ = cv.findContours(mask3, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # 找出面积最大的轮廓
    maxArea = 0
    maxIndex = 0
    for i, c in enumerate(contours):
        area = cv.contourArea(c)
        if area > maxArea:
            maxArea = area
            maxIndex = i

    # 绘制轮廓
    cv.drawContours(frame, contours, maxIndex, (255, 255, 0), 2)

    # 获取外切矩形和中心点坐标
    center_x = 0
    center_y = 0
    if contours:  # 检查是否有轮廓被找到
        x, y, w, h = cv.boundingRect(contours[maxIndex])
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        center_x = int(x + w / 2)
        center_y = int(y + h / 2)
        cv.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
    else:
        x, y, w, h = 0, 0, 0, 0  # 如果没有找到轮廓，将矩形和中心点的坐标设置为0

    # 简单的打印反馈数据，之后补充运动控制
    if center_x < screen_center - offset:
        print("向左转")
    elif screen_center - offset <= center_x <= screen_center + offset:
        print("保持位置")
    elif center_x > screen_center + offset:
        print("向右转")

    # 显示图像窗口
    cv.imshow("mask4", mask3)
    cv.imshow("frame", frame)

    # 等待1毫秒，然后获取下一帧
    cv.waitKey(1)
    ok, frame = capture.read()

# 释放摄像头资源
capture.release()
# 关闭所有图像窗口
cv.destroyAllWindows()
