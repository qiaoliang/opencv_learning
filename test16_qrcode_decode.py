# Description: 二维码识别
# pip install opencv-contrib-python

import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol

image = cv.imread("./qrcode_cd20.png", cv.IMREAD_GRAYSCALE)
blur = cv.GaussianBlur(image, (5, 5), 0)
ret, bw_im = cv.threshold(blur, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)

cv.imshow("qrcode_1", bw_im)
cv.waitKey()

decoded_symbols = decode(bw_im, symbols=[ZBarSymbol.QRCODE])

# Iterate through the detected symbols
for symbol in decoded_symbols:
    symbol_type = symbol.type
    symbol_data = symbol.data
    symbol_position = symbol.polygon  # The polygon vertices of the symbol

    # Do something with the decoded data
    print(f"Type: {symbol_type}, Data: {symbol_data}")
    print(f"Position: {symbol_position}")