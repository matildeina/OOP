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
        self.actionContrast_Streching.triggered.connect(self.contrastStreching)

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
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass

        minV = np.min(self.Image)
        maxV = np.max(self.Image)

        H, W = self.Image.shape[:2]
        stretched = np.zeros((H, W), np.uint8)

        for i in range(H):
            for j in range(W):
                a = self.Image.item(i, j)
                b = (a - minV) / (maxV - minV) * 255
                stretched[i, j] = np.clip(b, 0, 255)

        self.Image = stretched.astype(np.uint8)
        self.displayImage()

    def displayImage(self):
        if len(self.Image.shape) == 2:  # Grayscale
            qformat = QImage.Format_Grayscale8
        else:
            qformat = QImage.Format_RGB888

        img = QImage(self.Image, self.Image.shape[1], self.Image.shape[0],
                 self.Image.strides[0], qformat)

        img = img.rgbSwapped()
        self.label_Citra.setPixmap(QPixmap.fromImage(img))

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('A6')
window.show()
sys.exit(app.exec_())