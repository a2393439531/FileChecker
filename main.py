# encoding=utf8
import os
import io
import time
from wand.image import Image
from wand.color import Color
from PyPDF2 import PdfFileReader, PdfFileWriter
import json
import urllib2
import base64
import string
import tkinter as tk
from tkinter import filedialog
import sys
reload(sys)
sys.setdefaultencoding('utf8')
imagepaths=[]
memo = {}


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print "---  Create Folder...  ---"
        print "---  Done  ---"

    else:
        print "---  Folder exists  ---"

def getPdfReader(filename):
    reader = memo.get(filename, None)
    if reader is None:
        reader = PdfFileReader(filename, strict=False)
        memo[filename] = reader
    return reader

def main():
    root = tk.Tk()
    root.withdraw()
    pdfpath = filedialog.askopenfilename()
    PDF_input = PdfFileReader(pdfpath)
    pagecount  = PDF_input.getNumPages()
    print("总共页数"+str(pagecount))
    baseDir = os.path.dirname(os.path.abspath(pdfpath))
    img_dir = os.path.join(baseDir, 'img')
    print pdfpath
    mkdir(img_dir)
    pdfile = getPdfReader(pdfpath)
    for pageno in range(0,pagecount-1):
        pageObj = pdfile.getPage(pageno)
        dst_pdf = PdfFileWriter()
        dst_pdf.addPage(pageObj)
        pdf_bytes = io.BytesIO()
        dst_pdf.write(pdf_bytes)
        pdf_bytes.seek(0)
        img = Image(file=pdf_bytes, resolution=120)
        img.format = 'png'
        img.compression_quality = 99
        img.background_color = Color("white")
        # 保存图片
        img_path = os.path.join(img_dir, str(pageno) + '.jpg')
        img.save(filename=img_path)
        img.destroy()
        img = None
        pdf_bytes = None
        dst_pdf = None


if __name__ == '__main__':
    main()
