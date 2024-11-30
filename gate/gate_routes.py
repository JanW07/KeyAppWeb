from flask import Blueprint, jsonify, request, current_app
from middleware.middleware import check_authorization

gate_bp = Blueprint('gate', __name__)

@gate_bp.route('/open', methods=['POST'])
def open_gate():
    auth_response = check_authorization()
    if auth_response:
        return auth_response

    initiator = request.headers.get("Device-ID", "server")
    success = current_app.gate.open_gate(initiator)
    if success:
        return jsonify({"status": "success", "message": "Gate is opening."}), 200
    else:
        return jsonify({"status": "error", "message": "Gate is already open."}), 400

@gate_bp.route('/close', methods=['POST'])
def close_gate():
    auth_response = check_authorization()
    if auth_response:
        return auth_response

    initiator = request.headers.get("Device-ID", "server")
    success = current_app.gate.close_gate(initiator)
    if success:
        return jsonify({"status": "success", "message": "Gate is closing."}), 200
    else:
        return jsonify({"status": "error", "message": "Gate is already closed."}), 400

@gate_bp.route('/state', methods=['GET'])
def get_state():
    auth_response = check_authorization()
    if auth_response:
        return auth_response

    return jsonify({"state": current_app.gate.get_state()}), 200
