import time

opening_gate_time=3

class GateController:
    def __init__(self):
        self.state = "closed"

    def open_gate(self):
        if self.state == "closed":
            self.state = "opening"
            time.sleep(opening_gate_time)  # Simulate the gate opening process
            self.state = "open"
            return True
        else:
            return False  # Gate is already open

    def close_gate(self):
        if self.state == "open":
            self.state = "closing"
            time.sleep(opening_gate_time)  # Simulate the gate closing process
            self.state = "closed"
            return True
        else:
            return False  # Gate is already closed

    def get_state(self):
        return self.state
