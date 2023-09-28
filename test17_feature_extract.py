# Description: 图片特征提取
# pip install opencv-contrib-python
import cv2

# 读取两幅图像
image1 = cv2.imread('qrcode.png', cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread('qrcode_cd20.png', cv2.IMREAD_GRAYSCALE)

# 创建SIFT检测器对象
sift = cv2.SIFT_create()

# 在两幅图像中检测关键点并计算描述符
keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

# 创建BFMatcher对象，并进行描述符匹配
bf = cv2.BFMatcher()
matches = bf.knnMatch(descriptors1, descriptors2, k=2)

# 筛选最佳匹配
good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

# 绘制匹配结果
matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# 显示匹配结果
cv2.imshow('Matches', matched_image)
cv2.waitKey(0)
cv2.destroyAllWindows()