"""
Prediction functions for all 7 ML models.
Loads trained .joblib models and returns predictions.
"""
import os, json, warnings
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from joblib import load
from api.database import fetch_one, fetch_all

warnings.filterwarnings("ignore")

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

def _load(name):
    path = os.path.join(MODEL_DIR, f"{name}.joblib")
    if os.path.exists(path):
        return load(path)
    return None

def _features(name):
    # Feature files use number prefix (e.g. "ml01_features.json")
    prefix = name.split("_")[0] if "_" in name else name
    for fname in os.listdir(MODEL_DIR):
        if fname.startswith(prefix) and fname.endswith("_features.json"):
            with open(os.path.join(MODEL_DIR, fname)) as f:
                return json.load(f)
    return []

def _align(df, features):
    """Ensure df has all expected feature columns, filling missing with 0."""
    for col in features:
        if col not in df.columns:
            df[col] = 0
    return df[features].values

# ── ML-01: Scrap Prediction ──
def predict_scrap(machine_code: str = None, of_id: int = None):
    model = _load("ml01_scrap")
    if not model:
        return {"error": "Model not trained", "trained": False}

    rows = fetch_all("""
        SELECT ep.vitesse_coupe, ep.avance, ep.profondeur_passe,
               ep.nb_pieces_produites, ep.nb_pieces_rebut,
               m.type AS machine_type, m.rpm_max,
               ot.type_outil, ot.matiere_outil,
               op.niveau_competence,
               pg.temps_usinage_prevu
        FROM execution_phase ep
        JOIN machine m ON ep.machine_id = m.machine_id
        JOIN outil ot ON ep.outil_id = ot.outil_id
        LEFT JOIN operateur op ON ep.operateur_id = op.operateur_id
        JOIN phase_gamme pg ON ep.phase_gamme_id = pg.phase_gamme_id
        WHERE (%s IS NULL OR m.code = %s)
          AND (%s IS NULL OR ep.ordre_fabrication_id = %s)
          AND ep.nb_pieces_produites > 0
        LIMIT 500
    """, (machine_code, machine_code, of_id, of_id))

    if not rows:
        return {"error": "No execution data found", "trained": True}

    features = _features("ml01_scrap")
    df = pd.DataFrame(rows)
    for c in df.columns:
        try:
            df[c] = df[c].astype(float)
        except (ValueError, TypeError):
            pass
    for c in df.select_dtypes(exclude=["number"]).columns:
        if df[c].nunique() > 1:
            dummies = pd.get_dummies(df[c], prefix=c)
            df = pd.concat([df, dummies], axis=1)
            df.drop(columns=[c], inplace=True)

    X = _align(df, features)
    probs = model.predict_proba(X)[:, 1]
    avg_prob = float(probs.mean())

    return {
        "trained": True,
        "avg_scrap_probability": round(avg_prob, 3),
        "samples_analyzed": len(df),
        "risk_level": "HIGH" if avg_prob > 0.5 else "MODERATE" if avg_prob > 0.25 else "LOW",
    }

# ── ML-02: Machining Time Estimation ──
def predict_machining_time(machine_code: str = None, phase_gamme_id: int = None):
    model = _load("ml02_machining_time")
    if not model:
        return {"error": "Model not trained", "trained": False}

    rows = fetch_all("""
        SELECT ep.vitesse_coupe, ep.avance, ep.profondeur_passe,
               pg.temps_usinage_prevu, pg.temps_reglage_prevu,
               m.type AS machine_type, m.rpm_max,
               ot.type_outil, ot.matiere_outil,
               mat.type_matiere,
               op.niveau_competence
        FROM execution_phase ep
        JOIN phase_gamme pg ON ep.phase_gamme_id = pg.phase_gamme_id
        JOIN machine m ON ep.machine_id = m.machine_id
        JOIN outil ot ON ep.outil_id = ot.outil_id
        LEFT JOIN operateur op ON ep.operateur_id = op.operateur_id
        JOIN gamme_usinage g ON pg.gamme_id = g.gamme_id
        JOIN piece p ON g.piece_id = p.piece_id
        LEFT JOIN matiere mat ON p.matiere_id = mat.matiere_id
        WHERE (%s IS NULL OR m.code = %s)
          AND (%s IS NULL OR pg.phase_gamme_id = %s)
        LIMIT 200
    """, (machine_code, machine_code, phase_gamme_id, phase_gamme_id))

    if not rows:
        return {"error": "No matching data", "trained": True}

    features = _features("ml02_machining_time")
    df = pd.DataFrame(rows)
    for c in df.columns:
        try: df[c] = df[c].astype(float)
        except: pass
    for c in df.select_dtypes(exclude=["number"]).columns:
        if df[c].nunique() > 1:
            dummies = pd.get_dummies(df[c], prefix=c)
            df = pd.concat([df, dummies], axis=1)
            df.drop(columns=[c], inplace=True)

    X = _align(df, features)
    preds = model.predict(X)
    avg_pred = float(preds.mean())

    return {"trained": True, "estimated_time_min": round(avg_pred, 1), "samples_analyzed": len(df)}

