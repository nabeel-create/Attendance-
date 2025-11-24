import face_recognition
import cv2
import os
import numpy as np

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

def recognize_face(known_encodings, frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame, faces)

    for encoding in encodings:
        for roll_number, known_encoding in known_encodings.items():
            matches = face_recognition.compare_faces([known_encoding], encoding)
            if matches[0]:
                return roll_number
    return None
