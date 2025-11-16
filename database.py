# database.py
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = "attendance.db"
SCHEMA_PATH = "schema.sql"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    if Path(DB_PATH).exists():
        return
    conn = get_connection()
    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
        print("DB + seed created.")
    finally:
        conn.close()

# === THÊM: CRUD CHO COURSE, LECTURER, ENROLLMENT ===
def get_all_courses():
    conn = get_connection()
    try:
        cur = conn.execute("SELECT * FROM Course")
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()

def get_all_lecturers():
    conn = get_connection()
    try:
        cur = conn.execute("SELECT l.*, u.full_name FROM Lecturer l JOIN users u ON l.user_id = u.id")
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()

def enroll_student(student_id, class_id, enrollment_date=None, status="Active"):
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO Enrollment (student_id, class_id, enrollment_date, status)
            VALUES (?, ?, ?, ?)
        """, (student_id, class_id, enrollment_date or datetime.now().date(), status))
        conn.commit()
    finally:
        conn.close()

# === STUDENT TỰ ĐIỂM DANH ===
def student_mark_attendance(student_id, session_id, status="PRESENT", note=None):
    conn = get_connection()
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("""
            INSERT OR REPLACE INTO Attendance (student_id, session_id, status, note, marked_at)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, session_id, status, note, now))
        conn.commit()
    finally:
        conn.close()

# === LẤY PHIÊN ĐIỂM DANH ĐANG MỞ CHO STUDENT ===
def get_open_sessions_for_student(student_id):
    conn = get_connection()
    try:
        cur = conn.execute("""
            SELECT s.*, c.class_code, sub.subject_name
            FROM attendance_sessions s
            JOIN class_subjects cs ON s.class_subject_id = cs.id
            JOIN classes c ON cs.class_id = c.id
            JOIN subjects sub ON cs.subject_id = sub.id
            JOIN Enrollment e ON e.class_id = c.id
            WHERE e.student_id = ? AND s.status = 'ACTIVE'
        """, (student_id,))
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()
