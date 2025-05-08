from PyQt5 import QtWidgets, uic, QtGui
import sys
import cv2
import numpy as np


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('E-F.ui', self)

        self.button_LoadCitra.clicked.connect(self.load_image)
        self.actionDiscreate_2.triggered.connect(self.discrete_fourier_transform)

        self.img = None

        self.load_image()

    def load_image(self):
        # Fungsi untuk langsung load gambar dari file tetap
        file_name = 'noise.png'  # Nama file gambar yang sudah ditentukan

        self.img = cv2.imread(file_name, 0)  # Baca dalam mode grayscale

        if self.img is not None:
            # Tampilkan di imgLabel
            qimg = QtGui.QImage(self.img.data, self.img.shape[1], self.img.shape[0], self.img.strides[0],
                                QtGui.QImage.Format_Grayscale8)
            pixmap = QtGui.QPixmap.fromImage(qimg)
            self.imgLabel.setPixmap(
                pixmap.scaled(self.imgLabel.width(), self.imgLabel.height(), aspectRatioMode=True))
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", f"Gambar {file_name} tidak ditemukan.")

    def discrete_fourier_transform(self):
        if self.img is None:
            QtWidgets.QMessageBox.warning(self, "Warning", "Load gambar terlebih dahulu!")
            return

        img = self.img

        # DFT
        dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)

        magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

        # Masking
        rows, cols = img.shape
        crow, ccol = int(rows / 2), int(cols / 2)
        mask = np.ones((rows, cols, 2), np.uint8)
        r = 80
        center = [crow, ccol]
        x, y = np.ogrid[:rows, :cols]
        mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= r * r
        mask[mask_area] = 0

        fshift = dft_shift * mask
        fshift_mask_mag = 20 * np.log(cv2.magnitude(fshift[:, :, 0], fshift[:, :, 1]))

        f_ishift = np.fft.ifftshift(fshift)
        img_back = cv2.idft(f_ishift)
        img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

        # Tampilkan hasil pakai plt
        import matplotlib.pyplot as plt

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

        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
