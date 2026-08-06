from fastapi import APIRouter, Query, Path
from api.database import fetch_one, fetch_all
from api.ml.predict import predict_scrap

router = APIRouter()


@router.get("/kpi")
def quality_kpi(
    date_start: str = Query(None),
    date_end: str = Query(None),
    piece_ref: str = Query(None),
    machine_code: str = Query(None),
):
    where = []
    params = []
    if date_start and date_end:
        where.append("cq.date_controle::date BETWEEN %s AND %s")
        params += [date_start, date_end]
    if piece_ref:
        where.append("p.reference = %s")
        params.append(piece_ref)
    if machine_code:
        where.append("ma.code = %s")
        params.append(machine_code)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    kpi = fetch_one(f"""
        SELECT COUNT(*) AS nb_inspections,
               SUM(cq.nb_controles) AS total_controles,
               SUM(cq.nb_conformes) AS total_conformes,
               SUM(cq.nb_non_conformes) AS total_non_conformes,
               ROUND(CASE WHEN SUM(cq.nb_controles) > 0
                   THEN SUM(cq.nb_conformes)::decimal / SUM(cq.nb_controles) * 100 ELSE 0 END, 2) AS taux_conformite,
               ROUND(AVG(cq.dimension_mesuree - cq.dimension_cible), 4) AS ecart_dimension_moyen,
               ROUND(AVG(cq.rugosite_mesuree), 3) AS rugosite_moyenne
        FROM controle_qualite cq
        JOIN piece p ON cq.piece_id = p.piece_id
        JOIN execution_phase ep ON cq.execution_id = ep.execution_id
        JOIN machine ma ON ep.machine_id = ma.machine_id
        {where_sql}
    """, params or None)

    return kpi


