from dotenv import load_dotenv
load_dotenv()

import os, sys, datetime
from functools import wraps
from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
from werkzeug.security import check_password_hash

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from store import fetch_events, fetch_summary


app = Flask(__name__)
CORS(app)

JWT_SECRET = os.getenv("JWT_SECRET")
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_HASH = os.getenv("ADMIN_PASSWORD_HASH")
if not (JWT_SECRET and ADMIN_USER and ADMIN_HASH):
    raise SystemExit("Missing JWT_SECRET, ADMIN_USER or ADMIN_PASSWORD_HASH in .env")


def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return jsonify(error="unauthorized"), 401
        try:
            jwt.decode(header[7:], JWT_SECRET, algorithms=["HS256"])
        except jwt.PyJWTError:
            return jsonify(error="unauthorized"), 401
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def home():
    return jsonify({"status": "Honeypot API running"})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    ok = data.get("username") == ADMIN_USER and check_password_hash(
        ADMIN_HASH, data.get("password", ""))
    if not ok:
        return jsonify(error="invalid credentials"), 401
    token = jwt.encode(
        {"sub": ADMIN_USER,
         "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=8)},
        JWT_SECRET, algorithm="HS256")
    return jsonify(token=token)


@app.route("/api/events")
@require_auth
def get_events():
    events = fetch_events()
    return jsonify({"total": len(events), "events": events})



@app.route("/api/summary")
@require_auth
def get_summary():
    return jsonify(fetch_summary())



@app.route("/api/attackers")
@require_auth
def get_attackers():
    events = fetch_events()
    attackers = {}
    for e in events:
        ip = e.get("src_ip")
        if not ip:
            continue
        a = attackers.setdefault(ip, {
            "ip": ip, "geolocation": e.get("geolocation"), "total_events": 0,
            "commands": [], "login_attempts": [], "download_attempts": [],
            "first_seen": e["timestamp"], "last_seen": e["timestamp"]})
        a["total_events"] += 1
        a["last_seen"] = e["timestamp"]
        if e.get("command"):
            a["commands"].append(e["command"])
        if e.get("username"):
            a["login_attempts"].append(
                {"username": e["username"], "password": e["password"]})
        if e.get("download_url"):
            a["download_attempts"].append(e["download_url"])
    return jsonify({"total_unique_attackers": len(attackers),
                    "attackers": list(attackers.values())})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
    