import cv2
import face_recognition
import numpy as np
from datetime import datetime
import psycopg2
import os
from koneksi import get_connection

# Ambang batas untuk mengidentifikasi wajah yang tidak dikenal
UNKNOWN_THRESHOLD = 0.5

vid = cv2.VideoCapture(0)

# Inisialisasi daftar untuk menyimpan enkoding dan nama
known_face_encodings = []
known_face_names = []

# Buat koneksi ke database
conn = get_connection()

# Cursor untuk menjalankan query
cur = conn.cursor()

# Jalankan query untuk mengambil data wajah yang dikenal
cur.execute("SELECT id, nama_karyawan, foto_karyawan FROM data_karyawan")
rows = cur.fetchall()

# Dictionary untuk menyimpan data dari database
data = {}

# Loop melalui setiap baris hasil query dan isi dictionary
for row in rows:
    id, name, image_file = row
    data[f"employee"] = [{"id": id, "nama": name, "image": image_file}]
    image_source = face_recognition.load_image_file("wajah/"+image_file)
    face_encodings = face_recognition.face_encodings(image_source)
    if face_encodings:
        known_face_encodings.append(face_encodings[0])
        known_face_names.append(name)
    else:
        print(f"Tidak ada wajah yang ditemukan dalam gambar {image_file}.")
    # print(data)
# Tutup cursor dan koneksi
cur.close()
conn.close()

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
captured_names = []  # Daftar untuk menyimpan nama yang telah di-capture

while True:
    ret, frame = vid.read()
    frame = cv2.flip(frame, 1)

    # Tambahkan timestamp pada frame
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

    # Skala kecil dan konversi gambar
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        # Dapatkan lokasi dan enkoding wajah
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Bandingkan wajah yang dikenal dengan wajah yang terdeteksi
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Jika cocok, dapatkan nama wajah
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index] and face_distances[best_match_index] < UNKNOWN_THRESHOLD:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Tentukan path folder tempat Anda ingin menyimpan gambar
    folder_path = 'capture'

    # Pastikan folder tersebut ada, jika tidak, buat folder tersebut
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Tampilkan hasil dalam jendela
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        if name == "Unknown":
            color = (0, 0, 255)
        else:
            color = (0, 255, 0)
        # Gambar kotak dan label nama
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Jika nama yang terdeteksi sesuai dan belum di-capture, lakukan screen capture
        if name in known_face_names and name not in captured_names:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            file_name = f'{name} {timestamp}.jpg'
            file_path = os.path.join(folder_path, file_name)
            cv2.imwrite(file_path, frame)
            print(f"Gambar berhasil disimpan sebagai {name}|{timestamp}.jpg")
            captured_names.append(name) 
            print(captured_names) # Tambahkan nama ke daftar nama yang telah di-capture

    cv2.imshow('frame', frame)

    # Tekan 'q' untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepaskan kamera dan tutup semua jendela
vid.release()
cv2.destroyAllWindows()
