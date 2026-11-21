import sys, time, json
sys.path.insert(0, "backend")
import parser as p
from enricher import get_ip_geolocation, _cache
from ingest import ingest_once

path = sys.argv[1]
ips = set()
with open(path, encoding="utf-8") as f:
    for line in f:
        try:
            ip = json.loads(line).get("src_ip")
        except json.JSONDecodeError:
            continue
        if ip:
            ips.add(ip)

print(len(ips), "unique IPs to look up")
failed = 0
for ip in sorted(ips):
    for attempt in range(3):
        _cache.pop(ip, None)
        g = get_ip_geolocation(ip)
        if g["is_private"]:
            break
        if g["country"] not in ("Lookup Failed", "Unknown"):
            time.sleep(1.5)
            break
        time.sleep(10)
    else:
        failed += 1

print("lookups failed:", failed)
p.LOG_FILE = path
p.MAX_LINES = 10**9
ingest_once()
