import getpass
import requests
import socketio

API = "http://127.0.0.1:5000"
pw = getpass.getpass("Admin password: ")
token = requests.post(f"{API}/api/login", json={"username": "admin", "password": pw}).json()["token"]

sio = socketio.Client()

@sio.event
def connect():
    print("connected")

@sio.on("update")
def on_update(msg):
    print("update:", len(msg["events"]), "new events, total_events =", msg["summary"]["total_events"])

sio.connect(API, auth={"token": token})
print("waiting for events (Ctrl+C to stop)...")
sio.wait()
