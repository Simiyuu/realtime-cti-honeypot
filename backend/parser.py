import json
from enricher import get_ip_geolocation

LOG_FILE = "data/cowrie.json"

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
    
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                event = json.loads(line.strip())
                
                if event.get("eventid") not in IMPORTANT_EVENTS:
                    continue
                
                src_ip = event.get("src_ip")
                geolocation = get_ip_geolocation(src_ip) if src_ip else None
                
                parsed_event = {
                    "session": event.get("session"),
                    "timestamp": event.get("timestamp"),
                    "event_type": event.get("eventid"),
                    "src_ip": src_ip,
                    "src_port": event.get("src_port"),
                    "protocol": event.get("protocol"),
                    "username": event.get("username"),
                    "password": event.get("password"),
                    "command": event.get("input"),
                    "download_url": event.get("url"),
                    "file_hash": event.get("shasum"),
                    "duration_ms": event.get("duration_ms"),
                    "message": event.get("message"),
                    "geolocation": geolocation
                }
                
                parsed_events.append(parsed_event)
                
            except json.JSONDecodeError:
                continue
    
    return parsed_events

if __name__ == "__main__":
    events = parse_logs()
    print(f"Total events parsed: {len(events)}\n")
    for event in events:
        print(f"[{event['timestamp']}] {event['event_type']}")
        if event['src_ip']:
            print(f"  Source IP: {event['src_ip']}")
        if event.get('geolocation'):
            geo = event['geolocation']
            print(f"  Location: {geo['city']}, {geo['region']}, {geo['country']}")
            print(f"  ISP: {geo['isp']}")
            print(f"  Coordinates: {geo['latitude']}, {geo['longitude']}")
        if event['username']:
            print(f"  Login attempt: {event['username']} / {event['password']}")
        if event['command']:
            print(f"  Command: {event['command']}")
        if event['download_url']:
            print(f"  Download attempt: {event['download_url']}")
        print()