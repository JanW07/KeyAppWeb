from flask import request, jsonify, current_app
from utils.logging_helper import log_event

SERVER_TOKEN = "my_server_token"

def check_authorization():
    token = request.headers.get('Authorization')
    if token == SERVER_TOKEN:
        return None
    hashed_id = request.headers.get('Device-ID')
    if not hashed_id or not current_app.device_manager.is_authorized(hashed_id):
        return jsonify({"status": "error", "message": "Unauthorized device."}), 403
    return None


def log_request_middleware(app):
    """Middleware to log requests."""
    @app.before_request
    def log_request():
        # Extract relevant info
        action = request.endpoint
        
        # Skip logging specific actions
        if action == "gate.get_state":
            return  # Do not log this action
        
        device_id = request.headers.get("Device-ID", "Unknown")
        metadata = {
            "method": request.method,
            "url": request.url,
            "headers": dict(request.headers),
        }
        log_event(device_id, action, metadata)