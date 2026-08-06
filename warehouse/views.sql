-- ============================================================
-- AMIP KPI Views
-- ============================================================

-- OEE par machine par jour
CREATE OR REPLACE VIEW dwh.v_oee_machine_daily AS
SELECT
    f.date_key,
    d.full_date,
    dm.code AS machine_code,
    dm.nom AS machine_nom,
    dm.type AS machine_type,
    COUNT(*) AS nb_executions,
    SUM(f.nb_pieces_produites) AS total_produites,
    SUM(f.nb_pieces_rebut) AS total_rebut,
    ROUND(AVG(f.taux_disponibilite) * 100, 2) AS disponibilite_pct,
    ROUND(AVG(f.taux_performance) * 100, 2) AS performance_pct,
    ROUND(AVG(f.taux_qualite) * 100, 2) AS qualite_pct,
    ROUND(AVG(f.oee) * 100, 2) AS oee_pct
FROM dwh.fact_execution f
JOIN dwh.dim_date d ON f.date_key = d.date_key
JOIN dwh.dim_machine dm ON f.machine_key = dm.machine_key
GROUP BY f.date_key, d.full_date, dm.code, dm.nom, dm.type
ORDER BY d.full_date, dm.code;

COMMENT ON VIEW dwh.v_oee_machine_daily IS 'OEE journalier par machine';

-- OEE global par mois
CREATE OR REPLACE VIEW dwh.v_oee_monthly AS
SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(AVG(f.oee) * 100, 2) AS oee_moyen_pct,
    ROUND(AVG(f.taux_disponibilite) * 100, 2) AS disponibilite_moyenne_pct,
    ROUND(AVG(f.taux_performance) * 100, 2) AS performance_moyenne_pct,
    ROUND(AVG(f.taux_qualite) * 100, 2) AS qualite_moyenne_pct,
    SUM(f.nb_pieces_produites) AS total_produites,
    SUM(f.nb_pieces_rebut) AS total_rebut,
    ROUND(CASE WHEN SUM(f.nb_pieces_produites) > 0
        THEN SUM(f.nb_pieces_rebut)::decimal / SUM(f.nb_pieces_produites) * 100 ELSE 0 END, 2) AS taux_rebut_pct
FROM dwh.fact_execution f
JOIN dwh.dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

COMMENT ON VIEW dwh.v_oee_monthly IS 'OEE mensuel global';

-- Taux de rebut par piece
DROP VIEW IF EXISTS dwh.v_scrap_by_part;
CREATE VIEW dwh.v_scrap_by_part AS
SELECT
    dp.reference,
    dp.designation,
    dp.famille,
    COUNT(*) AS nb_executions,
    SUM(f.nb_pieces_produites) AS total_produites,
    SUM(f.nb_pieces_rebut) AS total_rebut,
    ROUND(CASE WHEN SUM(f.nb_pieces_produites) > 0
        THEN SUM(f.nb_pieces_rebut)::decimal / SUM(f.nb_pieces_produites) * 100 ELSE 0 END, 2) AS taux_rebut_pct
FROM dwh.fact_execution f
JOIN dwh.dim_part dp ON f.part_key = dp.part_key
GROUP BY dp.reference, dp.designation, dp.famille
ORDER BY taux_rebut_pct DESC;

COMMENT ON VIEW dwh.v_scrap_by_part IS 'Taux de rebut par piece';

-- Maintenance cost par machine
CREATE OR REPLACE VIEW dwh.v_maintenance_cost AS
SELECT
    dm.code AS machine_code,
    dm.nom AS machine_nom,
    dmt.type_maintenance,
    dmt.categorie,
    COUNT(*) AS nb_interventions,
    SUM(f.duree_min) AS duree_totale_min,
    ROUND(SUM(f.cout), 2) AS cout_total,
    ROUND(AVG(f.cout), 2) AS cout_moyen
FROM dwh.fact_maintenance f
JOIN dwh.dim_machine dm ON f.machine_key = dm.machine_key
JOIN dwh.dim_maintenance_type dmt ON f.maint_type_key = dmt.maint_type_key
GROUP BY dm.code, dm.nom, dmt.type_maintenance, dmt.categorie
ORDER BY cout_total DESC;

COMMENT ON VIEW dwh.v_maintenance_cost IS 'Couts de maintenance par machine';

-- Production summary
CREATE OR REPLACE VIEW dwh.v_production_summary AS
SELECT
    dp.reference AS piece_ref,
    dp.famille,
    fp.quantite_demandee,
    fp.quantite_produite,
    fp.quantite_rebut,
    ROUND(fp.taux_rendement * 100, 2) AS rendement_pct,
    ROUND(fp.taux_rebut * 100, 2) AS rebut_pct,
    fp.duree_prevue_jours,
    fp.duree_reelle_jours,
    fp.ecart_duree_jours
FROM dwh.fact_production fp
JOIN dwh.dim_part dp ON fp.part_key = dp.part_key
ORDER BY fp.taux_rebut DESC;

COMMENT ON VIEW dwh.v_production_summary IS 'Resume production par OF';

-- Qualite par type de cause
CREATE OR REPLACE VIEW dwh.v_quality_by_cause AS
SELECT
    dqr.cause_categorie,
    dqr.cause_description,
    COUNT(*) AS nb_inspections,
    SUM(fq.nb_non_conformes) AS total_non_conformes,
    ROUND(AVG(fq.taux_conformite) * 100, 2) AS conformite_moyenne_pct
FROM dwh.fact_quality fq
JOIN dwh.dim_quality_result dqr ON fq.quality_result_key = dqr.quality_result_key
WHERE dqr.cause_description IS NOT NULL
GROUP BY dqr.cause_categorie, dqr.cause_description
ORDER BY total_non_conformes DESC;

COMMENT ON VIEW dwh.v_quality_by_cause IS 'Qualite par cause de defeaut';

-- Sensor summary par machine
CREATE OR REPLACE VIEW dwh.v_sensor_summary AS
SELECT
    dm.code AS machine_code,
    dm.nom AS machine_nom,
    ROUND(AVG(fs.temperature), 2) AS temp_moyenne,
    ROUND(MAX(fs.temperature), 2) AS temp_max,
    ROUND(AVG(fs.vibration), 3) AS vibration_moyenne,
    ROUND(MAX(fs.vibration), 3) AS vibration_max,
    ROUND(AVG(fs.charge_frappe), 2) AS charge_moyenne,
    ROUND(AVG(fs.puissance), 2) AS puissance_moyenne
FROM dwh.fact_sensors fs
JOIN dwh.dim_machine dm ON fs.machine_key = dm.machine_key
WHERE fs.statut_machine = 'RUNNING'
GROUP BY dm.code, dm.nom
ORDER BY dm.code;

COMMENT ON VIEW dwh.v_sensor_summary IS 'Resume capteurs par machine';
