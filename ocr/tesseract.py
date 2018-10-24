# @Author  : lightXu
# @File    : tesseract.py
from subprocess import Popen, PIPE, STDOUT
import os

import pytesseract
from ocr import preprocess, radon_transform
import cv2
import numpy as np


def tesseract_by_cmd(img_path, save_txt_path):
    current_path = os.path.dirname(os.path.realpath(__file__))
    command = "tesseract {} {} --psm 1 --oem 3 -l chi_sim+epu+eng".format(img_path, save_txt_path)
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=current_path)
    output, errors = p.communicate()
    if errors:
        print(errors)
    print('{} by cmd done!'.format(img_path))


def tesseract_by_py(img_path, save_txt_path):
    img = preprocess.preprocess(img_path, show=False)
    img = radon_transform.radon_cv(img)
    txt = pytesseract.image_to_string(img, lang='chi_sim+epu+eng', boxes=False, output_type='string')
    with open(save_txt_path, 'w', encoding='utf-8') as writter:
        writter.writelines(txt)
    print('{} by python done!'.format(img_path))


def tesseract_boxes_by_py(img_path, save_txt_path):
    img = preprocess.preprocess(img_path, show=False)
    # img = radon_transform.radon_cv(img)
    txt = pytesseract.image_to_boxes(img, lang='chi_sim+epu+eng', output_type='dict')
    h, w = img.shape
    char_list = txt['char']
    left = txt['left']
    bottom = [(h-top) for top in txt['top']]
    right = txt['right']
    top = [(h - bottom) for bottom in txt['bottom']]
    mtx = np.matrix([left, top, right, bottom])

    print([txt])


if __name__ == '__main__':
    img_path = r'C:\Users\Administrator\Desktop\subject\history\01.jpg'
    tesseract_boxes_by_py(img_path, '')
