import json
import uuid
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PATIENTS_FILE = os.path.join(DATA_DIR, "patients.json")

def _read_patients():
    with open(PATIENTS_FILE, "r") as f:
        return json.load(f)

def _write_patients(patients):
    with open(PATIENTS_FILE, "w") as f:
        json.dump(patients, f, indent=2)

def generate_patient_id(name, age, symptoms):
    patients = _read_patients()
    pid = "P" + uuid.uuid4().hex[:6].upper()
    new_patient = {
        "patient_id": pid,
        "name": name,
        "age": age,
        "symptoms": symptoms
    }
    patients.append(new_patient)
    _write_patients(patients)
    return new_patient

def get_patient(patient_id):
    patients = _read_patients()
    for p in patients:
        if p["patient_id"] == patient_id:
            return p
    return None
