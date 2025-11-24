import sqlite3

DB_NAME = "attendance_records.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Table for students
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_number TEXT PRIMARY KEY,
            name TEXT,
            image_path TEXT
        )
    ''')
    # Table for attendance
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            roll_number TEXT,
            date TEXT,
            status TEXT,
            FOREIGN KEY(roll_number) REFERENCES students(roll_number)
        )
    ''')
    conn.commit()
    conn.close()

def add_student(roll_number, name, image_path):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO students (roll_number, name, image_path) VALUES (?, ?, ?)",
        (roll_number, name, image_path)
    )
    conn.commit()
    conn.close()

def get_students():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    data = c.fetchall()
    conn.close()
    return data

def mark_attendance(roll_number, date, status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO attendance (roll_number, date, status) VALUES (?, ?, ?)",
        (roll_number, date, status)
    )
    conn.commit()
    conn.close()

def get_attendance_records():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    data = c.fetchall()
    conn.close()
    return data
