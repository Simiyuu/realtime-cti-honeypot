from flask import Flask, jsonify
from parser import parse_logs

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "Honeypot API running",
        "endpoints": [
            "/api/events - all parsed attack events",
            "/api/summary - attack summary statistics"
        ]
    })

@app.route("/api/events")
def get_events():
    events = parse_logs()
    return jsonify({
        "total": len(events),
        "events": events
    })

@app.route("/api/summary")
def get_summary():
    events = parse_logs()
    
    commands = [e["command"] for e in events if e["command"]]
    logins = [e for e in events if e["event_type"] == "cowrie.login.success"]
    downloads = [e for e in events if e["event_type"] == "cowrie.session.file_download"]
    connections = [e for e in events if e["event_type"] == "cowrie.session.connect"]
    
    return jsonify({
        "total_events": len(events),
        "total_connections": len(connections),
        "successful_logins": len(logins),
        "commands_executed": len(commands),
        "file_downloads": len(downloads),
        "commands_list": commands,
        "credentials_captured": [
            {"username": e["username"], "password": e["password"]} 
            for e in logins
        ]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)