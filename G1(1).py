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
        self.originalImage = None

        self.button_LoadCitra.clicked.connect(self.fungsi)
        # self.button_Reset.clicked.connect(self.resetImage)

        self.actionDilasi.triggered.connect(self.dilasiClicked)
        self.actionErosi.triggered.connect(self.erosiClicked)
        self.actionOpening.triggered.connect(self.openingClicked)
        self.actionClosing.triggered.connect(self.closingClicked)

    def fungsi(self):
        self.Image = cv2.imread('paru-paru.png')
        if self.Image is None:
            QMessageBox.critical(self, "Error", "Gagal memuat gambar!")
            return
        self.originalImage = self.Image.copy()
        self.displayImage(self.Image, self.label)

    def resetImage(self):
        if self.originalImage is not None:
            self.Image = self.originalImage.copy()
            self.displayImage(self.Image, self.label)

    def erosiClicked(self):
        result = self.applyMorphology(cv2.MORPH_ERODE)
        if result is not None:
            self.displayImage(result, self.label_2)

    def dilasiClicked(self):
        result = self.applyMorphology(cv2.MORPH_DILATE)
        if result is not None:
            self.displayImage(result, self.label_2)

    def openingClicked(self):
        result = self.applyMorphology(cv2.MORPH_OPEN)
        if result is not None:
            self.displayImage(result, self.label_2)

    def closingClicked(self):
        result = self.applyMorphology(cv2.MORPH_CLOSE)
        if result is not None:
            self.displayImage(result, self.label_2)

    def applyMorphology(self, morph_type):
        if self.Image is None:
            QMessageBox.warning(self, "Peringatan", "Silakan muat citra terlebih dahulu!")
            return None

        try:
            img_copy = self.Image.copy()
            if len(img_copy.shape) == 3:
                img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
            _, threshold = cv2.threshold(img_copy, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            strel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
            result = cv2.morphologyEx(threshold, morph_type, strel, iterations=1)
            return result
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {str(e)}")
            return None

    def displayImage(self, img, target_label):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        qimg = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        if len(img.shape) == 3:
            qimg = qimg.rgbSwapped()

        target_label.setPixmap(QPixmap.fromImage(qimg))
        target_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        target_label.setScaledContents(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ShowImage()
    window.setWindowTitle('Pengolahan Citra Morfologi')
    window.show()
    sys.exit(app.exec_())