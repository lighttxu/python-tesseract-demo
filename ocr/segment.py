# @Author  : lightXu
# @File    : segment.py
# @Time    : 2018/11/13 0013 下午 15:03
import numpy as np
import cv2

from ocr import utils


def segment_parts(im_raw, save_path):
    # randon_img = radon_rotate_ski(im_raw)
    resize_radio = 1.0
    im_resize = utils.resize_by_percent(im_raw, resize_radio)
    # gray
    gray_img = cv2.cvtColor(im_resize, cv2.COLOR_BGR2GRAY)
    ry, rx = gray_img.shape
    # 高斯
    glur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
    # 膨胀
    _ret, threshed = cv2.threshold(glur_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((glur_img.shape[0], 10), np.uint8)  # height, width
    dilation = cv2.dilate(threshed, kernel, iterations=1)

    _, cnts, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    box_list = [cv2.boundingRect(cnt) for cnt in cnts]
    img_parts_dict_list = []
    index = 1
    for box in sorted(box_list):
        x, y, w, h = box
        if x - 70 > 0:
            x = x - 70
            w = w + 70
        else:
            w = w + x
            x = 0

        area = w * h
        if area > (rx * ry) / 6:
            # print(area)
            dst = im_raw[int(y / resize_radio):int((y + h) / resize_radio),
                         int(x / resize_radio):int((x + w) / resize_radio)]
            save_path_final = save_path.replace('.jpg', '') + '_{}_{}_{}.jpg'.format(x, y, index)
            cv2.imwrite(save_path_final, dst)
            part_dict = {'img_part': save_path_final, 'x_bias': x, 'y_bias': y}
            img_parts_dict_list.append(part_dict)
            index += 1

    return img_parts_dict_list
