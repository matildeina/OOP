import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore, uic

class ThresholdApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI3.ui", self)

        self.image = None

        self.button_LoadCitra.clicked.connect(self.load_image)
        self.actionBinary.triggered.connect(self.apply_binary)
        self.actionBinary_Invers.triggered.connect(self.apply_binary_inv)
        self.action_Trunc.triggered.connect(self.apply_trunc)
        self.actionTo_Zero.triggered.connect(self.apply_tozero)
        self.actionTo_Zero_Invers.triggered.connect(self.apply_tozero_inv)

    def load_image(self):
        """Memuat dan menampilkan gambar di QLabel."""
        try:
            self.image = cv2.imread('gambar.jpg', cv2.IMREAD_GRAYSCALE)
            if self.image is not None:
                self.display_image(self.image, self.label)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Gambar tidak ditemukan!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def apply_threshold(self, thresh_type, window_title):
        if self.image is None:
            QtWidgets.QMessageBox.warning(self, "Error", "Harap muat citra terlebih dahulu!")
            return

        T = 100  # Nilai ambang
        maxval = 255 # Nilai maksimum untuk thresholding
        _, result = cv2.threshold(self.image, T, maxval, thresh_type)

        self.display_image(result, self.label_2)

    def apply_binary(self):
        self.apply_threshold(cv2.THRESH_BINARY, "Binary") #Semua piksel di atas ambang menjadi 255 (putih), di bawah ambang menjadi 0 (hitam).

    def apply_binary_inv(self):
        self.apply_threshold(cv2.THRESH_BINARY_INV, "Binary Invers") #Semua piksel di atas ambang menjadi 0 (hitam), di bawah ambang menjadi 255 (putih).

    def apply_trunc(self):
        self.apply_threshold(cv2.THRESH_TRUNC, "Trunc") #Semua piksel di atas ambang menjadi nilai ambang, di bawah ambang tetap sama.

    def apply_tozero(self):
        self.apply_threshold(cv2.THRESH_TOZERO, "To Zero") #Semua piksel di atas ambang tetap sama, di bawah ambang menjadi 0 (hitam).

    def apply_tozero_inv(self):
        self.apply_threshold(cv2.THRESH_TOZERO_INV, "To Zero Invers") #Semua piksel di atas ambang menjadi 0 (hitam), di bawah ambang tetap sama.

    def display_image(self, img, label_target):
        """Menampilkan citra grayscale ke QLabel"""
        height, width = img.shape
        bytes_per_line = width
        q_img = QtGui.QImage(img.data, width, height, bytes_per_line, QtGui.QImage.Format_Grayscale8)
        pixmap = QtGui.QPixmap.fromImage(q_img)
        label_target.setPixmap(pixmap.scaled(label_target.width(), label_target.height(), QtCore.Qt.KeepAspectRatio))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ThresholdApp()
    window.show()
    sys.exit(app.exec_())
