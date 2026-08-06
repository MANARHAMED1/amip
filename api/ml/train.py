"""
Train all 7 ML models for AMIP.
Saves .joblib files to api/ml/models/
"""
import os, sys, json, warnings
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from api.database import fetch_all, fetch_one

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)

def df(q, p=None):
    rows = fetch_all(q, p)
    return pd.DataFrame(rows) if rows else pd.DataFrame()

metrics_file = os.path.join(MODEL_DIR, "metrics.json")
all_metrics = {}

# ─────────────────────────────────────────────
# ML-01: Scrap Prediction (XGBoost Classifier)
# ─────────────────────────────────────────────
print("="*60)
print("ML-01: Scrap Prediction")
print("="*60)

exec_df = df("""
    SELECT ep.execution_id, ep.vitesse_coupe, ep.avance, ep.profondeur_passe,
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
    WHERE ep.nb_pieces_produites > 0
""")

print(f"  Rows: {len(exec_df)}")

ml01_available = len(exec_df) >= 200

if ml01_available:
    # Target: scrap rate > median (~3.4%) = positive class (balanced split)
    exec_df["total"] = exec_df["nb_pieces_produites"] + exec_df["nb_pieces_rebut"]
    exec_df["scrap_rate"] = exec_df["nb_pieces_rebut"] / exec_df["total"].clip(1)
    med = exec_df["scrap_rate"].median()
    exec_df["target"] = (exec_df["scrap_rate"] > med).astype(int)

    features = ["vitesse_coupe","avance","profondeur_passe",
                "rpm_max","temps_usinage_prevu"]
    cat_features = ["machine_type","type_outil","matiere_outil","niveau_competence"]

    for col in cat_features:
        dummies = pd.get_dummies(exec_df[col], prefix=col)
        features.extend(dummies.columns.tolist())
        exec_df = pd.concat([exec_df, dummies], axis=1)

    exec_df = exec_df.replace([np.inf, -np.inf], np.nan).fillna(0)
    X = exec_df[features].values
    y = exec_df["target"].values

    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
    import xgboost as xgb

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = xgb.XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1,
                              eval_metric="logloss", use_label_encoder=False, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:,1]

    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    print(f"  Accuracy: {acc:.3f}, AUC: {auc:.3f}")
    print(classification_report(y_test, y_pred, target_names=["OK", "SCRAP"]))

    from joblib import dump
    dump(model, os.path.join(MODEL_DIR, "ml01_scrap.joblib"))
    with open(os.path.join(MODEL_DIR, "ml01_features.json"), "w") as f:
        json.dump(features, f)
    all_metrics["ml01_scrap"] = {"trained": True, "accuracy": round(acc,3), "auc": round(auc,3),
                                  "samples": len(exec_df), "features": len(features)}
else:
    all_metrics["ml01_scrap"] = {"trained": False,
        "reason": f"Insufficient execution data with features ({len(exec_df)} rows, need >= 200)"}

# ─────────────────────────────────────────────
# ML-02: Machining Time Estimation (XGBoost Regressor)
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("ML-02: Machining Time Estimation")
print("="*60)

time_df = df("""
    SELECT ep.temps_usinage_reel, ep.vitesse_coupe, ep.avance, ep.profondeur_passe,
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
    WHERE ep.temps_usinage_reel IS NOT NULL AND ep.temps_usinage_reel > 0
""")

print(f"  Rows: {len(time_df)}")

ml02_available = len(time_df) >= 200

if ml02_available:
    time_df = time_df.replace([np.inf, -np.inf], np.nan).fillna(0)

    features2 = ["vitesse_coupe","avance","profondeur_passe",
                 "temps_usinage_prevu","temps_reglage_prevu","rpm_max"]
    cat_features2 = ["machine_type","type_outil","matiere_outil","type_matiere","niveau_competence"]
    for col in cat_features2:
        dummies = pd.get_dummies(time_df[col], prefix=col)
        features2.extend(dummies.columns.tolist())
        time_df = pd.concat([time_df, dummies], axis=1)

    X2 = time_df[features2].values
    y2 = time_df["temps_usinage_reel"].values

    X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.2, random_state=42)

    model2 = xgb.XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42)
    model2.fit(X2_train, y2_train)

    y2_pred = model2.predict(X2_test)
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    mae = mean_absolute_error(y2_test, y2_pred)
    rmse = np.sqrt(mean_squared_error(y2_test, y2_pred))
    print(f"  MAE: {mae:.1f} min, RMSE: {rmse:.1f} min")
    print(f"  Mean actual: {y2.mean():.1f} min")

    dump(model2, os.path.join(MODEL_DIR, "ml02_machining_time.joblib"))
    with open(os.path.join(MODEL_DIR, "ml02_features.json"), "w") as f:
        json.dump(features2, f)
    all_metrics["ml02_machining_time"] = {"trained": True, "mae": round(mae,1), "rmse": round(rmse,1),
                                           "samples": len(time_df)}
