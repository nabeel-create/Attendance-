import face_recognition
import os

def encode_faces(folder='students'):
    encodings = {}
    for filename in os.listdir(folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            path = os.path.join(folder, filename)
            image = face_recognition.load_image_file(path)
            face_encoding = face_recognition.face_encodings(image)
            if face_encoding:
                encodings[filename.split('.')[0]] = face_encoding[0]
    return encodings

def recognize_face(known_encodings, uploaded_image):
    import numpy as np
    import cv2
    file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb_img)
    encodings = face_recognition.face_encodings(rgb_img, faces)

    for encoding in encodings:
        for roll_number, known_encoding in known_encodings.items():
            matches = face_recognition.compare_faces([known_encoding], encoding)
            if matches[0]:
                return roll_number
    return None
