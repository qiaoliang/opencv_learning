import cv2 as cv
import numpy as np

image = cv.imread("./qrcode.png")
qrcode_1 = image[746:960,400:627]
qrcode_2 = image[268:453,141:324]

cv.imshow("qrcode_1", qrcode_1)
cv.waitKey()
cv.imshow("qrcode_2", qrcode_2)
cv.waitKey()
cv.destroyAllWindows()

# 扣出倾斜的二维码，并将其转正
# 假设你已经知道斜放正方形的轮廓
contour = np.array([[193, 582],[51, 742], [218, 891], [361, 730]], dtype=np.int32)

# 创建一个与原始图像大小相同的掩模图像
mask = np.zeros_like(image)

# 在掩模上绘制已知轮廓
cv.drawContours(mask, [contour], 0, (255, 255, 255), thickness=cv.FILLED)

# 使用掩模提取原图中的斜放正方形区域
result = cv.bitwise_and(image, mask)

# 现在，'result' 包含了从原始图像中裁剪出的斜放正方形，但还没有转成正方形

# 找到斜放正方形的四个顶点
rect = cv.minAreaRect(contour)
box_float = cv.boxPoints(rect) # 返回值是浮点数

# 计算目标正方形的边长（最长边或最短边的长度）
side_length = max(rect[1])  # 或者使用 min(rect[1])，取决于你的需求

# 定义目标正方形的四个对应顶点
dst_points = np.array([[0, 0], [side_length, 0], [side_length, side_length], [0, side_length]], dtype=np.float32)
M = cv.getPerspectiveTransform(box_float, dst_points)

# 执行透视变换，将斜放正方形转成正方形
result = cv.warpPerspective(result, M, (int(side_length), int(side_length)))

cv.imshow("result", result)
cv.waitKey()
cv.destroyAllWindows()
