import os
import psycopg2

conn = psycopg2.connect(
    host="localhost", port=5432, dbname="amip", user="postgres",
    password=os.getenv("AMIP_DB_PASSWORD", "change_me_in_production"),
)
cur = conn.cursor()

cur.execute("SELECT table_name FROM information_schema.views WHERE table_schema='dwh'")
views = [r[0] for r in cur.fetchall()]
print(f"Views found: {len(views)}")
for v in views:
    print(f"  {v}")

print()
cur.execute("SELECT * FROM dwh.v_oee_machine_daily LIMIT 5")
cols = [d[0] for d in cur.description]
print(" | ".join(cols))
print("-" * 100)
for r in cur.fetchall():
    print(" | ".join(str(x) for x in r))

print()
cur.execute("SELECT COUNT(*) FROM dwh.v_oee_machine_daily")
print(f"OEE daily rows: {cur.fetchone()[0]}")

cur.execute("SELECT COUNT(*) FROM dwh.v_oee_monthly")
print(f"OEE monthly rows: {cur.fetchone()[0]}")

conn.close()
