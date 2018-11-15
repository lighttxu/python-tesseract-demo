# @Author  : lightXu
# @File    : box.py
# @Time    : 2018/11/15 0015 下午 15:51
import xml.etree.cElementTree as ET


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


def draw_box(txt, mtx, xml_save_path):
    tree = ET.parse(r'.\000000-template.xml')
    for i, ele in enumerate(txt):
        name = ele
        xmin = mtx[0][i]
        ymin = mtx[1][i]
        xmax = mtx[2][i]
        ymax = mtx[3][i]
        tree = create_xml(name, tree, xmin, ymin, xmax, ymax)
    tree.write(xml_save_path)
