from flask import request, jsonify, current_app

SERVER_TOKEN = "my_server_token"

def check_authorization():
    token = request.headers.get('Authorization')
    if token == SERVER_TOKEN:
        return None
    hashed_id = request.headers.get('Device-ID')
    if not hashed_id or not current_app.device_manager.is_authorized(hashed_id):
        return jsonify({"status": "error", "message": "Unauthorized device."}), 403
    return None
