# Face Attendance System (Streamlit + OpenCV LBPH)

This repo contains a Streamlit app that lets you:
- Register students (name, roll, face image)
- Train an LBPH face recognizer
- Take attendance via camera input (matches face -> marks Present)
- View attendance records and export as CSV

**Important**: Download the OpenCV Haarcascade file and place it in `models/haarcascade_frontalface_default.xml`.
You can copy it from OpenCV's GitHub: https://github.com/opencv/opencv/tree/master/data/haarcascades

## Run locally
1. Create virtualenv and install:
   ```
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Run:
   ```
   streamlit run app.py
   ```

## Deploy
- Push to GitHub and connect to Streamlit Community Cloud.
- Ensure `models/haarcascade_frontalface_default.xml` is included in the repo.

## Notes
- LBPH recognizer saved in `recognizer/lbph_model.yml`.
- Student face crops are saved under `students/` as `<roll>_N.jpg`.
- If you want higher accuracy, see alternatives in `README_alternatives.md`.
