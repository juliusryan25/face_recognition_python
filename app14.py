from package import *

UNKNOWN_THRESHOLD = 0.6  # lebih rendah untuk meningkatkan akurasi

vid = cv2.VideoCapture(0)
data = {}
known_face_encodings = []
known_face_names = []
captured_names = []
frame_skip = 2

#ambil data wajah
for row in rows:
    id, name, image_file = row
    data[f"employee"] = [{"id": id, "nama": name, "image": image_file}]
    image_source = face_recognition.load_image_file("package/wajah/" + image_file)
    face_encodings = face_recognition.face_encodings(image_source)

    if face_encodings:
        known_face_encodings.append(face_encodings[0])
        known_face_names.append(name)
    else:
        print(f"Tidak ada wajah yang ditemukan dalam gambar {image_file}.")

def process_frame(frame):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=UNKNOWN_THRESHOLD)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)

    return face_locations, face_names

def adjust_text_size(frame, text, max_width, min_font_size=0.5, max_font_size=1.5, step=0.1):
    for font_size in np.arange(max_font_size, min_font_size, -step):
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_size, 1)
        if text_width <= max_width:
            return font_size, (text_width, text_height)
    return min_font_size, cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, min_font_size, 1)[0]

def compress_and_save_image(image, name, folder_path, quality=70):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    buffer = io.BytesIO()
    pil_image.save(buffer, format="JPEG", quality=quality, optimize=True)
    image_data = buffer.getvalue()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    face_filename = f'{name}_{timestamp}.jpg'
    file_path = os.path.join(folder_path, face_filename)

    with open(file_path, 'wb') as f:
        f.write(image_data)

    captured_names.append(name)
    nama_karyawan = name
    jam_masuk = datetime.now()
    upload_to_database(nama_karyawan, file_path, jam_masuk, conn)
    print(f"Gambar berhasil disimpan sebagai {face_filename}")


def main():
    process_this_frame = True
    while True:
        ret, frame = vid.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        if absen_masuk_start <= now <= absen_masuk_end or absen_pulang_start <= now <= absen_pulang_end:
            if process_this_frame:
                face_locations, face_names = process_frame(frame)

            process_this_frame = not process_this_frame

            folder_path = 'package/capture'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                text_bottom = bottom + 25
                max_text_width = right - left
                font_size, (text_width, text_height) = adjust_text_size(frame, name, max_text_width)

                if text_bottom > frame.shape[0]:
                    text_bottom = frame.shape[0] - 10

                rectangle_color = (0, 0, 255) if name == "Unknown" else (0, 255, 0)
                cv2.rectangle(frame, (left, top), (right, bottom), rectangle_color, 2)
                cv2.rectangle(frame, (left, text_bottom - text_height + 3), (left + text_width, text_bottom + 3), rectangle_color, cv2.FILLED)
                cv2.putText(frame, name, (left + 1, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), 1)

                if name in known_face_names and name not in captured_names:
                    face_image = frame[top:bottom + 25, left:right]
                    if face_image.size != 0:
                        compress_and_save_image(face_image, name, folder_path)
                        binary_data = get_binary_data_from_database()
                        show_binary_image(binary_data)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            pesan = "Bukan Waktu Absen"
            cv2.putText(frame, pesan, (6, frame.shape[0] - 9), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

        jumlah_wajah_terdeteksi = str(len(face_names))
        cv2.putText(frame, jumlah_wajah_terdeteksi, (10, frame.shape[0] - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.imshow('frame', frame)

    vid.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()