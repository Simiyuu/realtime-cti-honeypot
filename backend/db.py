import os
from datetime import datetime
import pymysql
from dotenv import load_dotenv

load_dotenv()

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(32) NOT NULL,
    ts DATETIME(6) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    src_ip_masked VARCHAR(45),
    src_port INT,
    protocol VARCHAR(16),
    username VARCHAR(128),
    password_masked VARCHAR(128),
    command TEXT,
    download_url TEXT,
    file_hash VARCHAR(64),
    duration_ms INT,
    country VARCHAR(64),
    country_code VARCHAR(4),
    city VARCHAR(128),
    isp VARCHAR(255),
    latitude DOUBLE,
    longitude DOUBLE,
    UNIQUE KEY uq_event (session_id, ts, event_type),
    KEY idx_ts (ts),
    KEY idx_type (event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""


def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3307")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        autocommit=False,
    )


def init_schema():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def parse_ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
