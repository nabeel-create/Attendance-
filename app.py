import streamlit as st
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
            matched = False
            for roll_number, name, img_path in students:
                # Compare uploaded file name with registered photo name
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
