import math
import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi
from matplotlib import pyplot as plt


class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('untitled.ui', self)
        self.image = None

        self.pushButton.clicked.connect(self.loadClicked)
        self.actionHistogram_Grayscale.triggered.connect(self.loadClicked)
        self.actionNegative_2.triggered.connect(self.negative)

        self.actionBiner_2.triggered.connect(self.biner)
        self.actionHistogram_Grayscale.triggered.connect(self.grayHistogram)
        self.actionHistogram_RGB.triggered.connect(self.RGBHistogram)
        self.actionHistogram_Equalization.triggered.connect(self.EqualHistogram)

        # Operasi Geometri
        self.actionTranslasi.triggered.connect(self.translasi)
        self.action90_Derajat.triggered.connect(self.rotasi90derajat)

    @pyqtSlot()
    def loadClicked(self):
        self.loadImage("paru-paru.png")

    def loadImage(self, flname):
        self.image = cv2.imread(flname)
        self.displayImage()

    def displayImage(self, windows=1):
        qformat = QImage.Format_Indexed8
        if len(self.image.shape) == 3: 
            if (self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(
            self.image,
            self.image.shape[1],
            self.image.shape[0],
            self.image.strides[0],
            qformat,
        )
        img = img.rgbSwapped()

        if windows == 1:
            self.label_Citra.setPixmap(QPixmap.fromImage(img))
            self.label_Citra.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label_Citra.setScaledContents(True)
        elif windows == 2:
            self.label_proses.setPixmap(QPixmap.fromImage(img))
            self.label_proses.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
            )
            self.label_proses.setScaledContents(True)

    def grayHistogram(self):
        h, w = self.image.shape[:2]
        gray = np.zeros((h, w), np.uint8)
        for i in range(h):
            for j in range(w):
                gray[i, j] = np.clip(
                    0.299 * self.image[i, j, 0]
                    + 0.587 * self.image[i, j, 1]
                    + 0.114 * self.image[i, j, 2],
                    0,
                    255,
                )
        self.image = gray
        print(self.image)
        self.displayImage(2)
        plt.hist(self.image.ravel(), 255, [0, 255])
        plt.show()

    def biner(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        h, w = img.shape[:2]
        for i in np.arange(h):
            for j in np.arange(w):
                a = img.item(i, j)
                img.itemset((i, j), 0 if a < 180 else 255)
        self.image = img
        self.displayImage(2)

    def negative(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        h, w = img.shape[:2]
        for i in np.arange(h):
            for j in np.arange(w):
                a = img.item(i, j)
                b = math.ceil(255 - a)
                img.itemset((i, j), b)
        self.image = img
        print(self.image)
        self.displayImage(2)

    def RGBHistogram(self):
        color = ("b", "g", "r") #ini adalah tuple, tuple adalah koleksi yang disimpan dan tidak dapat diubah
        for i, col in enumerate(color): #membuat perulangan berdasarkan warna
            histo = cv2.calcHist([self.image], [i], None, [256], [0, 256]) #menghitung histrogram dari sekumpulan koleksi/array
            plt.plot(histo, color=col) #melakukan plotting kepada histogram
            plt.xlim([0, 256]) #mengatur batas sumbu x
        self.displayImage(2) #menampilkan image di windwo kedua
        plt.show() #melakukan visualisasi dari hasil histogram

    def EqualHistogram(self):
        hist, bins = np.histogram(self.image.flatten(), 256, [0, 256]) #nuat mengubah image array nya menjadi 1 dimensi, np nya untuk hitung histogram dari gambar tsb
        cdf = hist.cumsum() #menghitung jumlah komulatif elemen array pada sumbu tertentu
        cdf_normalized = cdf * hist.max() / cdf.max() #melakukan normalisasi
        cdf_m = np.ma.masked_equal(cdf, 0) #menutupi array yang sama dengan nilai yang diberikan
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min()) #retang perhitungannnya
        cdf = np.ma.filled(cdf_m, 0).astype("uint8") #buat mengisi nilai array nya dengan nilai scalar
        self.image = cdf[self.image] #array imagenya diganti dengan nilai array komulatif
        self.displayImage(2) #menampilkan image di windwo kedua

        plt.plot(cdf_normalized, color="b") #melakukan plotting sesuai dengan normalisasi
        plt.hist(self.image.flatten(), 256, [0, 256], color="r") #membuat histogram sesuai dengan arry gambar 
        plt.xlim([0, 256]) #mengatur batas sumbu x nya
        plt.legend(("cdf", "histogram"), loc="upper left") 
        plt.show()

    def translasi(self):
        h, w = self.image.shape[:2]
        quarter_h, quarter_w = h/4, w/4
        T = np.float32([[1, 0, quarter_w], [0, 1, quarter_h]])
        img = cv2.warpAffine(self.image, T, (w, h))

        self.image = img
        self.displayImage(2)

    def rotasi90derajat(self):
        self.rotasi(90)

    def rotasi(self, degree):
        h, w = self.image.shape[:2]
        rotationMatrix = cv2.getRotationMatrix2D((w / 2, h / 2), degree, 0.7)
        cos = np.abs(rotationMatrix[0, 0])
        sin = np.abs(rotationMatrix[0, 1])
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        rotationMatrix[0, 2] += (nW / 2) - w /2
        rotationMatrix[1, 2] += (nH / 2) - h /2

        rot_image = cv2.warpAffine(self.image, rotationMatrix, (h, w))
        self.image = rot_image
        self.displayImage(2)

    def grayClicked(self):
        h, w = self.image.shape[:2]
        gray = np.zeros((h, w), np.uint8)
        for i in range(h):
            for j in range(w):
                gray[i, j] = np.clip(
                    0.299 * self.image[i, j, 0]
                    + 0.587 * self.image[i, j, 1]
                    + 0.114 * self.image[i, j, 2],
                    0,
                    255,
                )
        self.image = gray
        print(self.image)
        self.displayImage(2)

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('B2')
window.show()
sys.exit(app.exec_())