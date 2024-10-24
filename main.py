from flask import Flask, render_template, jsonify, request
from gate_controller import GateController
from device_manager import DeviceManager

app = Flask(__name__)
gate = GateController()
device_manager = DeviceManager()

# Define a server secret token to bypass authorization for internal requests
SERVER_TOKEN = "my_server_token"

# Middleware to check if device is authorized or if it's a server request
def check_authorization():
    # Check if the request contains the server token
    token = request.headers.get('Authorization')
    if token == SERVER_TOKEN:
        # If the server token is present, skip device authorization
        return None

    # Otherwise, check device authorization
    hashed_id = request.headers.get('Device-Id')
    if not hashed_id or not device_manager.is_authorized(hashed_id):
        # Store the device info and deny access if unauthorized
        device_info = request.get_json()
        if device_manager.add_device(hashed_id, device_info):
            print(f"New device detected: {device_info}, awaiting authorization.")
        return jsonify({"status": "error", "message": "Unauthorized device."}), 403
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/open', methods=['POST'])
def open_gate():
    # Check authorization (server bypass or device auth)
    auth_response = check_authorization()
    if auth_response:
        return auth_response

    print(f"Current gate state before opening: {gate.get_state()}")
    if gate.open_gate():
        return jsonify({"status": "open"}), 200
    return jsonify({"status": "error", "message": "Gate is already open."}), 400

@app.route('/close', methods=['POST'])
def close_gate():
    # Check authorization (server bypass or device auth)
    auth_response = check_authorization()
    if auth_response:
        return auth_response

    print(f"Current gate state before closing: {gate.get_state()}")
    if gate.close_gate():
        return jsonify({"status": "closed"}), 200
    return jsonify({"status": "error", "message": "Gate is already closed."}), 400

@app.route('/state', methods=['GET'])
def get_state():
    # Check authorization (server bypass or device auth)
    auth_response = check_authorization()
    if auth_response:
        return auth_response

    return jsonify({"state": gate.get_state()}), 200

@app.route('/devices', methods=['GET'])
def list_devices():
    # Admin route to list all devices (for authorization purposes)
    return jsonify(device_manager.get_devices()), 200

@app.route('/authorize_device/<hashed_id>', methods=['POST'])
def authorize_device(hashed_id):
    if device_manager.authorize_device(hashed_id):
        return jsonify({'success': True, 'message': 'Device authorized successfully.'}), 200
    return jsonify({'success': False, 'message': 'Device not found.'}), 404

@app.route('/block_device/<hashed_id>', methods=['POST'])
def block_device(hashed_id):
    if device_manager.block_device(hashed_id):
        return jsonify({'success': True, 'message': 'Device blocked successfully.'}), 200
    return jsonify({'success': False, 'message': 'Device not found.'}), 404

@app.route('/delete_device/<hashed_id>', methods=['DELETE'])
def delete_device(hashed_id):
    if device_manager.delete_device(hashed_id):
        return jsonify({'success': True, 'message': 'Device deleted successfully.'}), 200
    return jsonify({'success': False, 'message': 'Device not found.'}), 404

@app.route('/devices_page')
def devices_page():
    return render_template('devices.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
