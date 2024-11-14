from flask import Blueprint, jsonify, request, current_app, render_template

# Define a Blueprint for device-related routes
device_bp = Blueprint('device', __name__)

@device_bp.route('/devices', methods=['GET'])
def list_devices():
    """List all devices, categorized by status (authorized, blocked, unknown)."""
    devices = current_app.device_manager.get_devices()
    return jsonify(devices), 200

@device_bp.route('/authorize_device/<hashed_id>', methods=['POST'])
def authorize_device(hashed_id):
    """Authorize a device by its hashed ID."""
    if current_app.device_manager.authorize_device(hashed_id):
        return jsonify({'success': True, 'message': 'Device authorized successfully.'}), 200
    return jsonify({'success': False, 'message': 'Device not found.'}), 404

@device_bp.route('/block_device/<hashed_id>', methods=['POST'])
def block_device(hashed_id):
    """Block a device by its hashed ID."""
    if current_app.device_manager.block_device(hashed_id):
        return jsonify({'success': True, 'message': 'Device blocked successfully.'}), 200
    return jsonify({'success': False, 'message': 'Device not found.'}), 404

@device_bp.route('/delete_device/<hashed_id>', methods=['DELETE'])
def delete_device(hashed_id):
    """Delete a device from the system by its hashed ID."""
    if current_app.device_manager.delete_device(hashed_id):
        return jsonify({'success': True, 'message': 'Device deleted successfully.'}), 200
    return jsonify({'success': False, 'message': 'Device not found.'}), 404

@device_bp.route('/authenticate', methods=['POST'])
def authenticate():
    """Authenticate a new device or check if an existing device is already known."""
    hashed_id = request.headers.get('Device-ID')
    device_info = request.get_json()  # Expect JSON data for device info

    if not hashed_id or not device_info:
        return jsonify({"status": "error", "message": "Device-ID header or device info is missing."}), 400

    # Check if the device is already known
    if current_app.device_manager.is_authorized(hashed_id) or hashed_id in current_app.device_manager.devices:
        return jsonify({"status": "info", "message": "Device already known."}), 200

    # Add the device info to DeviceManager and respond
    current_app.device_manager.add_device(hashed_id, device_info)
    return jsonify({"status": "success", "message": "Device registered successfully."}), 201

@device_bp.route('/devices_page')
def devices_page():
    """Render the device management page."""
    return render_template('devices.html')
