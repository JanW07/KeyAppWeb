import json
import os
from flask import Flask
from datetime import timedelta
from auth.auth import auth_bp
from gate.gate_routes import gate_bp
from device.device_routes import device_bp
from gate.gate_controller import GateController
from device.device_manager import DeviceManager

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    # Set session lifetime
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

    # Load config.json
    app.config['CREDENTIALS'] = load_config()

    # Initialize global instances
    app.gate = GateController()
    app.device_manager = DeviceManager()

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(gate_bp)
    app.register_blueprint(device_bp)

    return app