else:
    all_metrics["ml02_machining_time"] = {"trained": False,
        "reason": f"Insufficient data ({len(time_df)} rows, need >= 200)"}

# ─────────────────────────────────────────────
# ML-03: Predictive Maintenance (XGBoost Regressor)
# Days-until-failure from historical intervals
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("ML-03: Predictive Maintenance (days-until-failure)")
print("="*60)

maint_df = df("""
    SELECT m.maintenance_id, m.machine_id, m.type_maintenance,
           m.date_debut, m.date_fin, m.duree, m.cout,
           ma.code, ma.type AS machine_type, ma.rpm_max, ma.date_installation
    FROM maintenance m
    JOIN machine ma ON m.machine_id = ma.machine_id
    WHERE m.date_fin IS NOT NULL
    ORDER BY m.machine_id, m.date_fin
""")

print(f"  Maintenance records: {len(maint_df)}")

# Compute inter-failure intervals per machine
ml03_available = len(maint_df) >= 100

if ml03_available:
    maint_df["date_fin"] = pd.to_datetime(maint_df["date_fin"])
    maint_df["date_debut"] = pd.to_datetime(maint_df["date_debut"])
    machines_inst = dict(zip(maint_df["code"].unique(),
                              [None]*len(maint_df["code"].unique())))

    intervals = []
    for code, grp in maint_df.sort_values("date_fin").groupby("code"):
        grp = grp.reset_index(drop=True)
        for i in range(1, len(grp)):
            days = (grp.loc[i, "date_debut"] - grp.loc[i-1, "date_fin"]).total_seconds() / 86400
            if 0 <= days <= 365:
                intervals.append({
                    "code": code,
                    "machine_type": grp.loc[i, "machine_type"],
                    "rpm_max": grp.loc[i, "rpm_max"],
                    "prev_type": grp.loc[i-1, "type_maintenance"],
                    "prev_duree": grp.loc[i-1, "duree"] or 0,
                    "prev_cout": grp.loc[i-1, "cout"] or 0,
                    "days_until_failure": days
                })

    int_df = pd.DataFrame(intervals)
    print(f"  Failure intervals: {len(int_df)}")
    ml03_available = len(int_df) >= 50

if ml03_available:
    int_df = int_df.replace([np.inf, -np.inf], np.nan).fillna(0)

    features3 = ["rpm_max","prev_duree","prev_cout"]
    cat3 = ["machine_type","prev_type"]
    for col in cat3:
        dummies = pd.get_dummies(int_df[col], prefix=col)
        features3.extend(dummies.columns.tolist())
        int_df = pd.concat([int_df, dummies], axis=1)

    X3 = int_df[features3].values
    y3 = int_df["days_until_failure"].values

    X3_train, X3_test, y3_train, y3_test = train_test_split(X3, y3, test_size=0.2, random_state=42)

    model3 = xgb.XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42)
    model3.fit(X3_train, y3_train)
    y3_pred = model3.predict(X3_test)
    mae3 = mean_absolute_error(y3_test, y3_pred)
    rmse3 = np.sqrt(mean_squared_error(y3_test, y3_pred))
    print(f"  MAE: {mae3:.1f} days, RMSE: {rmse3:.1f} days")
    print(f"  Mean interval: {y3.mean():.1f} days")

    dump(model3, os.path.join(MODEL_DIR, "ml03_predictive_maint.joblib"))
    with open(os.path.join(MODEL_DIR, "ml03_features.json"), "w") as f:
        json.dump(features3, f)
    all_metrics["ml03_predictive_maint"] = {"trained": True, "mae": round(mae3,1), "rmse": round(rmse3,1),
                                              "samples": len(int_df)}
else:
    reason = f"Insufficient maintenance intervals ({len(intervals) if 'intervals' in dir() else 'N/A'}, need >= 50)"
    all_metrics["ml03_predictive_maint"] = {"trained": False, "reason": reason}

