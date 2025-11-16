# database.py
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import secrets
import string

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
        print("DB initialized with seed data.")
    finally:
        conn.close()

def row_to_dict(row):
    return dict(row) if row else None

def rows_to_list(rows):
    return [row_to_dict(r) for r in rows]

# === AUTH ===
def get_user_by_username(username: str):
    conn = get_connection()
    try:
        cur = conn.execute("SELECT * FROM users WHERE username = ? AND is_active = 1", (username,))
        return row_to_dict(cur.fetchone())
    finally:
        conn.close()

def get_user_by_email(email: str):
    conn = get_connection()
    try:
        cur = conn.execute("SELECT * FROM users WHERE email = ? AND is_active = 1", (email,))
        return row_to_dict(cur.fetchone())
    finally:
        conn.close()

# === PASSWORD RESET ===
def generate_reset_token():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

def request_password_reset(email: str):
    user = get_user_by_email(email)
    if not user:
        return None
    token = generate_reset_token()
    expires = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    conn = get_connection()
    try:
        conn.execute("INSERT INTO password_resets (user_id, token, expires_at) VALUES (?, ?, ?)", 
                     (user["id"], token, expires))
        conn.commit()
        return token
    finally:
        conn.close()

# === TEACHER & STUDENT ===
def get_teacher_by_user_id(user_id: int):
    conn = get_connection()
    try:
        cur = conn.execute("SELECT t.*, u.full_name FROM teachers t JOIN users u ON u.id = t.user_id WHERE t.user_id = ?", (user_id,))
        return row_to_dict(cur.fetchone())
    finally:
        conn.close()

def get_student_by_user_id(user_id: int):
    conn = get_connection()
    try:
        cur = conn.execute("SELECT s.*, u.full_name FROM students s JOIN users u ON u.id = s.user_id WHERE s.user_id = ?", (user_id,))
        return row_to_dict(cur.fetchone())
    finally:
        conn.close()

# === CLASS & SUBJECT ===
def get_classes_for_teacher(teacher_id: int):
    conn = get_connection()
    try:
        cur = conn.execute("""
            SELECT cs.id AS class_subject_id, c.id AS class_id, c.class_code, c.class_name,
                   s.id AS subject_id, s.subject_code, s.subject_name
            FROM class_subjects cs
            JOIN classes c ON c.id = cs.class_id
            JOIN subjects s ON s.id = cs.subject_id
            WHERE cs.teacher_id = ?
        """, (teacher_id,))
        return rows_to_list(cur.fetchall())
    finally:
        conn.close()

def get_students_in_class(class_id: int):
    conn = get_connection()
    try:
        cur = conn.execute("""
            SELECT s.id AS student_id, s.student_code, u.full_name, s.gender, u.email
            FROM students s JOIN users u ON u.id = s.user_id
            WHERE s.class_id = ?
        """, (class_id,))
        return rows_to_list(cur.fetchall())
    finally:
        conn.close()

# === SESSION ===
def create_attendance_session(class_subject_id, session_code, date_str, created_by):
    conn = get_connection()
    try:
        cur = conn.execute("""
            INSERT INTO attendance_sessions (class_subject_id, session_code, date, status, created_by)
            VALUES (?, ?, ?, 'ACTIVE', ?)
        """, (class_subject_id, session_code, date_str, created_by))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def get_open_session_for_class_subject(class_subject_id):
    conn = get_connection()
    try:
        cur = conn.execute("SELECT * FROM attendance_sessions WHERE class_subject_id = ? AND status = 'ACTIVE'", (class_subject_id,))
        return row_to_dict(cur.fetchone())
    finally:
        conn.close()

def close_attendance_session(session_id):
    conn = get_connection()
    try:
        conn.execute("UPDATE attendance_sessions SET status = 'CLOSED', end_time = CURRENT_TIMESTAMP WHERE id = ?", (session_id,))
        conn.commit()
    finally:
        conn.close()

# === ATTENDANCE ===
def upsert_attendance_record(session_id, student_id, status, note, updated_by):
    conn = get_connection()
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("""
            INSERT OR REPLACE INTO Attendance (session_id, student_id, status, note, marked_at, updated_at, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session_id, student_id, status, note, now, now, updated_by))
        conn.commit()
    finally:
        conn.close()

def get_attendance_records_for_session(session_id):
    conn = get_connection()
    try:
        cur = conn.execute("""
            SELECT ar.*, s.student_code, u.full_name
            FROM Attendance ar
            JOIN students s ON s.id = ar.student_id
            JOIN users u ON u.id = s.user_id
            WHERE ar.session_id = ?
        """, (session_id,))
        return rows_to_list(cur.fetchall())
    finally:
        conn.close()

# === STUDENT TỰ ĐIỂM DANH ===
def student_mark_attendance(student_id, session_id, status="PRESENT", note=None):
    conn = get_connection()
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("""
            INSERT OR REPLACE INTO Attendance (session_id, student_id, status, note, marked_at)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, student_id, status, note, now))
        conn.commit()
    finally:
        conn.close()

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
        return rows_to_list(cur.fetchall())
    finally:
        conn.close()

# === BÁO CÁO TỔNG HỢP TOÀN TRƯỜNG ===
def get_school_attendance_report(start_date=None, end_date=None):
    conn = get_connection()
    try:
        query = """
            SELECT 
                c.class_code,
                c.class_name,
                COUNT(DISTINCT s.id) AS total_students,
                COUNT(DISTINCT asess.id) AS total_sessions,
                SUM(CASE WHEN ar.status = 'PRESENT' THEN 1 ELSE 0 END) AS present_count,
                SUM(CASE WHEN ar.status LIKE 'ABSENT%' THEN 1 ELSE 0 END) AS absent_count,
                SUM(CASE WHEN ar.status = 'LATE' THEN 1 ELSE 0 END) AS late_count
            FROM classes c
            LEFT JOIN students s ON s.class_id = c.id
            LEFT JOIN class_subjects cs ON cs.class_id = c.id
            LEFT JOIN attendance_sessions asess ON asess.class_subject_id = cs.id AND asess.status = 'CLOSED'
            LEFT JOIN Attendance ar ON ar.session_id = asess.id
        """
        params = []
        if start_date:
            query += " AND asess.date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND asess.date <= ?"
            params.append(end_date)
        query += " GROUP BY c.id"
        
        cur = conn.execute(query, params)
        return rows_to_list(cur.fetchall())
    finally:
        conn.close()
