from fastapi import APIRouter, Query
from api.database import fetch_one, fetch_all

router = APIRouter()


@router.get("/kpi")
def executive_kpi(
    date_start: str = Query(None, description="Date debut YYYY-MM-DD"),
    date_end: str = Query(None, description="Date fin YYYY-MM-DD"),
):
    where = ""
    params = []
    if date_start and date_end:
        where = "WHERE d.full_date BETWEEN %s AND %s"
        params = [date_start, date_end]

    oee = fetch_one(f"""
        SELECT ROUND(AVG(f.oee) * 100, 2) AS oee_global,
               ROUND(AVG(f.taux_disponibilite) * 100, 2) AS disponibilite,
               ROUND(AVG(f.taux_performance) * 100, 2) AS performance,
               ROUND(AVG(f.taux_qualite) * 100, 2) AS qualite,
               SUM(f.nb_pieces_produites) AS production_totale,
               SUM(f.nb_pieces_rebut) AS rebut_total,
               ROUND(CASE WHEN SUM(f.nb_pieces_produites) > 0
                   THEN SUM(f.nb_pieces_rebut)::decimal / SUM(f.nb_pieces_produites) * 100 ELSE 0 END, 2) AS taux_rebut
        FROM dwh.fact_execution f
        JOIN dwh.dim_date d ON f.date_key = d.date_key
        {where}
    """, params or None)

    machines = fetch_one("""
        SELECT COUNT(*) FILTER (WHERE statut = 'RUNNING') AS running,
               COUNT(*) FILTER (WHERE statut = 'STOPPED') AS stopped,
               COUNT(*) FILTER (WHERE statut = 'MAINTENANCE') AS maintenance,
               COUNT(*) FILTER (WHERE statut = 'BROKEN') AS broken,
               COUNT(*) AS total
        FROM machine
    """)

    of_actifs = fetch_one("""
        SELECT COUNT(*) AS total,
               COUNT(*) FILTER (WHERE statut = 'EN_COURS') AS en_cours,
               COUNT(*) FILTER (WHERE statut = 'EN_ATTENTE') AS en_attente,
               COUNT(*) FILTER (WHERE statut = 'TERMINE') AS termine
        FROM ordre_fabrication
    """)

    of_retard = fetch_one("""
        SELECT COUNT(*) AS retard
        FROM ordre_fabrication
        WHERE statut = 'TERMINE' AND date_fin_reelle > date_fin_prevue
    """)

    return {
        "oee": oee,
        "machines": machines,
        "ordres_fabrication": of_actifs,
        "retards": of_retard,
    }


@router.get("/machine-status")
def machine_status_grid():
    return fetch_all("""
        SELECT m.code, m.nom, m.type, m.marque, m.modele, m.statut,
               s.nom AS secteur
        FROM machine m
        JOIN secteur s ON m.secteur_id = s.secteur_id
        ORDER BY m.code
    """)


@router.get("/alerts")
def active_alerts():
    alerts = []

    broken = fetch_all("SELECT code, nom FROM machine WHERE statut = 'BROKEN'")
    for m in broken:
        alerts.append({"type": "CRITICAL", "message": f"Machine {m['code']} en panne", "detail": m["nom"]})

    maint = fetch_all("SELECT code, nom FROM machine WHERE statut = 'MAINTENANCE'")
    for m in maint:
        alerts.append({"type": "WARNING", "message": f"Machine {m['code']} en maintenance", "detail": m["nom"]})

    critical_stock = fetch_all("""
        SELECT m.code, m.designation, sm.quantite_stock, sm.seuil_alerte
        FROM stock_matiere sm JOIN matiere m ON sm.matiere_id = m.matiere_id
        WHERE sm.quantite_stock <= sm.seuil_alerte
    """)
    for s in critical_stock:
        alerts.append({"type": "CRITICAL", "message": f"Stock critique: {s['code']}", "detail": f"{s['designation']} - {s['quantite_stock']} unités (seuil: {s['seuil_alerte']})"})

    critical_tools = fetch_all("""
        SELECT o.code, o.designation, so.quantite_stock, so.seuil_alerte
        FROM stock_outil so JOIN outil o ON so.outil_id = o.outil_id
        WHERE so.quantite_stock <= so.seuil_alerte
    """)
    for t in critical_tools:
        alerts.append({"type": "WARNING", "message": f"Stock outil bas: {t['code']}", "detail": f"{t['designation']} - {t['quantite_stock']} unités"})

    return alerts


