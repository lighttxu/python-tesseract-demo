# @Author  : lightXu
# @File    : tesseract.py
from subprocess import Popen, PIPE, STDOUT
import os

import pytesseract
from ocr import preprocess


def tesseract_by_cmd(img_path, save_txt_path):
    current_path = os.path.dirname(os.path.realpath(__file__))
    command = "tesseract {} {} --psm 1 --oem 3 -l chi_sim+epu+eng".format(img_path, save_txt_path)
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=current_path)
    output, errors = p.communicate()
    if errors:
        print(errors)
    print('{} by cmd done!'.format(img_path))


def tesseract_by_py(img_path, save_txt_path):
    img = preprocess.preprocess(img_path,  show=False)
    txt = pytesseract.image_to_string(img, lang='chi_sim+epu+eng', boxes=False, output_type='string')
    with open(save_txt_path, 'w', encoding='utf-8') as writter:
        writter.writelines(txt)
    print('{} by python done!'.format(img_path))
