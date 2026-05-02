"""Seed the failures table with sample historical data."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

import psycopg2
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

FAILURES = [
    "memory leak caused latency spike after deployment",
    "high latency on /slow endpoint under load",
    "timeout errors when response exceeds 1 second",
    "CPU spike due to unoptimized database query in new PR",
    "connection pool exhaustion after deploying auth service changes",
    "cascading failure from retry storm on payment endpoint",
    "disk I/O saturation from excessive logging in debug mode",
    "race condition causing intermittent 500 errors on checkout",
]

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": os.getenv("POSTGRES_DB", "aegis"),
    "user": os.getenv("POSTGRES_USER", "aegis"),
    "password": os.getenv("POSTGRES_PASSWORD", "aegis"),
}


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS failures (
            id SERIAL PRIMARY KEY,
            description TEXT NOT NULL,
            embedding VECTOR(384)
        )
    """)

    cur.execute("SELECT COUNT(*) FROM failures")
    count = cur.fetchone()[0]
    if count > 0:
        print(f"Table already has {count} rows, skipping seed.")
        conn.close()
        return

    for desc in FAILURES:
        vec = model.encode(desc).tolist()
        cur.execute(
            "INSERT INTO failures (description, embedding) VALUES (%s, %s::vector)",
            (desc, str(vec)),
        )
        print(f"  Inserted: {desc}")

    conn.commit()
    conn.close()
    print(f"\nSeeded {len(FAILURES)} failures.")


if __name__ == "__main__":
    main()
