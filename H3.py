import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QImage


class ResultWindow(QtWidgets.QWidget):
    def __init__(self, img):
        super(ResultWindow, self).__init__()
        self.setWindowTitle("Hasil Identifikasi Bentuk")
        self.setGeometry(200, 200, img.shape[1], img.shape[0])

        # Tampilkan gambar ke window ini
        self.label = QtWidgets.QLabel(self)
        self.display_image(img)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)


class ContourIdentifier(QtWidgets.QMainWindow):
    def __init__(self):
        super(ContourIdentifier, self).__init__()
        uic.loadUi("GUI3.ui", self)

        self.button_LoadCitra.clicked.connect(self.load_image)
        self.actionH_3_Identifikasi_Bentuk_Contour.triggered.connect(self.identify_shapes)
        self.image = None

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.image = cv2.imread(file_name)
            self.display_image(self.image)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

    def identify_shapes(self):
        if self.image is None:
            print("Gambar belum dimuat.")
            return

        # Proses identifikasi bentuk
        img_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

        # Ekstrak kontur dengan cv2.RETR_LIST dan cv2.CHAIN_APPROX_NONE
        contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        img_result = self.image.copy()

        for contour in contours:
            # Menentukan epsilon untuk approximasi poligon
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Menentukan titik tengah kontur
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                continue

            shape = "Unknown"
            sides = len(approx)

            # Menentukan bentuk berdasarkan jumlah sisi poligon
            if sides == 3:
                shape = "Segitiga"
            elif sides == 4:
                # Menentukan apakah poligon dengan 4 sisi adalah persegi atau persegi panjang
                x, y, w, h = cv2.boundingRect(approx)
                ratio = float(w) / h
                shape = "Persegi" if 0.95 < ratio < 1.05 else "Persegi Panjang"
            elif sides == 5:
                shape = "Segi Lima"
            elif sides == 10:
                shape = "Bintang"
            else:
                shape = "Lingkaran"

            # Gambar kontur dan nama bentuk di gambar
            cv2.drawContours(img_result, [approx], 0, (0, 255, 0), 2)
            cv2.putText(img_result, shape, (cx - 30, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Tampilkan hasil di window terpisah
        self.result_window = ResultWindow(img_result)
        self.result_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ContourIdentifier()
    window.setWindowTitle("Identifikasi Bentuk - Contour Detection")
    window.show()
    sys.exit(app.exec_())
