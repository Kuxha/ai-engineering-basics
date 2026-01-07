import sqlite3
import os

# Ensure we create the DB in the same folder as this script
DB_PATH = os.path.join(os.path.dirname(__file__), "hospital.db")

def init_db():
    # Remove existing DB to ensure a clean state
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create Patients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        insurance_id TEXT NOT NULL,
        condition_summary TEXT
    )
    """)

    # 2. Create Appointments Table
    # status can be 'open' or 'booked'
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        slot_time TEXT NOT NULL,
        status TEXT DEFAULT 'open',
        patient_id INTEGER,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
    """)

    # 3. Seed Data: Patients
    patients = [
        ("John Doe", "INS-12345", "Chronic migraines, history of hypertension"),
        ("Jane Smith", "INS-98765", "Acute abdominal pain, possible appendicitis"),
        ("Alice Brown", "INS-55555", "Routine checkup, no known conditions")
    ]
    cursor.executemany("INSERT INTO patients (name, insurance_id, condition_summary) VALUES (?, ?, ?)", patients)

    # 4. Seed Data: Doctors & Slots
    appointments = [
        ("Dr. House", "Diagnostic", "2025-02-15 09:00", "open", None),
        ("Dr. House", "Diagnostic", "2025-02-15 10:00", "open", None),
        ("Dr. Strange", "Surgery", "2025-02-15 11:00", "open", None),
        ("Dr. Who", "Cardiology", "2025-02-16 14:00", "open", None),
        ("Dr. Quinn", "General Practice", "2025-02-16 09:00", "open", None)
    ]
    cursor.executemany("INSERT INTO appointments (doctor_name, specialty, slot_time, status, patient_id) VALUES (?, ?, ?, ?, ?)", appointments)

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()