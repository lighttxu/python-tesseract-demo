# python-tesseract-demo

这个demo简单实现了使用tesseract-4.0[https://github.com/tesseract-ocr/tesseract/wiki]进行ocr识别的功能；
简体中文的识别需要预先下载chi_sim[https://github.com/tesseract-ocr/tesseract/wiki/Data-Files]。
  
* ```tesseract_by_cmd```直接调用命令行功能对图像进行识别；
* ```tesseract_by_cmd```先对图像进行了预处理，后调用pytesseract[https://pypi.org/project/pytesseract/]对图像进行识别。

TODO：根据坐标信息进行图像分割。