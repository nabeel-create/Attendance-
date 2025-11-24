# app.py - Streamlit attendance app with CSV export
import streamlit as st
from PIL import Image
import numpy as np
import os
import pandas as pd
from db import init_db, add_student, get_students, add_attendance, get_attendance
from face_utils import save_student_image, train_recognizer, predict_face, load_recognizer

init_db()
st.set_page_config(page_title="Face Attendance", layout="wide")
st.title("📸 Face-based Attendance System (OpenCV LBPH)")

menu = st.sidebar.selectbox("Menu", ["Register Student", "Train Model", "Take Attendance", "Attendance Records", "Students"])

if menu == "Register Student":
    st.header("Register a Student")
    roll = st.text_input("Roll Number (unique)")
    name = st.text_input("Student Name")
    uploaded = st.file_uploader("Upload face image (jpg/png)", type=["jpg","jpeg","png"])
    if st.button("Register"):
        if not roll or not name or not uploaded:
            st.warning("Fill roll, name and upload an image with a clear frontal face.")
        else:
            image = Image.open(uploaded).convert("RGB")
            image_np = np.array(image)[:, :, ::-1].copy()
            try:
                path = save_student_image(roll, image_np)
                add_student(roll, name, path)
                st.success(f"Student {name} ({roll}) registered. Face saved: {path}")
            except Exception as e:
                st.error(f"Failed to register: {e}")

if menu == "Train Model":
    st.header("Train LBPH Recognizer")
    st.write("Train the model from images in `students/`. Do this after registering or adding new images.")
    if st.button("Train"):
        try:
            train_recognizer()
            st.success("Training complete. Model saved to recognizer/lbph_model.yml")
        except Exception as e:
            st.error(f"Training failed: {e}")

if menu == "Take Attendance":
    st.header("Take Attendance")
    st.write("Use your camera to take a photo. If a registered face matches, it will be marked present.")
    img_file = st.camera_input("Take a photo")
    confidence_threshold = st.slider("Match threshold (LBPH confidence). Smaller = stricter", min_value=30, max_value=150, value=80)
    if img_file is not None:
        img = Image.open(img_file).convert("RGB")
        img_np = np.array(img)[:, :, ::-1].copy()
        roll, conf = predict_face(img_np, threshold=confidence_threshold)
        if roll is None:
            st.error("No match found or face not detected.")
            st.write("Confidence:", conf)
        else:
            students = dict((r, n) for r, n, _ in get_students())
            name = students.get(roll, "Unknown")
            add_attendance(roll, name, "Present")
            st.success(f"Matched {name} ({roll}) — marked PRESENT. Confidence: {conf:.2f}")
            st.image(img, caption=f"Captured — matched {name} ({roll})", use_column_width=True)

if menu == "Attendance Records":
    st.header("Attendance Records")
    rows = get_attendance(limit=1000)
    df = pd.DataFrame(rows, columns=["Roll", "Name", "Status", "Timestamp"])
    st.dataframe(df)
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", data=csv, file_name="attendance_records.csv", mime="text/csv")

if menu == "Students":
    st.header("Registered Students")
    rows = get_students()
    if len(rows) == 0:
        st.info("No students registered yet.")
    else:
        df = pd.DataFrame(rows, columns=["Roll", "Name", "ImagePath"])
        st.dataframe(df)
        for roll, name, imgpath in rows:
            if os.path.exists(imgpath):
                st.image(Image.open(imgpath), caption=f"{name} ({roll})", width=150)
