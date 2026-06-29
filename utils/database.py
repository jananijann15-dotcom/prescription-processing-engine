import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db_data", "prescription.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            doctor_name TEXT,
            medicines TEXT,
            dosage TEXT,
            precautions TEXT,
            summary TEXT,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def insert_prescription(patient_name, doctor_name, medicines, dosage, precautions, summary, image_path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO prescriptions (
            patient_name, doctor_name, medicines, dosage,
            precautions, summary, image_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (patient_name, doctor_name, medicines, dosage, precautions, summary, image_path),
    )
    conn.commit()
    conn.close()
