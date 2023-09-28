# Description: 图片相似度判断
# pip install skimage, matplotlib, numpy, cv2

from skimage.meature import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

def mse(imageA,imageB):
    err = np.sum((imageA.astype("float")-imageB.astype("float"))**2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def compare_image(imageA, imageB, title):
    m = mse(imageA,imageB)
    s = ssim(imageA,imageB)
    fig = plt.figure(title)
    return (m,s)

# 读取两个图片
image_a = cv2.imread("qrcode.png")
image_b = cv2.imread("qrcode.png")

# resizing images looking into zero patting
image_a = cv2.resize(image_a,(10000,10000))
image_b = cv2.resize(image_b,(10000,10000))

# converting to grayscale

image_a = cf2.cvtColor(image_a,cv2.CORLOR_BGR2GRAY)
image_b = cv2.cvtColor(image_b,cv2.CORLOR_BGR2GRAY)

m,s = compare_image(image_a,image_b,"just a test")
print("相似度 = %.2f",s)