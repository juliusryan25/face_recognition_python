from package import *

# Inisialisasi detektor wajah dari dlib
detector = dlib.get_frontal_face_detector()
# Inisialisasi model pencocokan wajah dari dlib
sp = dlib.shape_predictor('D:\\Document\\FR\\shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('D:\\Document\\FR\\dlib_face_recognition_resnet_model_v1.dat')

video_capture = cv2.VideoCapture(0)

def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = detector(gray_image)
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces

def get_face_descriptor(frame, face):
    shape = sp(frame, face)
    return facerec.compute_face_descriptor(frame, shape)

data = {}
known_face_encodings = []  # Isi dengan encoding wajah yang diketahui
known_face_names = []  # Isi dengan nama yang sesuai dengan encoding wajah

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

    for face in faces:
        face_descriptor = get_face_descriptor(video_frame, face)
        # Lakukan pencocokan dengan database wajah yang diketahui
        # ...

    cv2.imshow("My Face Detection Project", video_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
