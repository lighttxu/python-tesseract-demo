# @Author  : lightXu
# @File    : preprocess.py
import cv2
import numpy as np


def preprocess(picture, show=False):
    scale = 0
    dilate = 1
    blur = 3

    # 预处理图像
    img = cv2.imread(picture)

    # rescale the image
    if scale != 0:
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    if dilate != 0:
        kernel = np.ones((dilate, dilate), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

    # Apply blur to smooth out the edges
    if blur != 0:
        img = cv2.GaussianBlur(img, (blur, blur), 0)

    # Apply threshold to get image with only b&w (binarization)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    if show:
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return img
