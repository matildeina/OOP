import cv2
import numpy as np

# Fungsi callback untuk trackbar (tidak melakukan apa-apa)
def nothing(x):
    pass

# Fungsi callback untuk mouse klik (untuk mengambil warna saat diklik)
def get_color(event, x, y, flags, param):
    global l_h, l_s, l_v, u_h, u_s, u_v, hsv

    if event == cv2.EVENT_LBUTTONDOWN:  # Ketika tombol kiri mouse ditekan
        # Mengambil warna dari posisi klik
        color = hsv[y, x]
        # Mengubah nilai HSV sesuai dengan warna yang diklik
        l_h = max(0, color[0] - 10)  # Lower Hue (dengan sedikit toleransi)
        l_s = max(0, color[1] - 40)  # Lower Saturation
        l_v = max(0, color[2] - 40)  # Lower Value
        u_h = min(179, color[0] + 10)  # Upper Hue
        u_s = min(255, color[1] + 40)  # Upper Saturation
        u_v = min(255, color[2] + 40)  # Upper Value

        # Memperbarui trackbar secara otomatis
        cv2.setTrackbarPos("L - H", "Trackbars", l_h)
        cv2.setTrackbarPos("L - S", "Trackbars", l_s)
        cv2.setTrackbarPos("L - V", "Trackbars", l_v)
        cv2.setTrackbarPos("U - H", "Trackbars", u_h)
        cv2.setTrackbarPos("U - S", "Trackbars", u_s)
        cv2.setTrackbarPos("U - V", "Trackbars", u_v)

# Mengaktifkan kamera
cam = cv2.VideoCapture(0)

# Membuat jendela untuk Trackbars
cv2.namedWindow("Trackbars")

# Membuat trackbar untuk mengatur range HSV
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)  # Lower Hue
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)  # Lower Saturation
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)  # Lower Value
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)  # Upper Hue
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)  # Upper Saturation
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)  # Upper Value

# Variabel global untuk trackbar HSV
l_h, l_s, l_v, u_h, u_s, u_v = 0, 0, 0, 179, 255, 255

# Menambahkan callback mouse
cv2.namedWindow("Frame")  # Pastikan jendela Frame sudah ada
cv2.setMouseCallback("Frame", get_color)

while True:
    # Membaca frame dari kamera
    _, frame = cam.read()
    if not _:
        print("Gagal membaca frame dari kamera.")
        break

    # Konversi citra dari BGR ke HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Tampilkan HSV dari titik tengah frame
    h, s, v = hsv[frame.shape[0] // 2, frame.shape[1] // 2]
    cv2.putText(frame, f"HSV: {h},{s},{v}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Simpan nilai HSV dari trackbar ke variabel lokal (bukan global)
    lh = cv2.getTrackbarPos("L - H", "Trackbars")
    ls = cv2.getTrackbarPos("L - S", "Trackbars")
    lv = cv2.getTrackbarPos("L - V", "Trackbars")
    uh = cv2.getTrackbarPos("U - H", "Trackbars")
    us = cv2.getTrackbarPos("U - S", "Trackbars")
    uv = cv2.getTrackbarPos("U - V", "Trackbars")


    # Membuat array untuk batas bawah dan atas warna
    lower_color = np.array([lh, ls, lv])
    upper_color = np.array([uh, us, uv])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Menampilkan hasil deteksi warna
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Menampilkan frame asli, mask, dan hasil deteksi
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    # Keluar dari loop jika tombol 'ESC' ditekan
    key = cv2.waitKey(1)
    if key == 27:  # ESC key
        break

# Melepas kamera dan menutup semua jendela
cam.release()
cv2.destroyAllWindows()
