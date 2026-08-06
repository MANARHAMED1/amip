from fastapi import APIRouter, Query, Path
from api.database import fetch_one, fetch_all
from api.ml.predict import predict_machining_time, predict_anomaly

router = APIRouter()


@router.get("/list")
def list_machines():
    return fetch_all("""
        SELECT m.machine_id, m.code, m.nom, m.type, m.marque, m.modele,
               m.controller, m.axes, m.rpm_max, m.tool_capacity, m.statut,
               m.date_installation, s.nom AS secteur
        FROM machine m JOIN secteur s ON m.secteur_id = s.secteur_id
        ORDER BY m.code
    """)


@router.get("/{machine_code}")
def machine_detail(machine_code: str):
    machine = fetch_one("""
        SELECT m.*, s.nom AS secteur
        FROM machine m JOIN secteur s ON m.secteur_id = s.secteur_id
        WHERE m.code = %s
    """, (machine_code,))
    if not machine:
        return {"error": "Machine non trouvee"}

    current_of = fetch_one("""
        SELECT of2.numero_of, p.reference AS piece_ref, p.designation AS piece_nom,
               ep.nb_pieces_produites, ep.statut
        FROM execution_phase ep
        JOIN ordre_fabrication of2 ON ep.ordre_fabrication_id = of2.ordre_fabrication_id
        JOIN phase_gamme pg ON ep.phase_gamme_id = pg.phase_gamme_id
        JOIN gamme_usinage g ON pg.gamme_id = g.gamme_id
        JOIN piece p ON of2.piece_id = p.piece_id
        WHERE ep.machine_id = (SELECT machine_id FROM machine WHERE code = %s)
          AND ep.statut = 'EN_COURS'
        LIMIT 1
    """, (machine_code,))

    current_operator = fetch_one("""
        SELECT o.nom, o.prenom, o.niveau_competence
        FROM execution_phase ep
        JOIN operateur o ON ep.operateur_id = o.operateur_id
        WHERE ep.machine_id = (SELECT machine_id FROM machine WHERE code = %s)
          AND ep.statut = 'EN_COURS'
        LIMIT 1
    """, (machine_code,))

    current_tool = fetch_one("""
        SELECT ot.code, ot.type_outil, ot.usure_actuelle, ot.duree_vie_totale,
               ROUND(ot.usure_actuelle::decimal / ot.duree_vie_totale * 100, 1) AS pct_usure
        FROM execution_phase ep
        JOIN outil ot ON ep.outil_id = ot.outil_id
        WHERE ep.machine_id = (SELECT machine_id FROM machine WHERE code = %s)
          AND ep.statut = 'EN_COURS'
        LIMIT 1
    """, (machine_code,))

    return {
        "machine": machine,
        "of_actuel": current_of,
        "operateur": current_operator,
        "outil_actuel": current_tool,
    }


@router.get("/{machine_code}/performance")
def machine_performance(machine_code: str, date_start: str = Query(None), date_end: str = Query(None)):
    where_date = ""
    params = [machine_code]
    if date_start and date_end:
        where_date = "AND d.full_date BETWEEN %s AND %s"
        params += [date_start, date_end]

    return fetch_one(f"""
        SELECT ROUND(AVG(f.taux_disponibilite) * 100, 2) AS disponibilite,
               ROUND(AVG(f.taux_performance) * 100, 2) AS performance,
               ROUND(AVG(f.taux_qualite) * 100, 2) AS qualite,
               ROUND(AVG(f.oee) * 100, 2) AS oee,
               SUM(f.nb_pieces_produites) AS total_produites,
               SUM(f.nb_pieces_rebut) AS total_rebut,
               SUM(f.temps_usinage_reel) AS temps_usinage_total,
               SUM(f.temps_reglage_reel) AS temps_reglage_total
        FROM dwh.fact_execution f
        JOIN dwh.dim_machine dm ON f.machine_key = dm.machine_key
        JOIN dwh.dim_date d ON f.date_key = d.date_key
        WHERE dm.code = %s {where_date}
    """, params)


@router.get("/{machine_code}/oee-history")
def machine_oee_history(machine_code: str, date_start: str = Query(None), date_end: str = Query(None)):
    where_date = ""
    params = [machine_code]
    if date_start and date_end:
        where_date = "AND d.full_date BETWEEN %s AND %s"
        params += [date_start, date_end]

    return fetch_all(f"""
        SELECT d.full_date AS date,
               ROUND(AVG(f.oee) * 100, 2) AS oee,
               ROUND(AVG(f.taux_disponibilite) * 100, 2) AS disponibilite,
               ROUND(AVG(f.taux_performance) * 100, 2) AS performance,
               ROUND(AVG(f.taux_qualite) * 100, 2) AS qualite
        FROM dwh.fact_execution f
        JOIN dwh.dim_machine dm ON f.machine_key = dm.machine_key
        JOIN dwh.dim_date d ON f.date_key = d.date_key
        WHERE dm.code = %s {where_date}
        GROUP BY d.full_date
        ORDER BY d.full_date
    """, params)


