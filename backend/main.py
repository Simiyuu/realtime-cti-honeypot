from flask import Flask, jsonify
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import parse_logs

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "Honeypot API running",
        "project": "Real-Time Cyber Threat Intelligence Gathering and Visualization via Honeypot Deployment",
        "endpoints": [
            "/api/events - all parsed attack events with geolocation",
            "/api/summary - attack summary statistics",
            "/api/attackers - unique attacker IPs and their locations"
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
            {
                "username": e["username"],
                "password": e["password"]
            }
            for e in logins
        ]
    })

@app.route("/api/attackers")
def get_attackers():
    events = parse_logs()
    
    attackers = {}
    
    for event in events:
        ip = event.get("src_ip")
        if not ip:
            continue
            
        if ip not in attackers:
            attackers[ip] = {
                "ip": ip,
                "geolocation": event.get("geolocation"),
                "total_events": 0,
                "commands": [],
                "login_attempts": [],
                "download_attempts": [],
                "first_seen": event.get("timestamp"),
                "last_seen": event.get("timestamp")
            }
        
        attackers[ip]["total_events"] += 1
        attackers[ip]["last_seen"] = event.get("timestamp")
        
        if event.get("command"):
            attackers[ip]["commands"].append(event["command"])
            
        if event.get("username"):
            attackers[ip]["login_attempts"].append({
                "username": event["username"],
                "password": event["password"]
            })
            
        if event.get("download_url"):
            attackers[ip]["download_attempts"].append(event["download_url"])
    
    return jsonify({
        "total_unique_attackers": len(attackers),
        "attackers": list(attackers.values())
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)