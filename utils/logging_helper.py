import logging
import os
import json
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

LOG_FILE = os.path.join("gate_logs.txt")

def setup_logger():
    logger = logging.getLogger('event_logger')
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

logger = setup_logger()


def get_initiator(action, url, headers):
    if action and "auth" in action:
        if "login" in action or "logout" in action:
            return "user"
    if action and "gate" in action:
        if "open" in action or "close" in action:
            return "server"

    if url and "static" in url:
        return "server"

    return "server"

def log_event(initiator, action, metadata=None):

    if initiator == "Unknown":
        initiator = get_initiator(action, metadata.get("url") if metadata else None, metadata.get("headers") if metadata else None)

    event = {
        "timestamp": datetime.now().isoformat(),
        "initiator": initiator,
        "action": action,
        "metadata": metadata or {},
    }

    logger.info(json.dumps(event))


def clean_old_logs():
    """Remove logs older than 1 month."""
    cutoff_date = datetime.now() - timedelta(days=30)
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log_file:
            lines = log_file.readlines()
        
        new_logs = []
        for line in lines:
            try:
                log_entry = json.loads(line)
                log_date = datetime.fromisoformat(log_entry.get("timestamp"))
                if log_date >= cutoff_date:
                    new_logs.append(line)
            except (ValueError, KeyError):
                continue

        with open(LOG_FILE, "w") as log_file:
            log_file.writelines(new_logs)
