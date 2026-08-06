from fastapi import APIRouter, Query, Path
from api.database import fetch_one, fetch_all
from api.ml.predict import predict_production_duration

router = APIRouter()


@router.get("/kpi")
def production_kpi():
    return fetch_one("""
        SELECT COUNT(*) AS total,
               COUNT(*) FILTER (WHERE statut = 'EN_COURS') AS en_cours,
               COUNT(*) FILTER (WHERE statut = 'TERMINE') AS termine,
               COUNT(*) FILTER (WHERE statut = 'EN_ATTENTE') AS en_attente,
               COUNT(*) FILTER (WHERE statut = 'ANNULE') AS annule,
               COUNT(*) FILTER (WHERE date_fin_reelle > date_fin_prevue) AS en_retard
        FROM ordre_fabrication
    """)


@router.get("/list")
def list_orders(
    statut: str = Query(None),
    priorite: str = Query(None),
    limit: int = Query(50),
):
    where = []
    params = []
    if statut:
        where.append("of2.statut = %s")
        params.append(statut)
    if priorite:
        where.append("of2.priorite = %s")
        params.append(priorite)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""
    params.append(limit)

    return fetch_all(f"""
        SELECT of2.numero_of, of2.statut, of2.priorite,
               p.reference AS piece_ref, p.designation AS piece_nom,
               of2.quantite_demandee, of2.quantite_produite, of2.quantite_rebut,
               of2.date_debut_prevue, of2.date_fin_prevue,
               of2.date_debut_reelle, of2.date_fin_reelle,
               ROUND(CASE WHEN of2.quantite_produite > 0
                   THEN (of2.quantite_produite - of2.quantite_rebut)::decimal / of2.quantite_produite * 100
                   ELSE 0 END, 1) AS taux_rendement
        FROM ordre_fabrication of2
        JOIN piece p ON of2.piece_id = p.piece_id
        {where_sql}
        ORDER BY of2.numero_of DESC
        LIMIT %s
    """, params)


@router.get("/{numero_of}")
def order_detail(numero_of: str):
    of = fetch_one("""
        SELECT of2.*, p.reference AS piece_ref, p.designation AS piece_nom,
               p.famille, p.poids, p.dimensions,
               m.code AS matiere_code, m.designation AS matiere_nom, m.type_matiere,
               g.code AS gamme_code, g.nb_phases, g.duree_totale_estimee
        FROM ordre_fabrication of2
        JOIN piece p ON of2.piece_id = p.piece_id
        LEFT JOIN matiere m ON p.matiere_id = m.matiere_id
        JOIN gamme_usinage g ON of2.gamme_id = g.gamme_id
        WHERE of2.numero_of = %s
    """, (numero_of,))
    if not of:
        return {"error": "OF non trouve"}

    retard = None
    if of.get("date_fin_reelle") and of.get("date_fin_prevue"):
        retard = (of["date_fin_reelle"] - of["date_fin_prevue"]).days

    phases = fetch_all("""
        SELECT pg.numero_phase, pg.designation, pg.temps_usinage_prevu, pg.temps_reglage_prevu,
               ma.code AS machine_code, ot.code AS outil_code,
               ep.temps_usinage_reel, ep.temps_reglage_reel,
               ep.nb_pieces_produites, ep.nb_pieces_rebut, ep.statut AS exec_statut,
               op.nom AS operateur_nom, op.prenom AS operateur_prenom
        FROM phase_gamme pg
        JOIN machine ma ON pg.machine_id = ma.machine_id
        JOIN outil ot ON pg.outil_id = ot.outil_id
        LEFT JOIN execution_phase ep ON pg.phase_gamme_id = ep.phase_gamme_id
            AND ep.ordre_fabrication_id = %s
        LEFT JOIN operateur op ON ep.operateur_id = op.operateur_id
        WHERE pg.gamme_id = %s
        ORDER BY pg.numero_phase
    """, (of["ordre_fabrication_id"], of["gamme_id"]))

    return {
        "of": of,
        "retard_jours": retard,
        "phases": phases,
    }


