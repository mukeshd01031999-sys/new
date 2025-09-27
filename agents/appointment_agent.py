import json
import uuid
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
APPT_FILE = os.path.join(DATA_DIR, "appointments.json")

def _read_appts():
    with open(APPT_FILE, "r") as f:
        return json.load(f)

def _write_appts(appts):
    with open(APPT_FILE, "w") as f:
        json.dump(appts, f, indent=2)

def create_appointment(patient_id, doctor_id, slot_iso):
    appts = _read_appts()
    aid = "A" + uuid.uuid4().hex[:6].upper()
    appt = {
        "appointment_id": aid,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "slot": slot_iso,
        "status": "confirmed",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    appts.append(appt)
    _write_appts(appts)
    return appt

def list_appointments():
    return _read_appts()
