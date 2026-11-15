import sys
sys.path.insert(0, "backend")
from db import get_conn

mode = sys.argv[1] if len(sys.argv) > 1 else "insert"
conn = get_conn()
cur = conn.cursor()

if mode == "insert":
    cur.execute(
        "INSERT INTO events (session_id, ts, event_type, src_ip_masked, "
        "country, country_code, city) "
        "VALUES ('wstest', NOW(6), 'cowrie.session.connect', "
        "'203.0.113.xxx', 'Test', 'TT', 'Test')"
    )
    conn.commit()
    print("inserted")
elif mode == "delete":
    cur.execute("DELETE FROM events WHERE session_id = 'wstest'")
    conn.commit()
    print("deleted", cur.rowcount)

conn.close()

