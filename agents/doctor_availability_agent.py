import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DOCTORS_FILE = os.path.join(DATA_DIR, "doctors.json")

def _read_doctors():
    with open(DOCTORS_FILE, "r") as f:
        return json.load(f)

def find_doctor_by_specialization(specialization):
    doctors = _read_doctors()
    for d in doctors:
        if d["specialization"].lower() == specialization.lower():
            return d
    return None

def check_slot(doctor_id, slot_iso):
    doctors = _read_doctors()
    for d in doctors:
        if d["doctor_id"] == doctor_id:
            return slot_iso in d.get("available_slots", [])
    return False
