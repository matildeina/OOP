import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore, uic

class ThresholdApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI3.ui", self)

        self.image = None

        # Koneksi tombol untuk load gambar
        self.button_LoadCitra.clicked.connect(self.load_image)

        # Menambahkan aksi untuk Adaptive Thresholding dan Otsu Thresholding
        self.actionMean_Thresholding.triggered.connect(self.apply_adaptive_mean)
        self.actionGaussian_Thresholding.triggered.connect(self.apply_adaptive_gaussian)
        self.actionOtsu_Thresholding.triggered.connect(self.apply_otsu)

    def load_image(self):
        """Memuat gambar dan menampilkannya di QLabel"""
        try:
            # Buka dialog file untuk memilih gambar
            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Pilih Gambar", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
            if file_path:
                # Membaca gambar dalam format grayscale
                self.image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                if self.image is not None:
                    # Menampilkan gambar di QLabel
                    self.display_image(self.image, self.label)
                    print("Gambar berhasil dimuat:", file_path)
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Gagal membaca gambar!")
                    print("Gagal membaca gambar:", file_path)
            else:
                print("Pemilihan file dibatalkan.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))
            print("Error:", e)

    def display_image(self, img, label_target):
        """Menampilkan citra grayscale ke QLabel"""
        height, width = img.shape
        bytes_per_line = width
        q_img = QtGui.QImage(img.data, width, height, bytes_per_line, QtGui.QImage.Format_Grayscale8)
        pixmap = QtGui.QPixmap.fromImage(q_img)
        label_target.setPixmap(pixmap.scaled(label_target.width(), label_target.height(), QtCore.Qt.KeepAspectRatio))

    def apply_adaptive_mean(self):
        """Terapkan Adaptive Thresholding dengan metode Mean."""
        if self.image is None:
            QtWidgets.QMessageBox.warning(self, "Error", "Harap muat citra terlebih dahulu!")
            return

        # Terapkan adaptive mean thresholding
        thresholded = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2) 
        # Tampilkan hasilnya di QLabel
        self.display_image(thresholded, self.label_2)

    def apply_adaptive_gaussian(self):
        """Terapkan Adaptive Thresholding dengan metode Gaussian."""
        if self.image is None:
            QtWidgets.QMessageBox.warning(self, "Error", "Harap muat citra terlebih dahulu!")
            return

        # Terapkan adaptive gaussian thresholding
        thresholded = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # Tampilkan hasilnya di QLabel
        self.display_image(thresholded, self.label_2)

    def apply_otsu(self):
        """Terapkan Otsu Thresholding."""
        if self.image is None:
            QtWidgets.QMessageBox.warning(self, "Error", "Harap muat citra terlebih dahulu!")
            return

        # Terapkan otsu thresholding
        _, thresholded = cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Tampilkan hasilnya di QLabel
        self.display_image(thresholded, self.label_2)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ThresholdApp()
    window.show()
    sys.exit(app.exec_())
