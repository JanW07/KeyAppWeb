import hashlib
import json
import os

class DeviceManager:
    def __init__(self, file_path='devices.json'):
        self.file_path = file_path
        self.devices = self._load_devices()

    def _load_devices(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_devices(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.devices, f, indent=4)

    def hash_device_id(self, device_id):
        return hashlib.md5(device_id.encode()).hexdigest()

    def add_device(self, hashed_id, device_info):
        if hashed_id not in self.devices:
            self.devices[hashed_id] = {'info': device_info, 'authorized': False, 'unknown': True}
            self._save_devices()
            return True
        return False

    def authorize_device(self, hashed_id):
        if hashed_id in self.devices:
            self.devices[hashed_id]['authorized'] = True
            self.devices[hashed_id]['unknown'] = False
            self._save_devices()
            return True
        return False

    def block_device(self, hashed_id):
        if hashed_id in self.devices:
            self.devices[hashed_id]['authorized'] = False  # Mark the device as blocked
            self.devices[hashed_id]['unknown'] = False
            self._save_devices()
            return True
        return False

    def delete_device(self, hashed_id):
        """Delete a device from the list."""
        if hashed_id in self.devices:
            del self.devices[hashed_id]
            self._save_devices()
            return True
        return False

    def is_authorized(self, hashed_id):
        """Check if the device is authorized."""
        return self.devices.get(hashed_id, {}).get('authorized', False)

    def get_devices(self):
        # Organize devices into categories
        categorized_devices = {
            'authorized': {},
            'blocked': {},
            'unknown': {}
        }

        for device_id, device in self.devices.items():
            if device['authorized']:
                categorized_devices['authorized'][device_id] = device
            elif device['unknown']:
                categorized_devices['unknown'][device_id] = device
            else:
                categorized_devices['blocked'][device_id] = device

        return categorized_devices
