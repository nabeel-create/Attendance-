import streamlit as st
from db import init_db, add_student, get_students, mark_attendance, get_attendance_records
from datetime import date
import os
from PIL import Image
from io import BytesIOimport streamlit as st
from db import init_db, add_student, get_students, mark_attendance, get_attendance_records
from datetime import date
import os

# Initialize database and folders
init_db()
if not os.path.exists("students"):
    os.makedirs("students")

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
            img_path = f"students/{roll_number}.jpg"
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
        st.warning("No registered students yet!")
    else:
        uploaded_image = st.file_uploader("Upload your photo for attendance", type=["jpg", "png"])
        if uploaded_image:
            # Compare uploaded image file name with registered photos
            matched = False
            for roll_number, name, img_path in students:
                # Simple verification: exact file match (for demo purposes)
                if uploaded_image.name == os.path.basename(img_path):
                    mark_attendance(roll_number, str(date.today()), "Present")
                    st.success(f"Attendance marked for {name} ({roll_number})")
                    matched = True
                    break
            if not matched:
                st.error("Photo does not match any registered student. Attendance not marked.")

# ---------------- View Records ----------------
elif choice == "View Records":
    st.subheader("Attendance Records")
    records = get_attendance_records()
    st.table(records)

from deepface import DeepFace

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
    students = get_students()
    if not students:
        st.warning("No registered students found!")
    else:
        uploaded_image = st.camera_input("Take Photo for Attendance")
        if uploaded_image:
            pil_img = Image.open(BytesIO(uploaded_image.read())).convert('RGB')

            matched = False
            for roll_number, name, img_path in students:
                try:
                    result = DeepFace.verify(img_path, pil_img, enforce_detection=False)
                    if result["verified"]:
                        mark_attendance(roll_number, str(date.today()), "Present")
                        st.success(f"Attendance marked for {name} ({roll_number})")
                        matched = True
                        break
                except Exception as e:
                    st.error(f"Error processing {name}: {str(e)}")

            if not matched:
                st.error("Face not recognized. Attendance not marked.")

# ---------------- View Records ----------------
elif choice == "View Records":
    st.subheader("Attendance Records")
    records = get_attendance_records()
    st.table(records)
