# @Author  : lightXu
# @File    : tesseract.py
from subprocess import Popen, PIPE, STDOUT
import os

import time

import pytesseract
from ocr import preprocess, radon_transform
import cv2
import numpy as np


def tesseract_by_cmd(img_path, save_txt_path):
    current_path = os.path.dirname(os.path.realpath(__file__))
    command = "tesseract {} {} --psm 1 --oem 3 -l chi_sim+equ+eng".format(img_path, save_txt_path)
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=current_path)
    output, errors = p.communicate()
    if errors:
        print(errors)
    print('{} by cmd done!'.format(img_path))


def tesseract_by_py(ocr_lang, img_path, save_txt_path):
    img = preprocess.preprocess(img_path, show=False)
    # img = radon_transform.radon_cv(img)
    txt = pytesseract.image_to_string(img, lang=ocr_lang, boxes=False, output_type='string')
    with open(save_txt_path, 'w', encoding='utf-8') as writter:
        writter.writelines(txt)
    print('{} by python done!'.format(img_path))


def tesseract_boxes_by_py(ocr_lang, img_path):
    img = preprocess.preprocess(img_path, show=False)
    # img = radon_transform.radon_cv(img)
    txt = pytesseract.image_to_boxes(img, lang=ocr_lang, output_type='dict')
    h, w = img.shape
    char_list = txt['char']
    left = txt['left']
    bottom = [(h - top) for top in txt['top']]
    right = txt['right']
    top = [(h-bottom) for bottom in txt['bottom']]
    mtx = np.matrix([left, top, right, bottom])

    res_dict = {'chars': char_list, 'coordinates': mtx.tolist()}
    print(res_dict)
    return char_list, mtx.tolist()


if __name__ == '__main__':
    img_path = r'C:\Users\Administrator\Desktop\sheet\correct\info_title_flppy.jpg'
    lang = 'chi_sim+eng'
    t1 = time.time()
    tesseract_boxes_by_py(lang, img_path)
    t2 = time.time()
    print(t2-t1)
