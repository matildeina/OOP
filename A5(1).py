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
        self.pushButton.clicked.connect(self.fungsi)
        self.button_prosesCitra.clicked.connect(self.grayscale)
        self.actionOperasi_Pencerahan.triggered.connect(self.brightness)
        self.actionSimple_Contrast.triggered.connect(self.contrast)

    def fungsi(self):
        self.Image = cv2.imread('gambar(1).jpg')
        if self.Image is None:
            print("Error: Gambar tidak ditemukan!")
            return
        self.displayImage()

    def grayscale(self):
        if self.Image is None:
            print("Error: Gambar belum dimuat!")
            return
        
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
        if self.Image is None:
            print("Error: Gambar belum dimuat!")
            return

        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass

        brightness = 80
        self.Image = np.clip(self.Image + brightness, 0, 255).astype(np.uint8)
        self.displayImage()

    def contrast(self):
        if self.Image is None:
            print("Error: Gambar belum dimuat!")
            return

        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass

        contrast = 1.7
        self.Image = np.clip(self.Image * contrast, 0, 255).astype(np.uint8)
        self.displayImage()

    def displayImage(self):
        if self.Image is None:
            print("Error: Tidak ada gambar yang ditampilkan!")
            return

        if len(self.Image.shape) == 2:
            qformat = QImage.Format_Grayscale8
        else:
            qformat = QImage.Format_RGB888

        img = QImage(self.Image.data, self.Image.shape[1], self.Image.shape[0], self.Image.strides[0], qformat)
        img = img.rgbSwapped()

        self.label_Citra.setPixmap(QPixmap.fromImage(img))

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('A5')
window.show()
sys.exit(app.exec_())