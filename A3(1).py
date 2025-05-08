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

    def fungsi(self):
        self.Image = cv2.imread('gambar.jpg')
        self.displayImage()

    
    def grayscale(self):
        H, W = self.Image.shape[:2]
        gray = np.zeros((H, W), np.uint8)
    
        for i in range(H):
            for j in range(W):
                gray[i, j] = np.clip(0.299 * self.Image[i, j, 2] +  # R
                                 0.587 * self.Image[i, j, 1] +  # G
                                 0.114 * self.Image[i, j, 0], 0, 255)  # B
    
        self.Image = gray  # Simpan hasil grayscale ke atribut Image
        self.displayImage()  # Tampilkan hasilnya

    def displayImage(self):
        if len(self.Image.shape) == 2:  # Gambar grayscale
            qformat = QImage.Format_Indexed8
        else:
            qformat = QImage.Format_RGB888

        img = QImage(self.Image, self.Image.shape[1], self.Image.shape[0],
                    self.Image.strides[0], qformat)

        img = img.rgbSwapped() if len(self.Image.shape) == 3 else img

        self.label_Citra.setPixmap(QPixmap.fromImage(img))

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('A3')
window.show()
sys.exit(app.exec_())