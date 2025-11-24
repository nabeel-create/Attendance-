import streamlit as st
import cv2
import numpy as np
from db import init_db, add_student, get_students, mark_attendance, get_attendance_records
from face_utils import encode_faces, recognize_face
from datetime import date
import os

# Initialize DB
init_db()

st.title("Face Recognition Attendance System")

menu = ["Register Student", "Take Attendance", "View Records"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register Student":
    st.subheader("Register Student")
    roll_number = st.text_input("Roll Number")
    name = st.text_input("Name")
    image_file = st.file_uploader("Upload Student Image", type=["jpg", "png"])

    if st.button("Register"):
        if roll_number and name and image_file:
            img_path = f"students/{roll_number}.jpg"
            with open(img_path, "wb") as f:
                f.write(image_file.getbuffer())
            add_student(roll_number, name, img_path)
            st.success(f"Student {name} registered successfully!")
        else:
            st.error("Please provide all details.")

elif choice == "Take Attendance":
    st.subheader("Take Attendance")
    known_encodings = encode_faces()

    run = st.button("Start Camera")
    FRAME_WINDOW = st.image([])
    if run:
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to access camera.")
                break
            roll_number = recognize_face(known_encodings, frame)
            if roll_number:
                st.success(f"Attendance marked present for {roll_number}")
                mark_attendance(roll_number, str(date.today()), "Present")
            FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if st.button("Stop"):
                break
        cap.release()

elif choice == "View Records":
    st.subheader("Attendance Records")
    records = get_attendance_records()
    st.table(records)
