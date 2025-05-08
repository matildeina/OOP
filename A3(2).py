import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class ShowImage(QMainWindow):
    def _init_(self):
        super(ShowImage, self)._init_()
        loadUi('untitled.ui', self)
        self.Image = None  # Variabel untuk menyimpan gambar asli
        self.pushButton.clicked.connect(self.fungsi)  # Tombol untuk memuat gambar
        self.button_prosesCitra.clicked.connect(self.grayscale)  # Tombol untuk grayscale

    def fungsi(self):
        """Memuat dan menampilkan gambar asli"""
        self.Image = cv2.imread('paru-paru.png')

        if self.Image is None:
            print("Gagal memuat gambar! Periksa kembali lokasi file.")
            return

        self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2RGB)  # Konversi ke RGB
        self.displayImage(self.Image, self.label)  # Tampilkan gambar asli di label_asli

    def grayscale(self):
        """Mengubah gambar ke grayscale dan menampilkannya"""
        if self.Image is None:
            print("Belum ada gambar yang dimuat!")
            return

        gray = cv2.cvtColor(self.Image, cv2.COLOR_RGB2GRAY)  # Gunakan OpenCV untuk grayscale
        self.displayImage(gray, self.label_2)  # Tampilkan grayscale di label_gray

    def displayImage(self, img, label):
        """Menampilkan gambar di QLabel yang ditentukan"""
        if img is None:
            return

        # Pilih format yang benar untuk grayscale atau RGB
        qformat = QImage.Format_Indexed8 if len(img.shape) == 2 else QImage.Format_RGB888

        image = QImage(img.data, img.shape[1], img.shape[0], 
                       img.strides[0], qformat)

        label.setPixmap(QPixmap.fromImage(image))  # Tampilkan di QLabel yang diberikan

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('A3(2)')
window.show()
sys.exit(app.exec_())