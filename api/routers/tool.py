from fastapi import APIRouter, Query, Path
from api.database import fetch_one, fetch_all
from api.ml.predict import predict_tool_wear

router = APIRouter()


@router.get("/list")
def list_tools():
    return fetch_all("""
        SELECT o.outil_id, o.code, o.designation, o.type_outil, o.diametre,
               o.matiere_outil, o.duree_vie_totale, o.usure_actuelle, o.duree_vie_restante,
               o.cout_achat, o.cout_remplacement, o.disponible,
               ROUND(o.usure_actuelle::decimal / o.duree_vie_totale * 100, 1) AS pct_usure,
               CASE
                   WHEN o.usure_actuelle::decimal / o.duree_vie_totale > 0.8 THEN 'CRITICAL'
                   WHEN o.usure_actuelle::decimal / o.duree_vie_totale > 0.6 THEN 'WARNING'
                   ELSE 'OK'
               END AS indicateur_remplacement,
               so.quantite_stock AS stock
        FROM outil o
        LEFT JOIN stock_outil so ON o.outil_id = so.outil_id
        ORDER BY o.code
    """)


@router.get("/{tool_code}")
def tool_detail(tool_code: str):
    tool = fetch_one("""
        SELECT o.*, so.quantite_stock, so.seuil_alerte, so.emplacement,
               ROUND(o.usure_actuelle::decimal / o.duree_vie_totale * 100, 1) AS pct_usure
        FROM outil o
        LEFT JOIN stock_outil so ON o.outil_id = so.outil_id
        WHERE o.code = %s
    """, (tool_code,))
    if not tool:
        return {"error": "Outil non trouve"}

    executions = fetch_all("""
        SELECT eo.usure_debut, eo.usure_fin, eo.duree_utilisation,
               ep.date_debut, ma.code AS machine_code,
               p.reference AS piece_ref
        FROM execution_outil eo
        JOIN execution_phase ep ON eo.execution_id = ep.execution_id
        JOIN machine ma ON ep.machine_id = ma.machine_id
        JOIN phase_gamme pg ON ep.phase_gamme_id = pg.phase_gamme_id
        JOIN gamme_usinage g ON pg.gamme_id = g.gamme_id
        JOIN piece p ON g.piece_id = p.piece_id
        WHERE eo.outil_id = (SELECT outil_id FROM outil WHERE code = %s)
        ORDER BY ep.date_debut DESC
        LIMIT 20
    """, (tool_code,))

    stats = fetch_one("""
        SELECT COUNT(*) AS nb_executions,
               SUM(eo.duree_utilisation) AS duree_totale,
               ROUND(AVG(eo.usure_fin - eo.usure_debut), 1) AS usure_moyenne_par_exec
        FROM execution_outil eo
        JOIN outil o ON eo.outil_id = o.outil_id
        WHERE o.code = %s
    """, (tool_code,))

    return {"tool": tool, "executions": executions, "stats": stats}


@router.get("/{tool_code}/wear-prediction")
def tool_wear_prediction(tool_code: str = Path(...)):
    return predict_tool_wear(tool_code=tool_code)