# ── ML-03: Predictive Maintenance ──
def predict_next_maintenance(machine_code: str):
    model = _load("ml03_predictive_maint")
    if not model:
        return {"error": "Model not trained", "trained": False}

    last_maint = fetch_one("""
        SELECT m.type_maintenance, m.duree, m.cout,
               ma.type AS machine_type, ma.rpm_max
        FROM maintenance m
        JOIN machine ma ON m.machine_id = ma.machine_id
        WHERE ma.code = %s
        ORDER BY m.date_fin DESC NULLS LAST
        LIMIT 1
    """, (machine_code,))

    if not last_maint:
        return {"error": "No maintenance history for this machine", "trained": True}

    features = _features("ml03_predictive_maint")
    df = pd.DataFrame([last_maint])
    for c in df.columns:
        try: df[c] = df[c].astype(float)
        except: pass
    for c in df.select_dtypes(exclude=["number"]).columns:
        if df[c].nunique() > 1:
            dummies = pd.get_dummies(df[c], prefix=c)
            df = pd.concat([df, dummies], axis=1)
            df.drop(columns=[c], inplace=True)

    X = _align(df, features)
    days = max(0, float(model.predict(X)[0]))
    estimated_date = (datetime.now() + timedelta(days=int(days))).strftime("%Y-%m-%d")

    return {
        "trained": True,
        "estimated_days_until_maintenance": round(days, 1),
        "estimated_date": estimated_date,
        "confidence": "HIGH" if days > 0 else "LOW",
    }

# ── ML-04: Anomaly Detection ──
def predict_anomaly(machine_code: str):
    model = _load("ml04_failure_pred")
    if not model:
        return {"error": "Model not trained", "trained": False}

    rows = fetch_all("""
        SELECT s.temperature, s.vibration, s.rpm, s.charge_frappe, s.puissance,
               m.type AS machine_type, m.rpm_max
        FROM sensor_data s
        JOIN machine m ON s.machine_id = m.machine_id
        WHERE m.code = %s
        ORDER BY s.timestamp DESC
        LIMIT 1000
    """, (machine_code,))

    if not rows or len(rows) < 100:
        return {"error": "Insufficient sensor data (need >= 100 rows)", "trained": True}

    features = _features("ml04_failure_pred")
    temp = [float(r["temperature"]) for r in rows]
    vib = [float(r["vibration"]) for r in rows]
    rp = [float(r["rpm"]) for r in rows]
    ch = [float(r["charge_frappe"]) for r in rows]
    pw = [float(r["puissance"]) for r in rows]

    def m(arr): return sum(arr) / len(arr)
    def s(arr):
        avg = m(arr)
        return (sum((x - avg)**2 for x in arr) / len(arr))**0.5

    row = {
        "rpm_max": float(rows[0]["rpm_max"]),
        "temp_mean": m(temp), "temp_std": s(temp),
        "vib_mean": m(vib), "vib_std": s(vib),
        "rpm_mean": m(rp), "rpm_std": s(rp),
        "charge_mean": m(ch), "charge_std": s(ch),
        "power_mean": m(pw),
        "machine_type": rows[0]["machine_type"],
    }

    df = pd.DataFrame([row])
    for c in df.columns:
        try: df[c] = df[c].astype(float)
        except: pass
    for c in df.select_dtypes(exclude=["number"]).columns:
        if df[c].nunique() > 1:
            dummies = pd.get_dummies(df[c], prefix=c)
            df = pd.concat([df, dummies], axis=1)
            df.drop(columns=[c], inplace=True)

    X = _align(df, features)
    is_anomaly = int(model.predict(X)[0]) == -1
    anomaly_score = float(model.score_samples(X)[0])

    return {
        "trained": True,
        "is_anomaly": is_anomaly,
        "anomaly_score": round(anomaly_score, 4),
        "status": "ANOMALOUS" if is_anomaly else "NORMAL",
        "samples_analyzed": len(rows),
    }

