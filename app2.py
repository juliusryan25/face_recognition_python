from package import *

# Inisialisasi classifier wajah
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Inisialisasi capture video
video_capture = cv2.VideoCapture(0)

# Fungsi untuk mendeteksi bounding box
def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces

# Fungsi untuk membandingkan wajah dengan database
def match_face(known_face_encodings, face_encoding_to_check):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding_to_check)
    name = "Unknown"
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding_to_check)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]
    return name

# Contoh database wajah (harus diisi dengan encoding wajah yang diketahui)
data = {}
known_face_encodings = []
known_face_names = []

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


while True:
    result, video_frame = video_capture.read()
    if result is False:
        break

    faces = detect_bounding_box(video_frame)
 
    # Mendapatkan encoding untuk setiap wajah yang terdeteksi
    for (x, y, w, h) in faces:
        face_frame = video_frame[y:y+h, x:x+w]
        face_encodings = face_recognition.face_encodings(face_frame)

        # Pastikan bahwa wajah terdeteksi sebelum mencoba mengakses encoding
        if face_encodings:
            face_encoding = face_encodings[0]

            # Membandingkan wajah yang terdeteksi dengan database
            name = match_face(known_face_encodings, face_encoding)

            # Menampilkan nama pada frame
            cv2.putText(video_frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            continue

    cv2.imshow("My Face Detection Project", video_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
