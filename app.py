import streamlit as st
from db import init_db, add_student, get_students, mark_attendance, get_attendance_records
from face_utils import encode_faces, recognize_face
from datetime import date
import os

# Initialize
init_db()
if not os.path.exists("students"):
    os.makedirs("students")

st.title("Face Recognition Attendance System")

menu = ["Register Student", "Take Attendance", "View Records"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- Register Student ----------------
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

# ---------------- Take Attendance ----------------
elif choice == "Take Attendance":
    st.subheader("Take Attendance")
    known_encodings = encode_faces()

    uploaded_image = st.camera_input("Take Photo for Attendance")
    if uploaded_image:
        roll_number = recognize_face(known_encodings, uploaded_image)
        if roll_number:
            mark_attendance(roll_number, str(date.today()), "Present")
            st.success(f"Attendance marked for {roll_number}")
        else:
            st.error("Face not recognized. Attendance not marked.")

# ---------------- View Records ----------------
elif choice == "View Records":
    st.subheader("Attendance Records")
    records = get_attendance_records()
    st.table(records)
