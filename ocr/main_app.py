# @Author  : lightXu
# @File    : main_app.py
import os
import glob2 as glob
from ocr.tesseract import tesseract_by_cmd, tesseract_by_py, tesseract_boxes_by_py
from ocr.box import draw_box


if __name__ == '__main__':
    lang = 'chi_sim+eng'

    root_dir = r'C:\Users\Administrator\Desktop\test'
    # dir_list = os.listdir(root_dir)
    dir_list = ['test']
    for dir_path in dir_list:
        img_dir0 = os.path.join(root_dir, dir_path)
        find_str = os.path.join(img_dir0, '*.jpg')
        img_path_list = glob.glob(find_str)
        for img in img_path_list:
            txt_path = img.replace('.jpg', '_cmd')
            xml_path = img.replace('.jpg', '.xml')
            # tesseract_by_cmd(img, txt_path)
            char, matrix = tesseract_boxes_by_py(lang, img, txt_path.replace('_cmd', '_py.txt'))

            draw_box(char, matrix, xml_path)
            print(xml_path)