# ─────────────────────────────────────────────
# ML-04: Machine Anomaly Detection (IsolationForest)
# Flags abnormal sensor patterns that may indicate impending failure.
# Historical data has only 1 BROKEN record out of 1M, so anomaly
# detection is the appropriate approach.
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("ML-04: Machine Anomaly Detection (IsolationForest)")
print("="*60)

sensor_df = df("""
    SELECT s.machine_id, s.temperature, s.vibration,
           s.rpm, s.charge_frappe, s.puissance, s.statut_machine,
           m.code, m.type AS machine_type, m.rpm_max
    FROM sensor_data s
    JOIN machine m ON s.machine_id = m.machine_id
""")

print(f"  Sensor rows: {len(sensor_df)}")

ml04_available = len(sensor_df) >= 10000

if ml04_available:
    for col in ["temperature","vibration","rpm","charge_frappe","puissance"]:
        sensor_df[col] = sensor_df[col].astype(float)

    # Compute per-machine z-score features
    anomaly_rows = []
    for code, grp in sensor_df.groupby("code"):
        n = len(grp)
        step = max(1, n // 200)
        for i in range(0, n, step):
            window = grp.iloc[i:min(i+1000,n)]
            if len(window) < 100:
                continue
            anomaly_rows.append({
                "code": code,
                "machine_type": grp["machine_type"].iloc[0],
                "rpm_max": grp["rpm_max"].iloc[0],
                "temp_mean": window["temperature"].mean(),
                "temp_std": window["temperature"].std(ddof=0),
                "vib_mean": window["vibration"].mean(),
                "vib_std": window["vibration"].std(ddof=0),
                "rpm_mean": window["rpm"].mean(),
                "rpm_std": window["rpm"].std(ddof=0),
                "charge_mean": window["charge_frappe"].mean(),
                "charge_std": window["charge_frappe"].std(ddof=0),
                "power_mean": window["puissance"].mean(),
                "is_maintenance": int((window["statut_machine"] != "RUNNING").mean() > 0.5)
            })

    anomalydf = pd.DataFrame(anomaly_rows)
    print(f"  Windows: {len(anomalydf)}")
    ml04_available = len(anomalydf) >= 100

if ml04_available:
    anomalydf = anomalydf.replace([np.inf, -np.inf], np.nan).fillna(0)

    features4 = ["rpm_max","temp_mean","temp_std","vib_mean","vib_std",
                 "rpm_mean","rpm_std","charge_mean","charge_std","power_mean"]
    cat4 = ["machine_type"]
    for col in cat4:
        dummies = pd.get_dummies(anomalydf[col], prefix=col)
        features4.extend(dummies.columns.tolist())
        anomalydf = pd.concat([anomalydf, dummies], axis=1)

    X4 = anomalydf[features4].values

    from sklearn.ensemble import IsolationForest
    model4 = IsolationForest(n_estimators=200, contamination=0.05, random_state=42)
    model4.fit(X4)

    # Evaluate anomaly detection on the same data
    y4_pred = model4.predict(X4)
    anomaly_rate = (y4_pred == -1).mean()
    print(f"  Anomaly rate (train): {anomaly_rate:.3f}")

    dump(model4, os.path.join(MODEL_DIR, "ml04_failure_pred.joblib"))
    with open(os.path.join(MODEL_DIR, "ml04_features.json"), "w") as f:
        json.dump(features4, f)
    with open(os.path.join(MODEL_DIR, "ml04_code_map.json"), "w") as f:
        mappings = anomalydf[["code","machine_type","rpm_max"]].drop_duplicates("code")
        json.dump(mappings.to_dict(orient="records"), f, default=str)
    all_metrics["ml04_failure_pred"] = {"trained": True, "anomaly_rate": round(anomaly_rate,3),
                                         "samples": len(anomalydf), "type": "IsolationForest"}
else:
    all_metrics["ml04_failure_pred"] = {"trained": False,
        "reason": f"Insufficient data ({len(anomalydf) if 'anomalydf' in dir() else 'N/A'})"}

# ─────────────────────────────────────────────
# ML-05: Tool Wear Prediction (XGBoost Regressor)
# Predict remaining useful life based on cycles + params
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("ML-05: Tool Wear Prediction")
print("="*60)

wear_df = df("""
    SELECT eo.outil_id, eo.usure_debut, eo.usure_fin, eo.duree_utilisation,
           ep.vitesse_coupe, ep.avance, ep.profondeur_passe,
           ot.type_outil, ot.matiere_outil, ot.duree_vie_totale,
           ot.usure_actuelle
    FROM execution_outil eo
    JOIN execution_phase ep ON eo.execution_id = ep.execution_id
    JOIN outil ot ON eo.outil_id = ot.outil_id
    WHERE eo.usure_fin IS NOT NULL AND eo.usure_debut IS NOT NULL
""")

print(f"  Rows: {len(wear_df)}")

ml05_available = len(wear_df) >= 200

if ml05_available:
    wear_df["usure_increment"] = wear_df["usure_fin"] - wear_df["usure_debut"]
    wear_df = wear_df[wear_df["usure_increment"] >= 0].copy()
    wear_df = wear_df.replace([np.inf, -np.inf], np.nan).fillna(0)

    features5 = ["duree_utilisation","vitesse_coupe","avance","profondeur_passe","duree_vie_totale"]
    cat5 = ["type_outil","matiere_outil"]
    for col in cat5:
        dummies = pd.get_dummies(wear_df[col], prefix=col)
        features5.extend(dummies.columns.tolist())
        wear_df = pd.concat([wear_df, dummies], axis=1)

    X5 = wear_df[features5].values
    y5 = wear_df["usure_increment"].values

    X5_train, X5_test, y5_train, y5_test = train_test_split(X5, y5, test_size=0.2, random_state=42)

    model5 = xgb.XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42)
    model5.fit(X5_train, y5_train)
    y5_pred = model5.predict(X5_test)
    mae5 = mean_absolute_error(y5_test, y5_pred)
    rmse5 = np.sqrt(mean_squared_error(y5_test, y5_pred))
    print(f"  MAE: {mae5:.1f} wear units, RMSE: {rmse5:.1f}")
    print(f"  Mean increment: {y5.mean():.1f}")

    dump(model5, os.path.join(MODEL_DIR, "ml05_tool_wear.joblib"))
    with open(os.path.join(MODEL_DIR, "ml05_features.json"), "w") as f:
        json.dump(features5, f)
    all_metrics["ml05_tool_wear"] = {"trained": True, "mae": round(mae5,1), "rmse": round(rmse5,1),
                                      "samples": len(wear_df)}
