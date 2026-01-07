from fastmcp import FastMCP
import sqlite3
import os
from pydantic import BaseModel, Field
from typing import List, Optional

# Initialize FastMCP Server
mcp = FastMCP("Hospital Operations Server")

# DB Helper
DB_PATH = os.path.join(os.path.dirname(__file__), "hospital.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

# --- TOOLS ---

@mcp.tool()
def get_patient_details(name: str) -> str:
    """
    Retrieve patient details by name. 
    Use this to verify identity and insurance before booking.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE name LIKE ?", (f"%{name}%",))
        patient = cursor.fetchone()
        
        if patient:
            return f"ID: {patient['id']} | Name: {patient['name']} | Insurance: {patient['insurance_id']} | Condition: {patient['condition_summary']}"
        else:
            return "Error: Patient not found in database."
    finally:
        conn.close()

@mcp.tool()
def list_available_slots(specialty: str = None) -> str:
    """
    List open appointment slots. 
    Can filter by specialty (e.g., 'Cardiology', 'Surgery', 'Diagnostic').
    Returns a formatted string of available slots.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM appointments WHERE status = 'open'"
        params = []
        
        if specialty:
            query += " AND specialty = ?"
            params.append(specialty)
            
        cursor.execute(query, params)
        slots = cursor.fetchall()
        
        if not slots:
            return "No available slots found."
            
        result = "Available Slots:\n"
        for slot in slots:
            result += f"[Slot ID: {slot['id']}] {slot['doctor_name']} ({slot['specialty']}) at {slot['slot_time']}\n"
        return result
    finally:
        conn.close()

@mcp.tool()
def book_appointment(slot_id: int, patient_id: int) -> str:
    """
    Book a specific slot for a patient.
    Requires valid slot_id and patient_id.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # 1. Verify Slot is Open
        cursor.execute("SELECT status FROM appointments WHERE id = ?", (slot_id,))
        slot = cursor.fetchone()
        if not slot:
            return "Error: Slot ID not found."
        if slot['status'] != 'open':
            return "Error: Slot is already booked."
            
        # 2. Verify Patient Exists
        cursor.execute("SELECT id FROM patients WHERE id = ?", (patient_id,))
        if not cursor.fetchone():
            return "Error: Patient ID not found."
            
        # 3. Execute Booking
        cursor.execute("UPDATE appointments SET status = 'booked', patient_id = ? WHERE id = ?", (patient_id, slot_id))
        conn.commit()
        
        return f"Success: Appointment confirmed. (Slot {slot_id} assigned to Patient {patient_id})"
    finally:
        conn.close()

if __name__ == "__main__":
    mcp.run()