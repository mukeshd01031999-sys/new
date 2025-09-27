import os
from datetime import datetime
from agents.patient_id_agent import generate_patient_id
from agents.doctor_availability_agent import find_doctor_by_specialization, check_slot
from agents.calendar_agent import reserve_slot
from agents.appointment_agent import create_appointment

# optional usage of openai for free-text parsing
USE_LLM = True
OPENAI_KEY_ENV = "OPENAI_API_KEY"

def parse_nl_request_with_llm(nl_text):
    """
    PoC: minimal LLM parse - ask model to return JSON with keys:
      specialization, preferred_time (ISO like 2025-10-01T10:00), name, age, symptoms
    """
    try:
        import openai, os
        if OPENAI_KEY_ENV not in os.environ:
            raise RuntimeError("OPENAI_API_KEY not set")
        openai.api_key = os.environ[OPENAI_KEY_ENV]

        prompt = f"""Parse the following patient request into strict JSON with keys:
specialization, preferred_time (ISO), name, age, symptoms

Text:
\"\"\"{nl_text}\"\"\"

Return only valid JSON.
"""
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini", # change as needed
            messages=[{"role":"user","content":prompt}],
            temperature=0
        )
        content = resp["choices"][0]["message"]["content"]
        import json
        parsed = json.loads(content)
        return parsed
    except Exception as e:
        print("LLM parse failed:", e)
        return None

def handle_patient_request(nl_text=None, structured=None):
    """
    Either pass nl_text (natural language) OR structured dict:
    structured = {
      "specialization": "General Physician",
      "preferred_time": "2025-10-01T10:00",
      "name": "John",
      "age": 30,
      "symptoms": "fever"
    }
    """
    if structured is None:
        if USE_LLM and nl_text:
            parsed = parse_nl_request_with_llm(nl_text)
            if not parsed:
                raise RuntimeError("Failed to parse request")
            structured = parsed
        else:
            raise ValueError("Provide structured or enable LLM with nl_text")

    # 1) create patient id & record
    p = generate_patient_id(structured["name"], structured.get("age", None), structured.get("symptoms", ""))
    patient_id = p["patient_id"]

    # 2) find a doctor
    doc = find_doctor_by_specialization(structured["specialization"])
    if not doc:
        return {"error": "no_doctor_found"}

    # 3) check slot (we assume slot ISO contains date+time)
    slot_iso = structured["preferred_time"]
    available = check_slot(doc["doctor_id"], slot_iso)
    if not available:
        return {"error": "slot_not_available", "doctor": doc}

    # 4) reserve in calendar
    date_part = slot_iso.split("T")[0]
    time_part = slot_iso.split("T")[1]
    ok = reserve_slot(doc["doctor_id"], date_part, time_part)
    if not ok:
        return {"error": "failed_to_reserve_slot"}

    # 5) create appointment
    appt = create_appointment(patient_id, doc["doctor_id"], slot_iso)
    return {"appointment": appt, "patient": p, "doctor": doc}
