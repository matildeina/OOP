import numpy as np
import cv2
import matplotlib.pyplot as plt

def convolve2d(image, kernel):
    """Fungsi untuk melakukan konvolusi 2D."""
    h, w = image.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded_img = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
    output = np.zeros_like(image)
    
    for i in range(h):
        for j in range(w):
            region = padded_img[i:i+kh, j:j+kw]
            output[i, j] = np.sum(region * kernel)
    
    return output

def mean_filter(image):
    """Pelembutan citra menggunakan mean filter 3x3."""
    kernel = np.ones((3,3)) / 9.0
    return convolve2d(image, kernel)

def gaussian_filter(image, sigma=1):
    """Gaussian filter untuk pelembutan citra."""
    size = 5  # Ukuran kernel 5x5
    kernel = np.fromfunction(lambda x, y: (1/(2*np.pi*sigma**2)) * np.exp(-((x-2)**2 + (y-2)**2) / (2*sigma**2)), (size, size))
    kernel /= np.sum(kernel)
    return convolve2d(image, kernel)

def sharpen_filter(image):
    """Penajaman citra menggunakan kernel high-pass filter."""
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return convolve2d(image, kernel)

def median_filter(image):
    """Filter median untuk menghilangkan noise salt & pepper."""
    h, w = image.shape
    output = np.zeros_like(image)
    for i in range(1, h-1): #looping baris
        for j in range(1, w-1): #looping kolom
            neighbors = image[i-1:i+2, j-1:j+2].flatten()
            output[i, j] = np.median(neighbors)
    return output

def max_filter(image):
    """Filter max untuk mempertahankan nilai piksel terbesar dari tetangga."""
    h, w = image.shape
    output = np.zeros_like(image)
    for i in range(1, h-1):
        for j in range(1, w-1): 
            neighbors = image[i-1:i+2, j-1:j+2].flatten()
            output[i, j] = np.max(neighbors)
    return output

def process_and_show_separate(image):
    """Menampilkan setiap hasil filter di jendela terpisah."""
    filters = [
        (mean_filter, "Mean Filter"),
        (gaussian_filter, "Gaussian Filter"),
        (sharpen_filter, "Sharpen Filter"),
        (median_filter, "Median Filter"),
        (max_filter, "Max Filter")
    ]
    
    for filter_func, title in filters:
        result = filter_func(image)
        plt.figure()
        plt.imshow(result, cmap='gray')
        plt.title(title)
        plt.axis('off')
        plt.show(block=False)  # Tidak memblokir eksekusi sehingga semua jendela muncul sekaligus
    plt.show()

if __name__ == "__main__":
    img = cv2.imread('noise.png', cv2.IMREAD_GRAYSCALE)
    process_and_show_separate(img)