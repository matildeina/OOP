import sys #memproses eksekusi program
import cv2 #memproses gambar di python
from PyQt5 import QtCore, QtWidgets #modul unutk GUI
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi #memuat file ui yang kt buat di designer

class ShowImage(QMainWindow): #menaampilkan gambar
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('untitled.ui', self)
        self.Image = None 
        self.pushButton.clicked.connect(self.fungsi)

    def fungsi(self):
        print('Hello Word')

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('A2')
window.show()
sys.exit(app.exec_())