import streamlit as st
from db import init_db, add_student, get_students, mark_attendance, get_attendance_records
from datetime import date
import os
from PIL import Image
import numpy as np
from io import BytesIO

# Initialize DB and student folder
init_db()
img_folder = "students"
os.makedirs(img_folder, exist_ok=True)

st.title("Student Attendance System")

menu = ["Register Student", "Mark Attendance", "View Records"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- Register Student ----------------
if choice == "Register Student":
    st.subheader("Register Student")
    roll_number = st.text_input("Roll Number")
    name = st.text_input("Name")
    image_file = st.file_uploader("Upload Student Photo", type=["jpg", "png"])

    if st.button("Register"):
        if roll_number and name and image_file:
            existing_students = get_students()
            if any(roll_number == s[0] for s in existing_students):
                st.warning(f"Student with roll number {roll_number} already exists!")
            else:
                img_path = os.path.join(img_folder, f"{roll_number}.jpg")
                with open(img_path, "wb") as f:
                    f.write(image_file.getbuffer())
                add_student(roll_number, name, img_path)
                st.success(f"Student {name} registered successfully!")
        else:
            st.error("Please fill all details.")

# ---------------- Mark Attendance ----------------
elif choice == "Mark Attendance":
    st.subheader("Mark Attendance")
    students = get_students()
    if not students:
        st.warning("No registered students found!")
    else:
        uploaded_image = st.camera_input("Capture your photo for attendance")
        if uploaded_image:
            pil_uploaded = Image.open(BytesIO(uploaded_image.read())).convert("RGB")
            matched = False

            for roll_number, name, img_path in students:
                try:
                    pil_registered = Image.open(img_path).convert("RGB")
                    # Resize webcam image to match registered image
                    pil_uploaded_resized = pil_uploaded.resize(pil_registered.size)
                    uploaded_array = np.array(pil_uploaded_resized)
                    registered_array = np.array(pil_registered)

                    # Compare images (pixel-wise)
                    if np.array_equal(uploaded_array, registered_array):
                        mark_attendance(roll_number, str(date.today()), "Present")
                        st.success(f"Attendance marked for {name} ({roll_number})")
                        matched = True
                        break
                except Exception as e:
                    st.error(f"Error comparing image for {name}: {e}")

            if not matched:
                st.error("Face does not match any registered student.")

# ---------------- View Records ----------------
elif choice == "View Records":
    st.subheader("Attendance Records")
    records = get_attendance_records()
    st.table(records)