# ── ML-05: Tool Wear Prediction ──
def predict_tool_wear(tool_code: str):
    model = _load("ml05_tool_wear")
    if not model:
        return {"error": "Model not trained", "trained": False}

    tool = fetch_one("""
        SELECT ot.code, ot.type_outil, ot.matiere_outil, ot.duree_vie_totale,
               ot.usure_actuelle
        FROM outil ot WHERE ot.code = %s
    """, (tool_code,))

    if not tool:
        return {"error": "Tool not found", "trained": True}

    last_use = fetch_one("""
        SELECT eo.duree_utilisation, ep.vitesse_coupe, ep.avance, ep.profondeur_passe
        FROM execution_outil eo
        JOIN execution_phase ep ON eo.execution_id = ep.execution_id
        JOIN outil ot ON eo.outil_id = ot.outil_id
        WHERE ot.code = %s
        ORDER BY eo.execution_outil_id DESC
        LIMIT 1
    """, (tool_code,))

    features = _features("ml05_tool_wear")
    row = {
        "duree_utilisation": float(last_use["duree_utilisation"]) if last_use else 0,
        "vitesse_coupe": float(last_use["vitesse_coupe"]) if last_use else 0,
        "avance": float(last_use["avance"]) if last_use else 0,
        "profondeur_passe": float(last_use["profondeur_passe"]) if last_use else 0,
        "duree_vie_totale": float(tool["duree_vie_totale"] or 0),
        "type_outil": tool["type_outil"],
        "matiere_outil": tool["matiere_outil"],
    }

    df = pd.DataFrame([row])
    for c in df.columns:
        try: df[c] = df[c].astype(float)
        except: pass
    for c in df.select_dtypes(exclude=["number"]).columns:
        if df[c].nunique() > 1:
            dummies = pd.get_dummies(df[c], prefix=c)
            df = pd.concat([df, dummies], axis=1)
            df.drop(columns=[c], inplace=True)

    X = _align(df, features)
    wear_increment = max(0, float(model.predict(X)[0]))
    total_wear = float(tool["usure_actuelle"] or 0) + wear_increment
    max_wear = float(tool["duree_vie_totale"] or 1)
    pct = round(total_wear / max_wear * 100, 1)

    return {
        "trained": True,
        "predicted_wear_increment": round(wear_increment, 1),
        "projected_total_wear": round(total_wear, 1),
        "wear_percentage_after_use": pct,
        "status": "CRITICAL" if pct >= 90 else "WARNING" if pct >= 70 else "OK",
    }

# ── ML-06: Production Duration ──
def predict_production_duration(of_id: int = None, numero_of: str = None, piece_famille: str = None):
    model = _load("ml06_prod_duration")
    if not model:
        return {"error": "Model not trained", "trained": False}

    if numero_of and not of_id:
        row = fetch_one("SELECT ordre_fabrication_id FROM ordre_fabrication WHERE numero_of = %s", (numero_of,))
        if row:
            of_id = row["ordre_fabrication_id"]

    if of_id:
        row = fetch_one("""
            SELECT of2.quantite_demandee, of2.quantite_produite,
                   g.nb_phases, g.duree_totale_estimee,
                   p.famille, mat.type_matiere,
                   op.niveau_competence
            FROM ordre_fabrication of2
            JOIN gamme_usinage g ON of2.gamme_id = g.gamme_id
            JOIN piece p ON of2.piece_id = p.piece_id
            LEFT JOIN matiere mat ON p.matiere_id = mat.matiere_id
            JOIN execution_phase ep ON ep.ordre_fabrication_id = of2.ordre_fabrication_id
            LEFT JOIN operateur op ON ep.operateur_id = op.operateur_id
            WHERE of2.ordre_fabrication_id = %s
            LIMIT 1
        """, (of_id,))
    else:
        row = fetch_one("""
            SELECT AVG(of2.quantite_demandee) AS quantite_demandee,
                   AVG(of2.quantite_produite) AS quantite_produite,
                   AVG(g.nb_phases) AS nb_phases,
                   AVG(g.duree_totale_estimee) AS duree_totale_estimee,
                   %s AS famille,
                   MAX(mat.type_matiere) AS type_matiere,
                   MAX(op.niveau_competence) AS niveau_competence
            FROM ordre_fabrication of2
            JOIN gamme_usinage g ON of2.gamme_id = g.gamme_id
            JOIN piece p ON of2.piece_id = p.piece_id
            LEFT JOIN matiere mat ON p.matiere_id = mat.matiere_id
            JOIN execution_phase ep ON ep.ordre_fabrication_id = of2.ordre_fabrication_id
            LEFT JOIN operateur op ON ep.operateur_id = op.operateur_id
            WHERE of2.statut = 'TERMINE'
              AND (%s IS NULL OR p.famille = %s)
        """, (piece_famille or "Standard", piece_famille, piece_famille))

    if not row:
        return {"error": "No data for prediction", "trained": True}

    features = _features("ml06_prod_duration")
    df = pd.DataFrame([row])
    for c in df.columns:
        try: df[c] = df[c].astype(float)
        except: pass
    for c in df.select_dtypes(exclude=["number"]).columns:
        if df[c].nunique() > 1:
            dummies = pd.get_dummies(df[c], prefix=c)
            df = pd.concat([df, dummies], axis=1)
            df.drop(columns=[c], inplace=True)

    X = _align(df, features)
    duration = max(0, float(model.predict(X)[0]))

    return {
        "trained": True,
        "estimated_duration_min": round(duration, 1),
        "estimated_duration_hours": round(duration / 60, 1),
    }

# ── ML-07: Inventory Forecast ──
def predict_stockout(matiere_code: str = None):
    path = os.path.join(MODEL_DIR, "ml07_inventory_forecast.json")
    if not os.path.exists(path):
        return {"error": "Model not trained", "trained": False}

    with open(path) as f:
        data = json.load(f)

    if matiere_code:
        data = [d for d in data if d["code"] == matiere_code]

    return {"trained": True, "items": data}

# ── All models status ──
def all_models_status():
    path = os.path.join(MODEL_DIR, "metrics.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}
