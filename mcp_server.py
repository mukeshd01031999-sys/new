from flask import Flask, request, jsonify
from agents import patient_agent, patient_id_agent, calendar_agent, doctor_availability_agent, appointment_agent

app = Flask(__name__)

# Minimal JSON-RPC 2.0 handler
@app.route("/jsonrpc", methods=["POST"])
def jsonrpc():
    j = request.get_json()
    if not j:
        return jsonify(error="invalid-json"), 400

    json_id = j.get("id")
    method = j.get("method")
    params = j.get("params", {})

    try:
        if method == "patient.handle_request":
            # params: {nl_text} or {structured}
            result = patient_agent.handle_patient_request(params.get("nl_text"), params.get("structured"))
        elif method == "patient_id.generate":
            result = patient_id_agent.generate_patient_id(params["name"], params.get("age"), params.get("symptoms",""))
        elif method == "doctor.find_by_specialization":
            result = doctor_availability_agent.find_doctor_by_specialization(params["specialization"])
        elif method == "calendar.list_slots":
            result = calendar_agent.list_slots(params["doctor_id"])
        elif method == "appointment.create":
            result = appointment_agent.create_appointment(params["patient_id"], params["doctor_id"], params["slot_iso"])
        elif method == "appointment.list":
            result = appointment_agent.list_appointments()
        else:
            return jsonify(jsonrpc="2.0", error={"code": -32601, "message": "Method not found"}, id=json_id)

        return jsonify(jsonrpc="2.0", result=result, id=json_id)
    except Exception as e:
        return jsonify(jsonrpc="2.0", error={"code": -32000, "message": str(e)}, id=json_id)

if __name__ == "__main__":
    # run on localhost:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
