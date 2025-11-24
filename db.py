# db.py
import sqlite3
from datetime import datetime
from typing import List, Tuple

DB_PATH = "attendance.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT UNIQUE,
            name TEXT,
            image_path TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT,
            name TEXT,
            status TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_student(roll: str, name: str, image_path: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO students (roll, name, image_path) VALUES (?, ?, ?)', (roll, name, image_path))
    conn.commit()
    conn.close()

def get_students() -> List[Tuple]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT roll, name, image_path FROM students ORDER BY roll')
    rows = c.fetchall()
    conn.close()
    return rows

def add_attendance(roll: str, name: str, status: str):
    ts = datetime.now().isoformat(timespec='seconds')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO attendance (roll, name, status, timestamp) VALUES (?, ?, ?, ?)', (roll, name, status, ts))
    conn.commit()
    conn.close()

def get_attendance(limit=500):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT roll, name, status, timestamp FROM attendance ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows
