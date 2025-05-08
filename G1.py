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
        loadUi('GUI3.ui', self)
        self.Image = None
        self.button_LoadCitra.clicked.connect(self.fungsi)
        self.actionDilasi.triggered.connect(self.dilasiClicked)
        self.actionErosi.triggered.connect(self.erosiClicked)
        self.actionOpening.triggered.connect(self.openingClicked)
        self.actionClosing.triggered.connect(self.closingClicked)

    def erosiClicked(self): #menipiskan objek yang ada pada citra
        img = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY) #mengubah citra ke grayscale
        _, threshold = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) #thresholding
        strel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5)) #membuat struktur elemen
        imgh = cv2.erode(threshold, strel, iterations=1) #erosi
        self.Image = imgh
        self.displayImage(2)

    def dilasiClicked(self): #memperbesar objek yang ada pada citra
        img = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY) #mengubah citra ke grayscale
        _, threshold = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) #thresholding
        strel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5)) #membuat struktur elemen
        imgh = cv2.dilate(threshold, strel, iterations=1) #dilasi
        self.Image = imgh #menyimpan hasil dilasi ke dalam variabel Image
        self.displayImage(2) #menampilkan citra hasil dilasi

    def openingClicked(self): #menghilangkan noise pada citra
        img = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        strel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
        imgh = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, strel, iterations=1)
        self.Image = imgh
        self.displayImage(2)

    def closingClicked(self): #menutup celah pada citra
        img = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) 
        strel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
        imgh = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, strel, iterations=1)
        self.Image = imgh
        self.displayImage(2)

    def fungsi(self):
        self.Image = cv2.imread('paru-paru.png')
        self.displayImage(1)

    # def grayscale(self):
    #     H, W = self.Image.shape[:2]
    #     gray = np.zeros((H, W), np.uint8)
    #     for i in range(H):
    #         for j in range(W):
    #             gray[i, j] = np.clip(0.299 * self.Image[i, j, 0] +
    #                                  0.597 * self.Image[i, j, 1] +
    #                                  0.114 * self.Image[i, j, 2], 0, 255)

    #     self.Image = gray
    #     self.displayImage(2)

    def displayImage(self, windows=1):
        qformat = QImage.Format_Indexed8

        if windows == 1:
            if len(self.Image.shape) == 3: #3 channel
                if self.Image.shape[2] == 4: 
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888

            img = QImage(self.Image, self.Image.shape[1], self.Image.shape[0],
                         self.Image.strides[0], qformat)
            img = img.rgbSwapped()
            self.label.setPixmap(QPixmap.fromImage(img))
            self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label.setScaledContents(True)

        elif windows == 2:
            img = QImage(self.Image, self.Image.shape[1], self.Image.shape[0],
                         self.Image.strides[0], qformat)
            self.label_2.setPixmap(QPixmap.fromImage(img))
            self.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label_2.setScaledContents(True)


app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('G1')
window.show()
sys.exit(app.exec_())
