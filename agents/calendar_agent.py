import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CAL_FILE = os.path.join(DATA_DIR, "calendar.json")

def _read_calendar():
    with open(CAL_FILE, "r") as f:
        return json.load(f)

def _write_calendar(cal):
    with open(CAL_FILE, "w") as f:
        json.dump(cal, f, indent=2)

def list_slots(doctor_id):
    cal = _read_calendar()
    for entry in cal:
        if entry["doctor_id"] == doctor_id:
            return entry["slots"]
    return {}

def reserve_slot(doctor_id, date, time_str):
    cal = _read_calendar()
    for entry in cal:
        if entry["doctor_id"] == doctor_id and entry["date"] == date:
            if entry["slots"].get(time_str) == "free":
                entry["slots"][time_str] = "reserved"
                _write_calendar(cal)
                return True
            return False
    return False

def free_slot(doctor_id, date, time_str):
    cal = _read_calendar()
    for entry in cal:
        if entry["doctor_id"] == doctor_id and entry["date"] == date:
            entry["slots"][time_str] = "free"
            _write_calendar(cal)
            return True
    return False
