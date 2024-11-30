import time
from utils.logging_helper import log_event

opening_gate_time = 3

class GateController:
    def __init__(self):
        self.state = "closed"

    def open_gate(self, initiator="server"):
        if self.state == "closed":
            self.state = "opening"
            log_event(initiator, "open_gate", {"state": "opening"})
            time.sleep(opening_gate_time)
            self.state = "open"
            log_event(initiator, "open_gate", {"state": "open"})
            return True
        else:
            log_event(initiator, "open_gate_failed", {"reason": "already_open"})
            return False

    def close_gate(self, initiator="server"):
        if self.state == "open":
            self.state = "closing"
            log_event(initiator, "close_gate", {"state": "closing"})
            time.sleep(opening_gate_time)
            self.state = "closed"
            log_event(initiator, "close_gate", {"state": "closed"})
            return True
        else:
            log_event(initiator, "close_gate_failed", {"reason": "already_closed"})
            return False

    def get_state(self):
        return self.state
