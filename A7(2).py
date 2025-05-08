import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
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
            for j in range(W):
                gray[i, j] = np.clip(0.299 * self.Image[i, j, 0] +
                                     0.587 * self.Image[i, j, 1] +
                                     0.114 * self.Image[i, j, 2], 0, 255)
        self.Image = gray  # Pindahkan ke luar loop
        self.displayImage()

    def brightness(self):
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass

        H, W = self.Image.shape[:2]
        brightness = 80
        for i in range(H):
            for j in range(W):
                a = self.Image.item(i, j)
                b = np.clip(a + brightness, 0, 255)
                self.Image.itemset((i, j), b)

        self.displayImage()  # Pindahkan ke luar loop

    def contrast(self):
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass

        H, W = self.Image.shape[:2]
        contrast = 1.7
        for i in range(H):
            for j in range(W):
                a = self.Image.item(i, j)
                b = np.clip(a * contrast, 0, 255)
                self.Image.itemset((i, j), b)

        self.displayImage()

    def contrastStreching(self):
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass

        H, W = self.Image.shape[:2]
        minV = np.min(self.Image)  # Perbaikan dari self.image
        maxV = np.max(self.Image)

        for i in range(H):
            for j in range(W):
                a = self.Image.item(i, j)
                b = np.clip((a - minV) / (maxV - minV) * 255, 0, 255)
                self.Image.itemset((i, j), b)

        self.displayImage()

    def negative(self):
        self.processedImage = 255 - self.Image
        self.displayImage(isProcessed=True)

    def displayImage(self, isProcessed=False):
        qformat = QImage.Format_Grayscale8 if len(self.Image.shape) == 2 else QImage.Format_RGB888
    
        # Pilih gambar yang akan ditampilkan
        image = self.processedImage if isProcessed else self.Image

        img = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        img = img.rgbSwapped()

        if isProcessed:
            self.label_proses.setPixmap(QPixmap.fromImage(img))  # Tampilkan hasil di label_result
        else:
            self.label_Citra.setPixmap(QPixmap.fromImage(img))  # Tampilkan gambar asli

app = QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('A7')
window.show()
sys.exit(app.exec_())