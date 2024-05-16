import cv2
import face_recognition
import numpy as np

vid = cv2.VideoCapture(0)

# Daftar nama gambar dan nama yang diketahui
image_files = ["muka1.jpg", "muka2.jpg"]
known_face_names = ["Julius Ryan", "Daffa Bagus"]

# Inisialisasi daftar untuk menyimpan enkoding dan nama
known_face_encodings = []

# Muat setiap gambar dan dapatkan enkoding wajah
for image_file in image_files:
    image_source = face_recognition.load_image_file(image_file)
    face_encodings = face_recognition.face_encodings(image_source)
    if face_encodings:
        known_face_encodings.append(face_encodings[0])
    else:
        print(f"Tidak ada wajah yang ditemukan dalam gambar {image_file}.")

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = vid.read()
    frame = cv2.flip(frame,1)

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
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Tampilkan hasil dalam jendela
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Gambar kotak dan label nama
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('frame', frame)


    # Tekan 'q' untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepaskan kamera dan tutup semua jendela
vid.release()
cv2.destroyAllWindows()