@router.get("/{numero_of}/phases")
def order_phases(numero_of: str):
    return fetch_all("""
        SELECT pg.numero_phase, pg.designation,
               ma.code AS machine_code, ot.code AS outil_code,
               pg.temps_usinage_prevu, pg.temps_reglage_prevu,
               ep.temps_usinage_reel, ep.temps_reglage_reel,
               ep.nb_pieces_produites, ep.nb_pieces_rebut,
               ep.vitesse_coupe, ep.avance, ep.profondeur_passe,
               ep.statut, ep.date_debut, ep.date_fin,
               op.nom AS operateur_nom, op.prenom AS operateur_prenom
        FROM execution_phase ep
        JOIN phase_gamme pg ON ep.phase_gamme_id = pg.phase_gamme_id
        JOIN machine ma ON ep.machine_id = ma.machine_id
        LEFT JOIN outil ot ON ep.outil_id = ot.outil_id
        LEFT JOIN operateur op ON ep.operateur_id = op.operateur_id
        WHERE ep.ordre_fabrication_id = (
            SELECT ordre_fabrication_id FROM ordre_fabrication WHERE numero_of = %s
        )
        ORDER BY pg.numero_phase
    """, (numero_of,))


@router.get("/{numero_of}/efficiency")
def order_efficiency(numero_of: str):
    of = fetch_one("""
        SELECT of2.quantite_demandee, of2.quantite_produite, of2.quantite_rebut,
               of2.date_debut_prevue, of2.date_fin_prevue,
               of2.date_debut_reelle, of2.date_fin_reelle,
               g.duree_totale_estimee
        FROM ordre_fabrication of2
        JOIN gamme_usinage g ON of2.gamme_id = g.gamme_id
        WHERE of2.numero_of = %s
    """, (numero_of,))
    if not of:
        return {"error": "OF non trouve"}

    eff_globale = 0
    if of.get("quantite_demandee") and of["quantite_demandee"] > 0:
        eff_globale = round(of.get("quantite_produite", 0) / of["quantite_demandee"] * 100, 1)

    eff_temps = 0
    if of.get("duree_totale_estimee") and of["duree_totale_estimee"] > 0 and of.get("date_fin_reelle"):
        duree_reelle = (of["date_fin_reelle"] - of["date_debut_reelle"]).total_seconds() / 60 if of.get("date_debut_reelle") else 0
        if duree_reelle > 0:
            eff_temps = round(of["duree_totale_estimee"] / duree_reelle * 100, 1)

    phases_eff = fetch_all("""
        SELECT pg.numero_phase, pg.designation,
               pg.temps_usinage_prevu,
               ep.temps_usinage_reel,
               CASE WHEN ep.temps_usinage_reel > 0
                   THEN ROUND(pg.temps_usinage_prevu / ep.temps_usinage_reel * 100, 1)
                   ELSE 0 END AS efficacite_phase
        FROM phase_gamme pg
        LEFT JOIN execution_phase ep ON pg.phase_gamme_id = ep.phase_gamme_id
            AND ep.ordre_fabrication_id = (SELECT ordre_fabrication_id FROM ordre_fabrication WHERE numero_of = %s)
        WHERE pg.gamme_id = (SELECT gamme_id FROM ordre_fabrication WHERE numero_of = %s)
        ORDER BY pg.numero_phase
    """, (numero_of, numero_of))

    return {
        "efficacite_globale": eff_globale,
        "efficacite_temps": eff_temps,
        "phases": phases_eff,
    }


@router.get("/prediction/duration")
def predict_duration(
    of_id: int = Query(None),
    numero_of: str = Query(None),
    famille: str = Query(None),
):
    return predict_production_duration(of_id=of_id, numero_of=numero_of, piece_famille=famille)
