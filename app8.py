from package import *

# Ambang batas untuk mengidentifikasi wajah yang tidak dikenal
UNKNOWN_THRESHOLD = 3

#inisiasi untuk capture image
vid = cv2.VideoCapture('rtsp://admin:Admin1234@172.17.143.55:554')

# vid = cv2.VideoCapture()

# Dictionary untuk menampung data dari database
data = {}

# Inisialisasi daftar untuk menampung enkoding dan nama
known_face_encodings = []
known_face_names = []

# Loop melalui setiap baris hasil query dan isi dictionary
for row in rows:
    id, name, image_file = row
    data[f"employee"] = [{"id": id, "nama": name, "image": image_file}]
    image_source = face_recognition.load_image_file("package/wajah/"+image_file)
    face_encodings = face_recognition.face_encodings(image_source)

    if face_encodings:
        known_face_encodings.append(face_encodings[0])
        known_face_names.append(name)
    else:
        print(f"Tidak ada wajah yang ditemukan dalam gambar {image_file}.")


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
    folder_path = 'package/capture'

    # Pastikan folder tersebut ada, jika tidak, buat folder tersebut
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Tampilkan hasil dalam jendela (KOTAK SCAN)
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Membedakan warna jika wajah tidak dikenali
        if name == "Unknown" :
            rectangle_color = (0,0,225)
        elif name != "Unknown" :
            rectangle_color = (0,225,0)

        # Gambar kotak dan label nama
        cv2.rectangle(frame, (left, top), (right, bottom), (rectangle_color), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (rectangle_color), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Jika nama yang terdeteksi sesuai dan belum di-capture, lakukan screen capture
        if name in known_face_names and name not in captured_names:
            original_top = top * 1
            original_right = right * 1
            original_bottom = bottom * 1
            original_left = left * 1

            # Potong bagian wajah dari frame asli
            face_image = frame[original_top:original_bottom, original_left:original_right]

            # Pastikan face_image tidak kosong sebelum menyimpan
            if face_image.size != 0:

                # Proses Kompres Gambar
                def compress_and_save_image(image,name,folder_path,quality=40):
                    # Mengonversi frame OpenCV ke format PIL Image
                    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                    
                    # Menyiapkan buffer in-memory sebagai file
                    buffer = io.BytesIO()
                    
                    # Menyimpan gambar ke buffer dengan kualitas tertentu
                    pil_image.save(buffer, format="JPEG", quality=quality, optimize=True)
                    
                    # Mendapatkan byte data dari buffer
                    image_data = buffer.getvalue()

                    # Penamaan File
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
                    face_filename = f'{name}_{timestamp}.jpg' 
                    file_path = os.path.join(folder_path, face_filename)
                   
                    # Menyimpan gambar ke folder tujuan
                    with open(file_path, 'wb') as f:
                        f.write(image_data)
                    
                    # Print Keterangan gambar barhasil disimpan & menyimpan nama pegawai yang berhasil dipindai 
                    print(f"Gambar berhasil disimpan sebagai {face_filename}")
                    captured_names.append(name)

                #Menjalankan Proses save capture
                compress_and_save_image(face_image,name,folder_path)

    # Keterangan jumlah wajah yang terdeteksi
    jumlah_wajah_terdeteksi = str(len(face_names))
    cv2.putText(frame, jumlah_wajah_terdeteksi, (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
    cv2.imshow('frame', frame)#menampilkan aplikasi

    # Tekan 'q' untuk keluar dari loop
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break   

# Lepaskan kamera dan tutup semua jendela
vid.release()
cv2.destroyAllWindows()