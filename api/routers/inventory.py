from fastapi import APIRouter, Query, Path
from api.database import fetch_one, fetch_all
from api.ml.predict import predict_stockout

router = APIRouter()


@router.get("/overview")
def inventory_overview():
    matieres = fetch_one("""
        SELECT COUNT(*) AS total,
               COUNT(*) FILTER (WHERE sm.quantite_stock <= sm.seuil_alerte) AS critiques,
               ROUND(SUM(sm.quantite_stock * m.prix_kg), 2) AS valeur_totale
        FROM stock_matiere sm JOIN matiere m ON sm.matiere_id = m.matiere_id
    """)

    outils = fetch_one("""
        SELECT COUNT(*) AS total,
               COUNT(*) FILTER (WHERE so.quantite_stock <= so.seuil_alerte) AS critiques
        FROM stock_outil so
    """)

    pieces = fetch_one("""
        SELECT COUNT(*) AS total,
               SUM(sp.quantite_stock) AS stock_total
        FROM stock_piece sp
    """)

    return {"matieres": matieres, "outils": outils, "pieces": pieces}


@router.get("/matieres")
def list_matieres():
    return fetch_all("""
        SELECT m.code, m.designation, m.type_matiere, m.nuance, m.prix_kg,
               sm.quantite_stock, sm.seuil_alerte, sm.emplacement,
               CASE
                   WHEN sm.quantite_stock <= sm.seuil_alerte THEN 'CRITIQUE'
                   WHEN sm.quantite_stock <= sm.seuil_alerte * 1.5 THEN 'BAS'
                   WHEN sm.quantite_stock > sm.seuil_alerte * 3 THEN 'SURSTOCK'
                   ELSE 'NORMAL'
               END AS statut
        FROM stock_matiere sm
        JOIN matiere m ON sm.matiere_id = m.matiere_id
        ORDER BY sm.quantite_stock / GREATEST(sm.seuil_alerte, 0.01) ASC
    """)


@router.get("/outils")
def list_outils_stock():
    return fetch_all("""
        SELECT o.code, o.designation, o.type_outil, o.diametre,
               so.quantite_stock, so.seuil_alerte, so.emplacement,
               CASE
                   WHEN so.quantite_stock <= so.seuil_alerte THEN 'CRITIQUE'
                   WHEN so.quantite_stock <= so.seuil_alerte * 1.5 THEN 'BAS'
                   ELSE 'NORMAL'
               END AS statut
        FROM stock_outil so
        JOIN outil o ON so.outil_id = o.outil_id
        ORDER BY so.quantite_stock / GREATEST(so.seuil_alerte, 0.01) ASC
    """)


@router.get("/pieces")
def list_pieces_stock():
    return fetch_all("""
        SELECT p.reference, p.designation, p.famille, p.prix_revient,
               sp.quantite_stock, sp.emplacement,
               ROUND(sp.quantite_stock * p.prix_revient, 2) AS valeur_stock
        FROM stock_piece sp
        JOIN piece p ON sp.piece_id = p.piece_id
        ORDER BY sp.quantite_stock DESC
    """)


@router.get("/alerts")
def inventory_alerts():
    return fetch_all("""
        SELECT 'MATIERE' AS type, m.code, m.designation,
               sm.quantite_stock, sm.seuil_alerte, 'CRITIQUE' AS statut
        FROM stock_matiere sm JOIN matiere m ON sm.matiere_id = m.matiere_id
        WHERE sm.quantite_stock <= sm.seuil_alerte
        UNION ALL
        SELECT 'OUTIL' AS type, o.code, o.designation,
               so.quantite_stock, so.seuil_alerte, 'CRITIQUE' AS statut
        FROM stock_outil so JOIN outil o ON so.outil_id = o.outil_id
        WHERE so.quantite_stock <= so.seuil_alerte
        ORDER BY type, code
    """)


@router.get("/consumption-trend")
def consumption_trend():
    return fetch_all("""
        SELECT DATE_TRUNC('month', ep.date_debut) AS mois,
               SUM(ep.nb_pieces_produites) AS consommation
        FROM execution_phase ep
        WHERE ep.date_debut IS NOT NULL
        GROUP BY DATE_TRUNC('month', ep.date_debut)
        ORDER BY mois
    """)


@router.get("/status-distribution")
def status_distribution():
    matieres = fetch_one("""
        SELECT
            COUNT(*) FILTER (WHERE sm.quantite_stock <= sm.seuil_alerte) AS critique,
            COUNT(*) FILTER (WHERE sm.quantite_stock > sm.seuil_alerte
                AND sm.quantite_stock <= sm.seuil_alerte * 1.5) AS bas,
            COUNT(*) FILTER (WHERE sm.quantite_stock > sm.seuil_alerte * 1.5
                AND sm.quantite_stock <= sm.seuil_alerte * 3) AS normal,
            COUNT(*) FILTER (WHERE sm.quantite_stock > sm.seuil_alerte * 3) AS surstock
        FROM stock_matiere sm
    """)
    return matieres or {"critique": 0, "bas": 0, "normal": 0, "surstock": 0}


@router.get("/value-by-category")
def value_by_category():
    return fetch_all("""
        SELECT p.famille,
               SUM(sp.quantite_stock) AS quantite_totale,
               ROUND(SUM(sp.quantite_stock * p.prix_revient), 2) AS valeur_totale
        FROM stock_piece sp
        JOIN piece p ON sp.piece_id = p.piece_id
        GROUP BY p.famille
        ORDER BY valeur_totale DESC
    """)


@router.get("/stockout-forecast")
def stockout_forecast(matiere_code: str = Query(None)):
    return predict_stockout(matiere_code=matiere_code)
