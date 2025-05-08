import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets
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

    def fungsi(self):
        self.Image = cv2.imread('gambar(1).jpg')
        self.displayImage()

    def grayscale(self):
        if self.Image is None:
            return

        gray = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        self.Image = gray
        self.displayImage()

    def brightness(self):
        if self.Image is None:
            return

        # Jika gambar masih dalam format BGR, ubah ke grayscale
        if len(self.Image.shape) == 3:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)

        brightness = 80
        self.Image = np.clip(self.Image + brightness, 0, 255).astype(np.uint8)

        self.displayImage()

    def displayImage(self):
        if self.Image is None:
            return

        if len(self.Image.shape) == 2:  # Grayscale
            qformat = QImage.Format_Grayscale8
        else:  # Warna (BGR ke RGB)
            qformat = QImage.Format_RGB888
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2RGB)

        img = QImage(self.Image, self.Image.shape[1], self.Image.shape[0],
                     self.Image.strides[0], qformat)

        self.label_Citra.setPixmap(QPixmap.fromImage(img))
        self.label_Citra.setScaledContents(True)

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('A4')
window.show()
sys.exit(app.exec_())