@router.get("/causes")
def quality_causes(date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = []
    if date_start and date_end:
        where = "WHERE cq.date_controle::date BETWEEN %s AND %s"
        params = [date_start, date_end]

    return fetch_all(f"""
        SELECT cr.categorie, cr.description, COUNT(*) AS nb,
               SUM(cq.nb_non_conformes) AS total_rebut
        FROM controle_qualite cq
        JOIN cause_rebut cr ON cq.cause_rebut_id = cr.cause_rebut_id
        {where}
        GROUP BY cr.categorie, cr.description
        ORDER BY nb DESC
    """, params or None)


@router.get("/by-machine")
def quality_by_machine(date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = []
    if date_start and date_end:
        where = "WHERE cq.date_controle::date BETWEEN %s AND %s"
        params = [date_start, date_end]

    return fetch_all(f"""
        SELECT ma.code, ma.nom,
               SUM(cq.nb_controles) AS total_controles,
               SUM(cq.nb_non_conformes) AS total_non_conformes,
               ROUND(CASE WHEN SUM(cq.nb_controles) > 0
                   THEN SUM(cq.nb_non_conformes)::decimal / SUM(cq.nb_controles) * 100 ELSE 0 END, 2) AS taux_rebut
        FROM controle_qualite cq
        JOIN execution_phase ep ON cq.execution_id = ep.execution_id
        JOIN machine ma ON ep.machine_id = ma.machine_id
        {where}
        GROUP BY ma.code, ma.nom
        ORDER BY taux_rebut DESC
    """, params or None)


@router.get("/by-operator")
def quality_by_operator(date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = []
    if date_start and date_end:
        where = "WHERE cq.date_controle::date BETWEEN %s AND %s"
        params = [date_start, date_end]

    return fetch_all(f"""
        SELECT o.nom, o.prenom, o.niveau_competence,
               SUM(cq.nb_controles) AS total_controles,
               SUM(cq.nb_non_conformes) AS total_non_conformes,
               ROUND(CASE WHEN SUM(cq.nb_controles) > 0
                   THEN SUM(cq.nb_non_conformes)::decimal / SUM(cq.nb_controles) * 100 ELSE 0 END, 2) AS taux_rebut
        FROM controle_qualite cq
        JOIN execution_phase ep ON cq.execution_id = ep.execution_id
        JOIN operateur o ON ep.operateur_id = o.operateur_id
        {where}
        GROUP BY o.nom, o.prenom, o.niveau_competence
        ORDER BY taux_rebut DESC
    """, params or None)


@router.get("/evolution")
def quality_evolution(date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = []
    if date_start and date_end:
        where = "WHERE cq.date_controle::date BETWEEN %s AND %s"
        params = [date_start, date_end]

    return fetch_all(f"""
        SELECT cq.date_controle::date AS date,
               SUM(cq.nb_controles) AS controles,
               SUM(cq.nb_non_conformes) AS non_conformes,
               ROUND(CASE WHEN SUM(cq.nb_controles) > 0
                   THEN SUM(cq.nb_non_conformes)::decimal / SUM(cq.nb_controles) * 100 ELSE 0 END, 2) AS taux_rebut
        FROM controle_qualite cq
        {where}
        GROUP BY cq.date_controle::date
        ORDER BY cq.date_controle::date
    """, params or None)


@router.get("/by-part")
def quality_by_part(date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = []
    if date_start and date_end:
        where = "WHERE cq.date_controle::date BETWEEN %s AND %s"
        params = [date_start, date_end]

    return fetch_all(f"""
        SELECT p.reference, p.designation, p.famille,
               SUM(cq.nb_controles) AS controles,
               SUM(cq.nb_non_conformes) AS non_conformes,
               ROUND(CASE WHEN SUM(cq.nb_controles) > 0
                   THEN SUM(cq.nb_non_conformes)::decimal / SUM(cq.nb_controles) * 100 ELSE 0 END, 2) AS taux_rebut
        FROM controle_qualite cq
        JOIN piece p ON cq.piece_id = p.piece_id
        {where}
        GROUP BY p.reference, p.designation, p.famille
        ORDER BY taux_rebut DESC
        LIMIT 20
    """, params or None)


@router.get("/dimensions")
def quality_dimensions(date_start: str = Query(None), date_end: str = Query(None), piece_ref: str = Query(None)):
    where = []
    params = []
    if date_start and date_end:
        where.append("cq.date_controle::date BETWEEN %s AND %s")
        params += [date_start, date_end]
    if piece_ref:
        where.append("p.reference = %s")
        params.append(piece_ref)
    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    return fetch_all(f"""
        SELECT cq.dimension_mesuree, cq.dimension_cible,
               cq.tolerance_plus, cq.tolerance_moins,
               cq.rugosite_mesuree, cq.date_controle,
               p.reference AS piece_ref
        FROM controle_qualite cq
        JOIN piece p ON cq.piece_id = p.piece_id
        {where_sql}
        ORDER BY cq.date_controle DESC
        LIMIT 200
    """, params or None)


@router.get("/by-material")
def quality_by_material(date_start: str = Query(None), date_end: str = Query(None)):
    where = ""
    params = []
    if date_start and date_end:
        where = "WHERE cq.date_controle::date BETWEEN %s AND %s"
        params = [date_start, date_end]

    return fetch_all(f"""
        SELECT m.type_matiere,
               SUM(cq.nb_controles) AS total_controles,
               SUM(cq.nb_non_conformes) AS total_non_conformes,
               ROUND(CASE WHEN SUM(cq.nb_controles) > 0
                   THEN SUM(cq.nb_non_conformes)::decimal / SUM(cq.nb_controles) * 100 ELSE 0 END, 2) AS taux_rebut
        FROM controle_qualite cq
        JOIN piece p ON cq.piece_id = p.piece_id
        JOIN matiere m ON p.matiere_id = m.matiere_id
        {where}
        GROUP BY m.type_matiere
        ORDER BY taux_rebut DESC
    """, params or None)


@router.get("/scrap-prediction")
def scrap_prediction(
    machine_code: str = Query(None),
    of_id: int = Query(None),
):
    return predict_scrap(machine_code=machine_code, of_id=of_id)
