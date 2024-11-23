import json
import os
from datetime import datetime, timedelta

LOG_FILE = os.path.join("gate_logs.json")

def log_event(initiator, action, metadata=None):
    """Log an event to a JSON file with rotation."""
    timestamp = datetime.now().isoformat()
    event = {
        "initiator": initiator,  # Device ID or 'server'
        "metadata": metadata or {},
        "timestamp": timestamp
    }
    
    # Append the log event
    with open(LOG_FILE, "a") as log_file:
        log_file.write(json.dumps(event) + "\n")
    
    clean_old_logs()

def clean_old_logs():
    """Remove logs older than 1 month."""
    cutoff_date = datetime.now() - timedelta(days=30)
    new_logs = []
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log_file:
            for line in log_file:
                try:
                    log_entry = json.loads(line)
                    log_date = datetime.fromisoformat(log_entry["timestamp"])
                    if log_date >= cutoff_date:
                        new_logs.append(log_entry)
                except (ValueError, KeyError):
                    # Skip malformed lines
                    continue

        # Overwrite the log file with filtered entries
        with open(LOG_FILE, "w") as log_file:
            for entry in new_logs:
                log_file.write(json.dumps(entry) + "\n")
