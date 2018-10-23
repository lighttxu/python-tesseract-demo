# @Author  : lightXu
# @File    : utils.py
import os

import cv2
import numpy as np
import xml.etree.cElementTree as ET


def resize_by_percent(im, percent):
    """
    :param im:
    :param percent:
    :return: resize_img

    interpolation - 插值方法。共有5种：
    1)INTER_NEAREST - 最近邻插值法
    2)INTER_LINEAR - 双线性插值法（默认）
    3)INTER_AREA - 基于局部像素的重采样（resampling using pixel area relation）。
      对于图像抽取（image decimation）来说，这可能是一个更好的方法。但如果是放大图像时，它和最近邻法的效果类似。
    4)INTER_CUBIC - 基于4x4像素邻域的3次插值法
    5)INTER_LANCZOS4 - 基于8x8像素邻域的Lanczos插值
    """

    height, width = im.shape[:2]
    new_x = int(width * percent)
    new_y = int(height * percent)

    res = cv2.resize(im, (new_x, new_y), interpolation=cv2.INTER_AREA)

    return res


def resize_by_fixed_size(im, new_x, new_y):
    """
    :param im:
    :param percent:
    :return: resize_img

    interpolation - 插值方法。共有5种：
    1)INTER_NEAREST - 最近邻插值法
    2)INTER_LINEAR - 双线性插值法（默认）
    3)INTER_AREA - 基于局部像素的重采样（resampling using pixel area relation）。
      对于图像抽取（image decimation）来说，这可能是一个更好的方法。但如果是放大图像时，它和最近邻法的效果类似。
    4)INTER_CUBIC - 基于4x4像素邻域的3次插值法
    5)INTER_LANCZOS4 - 基于8x8像素邻域的Lanczos插值
    """
    res = cv2.resize(im, (new_x, new_y), interpolation=cv2.INTER_AREA)

    return res


def rgb2binary(im):
    gray_img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    _ret, thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh_img
