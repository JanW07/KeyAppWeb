from flask import Blueprint, jsonify, current_app

device_bp = Blueprint('device', __name__)

@device_bp.route('/devices', methods=['GET'])
def list_devices():
    return jsonify(current_app.device_manager.get_devices()), 200

@device_bp.route('/authorize_device/<hashed_id>', methods=['POST'])
def authorize_device(hashed_id):
    if device_manager.authorize_device(hashed_id):
        return jsonify({'success': True, 'message': 'Device authorized successfully.'}), 200
    return jsonify({'success': False, 'message': 'Device not found.'}), 404

@device_bp.route('/block_device/<hashed_id>', methods=['POST'])
def block_device(hashed_id):
    if device_manager.block_device(hashed_id):
        return jsonify({'success': True, 'message': 'Device blocked successfully.'}), 200
    return jsonify({'success': False, 'message': 'Device not found.'}), 404

@device_bp.route('/delete_device/<hashed_id>', methods=['DELETE'])
def delete_device(hashed_id):
    if device_manager.delete_device(hashed_id):
        return jsonify({'success': True, 'message': 'Device deleted successfully.'}), 200
    return jsonify({'success': False, 'message': 'Device not found.'}), 404
