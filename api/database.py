import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

DB_CONFIG = {
    "host": os.getenv("AMIP_DB_HOST", "localhost"),
    "port": int(os.getenv("AMIP_DB_PORT", "5432")),
    "dbname": os.getenv("AMIP_DB_NAME", "amip"),
    "user": os.getenv("AMIP_DB_USER", "postgres"),
    "password": os.getenv("AMIP_DB_PASSWORD", "change_me_in_production"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


@contextmanager
def get_cursor():
    conn = get_connection()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    finally:
        cur.close()
        conn.close()


def fetch_all(query, params=None):
    with get_cursor() as cur:
        cur.execute(query, params)
        return [dict(row) for row in cur.fetchall()]


def fetch_one(query, params=None):
    with get_cursor() as cur:
        cur.execute(query, params)
        row = cur.fetchone()
        return dict(row) if row else None
