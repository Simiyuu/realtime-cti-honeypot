import sys
import time
from db import get_conn, init_schema, parse_ts
from parser import parse_logs

INSERT = """
INSERT IGNORE INTO events
(session_id, ts, event_type, src_ip_masked, src_port, protocol, username,
 password_masked, command, download_url, file_hash, duration_ms,
 country, country_code, city, isp, latitude, longitude)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""


def clip(value, n):
    return value[:n] if isinstance(value, str) else value


def to_row(e):
    g = e.get("geolocation") or {}
    return (
        clip(e["session"], 32),
        parse_ts(e["timestamp"]),
        clip(e["event_type"], 64),
        clip(e.get("src_ip"), 45),
        e.get("src_port"),
        clip(e.get("protocol"), 16),
        clip(e.get("username"), 128),
        clip(e.get("password"), 128),
        e.get("command"),
        e.get("download_url"),
        clip(e.get("file_hash"), 64),
        e.get("duration_ms"),
        clip(g.get("country"), 64),
        clip(g.get("country_code"), 4),
        clip(g.get("city"), 128),
        clip(g.get("isp"), 255),
        g.get("latitude"),
        g.get("longitude"),
    )


def ingest_once():
    events = parse_logs()
    rows = [to_row(e) for e in events if e.get("session") and e.get("timestamp")]
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.executemany(INSERT, rows)
            inserted = cur.rowcount
        conn.commit()
    finally:
        conn.close()
    print(f"parsed {len(rows)} events, inserted {inserted} new")


def stats():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*), MIN(ts), MAX(ts) FROM events")
            print("total, first, last:", cur.fetchone())
            cur.execute("SELECT event_type, COUNT(*) FROM events GROUP BY event_type ORDER BY 2 DESC")
            for row in cur.fetchall():
                print(row)
            cur.execute("SELECT country, COUNT(*) FROM events GROUP BY country ORDER BY 2 DESC LIMIT 5")
            print("top countries:", cur.fetchall())
    finally:
        conn.close()


if __name__ == "__main__":
    init_schema()
    if "--stats" in sys.argv:
        stats()
    elif "--loop" in sys.argv:
        interval = int(sys.argv[sys.argv.index("--loop") + 1])
        while True:
            ingest_once()
            time.sleep(interval)
    else:
        ingest_once()
        