@router.get("/production-trend")
def production_trend(
    date_start: str = Query(None),
    date_end: str = Query(None),
):
    where = ""
    params = []
    if date_start and date_end:
        where = "WHERE d.full_date BETWEEN %s AND %s"
        params = [date_start, date_end]

    return fetch_all(f"""
        SELECT d.full_date AS date,
               SUM(f.nb_pieces_produites) AS produites,
               SUM(f.nb_pieces_rebut) AS rebuts
        FROM dwh.fact_execution f
        JOIN dwh.dim_date d ON f.date_key = d.date_key
        {where}
        GROUP BY d.full_date
        ORDER BY d.full_date
    """, params or None)


@router.get("/oee-by-machine")
def oee_by_machine(date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = []
    if date_start and date_end:
        where = "WHERE d.full_date BETWEEN %s AND %s"
        params = [date_start, date_end]

    return fetch_all(f"""
        SELECT dm.code, dm.nom,
               ROUND(AVG(f.taux_disponibilite) * 100, 2) AS disponibilite,
               ROUND(AVG(f.taux_performance) * 100, 2) AS performance,
               ROUND(AVG(f.taux_qualite) * 100, 2) AS qualite,
               ROUND(AVG(f.oee) * 100, 2) AS oee,
               SUM(f.nb_pieces_produites) AS production
        FROM dwh.fact_execution f
        JOIN dwh.dim_machine dm ON f.machine_key = dm.machine_key
        JOIN dwh.dim_date d ON f.date_key = d.date_key
        {where}
        GROUP BY dm.code, dm.nom
        ORDER BY oee DESC
    """, params or None)


@router.get("/production-vs-plan")
def production_vs_plan(date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = []
    if date_start and date_end:
        where = "WHERE d.full_date BETWEEN %s AND %s"
        params = [date_start, date_end]

    return fetch_all(f"""
        SELECT d.full_date AS date,
               SUM(fp.quantite_demandee) AS planifie,
               SUM(fp.quantite_produite) AS reel
        FROM dwh.fact_production fp
        JOIN dwh.dim_date d ON fp.date_key = d.date_key
        {where}
        GROUP BY d.full_date
        ORDER BY d.full_date
    """, params or None)


@router.get("/scrap-by-family")
def scrap_by_family(date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = []
    if date_start and date_end:
        where = "WHERE d.full_date BETWEEN %s AND %s"
        params = [date_start, date_end]

    return fetch_all(f"""
        SELECT dp.famille,
               SUM(f.nb_pieces_rebut) AS nb_rebut,
               SUM(f.nb_pieces_produites) AS nb_produites,
               ROUND(CASE WHEN SUM(f.nb_pieces_produites) > 0
                   THEN SUM(f.nb_pieces_rebut)::decimal / SUM(f.nb_pieces_produites) * 100
                   ELSE 0 END, 2) AS taux_rebut
        FROM dwh.fact_execution f
        JOIN dwh.dim_date d ON f.date_key = d.date_key
        JOIN dwh.dim_part dp ON f.part_key = dp.part_key
        {where}
        GROUP BY dp.famille
        ORDER BY nb_rebut DESC
    """, params or None)


@router.get("/active-orders")
def active_orders(date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = []
    if date_start and date_end:
        where = "WHERE of2.date_debut_prevue BETWEEN %s AND %s"
        params = [date_start, date_end]

    return fetch_all(f"""
        SELECT of2.numero_of, p.reference AS piece_ref, p.designation AS piece_nom,
               of2.quantite_demandee, of2.quantite_produite, of2.quantite_rebut,
               of2.statut, of2.priorite,
               ROUND(CASE WHEN of2.quantite_demandee > 0
                   THEN of2.quantite_produite::decimal / of2.quantite_demandee * 100
                   ELSE 0 END, 1) AS avancement_pct,
               CASE WHEN of2.date_fin_reelle > of2.date_fin_prevue
                    THEN (of2.date_fin_reelle - of2.date_fin_prevue)
                    ELSE 0 END AS retard_jours
        FROM ordre_fabrication of2
        JOIN piece p ON of2.piece_id = p.piece_id
        {where}
        ORDER BY of2.statut = 'EN_COURS' DESC, of2.numero_of DESC
        LIMIT 20
    """, params or None)
