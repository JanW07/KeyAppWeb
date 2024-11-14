from flask import Flask
from auth.auth import auth_bp
from gate.gate_routes import gate_bp
from device.device_routes import device_bp
from gate.gate_controller import GateController
from device.device_manager import DeviceManager

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    
    # Initialize global instances
    app.gate = GateController()
    app.device_manager = DeviceManager()

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(gate_bp)
    app.register_blueprint(device_bp)
    
    return app
