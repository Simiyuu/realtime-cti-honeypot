import json
from collections import deque
from enricher import get_ip_geolocation
from sanitize import mask_ip, mask_password

LOG_FILE = "data/cowrie.json"
MAX_LINES = 5000

IMPORTANT_EVENTS = [
    "cowrie.session.connect",
    "cowrie.login.success",
    "cowrie.login.failed",
    "cowrie.command.input",
    "cowrie.session.file_download",
    "cowrie.session.closed"
]

def parse_logs():
    parsed_events = []

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = deque(f, maxlen=MAX_LINES)
    except FileNotFoundError:
        return []

    for line in lines:
        try:
            event = json.loads(line.strip())
        except json.JSONDecodeError:
            continue

        if event.get("eventid") not in IMPORTANT_EVENTS:
            continue

        src_ip = event.get("src_ip")
        geolocation = get_ip_geolocation(src_ip) if src_ip else None

        parsed_events.append({
            "session": event.get("session"),
            "timestamp": event.get("timestamp"),
            "event_type": event.get("eventid"),
            "src_ip": mask_ip(src_ip),
            "src_port": event.get("src_port"),
            "protocol": event.get("protocol"),
            "username": event.get("username"),
            "password": mask_password(event.get("password")),
            "command": event.get("input"),
            "download_url": event.get("url"),
            "file_hash": event.get("shasum"),
            "duration_ms": event.get("duration_ms"),
            "geolocation": geolocation
        })

    return parsed_events

if __name__ == "__main__":
    events = parse_logs()
    print(f"Events parsed: {len(events)}")
    for e in events[:5]:
        print(e["event_type"], e["src_ip"], e["password"])
        