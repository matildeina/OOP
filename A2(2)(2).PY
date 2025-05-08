import sys
import cv2
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

    def fungsi(self):
        self.Image = cv2.imread('gambar.jpg')

        if self.Image is None:
            print("Error: Gambar tidak ditemukan atau tidak bisa dibuka!")
            return

        print(f"Gambar dimensi: {self.Image.shape}")
        self.displayImage()

    def displayImage(self):
        height, width, channel = self.Image.shape
        bytes_per_line = 3 * width  # 3 karena RGB memiliki 3 channel

        if channel == 3:
            qformat = QImage.Format_RGB888
        elif channel == 4:
            qformat = QImage.Format_RGBA8888
        else:
            qformat = QImage.Format_Indexed8

        img = QImage(self.Image.data, width, height, bytes_per_line, qformat)
        img = img.rgbSwapped()  # Mengubah format BGR ke RGB

        self.label_Citra.setPixmap(QPixmap.fromImage(img))
        self.label_Citra.setScaledContents(True)  # Agar gambar menyesuaikan label

# Menjalankan aplikasi PyQt5
app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('A2(2)')
window.show()
sys.exit(app.exec_())