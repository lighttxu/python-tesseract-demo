# @Author  : lightXu
# @File    : main_app.py
import os
import glob2 as glob
from ocr.tesseract import tesseract_by_cmd, tesseract_by_py


if __name__ == '__main__':
    root_dir = r'C:\Users\Administrator\Desktop\subject'
    dir_list = os.listdir(root_dir)
    # dir_list = ['math']
    for dir in dir_list:
        img_dir0 = os.path.join(root_dir, dir)
        find_str = os.path.join(img_dir0, '*.jpg')
        img_path_list = glob.glob(find_str)
        for img in img_path_list:
            txt_path = img.replace('.jpg', '_cmd')
            tesseract_by_cmd(img, txt_path)
            tesseract_by_py(img, txt_path.replace('_cmd', '_py.txt'))
