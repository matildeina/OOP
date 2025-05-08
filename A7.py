# 1. load image
# 2. ubah ke grayscale
# 3. ambil tinggi dan lebar dari gambar
# 4. melakukan nested looping, looping pertama itu berdasarkan tinggi, looping kedua berdasarkan lebar gambar
# 5. ambil array item menggunakan img.item(i, j) berdasarkan looping, fungsinya itu untuk mengambil setiap pixel
# 6. lalu kurangi menggunakan match.ceil contohnya math.ceil(255 - img.item(i, )
# 7. lalu mengubah nilai array menggunakn img.itemset()
# 8. kemudian tampilkan image

import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('untitled.ui', self)
        self.Image = None
        self.pushButton.clicked.connect(self.fungsi)
        self.button_prosesCitra.clicked.connect(self.grayscale)
        self.actionOperasi_Pencerahan.triggered.connect(self.brightness)
        self.actionSimple_Contrast.triggered.connect(self.contrast)
        self.action.Contrast_Streching.triggered.connect(self.contrastStreching)

    def fungsi(self):
        self.Image = cv2.imread('gambar.jpg')
        self.displayImage()

    def grayscale(self):
        H, W = self.Image.shape[:2]
        gray = np.zeros((H, W), np.uint8)
        for i in range(H):
            for j in range (W):
                gray[i, j] = np.clip(0.299 * self.Image[i, j, 0] +
                                     0.587 * self.Image[i, j, 1] +
                                     0.114 * self.Image[i, j, 2], 0, 255)
            self.Image = gray
            self.displayImage(2)

    def brightness(self):
        # Agar menghindari error ketika melewati prosess Grayscalling citra
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass

        H, W = self.Image.shape[:2]
        brightness = 80
        for i in range(H):
            for j in range (W):
                a = self.Image.item(i, j)
                b = np.clip(a + brightness, 0, 255)

                self.Image.itemset((i, j), b)
                
            self.displayImage(1)

    def contrast(self):
        # Agar menghindari error ketika melewati prosess Grayscalling citra
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass

        H, W = self.Image.shape[:2]
        contrast = 1.7
        for i in range(H):
            for j in range (W):
                a = self.Image.item(i, j)
                b = np.clip(a *contrast, 0, 255)

                self.Image.itemset((i, j), b)
                
            self.displayImage(1)

    def contrastStreching(self):
        # Agar menghindari error ketika melewati prosess Grayscalling citra
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass

        H, W = self.Image.shape[:2]
        minV = np.min(self.image)
        maxV = np.max(self.Image)


        for i in range(H):
            for j in range (W):
                a = self.Image.item(i, j)
                b = float(a - minV) / (maxV - minV) * 255

                self.Image.itemset((i, j), b)
    
    def negative(self):
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass
        
        H, W = self.Image.shape[:2]
        for i in range(H):
            for j in range(W):
                a = self.Image.item(i, j)
                b = 255 - a
                self.Image.itemset((i, j), b)
        self.displayImage()

    def displayImage(self):
        qformat = QImage.Format_Indexed8

        if len(self.Image.shape)==3:
            if(self.Image.shape[2])==4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGBA8888

        img = QImage(self.Image, self.Image.shape[1], self.Image.shape[0],
                     self.Image.strides[0], qformat)
        
        img = img.rgbSwapped()

        self.label.setPixmap(QPixmap.fromImage(img))

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('A7')
window.show()
sys.exit(app.exec_())