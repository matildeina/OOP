import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap 
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('untitled.ui', self)
        self.Image = None

        # Koneksi tombol ke fungsi
        self.pushButton.clicked.connect(self.fungsi)
        self.button_prosesCitra.clicked.connect(self.grayscale)
        self.button_prosesCitra.clicked.connect(self.processPixels)  # Tambahkan tombol di UI
        self.actionOperasi_Pencerahan.triggered.connect(self.brightness)
        self.actionSimple_Contrast.triggered.connect(self.contrast)
        self.actionContrast_Streching.triggered.connect(self.contrastStreching)

    def fungsi(self):
        self.Image = cv2.imread('paru-paru.png')
        self.displayImage()

    def grayscale(self):
        H, W = self.Image.shape[:2]
        gray = np.zeros((H, W), np.uint8)

        for i in range(H):
            for j in range(W):
                gray[i, j] = np.clip(0.299 * self.Image[i, j, 0] +
                                     0.587 * self.Image[i, j, 1] +
                                     0.114 * self.Image[i, j, 2], 0, 255)
        
        self.Image = gray 
        self.displayImage()

    def brightness(self):
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass

        brightness = 80
        self.Image = np.clip(self.Image + brightness, 0, 255).astype(np.uint8)

        self.displayImage(1)

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
        minV = np.min(self.Image)
        maxV = np.max(self.Image)

        for i in range(H):
            for j in range(W):
                a = self.Image.item(i, j)
                b = float(a - minV) / (maxV - minV) * 255
                self.Image.itemset((i, j), b)

        self.displayImage()

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

    def binary(self):
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass
        
        _, self.Image = cv2.threshold(self.Image, 127, 255, cv2.THRESH_BINARY)
        self.displayImage()

    def processPixels(self):
        """Fungsi untuk mengubah nilai piksel berdasarkan kondisi yang diberikan"""
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass

        H, W = self.Image.shape[:2]

        for i in range(H):
            for j in range(W):
                pixel = self.Image.item(i, j)
                if pixel == 127:
                    new_pixel = 0
                elif pixel < 127:
                    new_pixel = 1
                else:
                    new_pixel = 255
                self.Image.itemset((i, j), new_pixel)

        self.displayImage()

    def displayImage(self):
        """Menampilkan citra di label pada UI"""
        qformat = QImage.Format_Indexed8

        if len(self.Image.shape) == 3:
            if self.Image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(self.Image, self.Image.shape[1], self.Image.shape[0],
                     self.Image.strides[0], qformat)
        
        img = img.rgbSwapped()
        self.label_Citra.setPixmap(QPixmap.fromImage(img))

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('A8 - Image Processing')
window.show()
sys.exit(app.exec_())