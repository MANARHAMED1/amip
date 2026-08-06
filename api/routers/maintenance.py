from fastapi import APIRouter, Query, Path
from api.database import fetch_one, fetch_all
from api.ml.predict import predict_next_maintenance

router = APIRouter()


@router.get("/list")
def list_maintenance():
    return fetch_all("""
        SELECT m.maintenance_id, ma.code AS machine_code, ma.nom AS machine_nom,
               m.type_maintenance, m.description, m.date_debut, m.date_fin,
               m.duree, m.cout, m.statut,
               op.nom AS operateur_nom, op.prenom AS operateur_prenom
        FROM maintenance m
        JOIN machine ma ON m.machine_id = ma.machine_id
        LEFT JOIN operateur op ON m.operateur_id = op.operateur_id
        ORDER BY m.date_debut DESC
        LIMIT 100
    """)


@router.get("/kpi")
def maintenance_kpi(
    machine_code: str = Query(None),
    date_start: str = Query(None),
    date_end: str = Query(None),
):
    where = []
    params = []
    if machine_code:
        where.append("ma.code = %s")
        params.append(machine_code)
    if date_start and date_end:
        where.append("m.date_debut::date BETWEEN %s AND %s")
        params += [date_start, date_end]

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    stats = fetch_one(f"""
        SELECT COUNT(*) AS nb_interventions,
               SUM(m.cout) AS cout_total,
               ROUND(AVG(m.cout), 2) AS cout_moyen,
               SUM(m.duree) AS duree_totale_min,
               ROUND(AVG(m.duree), 2) AS duree_moyenne_min,
               COUNT(*) FILTER (WHERE m.type_maintenance IN ('Preventive','Changement huile','Nettoyage','Inspection','Changement liquide','Alignement machine')) AS nb_preventive,
               COUNT(*) FILTER (WHERE m.type_maintenance IN ('Corrective','Remplacement roulement')) AS nb_corrective
        FROM maintenance m
        JOIN machine ma ON m.machine_id = ma.machine_id
        {where_sql}
    """, params or None)

    by_type = fetch_all(f"""
        SELECT m.type_maintenance,
               COUNT(*) AS nb,
               SUM(m.cout) AS cout_total,
               ROUND(AVG(m.duree), 1) AS duree_moyenne
        FROM maintenance m
        JOIN machine ma ON m.machine_id = ma.machine_id
        {where_sql}
        GROUP BY m.type_maintenance
        ORDER BY nb DESC
    """, params or None)

    return {"stats": stats, "by_type": by_type}


@router.get("/history/{machine_code}")
def maintenance_history(machine_code: str):
    return fetch_all("""
        SELECT m.type_maintenance, m.description, m.date_debut, m.date_fin,
               m.duree, m.cout, m.statut,
               op.nom AS operateur_nom, op.prenom AS operateur_prenom
        FROM maintenance m
        JOIN machine ma ON m.machine_id = ma.machine_id
        LEFT JOIN operateur op ON m.operateur_id = op.operateur_id
        WHERE ma.code = %s
        ORDER BY m.date_debut DESC
    """, (machine_code,))


@router.get("/cost-evolution")
def maintenance_cost_evolution(machine_code: str = Query(None)):
    where = ""
    params = []
    if machine_code:
        where = "WHERE ma.code = %s"
        params = [machine_code]

    return fetch_all(f"""
        SELECT DATE_TRUNC('month', m.date_debut) AS mois,
               SUM(m.cout) AS cout_mensuel,
               COUNT(*) AS nb_interventions
        FROM maintenance m
        JOIN machine ma ON m.machine_id = ma.machine_id
        {where}
        GROUP BY DATE_TRUNC('month', m.date_debut)
        ORDER BY mois
    """, params or None)


@router.get("/{machine_code}/next-maintenance")
def next_maintenance_prediction(machine_code: str = Path(...)):
    return predict_next_maintenance(machine_code=machine_code)
