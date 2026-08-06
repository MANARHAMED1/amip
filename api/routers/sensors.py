from fastapi import APIRouter, Query
from api.database import fetch_one, fetch_all

router = APIRouter()


@router.get("/current/{machine_code}")
def sensor_current(machine_code: str):
    current = fetch_one("""
        SELECT s.temperature, s.vibration, s.rpm, s.charge_frappe,
               s.puissance, s.vitesse_avance, s.temps_cycle, s.statut_machine,
               s.timestamp
        FROM sensor_data s
        WHERE s.machine_id = (SELECT machine_id FROM machine WHERE code = %s)
        ORDER BY s.timestamp DESC LIMIT 1
    """, (machine_code,))

    return current or {"error": "Aucune donnee capteur"}


@router.get("/stats/{machine_code}")
def sensor_stats(machine_code: str, date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = [machine_code]
    if date_start and date_end:
        where = "AND s.timestamp::date BETWEEN %s AND %s"
        params += [date_start, date_end]

    return fetch_one(f"""
        SELECT ROUND(AVG(s.temperature), 2) AS temp_moy,
               ROUND(MAX(s.temperature), 2) AS temp_max,
               ROUND(MIN(s.temperature), 2) AS temp_min,
               ROUND(AVG(s.vibration), 3) AS vib_moy,
               ROUND(MAX(s.vibration), 3) AS vib_max,
               ROUND(MIN(s.vibration), 3) AS vib_min,
               ROUND(AVG(s.rpm), 0) AS rpm_moy,
               ROUND(MAX(s.rpm), 0) AS rpm_max,
               ROUND(AVG(s.charge_frappe), 2) AS charge_moy,
               ROUND(MAX(s.charge_frappe), 2) AS charge_max,
               ROUND(AVG(s.puissance), 2) AS puissance_moy,
               ROUND(MAX(s.puissance), 2) AS puissance_max,
               COUNT(*) AS nb_readings,
               COUNT(*) FILTER (WHERE s.temperature > 80) AS alertes_temp,
               COUNT(*) FILTER (WHERE s.vibration > 4.5) AS alertes_vibration
        FROM sensor_data s
        WHERE s.machine_id = (SELECT machine_id FROM machine WHERE code = %s)
          {where}
    """, params)


@router.get("/history/{machine_code}")
def sensor_history(machine_code: str, date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = [machine_code]
    if date_start and date_end:
        where = "AND s.timestamp::date BETWEEN %s AND %s"
        params += [date_start, date_end]

    return fetch_all(f"""
        SELECT s.timestamp, s.temperature, s.vibration, s.rpm,
               s.charge_frappe, s.puissance, s.temps_cycle, s.statut_machine
        FROM sensor_data s
        WHERE s.machine_id = (SELECT machine_id FROM machine WHERE code = %s)
          {where}
        ORDER BY s.timestamp DESC
        LIMIT 500
    """, params)


@router.get("/alerts/{machine_code}")
def sensor_alerts(machine_code: str):
    return fetch_all("""
        SELECT s.timestamp, s.temperature, s.vibration,
               CASE
                   WHEN s.temperature > 80 OR s.vibration > 4.5 THEN 'CRITIQUE'
                   WHEN s.temperature > 60 OR s.vibration > 2.5 THEN 'ATTENTION'
                   ELSE 'NORMAL'
               END AS niveau
        FROM sensor_data s
        WHERE s.machine_id = (SELECT machine_id FROM machine WHERE code = %s)
          AND (s.temperature > 60 OR s.vibration > 2.5)
        ORDER BY s.timestamp DESC
        LIMIT 50
    """, (machine_code,))


@router.get("/all-machines")
def sensors_all_machines():
    return fetch_all("""
        SELECT ma.code, ma.nom,
               s.temperature, s.vibration, s.rpm, s.charge_frappe,
               s.puissance, s.statut_machine, s.timestamp
        FROM sensor_data s
        JOIN machine ma ON s.machine_id = ma.machine_id
        WHERE s.timestamp = (
            SELECT MAX(s2.timestamp)
            FROM sensor_data s2
            WHERE s2.machine_id = s.machine_id
        )
        ORDER BY ma.code
    """)


@router.get("/heatmap/{machine_code}")
def sensor_heatmap(machine_code: str, date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = [machine_code]
    if date_start and date_end:
        where = "AND s.timestamp::date BETWEEN %s AND %s"
        params += [date_start, date_end]

    return fetch_all(f"""
        SELECT EXTRACT(HOUR FROM s.timestamp) AS heure,
               EXTRACT(DOW FROM s.timestamp) AS jour,
               ROUND(AVG(s.temperature), 2) AS temperature,
               ROUND(AVG(s.vibration), 3) AS vibration,
               ROUND(AVG(s.puissance), 2) AS puissance
        FROM sensor_data s
        WHERE s.machine_id = (SELECT machine_id FROM machine WHERE code = %s)
          {where}
        GROUP BY EXTRACT(HOUR FROM s.timestamp), EXTRACT(DOW FROM s.timestamp)
        ORDER BY jour, heure
    """, params)


@router.get("/correlation/{machine_code}")
def sensor_correlation(machine_code: str, date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = [machine_code]
    if date_start and date_end:
        where = "AND s.timestamp::date BETWEEN %s AND %s"
        params += [date_start, date_end]

    return fetch_all(f"""
        SELECT s.temperature, s.vibration, s.rpm, s.puissance, s.charge_frappe,
               s.timestamp
        FROM sensor_data s
        WHERE s.machine_id = (SELECT machine_id FROM machine WHERE code = %s)
          {where}
        ORDER BY s.timestamp DESC
        LIMIT 500
    """, params)
