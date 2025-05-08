import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class ShowImage(QMainWindow):
    def _init_(self):
        super(ShowImage, self)._init_()
        loadUi('untitled.ui', self)
        self.Image = None  # menyimpan gambar asli
        
 
        self.pushButton.clicked.connect(self.fungsi)  # Tombol untuk memuat gambar
        self.button_prosesCitra.clicked.connect(self.grayscale)  # Tombol untuk grayscale
        self.actionOperasi_Pencerahan.triggered.connect(self.brightness)  # Brightness
        self.actionSimple_Contrast.triggered.connect(self.contrast)  # Contrast
        self.actionContrast_Streching.triggered.connect(self.contrastStreching)  # Contrast Stretching
        self.actionNegative.triggered.connect(self.negative) # tombol untukk negatif
        self.actionBiner.triggered.connect(self.biner) # tombol untuk biner

    @pyqtSlot()
    def fungsi(self):
        """Memuat dan menampilkan gambar asli"""
        self.Image = cv2.imread('paru-paru.png')

        if self.Image is None:
            print("Gagal memuat gambar! Periksa kembali lokasi file.")
            return

        self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2RGB)  # Konversi ke RGB
        self.displayImage(self.Image, self.label_proses)  
    def grayscale(self):
        """Mengubah gambar ke grayscale dan menampilkannya"""
        if self.Image is None:
            print("Belum ada gambar yang dimuat!")
            return 

        gray = cv2.cvtColor(self.Image, cv2.COLOR_RGB2GRAY)  # Gunakan OpenCV untuk grayscale
        self.displayImage(gray, self.label_proses)  
    def brightness(self):
        """Meningkatkan kecerahan gambar dan menampilkannya"""
        if self.Image is None:
            print("Belum ada gambar yang dimuat!")
            return

        bright_value = 50  # Nilai brightness 
        bright = cv2.convertScaleAbs(self.Image, alpha=1, beta=bright_value)  
        
        self.displayImage(bright, self.label_proses) 
    def contrast(self):
        """Meningkatkan kontras gambar dan menampilkannya"""
        if self.Image is None:
            print("Belum ada gambar yang dimuat!")
            return

        contrast_value = 1.7  # Nilai peningkatan kontras (bisa diubah)
        contrast = cv2.convertScaleAbs(self.Image, alpha=contrast_value, beta=0)  
        
        self.displayImage(contrast, self.label_proses)  # Tampilkan gambar dengan kontras lebih tinggi di label

    def negative(self):
        if self.Image is None:
            print("Belum ada gambar yang dimuat!!")
            return
        if len(self.Image.shape) == 3: # jika gambar memiliki 3 dimensi
            negative_img =255 - self.Image 
        else:
            negative_img = 255 - cv2.cvtColor(self.Image, cv2.COLOR_RGB2GRAY) # konversi ke grayscla dulu

        self.displayImage(negative_img, self.label_proses)

    def biner(self):
        if self.Image is None:
            print("Belum ada gmabr yang dimuat!!")
            return
        
        # Konversi ke grayscale
        gray = cv2.cvtColor(self.Image, cv2.COLOR_RGB2GRAY)

        # Ambil tinggi dan lebar gambar
        height, width = gray.shape

        # Looping setiap pixel dan ubah sesuai aturan binerisasi
        for i in range(height):
            for j in range(width):
                pixel_value = gray[i, j] # Mengambil nilai piksel p

                if pixel_value == 90:
                    gray[i, j] = 0 # ubah ke hitam
                elif pixel_value < 90:
                    gray[i, j] = 1 # abu
                else:  
                    gray[i, j] = 255 # putih 

        # Tampilkan hasil biner di label_2
        self.displayImage(gray, self.label_proses)

    def contrastStreching(self):
        """Melakukan perenggangan kontras pada gambar"""
        if self.Image is None:
            print("Belum ada gambar yang dimuat!")
            return

        # Konversi ke grayscale jika masih RGB
        if len(self.Image.shape) == 3:
            gray = cv2.cvtColor(self.Image, cv2.COLOR_RGB2GRAY)
        else:
            gray = self.Image.copy()

        # Cari nilai minimum dan maksimum dari gambar
        r_min = np.min(gray)
        r_max = np.max(gray)

        # Terapkan contrast stretching 
        stretched = ((gray - r_min) / (r_max - r_min)) * 255
        stretched = np.clip(stretched, 0, 255).astype(np.uint8)  # rentang 0-255

        # Tampilkan hasil di label_2
        self.displayImage(stretched, self.label_proses)

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
window.setWindowTitle('A8(2)')
window.show()
sys.exit(app.exec_())