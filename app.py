# app.py
import streamlit as st
from PIL import Image
import numpy as np
from db import init_db, add_student, get_students, add_attendance, get_attendance
from face_utils import save_student_image, train_encodings, predict_face

init_db()
st.set_page_config(page_title="Face Attendance", layout="wide")
st.title("📸 Face Attendance System (face_recognition)")

menu = st.sidebar.selectbox("Menu", ["Register Student", "Train Model", "Take Attendance", "Attendance Records", "Students"])

if menu == "Register Student":
    st.header("Register a Student")
    roll = st.text_input("Roll Number (unique)")
    name = st.text_input("Student Name")
    uploaded = st.file_uploader("Upload face image (jpg/png)", type=["jpg","jpeg","png"])
    if st.button("Register"):
        if not roll or not name or not uploaded:
            st.warning("Fill roll, name and upload an image.")
        else:
            image = Image.open(uploaded).convert("RGB")
            path = save_student_image(roll, image)
            add_student(roll, name, path)
            st.success(f"Registered {name} ({roll}). Image saved: {path}")

if menu == "Train Model":
    st.header("Train Face Recognition Encodings")
    if st.button("Train"):
        try:
            train_encodings()
            st.success("Training complete. Encodings saved.")
        except Exception as e:
            st.error(f"Training failed: {e}")

if menu == "Take Attendance":
    st.header("Take Attendance")
    img_file = st.camera_input("Capture Face")
    tolerance = st.slider("Matching tolerance (lower = stricter)", min_value=0.3, max_value=0.7, value=0.5)
    if img_file is not None:
        img = Image.open(img_file).convert("RGB")
        roll = predict_face(img, tolerance=tolerance)
        if roll is None:
            st.error("No match found or no face detected.")
        else:
            students = dict((r, n) for r, n, _ in get_students())
            name = students.get(roll, "Unknown")
            add_attendance(roll, name, "Present")
            st.success(f"Matched {name} ({roll}) — marked PRESENT.")
            st.image(img, caption=f"Matched {name} ({roll})", use_column_width=True)

if menu == "Attendance Records":
    st.header("Attendance Records")
    rows = get_attendance(limit=1000)
    import pandas as pd
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
        import pandas as pd
        df = pd.DataFrame(rows, columns=["Roll", "Name", "ImagePath"])
        st.dataframe(df)
        for roll, name, imgpath in rows:
            from PIL import Image
            if os.path.exists(imgpath):
                st.image(Image.open(imgpath), caption=f"{name} ({roll})", width=150)
