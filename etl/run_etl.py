import os
import sys
import time
import subprocess

DB_HOST = os.environ.get("AMIP_DB_HOST", "db")
DB_PORT = os.environ.get("AMIP_DB_PORT", "5432")
DB_NAME = os.environ.get("AMIP_DB_NAME", "amip")
DB_USER = os.environ.get("AMIP_DB_USER", "postgres")
MAX_WAIT = int(os.environ.get("ETL_MAX_WAIT", "300"))
INTERVAL = 5

def wait_for_db():
    for i in range(MAX_WAIT // INTERVAL):
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
                user=DB_USER, password=os.environ.get("AMIP_DB_PASSWORD", ""),
            )
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM pg_tables WHERE schemaname='dwh' LIMIT 1")
            if cur.fetchone():
                print(f"[ETL] DWH schema ready after {i*INTERVAL}s")
                conn.close()
                return True
            conn.close()
        except Exception:
            pass
        print(f"[ETL] Waiting for DWH schema... ({i*INTERVAL}s)")
        time.sleep(INTERVAL)
    print("[ETL] Timeout waiting for DWH schema")
    return False

if __name__ == "__main__":
    if not wait_for_db():
        sys.exit(1)

    import populate_dwh
    populate_dwh.DB_CONFIG = {
        "host": DB_HOST,
        "port": int(DB_PORT),
        "dbname": DB_NAME,
        "user": DB_USER,
        "password": os.environ.get("AMIP_DB_PASSWORD", ""),
    }
    populate_dwh.main()