else:
    all_metrics["ml05_tool_wear"] = {"trained": False,
        "reason": f"Insufficient tool usage records ({len(wear_df)}, need >= 200)"}

# ─────────────────────────────────────────────
# ML-06: Production Duration Prediction (XGBoost Regressor)
# Predict total duration of an OF based on qty, gamme, operator, material
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("ML-06: Production Duration Prediction")
print("="*60)

duration_df = df("""
    SELECT of2.ordre_fabrication_id, of2.quantite_demandee, of2.quantite_produite,
           g.nb_phases, g.duree_totale_estimee,
           p.famille,
           mat.type_matiere,
           op.niveau_competence,
           SUM(ep.temps_usinage_reel + COALESCE(ep.temps_reglage_reel,0)) AS duree_totale_reelle
    FROM ordre_fabrication of2
    JOIN gamme_usinage g ON of2.gamme_id = g.gamme_id
    JOIN piece p ON of2.piece_id = p.piece_id
    LEFT JOIN matiere mat ON p.matiere_id = mat.matiere_id
    JOIN execution_phase ep ON ep.ordre_fabrication_id = of2.ordre_fabrication_id
    LEFT JOIN operateur op ON ep.operateur_id = op.operateur_id
    WHERE of2.statut = 'TERMINE'
      AND ep.temps_usinage_reel IS NOT NULL
    GROUP BY of2.ordre_fabrication_id, of2.quantite_demandee, of2.quantite_produite,
             g.nb_phases, g.duree_totale_estimee, p.famille, mat.type_matiere, op.niveau_competence
""")

print(f"  Completed OFs: {len(duration_df)}")

ml06_available = len(duration_df) >= 200

