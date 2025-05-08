import math
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load image
image = cv2.imread('paru-paru.png')

# Fungsi untuk menampilkan gambar
def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Grayscale + Histogram Grayscale
def gray_histogram(img):
    h, w = img.shape[:2]
    gray = np.zeros((h, w), np.uint8)
    for i in range(h):
        for j in range(w):
            gray[i, j] = np.clip(
                0.299 * img[i, j, 0]
                + 0.587 * img[i, j, 1]
                + 0.114 * img[i, j, 2],
                0,
                255,
            )
    plt.hist(gray.ravel(), 255, [0, 255])
    plt.title("Grayscale Histogram")
    plt.show()
    show_image("Grayscale", gray)

# Binerisasi
def biner(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape[:2]
    for i in range(h):
        for j in range(w):
            a = gray.item(i, j)
            gray.itemset((i, j), 0 if a < 180 else 255)
    show_image("Biner", gray)

# Negatif
def negative(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape[:2]
    for i in range(h):
        for j in range(w):
            a = gray.item(i, j)
            b = math.ceil(255 - a)
            gray.itemset((i, j), b)
    show_image("Negatif", gray)

# Histogram RGB
def rgb_histogram(img):
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histo = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histo, color=col)
        plt.xlim([0, 256])
    plt.title("RGB Histogram")
    plt.show()

# Histogram Equalization
def equal_histogram(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist, bins = np.histogram(gray.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()
    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')
    img_eq = cdf[gray]
    show_image("Equalized Image", img_eq)

    plt.plot(cdf_normalized, color='b')
    plt.hist(gray.flatten(), 256, [0, 256], color='r')
    plt.legend(('cdf', 'histogram'), loc='upper left')
    plt.title("Equalization Histogram")
    plt.xlim([0, 256])
    plt.show()

# Jalankan semua fungsi
gray_histogram(image)
biner(image)
negative(image)
rgb_histogram(image)
equal_histogram(image)