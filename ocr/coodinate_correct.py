# @Author  : lightXu
# @File    : coodinate_correct.py
# @Time    : 2018/11/15 0015 下午 16:29
import cv2
import numpy as np
import matplotlib.pyplot as plt


def correct(path):
    img = cv2.imread(path)
    rows, cols, ch = img.shape

    pts1 = np.float32([[694, 3333], [939, 3369], [2336, 3348], [2580, 3385]])  # 原始坐标
    pts2 = np.float32([[748, 3377], [993, 3411], [2390, 3375], [2634, 3410]])  # 校正后的坐标

    M = cv2.getPerspectiveTransform(pts1, pts2)

    dst = cv2.warpPerspective(img, M, (3161, 3508), borderValue=(255, 255, 255))

    plt.subplot(121), plt.imshow(img), plt.title('Input')
    plt.subplot(122), plt.imshow(dst), plt.title('Output')
    plt.show()
    save_path = path.replace('.jpg', '_correct.jpg')
    cv2.imwrite(save_path, dst)


def correct1(path):
    img = cv2.imread(path)
    rows, cols, ch = img.shape

    pts1 = np.float32([[694, 3333], [939, 3369], [2336, 3348]])
    pts2 = np.float32([[748, 3377], [993, 3411], [2390, 3375]])

    M = cv2.getAffineTransform(pts1, pts2)

    dst = cv2.warpAffine(img, M, (3161, 3508), borderValue=(255, 255, 255))

    plt.subplot(121), plt.imshow(img), plt.title('Input')
    plt.subplot(122), plt.imshow(dst), plt.title('Output')
    plt.show()
    save_path = path.replace('.jpg', '_correct.jpg')
    cv2.imwrite(save_path, dst)


if __name__ == '__main__':
    path0 = r'C:\Users\Administrator\Desktop\test\0000x2.jpg'
    correct1(path0)
