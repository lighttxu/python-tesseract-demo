# @Author  : lightXu
# @File    : tesseract.py
from subprocess import Popen, PIPE, STDOUT
import os

import time

import pytesseract
from ocr import preprocess, radon_transform, utils
import cv2
import numpy as np
import xml.etree.cElementTree as ET


def tesseract_by_cmd(img_path, save_txt_path):
    current_path = os.path.dirname(os.path.realpath(__file__))
    command = "tesseract {} {} --psm 0 --oem 1 -l chi_sim+equ+eng".format(img_path, save_txt_path)
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
    matrix = []
    for i, ele in enumerate(left):
        matrix.append((ele, top[i], right[i], bottom[i]))

    res_dict = {'chars': char_list, 'coordinates': matrix}
    return res_dict


def tesseract_osd_by_py(img_path):
    config = '--oem 3 -l chi_sim+equ+eng'
    img = preprocess.preprocess(img_path, show=False)
    text = pytesseract.image_to_osd(img, config=config)
    print(text)


def gen_xml(lang, img_path):
    res_dict = tesseract_boxes_by_py(lang, img_path)
    box_list = res_dict['coordinates']
    tree = ET.parse(r'./000000-template.xml')  # xml tree
    for index_num, exam_bbox in enumerate(box_list):
        tree = utils.create_xml('{}'.format(res_dict['chars'][index_num]), tree,
                          exam_bbox[0], exam_bbox[1], exam_bbox[2], exam_bbox[3])
    # print(exam_items_bbox)
    tree.write(img_path.replace('.png', '.xml'))


if __name__ == '__main__':
    img_path0 = r'C:\Users\Administrator\Desktop\test\20180719004308818_0001.jpg'
    save_path0 = img_path0.replace('.jpg', '')
    lang = 'chi_sim+equ+eng'
    t1 = time.time()
    # res = tesseract_boxes_by_py(lang, img_path)
    # gen_xml(lang, img_path)

    # tesseract_by_py(lang, img_path, img_path.replace('.png', '.txt'))
    t2 = time.time()
    print(t2-t1)

    tesseract_by_cmd(img_path0, save_path0)
    tesseract_osd_by_py(img_path0)