@router.get("/{machine_code}/maintenance")
def machine_maintenance(machine_code: str):
    return fetch_all("""
        SELECT m.type_maintenance, m.description, m.date_debut, m.date_fin,
               m.duree, m.cout, m.statut
        FROM maintenance m
        JOIN machine ma ON m.machine_id = ma.machine_id
        WHERE ma.code = %s
        ORDER BY m.date_debut DESC
        LIMIT 20
    """, (machine_code,))


@router.get("/{machine_code}/maintenance-kpi")
def machine_maintenance_kpi(machine_code: str):
    stats = fetch_one("""
        SELECT COUNT(*) AS nb_interventions,
               SUM(cout) AS cout_total,
               ROUND(AVG(cout), 2) AS cout_moyen,
               SUM(duree) AS duree_totale_min,
               ROUND(AVG(duree), 2) AS duree_moyenne_min,
               COUNT(*) FILTER (WHERE type_maintenance = 'Preventive') AS nb_preventive,
               COUNT(*) FILTER (WHERE type_maintenance = 'Corrective') AS nb_corrective
        FROM maintenance
        WHERE machine_id = (SELECT machine_id FROM machine WHERE code = %s)
    """, (machine_code,))

    mtbf_mttr = fetch_one("""
        SELECT ROUND(
            EXTRACT(EPOCH FROM (MAX(date_fin) - MIN(date_debut))) / 3600
            / GREATEST(COUNT(*) FILTER (WHERE type_maintenance = 'Corrective'), 1), 1
        ) AS mtbf_heures,
        ROUND(
            AVG(duree) / 60.0, 1
        ) AS mttr_heures
        FROM maintenance
        WHERE machine_id = (SELECT machine_id FROM machine WHERE code = %s)
          AND date_fin IS NOT NULL
    """, (machine_code,))

    return {"stats": stats, "mtbf_mttr": mtbf_mttr}


@router.get("/{machine_code}/sensors")
def machine_sensors(machine_code: str, date_start: str = Query(None), date_end: str = Query(None)):
    where_date = ""
    params = [machine_code]
    if date_start and date_end:
        where_date = "AND timestamp BETWEEN %s AND %s"
        params += [date_start, date_end]

    current = fetch_one(f"""
        SELECT temperature, vibration, rpm, charge_frappe, puissance,
               vitesse_avance, temps_cycle, statut_machine
        FROM sensor_data
        WHERE machine_id = (SELECT machine_id FROM machine WHERE code = %s)
          {where_date}
        ORDER BY timestamp DESC LIMIT 1
    """, params)

    stats = fetch_one(f"""
        SELECT ROUND(AVG(temperature), 2) AS temp_moy, ROUND(MAX(temperature), 2) AS temp_max,
               ROUND(AVG(vibration), 3) AS vib_moy, ROUND(MAX(vibration), 3) AS vib_max,
               ROUND(AVG(rpm), 0) AS rpm_moy,
               ROUND(AVG(charge_frappe), 2) AS charge_moy,
               ROUND(AVG(puissance), 2) AS puissance_moy
        FROM sensor_data
        WHERE machine_id = (SELECT machine_id FROM machine WHERE code = %s)
          {where_date}
    """, params)

    return {"current": current, "stats": stats}


@router.get("/{machine_code}/phases-timeline")
def machine_phases_timeline(machine_code: str, date_start: str = Query(None), date_end: str = Query(None)):
    where_date = ""
    params = [machine_code]
    if date_start and date_end:
        where_date = "AND ep.date_debut BETWEEN %s AND %s"
        params += [date_start, date_end]

    return fetch_all(f"""
        SELECT pg.numero_phase,
               pg.designation AS phase_name,
               ma.code AS machine_code,
               ot.code AS outil_code,
               pg.temps_usinage_prevu, ep.temps_usinage_reel,
               ep.date_debut, ep.date_fin,
               ep.statut,
               CASE
                    WHEN ep.date_debut IS NOT NULL AND ep.date_fin IS NOT NULL
                    THEN EXTRACT(EPOCH FROM (ep.date_fin - ep.date_debut)) / 60
                    ELSE pg.temps_usinage_prevu
                END AS duree
        FROM execution_phase ep
        JOIN phase_gamme pg ON ep.phase_gamme_id = pg.phase_gamme_id
        JOIN machine ma ON ep.machine_id = ma.machine_id
        LEFT JOIN outil ot ON ep.outil_id = ot.outil_id
        WHERE ma.code = %s {where_date}
        ORDER BY ep.date_debut
    """, params)


@router.get("/{machine_code}/tool-history")
def machine_tool_history(machine_code: str):
    return fetch_all("""
        SELECT ot.code AS outil_code, ot.type_outil,
               eo.usure_debut, eo.usure_fin, eo.duree_utilisation,
               ep.date_debut
        FROM execution_outil eo
        JOIN execution_phase ep ON eo.execution_id = ep.execution_id
        JOIN outil ot ON eo.outil_id = ot.outil_id
        WHERE ep.machine_id = (SELECT machine_id FROM machine WHERE code = %s)
        ORDER BY ep.date_debut DESC
        LIMIT 20
    """, (machine_code,))


@router.get("/{machine_code}/machining-time")
def machining_time_prediction(machine_code: str = Path(...)):
    return predict_machining_time(machine_code=machine_code)


@router.get("/{machine_code}/anomaly")
def anomaly_prediction(machine_code: str = Path(...)):
    return predict_anomaly(machine_code=machine_code)
