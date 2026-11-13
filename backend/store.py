import pymysql
from db import get_conn


def _iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


def _to_event(r):
    country = r["country"]
    return {
        "session": r["session_id"],
        "timestamp": _iso(r["ts"]),
        "event_type": r["event_type"],
        "src_ip": r["src_ip_masked"],
        "src_port": r["src_port"],
        "protocol": r["protocol"],
        "username": r["username"],
        "password": r["password_masked"],
        "command": r["command"],
        "download_url": r["download_url"],
        "file_hash": r["file_hash"],
        "duration_ms": r["duration_ms"],
        "geolocation": {
            "country": country,
            "country_code": r["country_code"],
            "city": r["city"],
            "isp": r["isp"],
            "latitude": r["latitude"],
            "longitude": r["longitude"],
            "is_private": country == "Local Network",
        },
    }


def fetch_events(limit=5000):
    conn = get_conn()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(
                "SELECT * FROM (SELECT * FROM events ORDER BY ts DESC, id DESC LIMIT %s) t "
                "ORDER BY ts ASC, id ASC", (limit,))
            return [_to_event(r) for r in cur.fetchall()]
    finally:
        conn.close()


def fetch_summary():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT event_type, COUNT(*) FROM events GROUP BY event_type")
            counts = dict(cur.fetchall())
            cur.execute("SELECT command FROM events WHERE command IS NOT NULL ORDER BY ts DESC LIMIT 50")
            commands = [r[0] for r in cur.fetchall()]
            cur.execute("SELECT username, password_masked FROM events "
                        "WHERE event_type='cowrie.login.success' ORDER BY ts DESC LIMIT 50")
            creds = [{"username": u, "password": p} for u, p in cur.fetchall()]
    finally:
        conn.close()
    return {
        "total_events": sum(counts.values()),
        "total_connections": counts.get("cowrie.session.connect", 0),
        "successful_logins": counts.get("cowrie.login.success", 0),
        "failed_logins": counts.get("cowrie.login.failed", 0),
        "sessions_closed": counts.get("cowrie.session.closed", 0),
        "commands_executed": counts.get("cowrie.command.input", 0),
        "file_downloads": counts.get("cowrie.session.file_download", 0),
        "commands_list": commands,
        "credentials_captured": creds,
    }