if ml06_available:
    duration_df = duration_df.replace([np.inf, -np.inf], np.nan).fillna(0)

    features6 = ["quantite_demandee","quantite_produite","nb_phases","duree_totale_estimee"]
    cat6 = ["famille","type_matiere","niveau_competence"]
    for col in cat6:
        dummies = pd.get_dummies(duration_df[col], prefix=col)
        features6.extend(dummies.columns.tolist())
        duration_df = pd.concat([duration_df, dummies], axis=1)

    X6 = duration_df[features6].values
    y6 = duration_df["duree_totale_reelle"].values

    X6_train, X6_test, y6_train, y6_test = train_test_split(X6, y6, test_size=0.2, random_state=42)

    model6 = xgb.XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42)
    model6.fit(X6_train, y6_train)
    y6_pred = model6.predict(X6_test)
    mae6 = mean_absolute_error(y6_test, y6_pred)
    rmse6 = np.sqrt(mean_squared_error(y6_test, y6_pred))
    print(f"  MAE: {mae6:.1f} min, RMSE: {rmse6:.1f} min")
    print(f"  Mean duration: {y6.mean():.1f} min")

    dump(model6, os.path.join(MODEL_DIR, "ml06_prod_duration.joblib"))
    with open(os.path.join(MODEL_DIR, "ml06_features.json"), "w") as f:
        json.dump(features6, f)
    all_metrics["ml06_prod_duration"] = {"trained": True, "mae": round(mae6,1), "rmse": round(rmse6,1),
                                          "samples": len(duration_df)}
else:
    all_metrics["ml06_prod_duration"] = {"trained": False,
        "reason": f"Insufficient completed OFs ({len(duration_df)}, need >= 200)"}

# ─────────────────────────────────────────────
# ML-07: Inventory Forecasting (Linear trend projection)
# Predict stock-out date based on consumption rate
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("ML-07: Inventory Forecasting")
print("="*60)

# For matieres: get current stock, consumption from OFs
inv_df = df("""
    SELECT sm.stock_matiere_id, sm.quantite_stock, sm.seuil_alerte,
           m.code, m.designation, m.type_matiere
    FROM stock_matiere sm
    JOIN matiere m ON sm.matiere_id = m.matiere_id
""")

# Get consumption rate: total matiere used in completed OFs (approximate via pieces)
consumption = df("""
    SELECT mat.matiere_id, COUNT(*) AS nb_of, SUM(of2.quantite_produite) AS total_produit
    FROM ordre_fabrication of2
    JOIN piece p ON of2.piece_id = p.piece_id
    JOIN matiere mat ON p.matiere_id = mat.matiere_id
    WHERE of2.statut = 'TERMINE'
    GROUP BY mat.matiere_id
""")

if len(inv_df) > 0 and len(consumption) > 0:
    inv_df = inv_df.merge(consumption, left_on="stock_matiere_id", right_on="matiere_id", how="left")
    for col in ["quantite_stock","seuil_alerte","total_produit"]:
        inv_df[col] = inv_df[col].astype(float)
    inv_df = inv_df.replace([np.inf, -np.inf], np.nan).fillna(0)
    inv_df["monthly_consumption"] = inv_df["total_produit"] / 6.0  # ~6 months simulated data
    inv_df["months_to_depletion"] = inv_df.apply(
        lambda r: r["quantite_stock"] / max(r["monthly_consumption"], 0.01), axis=1)
    inv_df["depletion_date_est"] = (datetime.now() + pd.to_timedelta(inv_df["months_to_depletion"] * 30, unit="D")).dt.strftime("%Y-%m-%d")

    result = inv_df[["code","designation","type_matiere","quantite_stock","seuil_alerte",
                     "monthly_consumption","months_to_depletion","depletion_date_est"]].to_dict(orient="records")
    with open(os.path.join(MODEL_DIR, "ml07_inventory_forecast.json"), "w") as f:
        json.dump(result, f, default=str)
    all_metrics["ml07_inventory"] = {"trained": True, "items": len(result),
                                      "note": "Trend projection (linear consumption rate)"}
    print(f"  Items forecasted: {len(result)}")
else:
    all_metrics["ml07_inventory"] = {"trained": False,
        "reason": f"No inventory or consumption data found"}

# ─────────────────────────────────────────────
# Final report
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("TRAINING COMPLETE")
print("="*60)
for k, v in all_metrics.items():
    status = "TRAINED" if v.get("trained") else "SKIPPED"
    print(f"  {k}: {status} - {v}")

with open(metrics_file, "w") as f:
    json.dump(all_metrics, f, indent=2, default=str)

print(f"\nModels saved to: {MODEL_DIR}")
print(f"Metrics: {metrics_file}")
