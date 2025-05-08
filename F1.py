import sys
import os
import cv2
import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class EdgeDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("E-F.ui", self)  # Load desain dari E-F.ui

        self.Image = None

        # Connect tombol
        self.button_LoadCitra.clicked.connect(self.load_image)
        self.actionSobel.triggered.connect(self.Sobel)



    def load_image(self):
        self.Image = cv2.imread("paru-paru.png")
        if self.Image is None:
            print("Gagal memuat gambar paru-paru.png")
            return

        rgb_image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.imgLabel.width(), self.imgLabel.height(), Qt.KeepAspectRatio)
        self.imgLabel.setPixmap(QPixmap.fromImage(p))

    def Sobel(self):
        if self.Image is None:
            print("Gambar belum dimuat!")
            return

        img_gray = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)

        # Operator Sobel
        Sx = np.array([[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]])
        Sy = np.array([[-1, -2, -1],
                       [0, 0, 0],
                       [1, 2, 1]])

        img_x = cv2.filter2D(img_gray, -1, Sx)
        img_y = cv2.filter2D(img_gray, -1, Sy)

        img_out = np.sqrt(img_x ** 2 + img_y ** 2)
        img_out = (img_out / np.max(img_out)) * 255
        img_out = img_out.astype(np.uint8)

        # Tampilkan hasil ke hasilLabel
        img_display = cv2.cvtColor(img_out, cv2.COLOR_GRAY2RGB)
        h, w, ch = img_display.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(img_display.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.hasilLabel.width(), self.hasilLabel.height(), Qt.KeepAspectRatio)
        self.hasilLabel.setPixmap(QPixmap.fromImage(p))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EdgeDetectionApp()
    window.show()
    sys.exit(app.exec_())
