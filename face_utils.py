# face_utils.py
import cv2
import os
import numpy as np
from typing import Optional, Tuple

CASCADE_PATH = os.path.join("models", "haarcascade_frontalface_default.xml")
STUDENTS_DIR = "students"
RECOGNIZER_DIR = "recognizer"
RECOGNIZER_PATH = os.path.join(RECOGNIZER_DIR, "lbph_model.yml")
LABELS_PATH = os.path.join(RECOGNIZER_DIR, "labels.npy")

os.makedirs(STUDENTS_DIR, exist_ok=True)
os.makedirs(RECOGNIZER_DIR, exist_ok=True)

# Load Haar cascade
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# Create LBPH recognizer (opencv-contrib required)
recognizer = cv2.face.LBPHFaceRecognizer_create()

def detect_face_from_image(image_bgr: np.ndarray) -> Optional[np.ndarray]:
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80,80))
    if len(faces) == 0:
        return None
    x, y, w, h = faces[0]
    return gray[y:y+h, x:x+w]

def save_student_image(roll: str, image_bgr: np.ndarray) -> str:
    face = detect_face_from_image(image_bgr)
    if face is None:
        raise ValueError("No face detected in the uploaded image.")
    existing = [f for f in os.listdir(STUDENTS_DIR) if f.startswith(f"{roll}_")]
    idx = len(existing) + 1
    path = os.path.join(STUDENTS_DIR, f"{roll}_{idx}.jpg")
    cv2.imwrite(path, face)
    return path

def train_recognizer():
    images = []
    labels = []
    label_map = {}
    next_label = 0
    for fname in os.listdir(STUDENTS_DIR):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        roll = fname.split("_")[0]
        if roll not in label_map:
            label_map[roll] = next_label
            next_label += 1
        path = os.path.join(STUDENTS_DIR, fname)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        images.append(img)
        labels.append(label_map[roll])
    if len(images) == 0:
        raise ValueError("No student images to train on. Register at least one student.")
    recognizer.train(images, np.array(labels))
    recognizer.save(RECOGNIZER_PATH)
    rev = {v:k for k,v in label_map.items()}
    max_label = max(rev.keys())
    arr = ["" for _ in range(max_label+1)]
    for k, v in rev.items():
        arr[k] = v
    np.save(LABELS_PATH, np.array(arr))
    return True

def load_recognizer() -> bool:
    if not os.path.exists(RECOGNIZER_PATH) or not os.path.exists(LABELS_PATH):
        return False
    recognizer.read(RECOGNIZER_PATH)
    return True

def predict_face(image_bgr: np.ndarray, threshold: float = 80.0) -> Tuple[Optional[str], Optional[float]]:
    face = detect_face_from_image(image_bgr)
    if face is None:
        return None, None
    if not load_recognizer():
        return None, None
    lbl, conf = recognizer.predict(face)
    labels = np.load(LABELS_PATH, allow_pickle=True)
    if lbl < 0 or lbl >= len(labels):
        return None, None
    roll = labels[lbl].item()
    if conf <= threshold:
        return roll, float(conf)
    return None, float(conf)
