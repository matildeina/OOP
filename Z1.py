import cv2
import numpy as np

def load_image(path='paru-paru.png'):
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

def brightness(image, value=80):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return np.clip(gray + value, 0, 255).astype(np.uint8)

def contrast(image, factor=1.7):
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

def negative(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return 255 - gray

def binary(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return binary_img

def process_pixels(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    H, W = gray.shape
    for i in range(H):
        for j in range(W):
            pixel = gray.item(i, j)
            if pixel == 127:
                new_pixel = 0
            elif pixel < 127:
                new_pixel = 1
            else:
                new_pixel = 255
            gray.itemset((i, j), new_pixel)
    return gray

# --- Main Program ---
if __name__ == "__main__":
    image = load_image()

    gray = grayscale(image)
    show_image(gray, "Grayscale")

    bright = brightness(image)
    show_image(bright, "Brightness")

    contr = contrast(image)
    show_image(contr, "Contrast")

    stretch = contrast_stretching(image)
    show_image(stretch, "Contrast Stretching")

    neg = negative(image)
    show_image(neg, "Negative")

    bin_img = binary(image)
    show_image(bin_img, "Binary")

    processed = process_pixels(image)
    show_image(processed, "Process Pixels")