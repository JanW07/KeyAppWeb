# extensions.py
from flask import Flask
from app.gate.gate_controller import GateController
from app.device.device_manager import DeviceManager

SERVER_TOKEN = "my_server_token"

app = Flask(__name__)
app.secret_key = 'your_secret_key'
gate = GateController()
device_manager = DeviceManager()
