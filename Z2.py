import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

def load_image(path):
    image = cv2.imread(path)
    if image is None:
        print("Gambar tidak ditemukan.")
        exit()
    return image

def gray_histogram(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plt.hist(gray.ravel(), 256, [0, 256])
    plt.title("Histogram Grayscale")
    plt.show()
    return gray

def negative(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    neg = 255 - gray
    return neg

def biner(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    return binary

def rgb_histogram(image):
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histo = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(histo, color=col)
        plt.xlim([0, 256])
    plt.title("Histogram RGB")
    plt.show()

def equal_histogram(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equal = cv2.equalizeHist(gray)
    plt.hist(equal.ravel(), 256, [0, 256])
    plt.title("Equalized Histogram")
    plt.show()
    return equal

def translasi(image):
    h, w = image.shape[:2]
    T = np.float32([[1, 0, w / 4], [0, 1, h / 4]])
    translated = cv2.warpAffine(image, T, (w, h))
    return translated

def rotasi(image, degree=90):
    h, w = image.shape[:2]
    matrix = cv2.getRotationMatrix2D((w / 2, h / 2), degree, 0.7)
    rotated = cv2.warpAffine(image, matrix, (w, h))
    return rotated

def zoom_in(image, scale=2):
    return cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

def crop_image(image):
    h, w = image.shape[:2]
    ch, cw = int(h * 0.5), int(w * 0.5)
    start_row, start_col = (h - ch) // 2, (w - cw) // 2
    cropped = image[start_row:start_row+ch, start_col:start_col+cw]
    return cropped

img_path = "paru-paru.png"
img = load_image(img_path)

# Proses langsung
gray = gray_histogram(img)
cv2.imshow("Grayscale", gray)

neg = negative(img)
cv2.imshow("Negative", neg)

binary = biner(img)
cv2.imshow("Binary", binary)

rgb_histogram(img)

equal = equal_histogram(img)
cv2.imshow("Equalized Histogram", equal)

translated = translasi(img)
cv2.imshow("Translated", translated)

rotated = rotasi(img)
cv2.imshow("Rotated 90°", rotated)

zoomed = zoom_in(img)
cv2.imshow("Zoomed In", zoomed)

cropped = crop_image(img)
cv2.imshow("Cropped", cropped)

cv2.waitKey(0)
cv2.destroyAllWindows()