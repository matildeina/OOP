import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic

class EdgeDetectionCannyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('E-F.ui', self)

        self.Image = None

        self.button_LoadCitra.clicked.connect(self.load_image)
        self.actionCanny_2.triggered.connect(self.Canny)

    def load_image(self):
        self.Image = cv2.imread("noise.png")
        if self.Image is None:
            print("Gagal memuat gambar noise.png")
            return

        rgb_image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.imgLabel.width(), self.imgLabel.height(), Qt.KeepAspectRatio)
        self.imgLabel.setPixmap(QPixmap.fromImage(p))

    def Canny(self):
        if self.Image is None:
            print("Gambar belum dimuat!")
            return

        # === Langkah 1: Konversi ke grayscale ===
        img_gray = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)

        # === Langkah 2: Gaussian Blur ===
        img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1.4)

        # === Langkah 3: Sobel (Gradien Magnitude) ===
        grad_x = cv2.Sobel(img_blur, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(img_blur, cv2.CV_64F, 0, 1, ksize=3)

        magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
        magnitude = np.uint8(np.clip(magnitude, 0, 255))

        # Tampilkan hasil langkah 1-3 di imgLabel
        img_display1 = cv2.cvtColor(magnitude, cv2.COLOR_GRAY2RGB)
        h, w, ch = img_display1.shape
        bytes_per_line = ch * w
        convert_to_Qt_format1 = QImage(img_display1.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p1 = convert_to_Qt_format1.scaled(self.imgLabel.width(), self.imgLabel.height(), Qt.KeepAspectRatio)
        self.imgLabel.setPixmap(QPixmap.fromImage(p1))

        # === Langkah 4: Canny Edge Detection ===
        edges = cv2.Canny(img_blur, 100, 200)

        # Tampilkan hasil langkah 4 di hasilLabel
        img_display2 = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        h2, w2, ch2 = img_display2.shape
        bytes_per_line2 = ch2 * w2
        convert_to_Qt_format2 = QImage(img_display2.data, w2, h2, bytes_per_line2, QImage.Format_RGB888)
        p2 = convert_to_Qt_format2.scaled(self.hasilLabel.width(), self.hasilLabel.height(), Qt.KeepAspectRatio)
        self.hasilLabel.setPixmap(QPixmap.fromImage(p2))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EdgeDetectionCannyApp()
    window.show()
    sys.exit(app.exec_())