import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, uic
from matplotlib import pyplot as plt

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('E-F.ui', self)

        # Hubungkan tombol/aksi
        self.button_LoadCitra.clicked.connect(self.load_image)
        self.actionDiscreate_1.triggered.connect(self.apply_fft)

        self.img = None  # Simpan citra di sini

    def load_image(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "noise.png")
        if filename:
            self.img = cv2.imread(filename, 0)  # Baca dalam grayscale
            QtWidgets.QMessageBox.information(self, "Info", "Citra berhasil dimuat!")

    def apply_fft(self):
        if self.img is None:
            QtWidgets.QMessageBox.warning(self, "Warning", "Silakan load citra dulu!")
            return

        img = self.img

        # Fourier Transform
        dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)

        magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

        # Masking
        rows, cols = img.shape
        crow, ccol = int(rows / 2), int(cols / 2)
        mask = np.zeros((rows, cols, 2), np.uint8)
        r = 50  # radius lingkaran
        center = [crow, ccol]
        x, y = np.ogrid[:rows, :cols]
        mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= r*r
        mask[mask_area] = 1

        fshift = dft_shift * mask
        fshift_mask_mag = 20 * np.log(cv2.magnitude(fshift[:, :, 0], fshift[:, :, 1]))
        f_ishift = np.fft.ifftshift(fshift)

        img_back = cv2.idft(f_ishift)
        img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

        # Tampilkan
        fig = plt.figure(figsize=(12, 12))
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.imshow(img, cmap='gray')
        ax1.title.set_text('Input Image')
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.imshow(magnitude_spectrum, cmap='gray')
        ax2.title.set_text('FFT of Image')
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.imshow(fshift_mask_mag, cmap='gray')
        ax3.title.set_text('FFT + Mask')
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.imshow(img_back, cmap='gray')
        ax4.title.set_text('Inverse Fourier')
        plt.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
