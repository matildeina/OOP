import cv2

image = cv2.imread('gambar.jpg')
if image is None:
    print("Gagal membuka gambar!")
else:
    cv2.imshow("Cek Gambar", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()