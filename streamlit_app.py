import streamlit as st
import requests
import json

RPC_URL = "http://localhost:5000/jsonrpc"

st.title("Doctor Appointment — PoC (MCP JSON-RPC)")

mode = st.radio("Input mode", ["Natural language", "Structured"])

if mode == "Natural language":
    nl = st.text_area("Describe your appointment request (e.g. 'I need a GP tomorrow at 10am, name John, age 30, symptoms fever')", height=120)
    if st.button("Request appointment (NL)"):
        payload = {"jsonrpc":"2.0","method":"patient.handle_request","params":{"nl_text":nl},"id":1}
        r = requests.post(RPC_URL, json=payload)
        st.write("Response status:", r.status_code)
        st.json(r.json())
else:
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    specialization = st.text_input("Specialization (e.g. General Physician)")
    pref_time = st.text_input("Preferred time (ISO: YYYY-MM-DDTHH:MM) e.g. 2025-10-01T10:00")
    symptoms = st.text_area("Symptoms")
    if st.button("Request appointment (structured)"):
        structured = {
            "name": name,
            "age": age,
            "specialization": specialization,
            "preferred_time": pref_time,
            "symptoms": symptoms
        }
        payload = {"jsonrpc":"2.0","method":"patient.handle_request","params":{"structured":structured},"id":1}
        r = requests.post(RPC_URL, json=payload)
        st.write("Response status:", r.status_code)
        st.json(r.json())

st.markdown("---")
if st.button("List appointments"):
    payload = {"jsonrpc":"2.0","method":"appointment.list","params":{},"id":2}
    r = requests.post(RPC_URL, json=payload)
    st.json(r.json())
