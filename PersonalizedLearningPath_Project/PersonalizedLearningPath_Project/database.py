import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).parent / "data" / "learning_path.db"

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course TEXT NOT NULL,
            concept TEXT NOT NULL,
            question TEXT NOT NULL,
            is_correct INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES students(id))""")

def create_student(name):
    clean = name.strip()
    if not clean:
        raise ValueError("Please enter a student name.")
    with connect() as conn:
        conn.execute("INSERT OR IGNORE INTO students(name) VALUES (?)", (clean,))
        row = conn.execute("SELECT id, name FROM students WHERE name=?", (clean,)).fetchone()
        return dict(row)

def get_students():
    with connect() as conn:
        return [dict(r) for r in conn.execute("SELECT id, name FROM students ORDER BY name")]

def save_attempt(student_id, course, concept, question, is_correct):
    with connect() as conn:
        conn.execute("INSERT INTO attempts(student_id,course,concept,question,is_correct) VALUES (?,?,?,?,?)",
                     (student_id, course, concept, question, int(is_correct)))

def get_history(student_id, course=None):
    sql = "SELECT course,concept,question,is_correct,created_at FROM attempts WHERE student_id=?"
    params = [student_id]
    if course:
        sql += " AND course=?"
        params.append(course)
    sql += " ORDER BY id"
    with connect() as conn:
        rows = conn.execute(sql, params).fetchall()
    return pd.DataFrame([dict(r) for r in rows],
                        columns=["course","concept","question","is_correct","created_at"])
