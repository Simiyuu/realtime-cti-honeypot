import os

MASK_DATA = os.getenv("MASK_DATA", "true").lower() != "false"


def mask_ip(ip):
    if not ip or not MASK_DATA:
        return ip
    if ":" in ip:
        return ":".join(ip.split(":")[:3]) + ":xxxx"
    parts = ip.split(".")
    if len(parts) == 4:
        return ".".join(parts[:3]) + ".xxx"
    return ip


def mask_password(pw):
    if pw is None or not MASK_DATA:
        return pw
    return pw[0] + "*" * (len(pw) - 1) if len(pw) > 1 else "*"
