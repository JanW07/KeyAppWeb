from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from gate_controller import GateController
from device_manager import DeviceManager

app = Flask(__name__)
gate = GateController()
device_manager = DeviceManager()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

SERVER_TOKEN = "my_server_token"
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin"

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return "Invalid credentials, please try again."
    return '''
        <form method="post">
            <label>Username: <input type="text" name="username"></label><br>
            <label>Password: <input type="password" name="password"></label><br>
            <button type="submit">Login</button>
        </form>
    '''

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Decorator to protect routes
def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# Middleware to check if device is authorized or if it's a server request
def check_authorization():
    # Check if the request contains the server token
    token = request.headers.get('Authorization')
    if token == SERVER_TOKEN:
        # If the server token is present, skip device authorization
        return None

    # Otherwise, check device authorization
    hashed_id = request.headers.get('Device-ID')
    if not hashed_id or not device_manager.is_authorized(hashed_id):
        # If the device is not authorized, deny access without adding it to DeviceManager
        return jsonify({"status": "error", "message": "Unauthorized device."}), 403
    return None

@app.route('/')
@login_required
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
@login_required
def devices_page():
    return render_template('devices.html')

# New endpoint to handle initial device registration
@app.route('/authenticate', methods=['POST'])
def authenticate():
    hashed_id = request.headers.get('Device-ID')
    device_info = request.get_json()  # Expect JSON data for device info

    if not hashed_id or not device_info:
        return jsonify({"status": "error", "message": "Device-ID header or device info is missing."}), 400

    # Check if device is already known
    if device_manager.is_authorized(hashed_id) or hashed_id in device_manager.devices:
        return jsonify({"status": "info", "message": "Device already known."}), 200

    # Add the device info to DeviceManager and respond
    device_manager.add_device(hashed_id, device_info)
    print(f"New device registered: {device_info}")
    return jsonify({"status": "success", "message": "Device registered successfully."}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
