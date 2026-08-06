import os
import psycopg2

conn = psycopg2.connect(
    host="localhost", port=5432, dbname="amip",
    user="postgres", password=os.getenv("AMIP_DB_PASSWORD", "change_me_in_production"),
)
cur = conn.cursor()

print("=" * 60)
print("  AMIP Data Validation")
print("=" * 60)

print("\n[1] ROW COUNTS")
cur.execute("""
    SELECT t.table_name,
           (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) AS cols,
           (xpath('/row/cnt/text()', query_to_xml(format('SELECT COUNT(*) AS cnt FROM %I', t.table_name), false, true, '')))[1]::text::int AS rows
    FROM information_schema.tables t
    WHERE table_schema = 'public' ORDER BY t.table_name
""")
for table_name, cols, rows in cur.fetchall():
    print(f"  {table_name:25s} {cols:>3d} cols  {rows:>10d} rows")

print("\n[2] FK INTEGRITY CHECKS")
checks = [
    ("MACHINE -> SECTEUR", "SELECT COUNT(*) FROM machine m LEFT JOIN secteur s ON m.secteur_id = s.secteur_id WHERE s.secteur_id IS NULL"),
    ("PHASE_GAMME -> MACHINE", "SELECT COUNT(*) FROM phase_gamme p LEFT JOIN machine m ON p.machine_id = m.machine_id WHERE m.machine_id IS NULL"),
    ("PHASE_GAMME -> OUTIL", "SELECT COUNT(*) FROM phase_gamme p LEFT JOIN outil o ON p.outil_id = o.outil_id WHERE o.outil_id IS NULL"),
    ("EXEC_PHASE -> OF", "SELECT COUNT(*) FROM execution_phase e LEFT JOIN ordre_fabrication o ON e.ordre_fabrication_id = o.ordre_fabrication_id WHERE o.ordre_fabrication_id IS NULL"),
    ("EXEC_PHASE -> MACHINE", "SELECT COUNT(*) FROM execution_phase e LEFT JOIN machine m ON e.machine_id = m.machine_id WHERE m.machine_id IS NULL"),
    ("EXEC_PHASE -> OPERATEUR", "SELECT COUNT(*) FROM execution_phase e LEFT JOIN operateur o ON e.operateur_id = o.operateur_id WHERE o.operateur_id IS NULL"),
    ("CONTROLE -> EXECUTION", "SELECT COUNT(*) FROM controle_qualite c LEFT JOIN execution_phase e ON c.execution_id = e.execution_id WHERE e.execution_id IS NULL"),
    ("MAINTENANCE -> MACHINE", "SELECT COUNT(*) FROM maintenance m LEFT JOIN machine ma ON m.machine_id = ma.machine_id WHERE ma.machine_id IS NULL"),
    ("SENSOR -> MACHINE", "SELECT COUNT(*) FROM sensor_data s LEFT JOIN machine m ON s.machine_id = m.machine_id WHERE m.machine_id IS NULL"),
]
for label, sql in checks:
    cur.execute(sql)
    orphans = cur.fetchone()[0]
    status = "OK" if orphans == 0 else f"FAIL ({orphans} orphans)"
    print(f"  {label:30s} {status}")

print("\n[3] SAMPLE DATA")
cur.execute("SELECT code, nom, type, marque, modele, statut FROM machine LIMIT 4")
print("  Machines:")
for row in cur.fetchall():
    print(f"    {row}")

cur.execute("SELECT numero_of, piece_id, gamme_id, quantite_demandee, statut FROM ordre_fabrication LIMIT 3")
print("  OF:")
for row in cur.fetchall():
    print(f"    {row}")

cur.execute("SELECT machine_id, temperature, vibration, rpm, charge_frappe FROM sensor_data WHERE statut_machine = 'RUNNING' LIMIT 3")
print("  Sensor (RUNNING):")
for row in cur.fetchall():
    print(f"    {row}")

cur.close()
conn.close()
print("\nDone.")
