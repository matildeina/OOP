import cv2
import numpy as np

def load_image(path='cat.jpg'):
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError("Gambar tidak ditemukan.")
    return image

def show_image(image, title="Image"):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def grayscale(image):
    H, W = image.shape[:2]
    gray = np.zeros((H, W), np.uint8)
    for i in range(H):
        for j in range(W):
            gray[i, j] = np.clip(0.299 * image[i, j, 0] +
                                 0.587 * image[i, j, 1] +
                                 0.114 * image[i, j, 2], 0, 255)
    return gray

def contrast(image, factor=2.1):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    H, W = gray.shape[:2]
    for i in range(H):
        for j in range(W):
            val = gray.item(i, j)
            gray.itemset((i, j), np.clip(val * factor, 0, 255))
    return gray

def contrast_stretching(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    minV = np.min(gray)
    maxV = np.max(gray)
    stretched = np.zeros_like(gray)
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            val = gray.item(i, j)
            new_val = float(val - minV) / (maxV - minV) * 255
            stretched.itemset((i, j), new_val)
    return stretched

if __name__ == "__main__":
    image = load_image()

    gray = grayscale(image)
    show_image(gray, "Grayscale")

    contr = contrast(image)
    show_image(contr, "Contrast")

    stretch = contrast_stretching(image)
    show_image(stretch, "Contrast Stretching")