from flask import Flask, render_template, jsonify
from gate_controller import GateController

app = Flask(__name__)
gate = GateController()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/open', methods=['POST'])
def open_gate():
    print(f"Current gate state before opening: {gate.get_state()}")
    if gate.open_gate():
        return jsonify({"status": "open"}), 200
    return jsonify({"status": "error", "message": "Gate is already open."}), 400

@app.route('/close', methods=['POST'])
def close_gate():
    print(f"Current gate state before closing: {gate.get_state()}")
    if gate.close_gate():
        return jsonify({"status": "closed"}), 200
    return jsonify({"status": "error", "message": "Gate is already closed."}), 400

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify({"state": gate.get_state()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('flask.crt', 'flask.key'))
