import cv2
import numpy as np

# Mengaktifkan kamera
cam = cv2.VideoCapture(0)

while True:
    # Membaca frame dari kamera
    _, frame = cam.read()

    # Konversi dari BGR (RGB OpenCV) ke HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([66, 98, 100])
    upper_color = np.array([156, 232, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Menampilkan hasil dengan menggunakan mask
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Menampilkan frame asli, mask, dan hasil akhir
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    # Keluar dari loop jika tombol 'ESC' ditekan
    key = cv2.waitKey(1)
    if key == 27:  # Tombol ESC
        break

# Melepas kamera dan menutup semua jendela
cam.release()
cv2.destroyAllWindows()