# @Author  : lightXu
# @File    : radon_transform.py
from skimage.transform import radon
from PIL import Image
import numpy as np
from numpy import asarray, mean, array, blackman, argmax
from numpy.fft import rfft
import matplotlib.pyplot as plt
from matplotlib.mlab import rms_flat
import cv2

from ocr.utils import resize_by_percent


def radon_demo():
    filename = 'skew-linedetection.png'

    # Load file, converting to grayscale
    I = asarray(Image.open(filename).convert('L'))
    I = I - mean(I)  # Demean; make the brightness extend above and below zero
    plt.subplot(2, 2, 1)
    plt.imshow(I)

    # Do the radon transform and display the result
    sinogram = radon(I)

    plt.subplot(2, 2, 2)
    plt.imshow(sinogram.T, aspect='auto')
    plt.gray()

    # Find the RMS value of each row and find "busiest" rotation,
    # where the transform is lined up perfectly with the alternating dark
    # text and white lines
    r = array([rms_flat(line) for line in sinogram.transpose()])
    rotation = argmax(r)
    print('Rotation: {:.2f} degrees'.format(90 - rotation))
    plt.axhline(rotation, color='r')

    # Plot the busy row
    row = sinogram[:, rotation]
    N = len(row)
    plt.subplot(2, 2, 3)
    plt.plot(row)

    # Take spectrum of busy row and find line spacing
    window = blackman(N)
    spectrum = rfft(row * window)
    plt.plot(row * window)
    frequency = argmax(abs(spectrum))
    line_spacing = N / frequency  # pixels
    print('Line spacing: {:.2f} pixels'.format(line_spacing))

    plt.subplot(2, 2, 4)
    plt.plot(abs(spectrum))
    plt.axvline(frequency, color='r')
    plt.yscale('log')
    plt.show()


def radon_ski(image):
    """ Long time consuming, Strong generalization ability, high accuracy"""
    img_np = resize_by_percent(asarray(image), 0.8)
    if len(img_np.shape) == 3:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    img_np_mean = img_np - mean(img_np)
    sinogram = radon(img_np_mean, circle=True)
    r = array([rms_flat(line) for line in sinogram.transpose()])
    rotation = 90 - argmax(r)
    print('radon', rotation)

    def rotate(image, angle, center=None, scale=1.0):
        # 获取图像尺寸
        (h, w) = image.shape[:2]

        # 若未指定旋转中心，则将图像中心设为旋转中心
        if center is None:
            center = (w / 2, h / 2)

        # 执行旋转
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(image, M, (w, h), borderValue=(255, 255, 255))

        # 返回旋转后的图像
        return rotated

    if 0 < abs(rotation) <= 7:
        img_correct = rotate(image, rotation)
        cv2.imwrite('test.jpg', img_correct)

        return img_correct
    else:
        return image


def rotate_cv(image):
    """ not Long time consuming, not Strong generalization ability, not high accuracy, more super parameters"""
    img_np = resize_by_percent(asarray(image), 0.8)  # 500, 700
    if len(img_np.shape) == 3:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    canny_image = cv2.Canny(img_np, 0, 255, apertureSize=3)
    # cv2.imshow('canny', canny_image)
    # cv2.waitKey(10)
    lines = cv2.HoughLinesP(canny_image, 1, np.pi / 180, 160, minLineLength=500, maxLineGap=65)
    # lines = cv2.HoughLines(canny_image, 1, np.pi / 180, 160, max_theta=30, min_theta=0)

    # 寻找长度最长的线
    distance = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        dis = np.sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))
        distance.append(dis)
    max_dis_index = distance.index(max(distance))
    max_line = lines[max_dis_index]
    x1, y1, x2, y2 = max_line[0]

    # 获取旋转角度
    angle = cv2.fastAtan2((y2 - y1), (x2 - x1))
    print('cv: ', angle)

    if 0.5 <= 1 <= 7:  # 因为识别误差问题，根据实际情况设置旋转阈值
        centerpoint = (image.shape[1] / 2, image.shape[0] / 2)
        rotate_mat = cv2.getRotationMatrix2D(centerpoint, -1, 1.0)  # 获取旋转矩阵
        correct_image = cv2.warpAffine(image, rotate_mat, (image.shape[1], image.shape[0]),
                                       borderValue=(255, 255, 255))

        # cv2.imshow('test', resize_by_percent(correct_image, 0.1))
        # cv2.waitKey(10)
        cv2.imwrite('test.jpg', correct_image)
        return correct_image
    else:
        return image


if __name__ == '__main__':
    import time
    img_path = r'C:\Users\Administrator\Desktop\11142018043727\Page0001_2.jpg'
    img = cv2.imread(img_path)

    # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    time1 = time.time()
    # rotate_cv(img)
    time2 = time.time()
    print(time2-time1)

    radon_ski(img)
    time3 = time.time()
    print(time3-time2)



