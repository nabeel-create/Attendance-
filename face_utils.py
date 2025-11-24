# face_utils.py
import face_recognition
import numpy as np
import os
from typing import Optional, Tuple

STUDENTS_DIR = "students"
ENCODINGS_DIR = "encodings"
ENCODINGS_PATH = os.path.join(ENCODINGS_DIR, "encodings.npy")
ROLLS_PATH = os.path.join(ENCODINGS_DIR, "rolls.npy")

os.makedirs(STUDENTS_DIR, exist_ok=True)
os.makedirs(ENCODINGS_DIR, exist_ok=True)

def save_student_image(roll: str, image_rgb) -> str:
    """Save student image as JPG"""
    existing = [f for f in os.listdir(STUDENTS_DIR) if f.startswith(f"{roll}_")]
    idx = len(existing) + 1
    path = os.path.join(STUDENTS_DIR, f"{roll}_{idx}.jpg")
    image_rgb.save(path)
    return path

def train_encodings():
    """Compute encodings for all students and save them"""
    encodings = []
    rolls = []
    for fname in os.listdir(STUDENTS_DIR):
        if not fname.lower().endswith(('.jpg','.png','.jpeg')):
            continue
        roll = fname.split("_")[0]
        path = os.path.join(STUDENTS_DIR, fname)
        img = face_recognition.load_image_file(path)
        face_locations = face_recognition.face_locations(img)
        if len(face_locations) == 0:
            continue
        face_encoding = face_recognition.face_encodings(img, known_face_locations=face_locations)[0]
        encodings.append(face_encoding)
        rolls.append(roll)
    if len(encodings) == 0:
        raise ValueError("No student faces found to train.")
    np.save(ENCODINGS_PATH, encodings)
    np.save(ROLLS_PATH, rolls)
    return True

def load_encodings() -> Tuple[list, list]:
    if not os.path.exists(ENCODINGS_PATH) or not os.path.exists(ROLLS_PATH):
        return [], []
    encodings = np.load(ENCODINGS_PATH, allow_pickle=True)
    rolls = np.load(ROLLS_PATH, allow_pickle=True)
    return encodings.tolist(), rolls.tolist()

def predict_face(image_rgb, tolerance=0.5) -> Optional[str]:
    """Return roll if face matches, else None"""
    unknown_image = np.array(image_rgb)
    unknown_encodings = face_recognition.face_encodings(unknown_image)
    if len(unknown_encodings) == 0:
        return None
    unknown_encoding = unknown_encodings[0]
    known_encodings, known_rolls = load_encodings()
    if len(known_encodings) == 0:
        return None
    matches = face_recognition.compare_faces(known_encodings, unknown_encoding, tolerance=tolerance)
    if True in matches:
        idx = matches.index(True)
        return known_rolls[idx]
    return None
