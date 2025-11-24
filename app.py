import streamlit as st
from db import init_db, add_student, get_students, mark_attendance, get_attendance_records
from datetime import date
import os
from PIL import Image
import numpy as np

# Initialize database and folder
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
        st.warning("No registered students yet!")
    else:
        uploaded_image = st.file_uploader("Upload your photo for attendance", type=["jpg", "png"])
        if uploaded_image:
            pil_uploaded = Image.open(uploaded_image).convert("RGB")
            uploaded_array = np.array(pil_uploaded)

            matched = False
            for roll_number, name, img_path in students:
                try:
                    pil_registered = Image.open(img_path).convert("RGB")
                    registered_array = np.array(pil_registered)

                    # Resize uploaded image to match registered image
                    pil_uploaded_resized = pil_uploaded.resize(pil_registered.size)
                    uploaded_resized_array = np.array(pil_uploaded_resized)

                    # Compare images
                    if np.array_equal(registered_array, uploaded_resized_array):
                        mark_attendance(roll_number, str(date.today()), "Present")
                        st.success(f"Attendance marked for {name} ({roll_number})")
                        matched = True
                        break
                except Exception as e:
                    st.error(f"Error comparing image for {name}: {e}")

            if not matched:
                st.error("Uploaded photo does not match any registered student.")

# ---------------- View Records ----------------
elif choice == "View Records":
    st.subheader("Attendance Records")
    records = get_attendance_records()
    st.table(records)
