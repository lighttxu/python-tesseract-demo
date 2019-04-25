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
    :param new_y: y轴像素
    :param new_x: x轴像素
    :param im:
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


def resize_by_radio(im):
    """
    :param im:
    :return: resize_img

    interpolation - 插值方法。共有5种：
    1)INTER_NEAREST - 最近邻插值法
    2)INTER_LINEAR - 双线性插值法（默认）
    3)INTER_AREA - 基于局部像素的重采样（resampling using pixel area relation）。
      对于图像抽取（image decimation）来说，这可能是一个更好的方法。但如果是放大图像时，它和最近邻法的效果类似。
    4)INTER_CUBIC - 基于4x4像素邻域的3次插值法
    5)INTER_LANCZOS4 - 基于8x8像素邻域的Lanczos插值
    """
    # res = cv2.resize(im, (new_x, new_y), interpolation=cv2.INTER_AREA)

    longer = 750
    shorter = 500

    im_shape = im.shape
    im_size_min = np.min(im_shape[0:2])
    im_size_max = np.max(im_shape[0:2])

    im_scale = float(shorter) / float(im_size_min)
    # Prevent the biggest axis from being more than MAX_SIZE
    if np.round(im_scale * im_size_max) > longer:
        im_scale = float(longer) / float(im_size_max)
    res = cv2.resize(im, None, None, fx=im_scale, fy=im_scale,
                     interpolation=cv2.INTER_AREA)

    return res


def rgb2binary(im):
    gray_img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    _ret, thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh_img


def create_xml(obj_name, tree, xmin, ymin, xmax, ymax):
    root = tree.getroot()

    pobject = ET.SubElement(root, 'object', {})
    pname = ET.SubElement(pobject, 'name')
    pname.text = obj_name
    ppose = ET.SubElement(pobject, 'pose')
    ppose.text = 'Unspecified'
    ptruncated = ET.SubElement(pobject, 'truncated')
    ptruncated.text = '0'
    pdifficult = ET.SubElement(pobject, 'difficult')
    pdifficult.text = '0'
    # add bndbox
    pbndbox = ET.SubElement(pobject, 'bndbox')
    pxmin = ET.SubElement(pbndbox, 'xmin')
    pxmin.text = str(xmin)

    pymin = ET.SubElement(pbndbox, 'ymin')
    pymin.text = str(ymin)

    pxmax = ET.SubElement(pbndbox, 'xmax')
    pxmax.text = str(xmax)

    pymax = ET.SubElement(pbndbox, 'ymax')
    pymax.text = str(ymax)

    return tree


if __name__ == '__main__':

    img_path = r'C:\Users\Administrator\Desktop\2018-11-12\new\600.jpg'
    img = cv2.imread(img_path)
    img = resize_by_fixed_size(img, '', '')
