import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import psycopg2
from datetime import date

DB_CONFIG = {
    "host": os.environ.get("AMIP_DB_HOST", "localhost"),
    "port": int(os.environ.get("AMIP_DB_PORT", "5432")),
    "dbname": os.environ.get("AMIP_DB_NAME", "amip"),
    "user": os.environ.get("AMIP_DB_USER", "postgres"),
    "password": os.environ.get("AMIP_DB_PASSWORD", "change_me_in_production"),
}


def etl_dim_date(cur, conn):
    cur.execute("DELETE FROM dwh.dim_date")
    start = date(2025, 1, 1)
    end = date(2027, 12, 31)
    d = start
    rows = []
    while d <= end:
        key = d.year * 10000 + d.month * 100 + d.day
        rows.append((
            key, d, d.year, (d.month - 1) // 3 + 1, d.month,
            d.strftime("%B"), d.isocalendar()[1], d.day,
            d.isoweekday(), d.strftime("%A"),
            d.isoweekday() >= 6, d.strftime("%Y-%m"),
        ))
        d = __import__("datetime").timedelta(days=1) + d
    cur.executemany(
        "INSERT INTO dwh.dim_date VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        rows,
    )
    conn.commit()
    return len(rows)


def etl_dim_machine(cur, conn):
    cur.execute("DELETE FROM dwh.dim_machine")
    cur.execute("""
        INSERT INTO dwh.dim_machine
            (machine_id, code, nom, type, marque, modele, controller, axes, rpm_max, statut, secteur_code, secteur_nom)
        SELECT m.machine_id, m.code, m.nom, m.type, m.marque, m.modele, m.controller,
               m.axes, m.rpm_max, m.statut, s.code, s.nom
        FROM machine m JOIN secteur s ON m.secteur_id = s.secteur_id
        ORDER BY m.machine_id
    """)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dwh.dim_machine")
    return cur.fetchone()[0]


def etl_dim_part(cur, conn):
    cur.execute("DELETE FROM dwh.dim_part")
    cur.execute("""
        INSERT INTO dwh.dim_part
            (piece_id, reference, designation, famille, matiere_code, matiere_designation, matiere_type, matiere_nuance, poids, dimensions)
        SELECT p.piece_id, p.reference, p.designation, p.famille,
               m.code, m.designation, m.type_matiere, m.nuance, p.poids, p.dimensions
        FROM piece p LEFT JOIN matiere m ON p.matiere_id = m.matiere_id
        ORDER BY p.piece_id
    """)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dwh.dim_part")
    return cur.fetchone()[0]


def etl_dim_material(cur, conn):
    cur.execute("DELETE FROM dwh.dim_material")
    cur.execute("""
        INSERT INTO dwh.dim_material (matiere_id, code, designation, type_matiere, nuance, densite, prix_kg)
        SELECT matiere_id, code, designation, type_matiere, nuance, densite, prix_kg
        FROM matiere ORDER BY matiere_id
    """)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dwh.dim_material")
    return cur.fetchone()[0]


def etl_dim_tool(cur, conn):
    cur.execute("DELETE FROM dwh.dim_tool")
    cur.execute("""
        INSERT INTO dwh.dim_tool (outil_id, code, designation, type_outil, diametre, matiere_outil, duree_vie_totale, cout_achat, cout_remplacement)
        SELECT outil_id, code, designation, type_outil, diametre, matiere_outil, duree_vie_totale, cout_achat, cout_remplacement
        FROM outil ORDER BY outil_id
    """)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dwh.dim_tool")
    return cur.fetchone()[0]


def etl_dim_sector(cur, conn):
    cur.execute("DELETE FROM dwh.dim_sector")
    cur.execute("""
        INSERT INTO dwh.dim_sector (secteur_id, code, nom, description)
        SELECT secteur_id, code, nom, description FROM secteur ORDER BY secteur_id
    """)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dwh.dim_sector")
    return cur.fetchone()[0]


def etl_dim_order(cur, conn):
    cur.execute("DELETE FROM dwh.dim_production_order")
    cur.execute("""
        INSERT INTO dwh.dim_production_order
            (ordre_fabrication_id, numero_of, priorite, statut, date_debut_prevue, date_fin_prevue, date_debut_reelle, date_fin_reelle)
        SELECT ordre_fabrication_id, numero_of, priorite, statut,
               date_debut_prevue, date_fin_prevue, date_debut_reelle, date_fin_reelle
        FROM ordre_fabrication ORDER BY ordre_fabrication_id
    """)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dwh.dim_production_order")
    return cur.fetchone()[0]


def etl_dim_operateur(cur, conn):
    cur.execute("DELETE FROM dwh.dim_operateur")
    cur.execute("""
        INSERT INTO dwh.dim_operateur (operateur_id, matricule, nom, prenom, poste, niveau_competence)
        SELECT operateur_id, matricule, nom, prenom, poste, niveau_competence
        FROM operateur ORDER BY operateur_id
    """)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dwh.dim_operateur")
    return cur.fetchone()[0]


def etl_dim_maint_type(cur, conn):
    cur.execute("DELETE FROM dwh.dim_maintenance_type")
    types = [
        ("Preventive", "Planifiee"),
        ("Corrective", "Non planifiee"),
        ("Changement huile", "Planifiee"),
        ("Nettoyage", "Planifiee"),
        ("Inspection", "Planifiee"),
        ("Remplacement roulement", "Corrective"),
        ("Changement liquide", "Planifiee"),
        ("Alignement machine", "Planifiee"),
    ]
    cur.executemany("INSERT INTO dwh.dim_maintenance_type (type_maintenance, categorie) VALUES (%s, %s)", types)
    conn.commit()
    return len(types)


def etl_dim_quality_result(cur, conn):
    cur.execute("DELETE FROM dwh.dim_quality_result")
    cur.execute("""
        INSERT INTO dwh.dim_quality_result (resultat, est_conforme, cause_categorie, cause_description)
        SELECT DISTINCT cr.code, FALSE, cr.categorie, cr.description
        FROM cause_rebut cr
        UNION ALL
        SELECT 'CONFORME', TRUE, NULL, NULL
        UNION ALL
        SELECT 'EN_ATTENTE', FALSE, NULL, NULL
    """)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dwh.dim_quality_result")
    return cur.fetchone()[0]


def etl_fact_production(cur, conn):
    cur.execute("DELETE FROM dwh.fact_production")
    cur.execute("""
        INSERT INTO dwh.fact_production (
            date_key, part_key, material_key, order_key, sector_key,
            quantite_demandee, quantite_produite, quantite_rebut,
            taux_rebut, taux_rendement, duree_prevue_jours, duree_reelle_jours, ecart_duree_jours
        )
        SELECT
            EXTRACT(YEAR FROM o.date_fin_reelle)::int * 10000 + EXTRACT(MONTH FROM o.date_fin_reelle)::int * 100 + EXTRACT(DAY FROM o.date_fin_reelle)::int,
            dp.part_key,
            dm.material_key,
            dpo.order_key,
            ds.sector_key,
            o.quantite_demandee,
            o.quantite_produite,
            o.quantite_rebut,
            CASE WHEN o.quantite_produite > 0 THEN o.quantite_rebut::decimal / o.quantite_produite ELSE 0 END,
            CASE WHEN o.quantite_demandee > 0 THEN o.quantite_produite::decimal / o.quantite_demandee ELSE 0 END,
            EXTRACT(EPOCH FROM (o.date_fin_prevue::timestamp - o.date_debut_prevue::timestamp)) / 86400,
            CASE WHEN o.date_fin_reelle IS NOT NULL AND o.date_debut_reelle IS NOT NULL
                 THEN EXTRACT(EPOCH FROM (o.date_fin_reelle::timestamp - o.date_debut_reelle::timestamp)) / 86400 ELSE NULL END,
            CASE WHEN o.date_fin_reelle IS NOT NULL AND o.date_debut_reelle IS NOT NULL
                 THEN EXTRACT(EPOCH FROM (o.date_fin_reelle::timestamp - o.date_debut_reelle::timestamp)) / 86400
                    - EXTRACT(EPOCH FROM (o.date_fin_prevue::timestamp - o.date_debut_prevue::timestamp)) / 86400
                 ELSE NULL END
        FROM ordre_fabrication o
        JOIN piece p ON o.piece_id = p.piece_id
        JOIN dwh.dim_part dp ON o.piece_id = dp.piece_id
        LEFT JOIN dwh.dim_material dm ON p.matiere_id = dm.matiere_id
        JOIN dwh.dim_production_order dpo ON o.ordre_fabrication_id = dpo.ordre_fabrication_id
        JOIN dwh.dim_sector ds ON ds.code = 'T01'
        WHERE o.statut = 'TERMINE' AND o.date_fin_reelle IS NOT NULL
    """)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dwh.fact_production")
    return cur.fetchone()[0]


def etl_fact_execution(cur, conn):
    cur.execute("DELETE FROM dwh.fact_execution")
    cur.execute("""
        INSERT INTO dwh.fact_execution (
            date_key, machine_key, part_key, tool_key, operateur_key, order_key,
            temps_usinage_prevu, temps_reglage_prevu, temps_usinage_reel, temps_reglage_reel,
            nb_pieces_produites, nb_pieces_rebut, vitesse_coupe, avance, profondeur_passe,
            temps_disponible_min, temps_operation_min, nb_cycles,
            taux_disponibilite, taux_performance, taux_qualite, oee
        )
        SELECT
            EXTRACT(YEAR FROM e.date_debut)::int * 10000 + EXTRACT(MONTH FROM e.date_debut)::int * 100 + EXTRACT(DAY FROM e.date_debut)::int,
            dm.machine_key,
            dp.part_key,
            dt.tool_key,
            dop.operateur_key,
            dpo.order_key,
            pg.temps_usinage_prevu,
            pg.temps_reglage_prevu,
            e.temps_usinage_reel,
            e.temps_reglage_reel,
            e.nb_pieces_produites,
            e.nb_pieces_rebut,
            e.vitesse_coupe,
            e.avance,
            e.profondeur_passe,
            e.temps_usinage_reel + e.temps_reglage_reel,
            e.temps_usinage_reel,
            CASE WHEN e.nb_pieces_produites > 0 THEN e.nb_pieces_produites ELSE 1 END,
            CASE WHEN (e.temps_usinage_reel + e.temps_reglage_reel) > 0
                 THEN e.temps_usinage_reel::decimal / (e.temps_usinage_reel + e.temps_reglage_reel) ELSE 0 END,
            CASE WHEN e.temps_usinage_reel > 0 AND pg.temps_usinage_prevu > 0
                 THEN LEAST(1.0, (pg.temps_usinage_prevu::decimal * e.nb_pieces_produites) / e.temps_usinage_reel) ELSE 0 END,
            CASE WHEN e.nb_pieces_produites > 0
                 THEN (e.nb_pieces_produites - e.nb_pieces_rebut)::decimal / e.nb_pieces_produites ELSE 0 END,
            0
        FROM execution_phase e
        JOIN dwh.dim_machine dm ON e.machine_id = dm.machine_id
        JOIN phase_gamme pg ON e.phase_gamme_id = pg.phase_gamme_id
        JOIN gamme_usinage g ON pg.gamme_id = g.gamme_id
        JOIN dwh.dim_part dp ON g.piece_id = dp.piece_id
        LEFT JOIN dwh.dim_tool dt ON e.outil_id = dt.outil_id
        LEFT JOIN dwh.dim_operateur dop ON e.operateur_id = dop.operateur_id
        JOIN dwh.dim_production_order dpo ON e.ordre_fabrication_id = dpo.ordre_fabrication_id
        WHERE e.statut = 'TERMINE'
    """)
    cur.execute("""
        UPDATE dwh.fact_execution
        SET oee = taux_disponibilite * taux_performance * taux_qualite
    """)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dwh.fact_execution")
    return cur.fetchone()[0]


def etl_fact_quality(cur, conn):
    cur.execute("DELETE FROM dwh.fact_quality")
    cur.execute("""
        INSERT INTO dwh.fact_quality (
            date_key, part_key, quality_result_key, machine_key,
            nb_controles, nb_conformes, nb_non_conformes, taux_conformite,
            dimension_mesuree, dimension_cible, ecart_dimension, rugosite_mesuree
        )
        SELECT
            EXTRACT(YEAR FROM cq.date_controle)::int * 10000 + EXTRACT(MONTH FROM cq.date_controle)::int * 100 + EXTRACT(DAY FROM cq.date_controle)::int,
            dp.part_key,
            dqr.quality_result_key,
            dm.machine_key,
            cq.nb_controles,
            cq.nb_conformes,
            cq.nb_non_conformes,
            CASE WHEN cq.nb_controles > 0 THEN cq.nb_conformes::decimal / cq.nb_controles ELSE 0 END,
            cq.dimension_mesuree,
            cq.dimension_cible,
            CASE WHEN cq.dimension_mesuree IS NOT NULL AND cq.dimension_cible IS NOT NULL
                 THEN cq.dimension_mesuree - cq.dimension_cible ELSE NULL END,
            cq.rugosite_mesuree
        FROM controle_qualite cq
        JOIN dwh.dim_part dp ON cq.piece_id = dp.piece_id
        JOIN execution_phase ep ON cq.execution_id = ep.execution_id
        JOIN dwh.dim_machine dm ON ep.machine_id = dm.machine_id
        LEFT JOIN cause_rebut cr ON cq.cause_rebut_id = cr.cause_rebut_id
        LEFT JOIN dwh.dim_quality_result dqr ON (
            (cq.resultat = dqr.resultat AND cr IS NULL AND dqr.cause_description IS NULL)
            OR (cr.description = dqr.cause_description)
        )
        WHERE cq.resultat IN ('CONFORME', 'NON_CONFORME')
    """)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dwh.fact_quality")
    return cur.fetchone()[0]


def etl_fact_sensors(cur, conn):
    cur.execute("DELETE FROM dwh.fact_sensors")
    cur.execute("""
        INSERT INTO dwh.fact_sensors (
            date_key, machine_key, timestamp, temperature, vibration, rpm,
            charge_frappe, puissance, vitesse_avance, statut_machine, temps_cycle
        )
        SELECT
            EXTRACT(YEAR FROM s.timestamp)::int * 10000 + EXTRACT(MONTH FROM s.timestamp)::int * 100 + EXTRACT(DAY FROM s.timestamp)::int,
            dm.machine_key,
            s.timestamp, s.temperature, s.vibration, s.rpm,
            s.charge_frappe, s.puissance, s.vitesse_avance, s.statut_machine, s.temps_cycle
        FROM sensor_data s
        JOIN dwh.dim_machine dm ON s.machine_id = dm.machine_id
    """)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dwh.fact_sensors")
    return cur.fetchone()[0]


def etl_fact_maintenance(cur, conn):
    cur.execute("DELETE FROM dwh.fact_maintenance")
    cur.execute("""
        INSERT INTO dwh.fact_maintenance (
            date_key, machine_key, maint_type_key, operateur_key,
            duree_min, cout, date_debut, date_fin
        )
        SELECT
            EXTRACT(YEAR FROM m.date_debut)::int * 10000 + EXTRACT(MONTH FROM m.date_debut)::int * 100 + EXTRACT(DAY FROM m.date_debut)::int,
            dm.machine_key,
            dmt.maint_type_key,
            dop.operateur_key,
            m.duree, m.cout, m.date_debut, m.date_fin
        FROM maintenance m
        JOIN dwh.dim_machine dm ON m.machine_id = dm.machine_id
        JOIN dwh.dim_maintenance_type dmt ON m.type_maintenance = dmt.type_maintenance
        LEFT JOIN dwh.dim_operateur dop ON m.operateur_id = dop.operateur_id
    """)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM dwh.fact_maintenance")
    return cur.fetchone()[0]


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("=" * 60)
    print("  AMIP ETL - Data Warehouse Population")
    print("=" * 60)

    print("\n[CLEANUP] Truncating facts before dimensions...")
    for tbl in ["fact_sensors", "fact_maintenance", "fact_quality", "fact_execution", "fact_production"]:
        cur.execute(f"DELETE FROM dwh.{tbl}")
    conn.commit()

    print("\n[DIMENSIONS]")
    print(f"  dim_date:           {etl_dim_date(cur, conn)} rows")
    print(f"  dim_machine:        {etl_dim_machine(cur, conn)} rows")
    print(f"  dim_part:           {etl_dim_part(cur, conn)} rows")
    print(f"  dim_material:       {etl_dim_material(cur, conn)} rows")
    print(f"  dim_tool:           {etl_dim_tool(cur, conn)} rows")
    print(f"  dim_sector:         {etl_dim_sector(cur, conn)} rows")
    print(f"  dim_order:          {etl_dim_order(cur, conn)} rows")
    print(f"  dim_operateur:      {etl_dim_operateur(cur, conn)} rows")
    print(f"  dim_maint_type:     {etl_dim_maint_type(cur, conn)} rows")
    print(f"  dim_quality_result: {etl_dim_quality_result(cur, conn)} rows")

    print("\n[FACTS]")
    print(f"  fact_production:    {etl_fact_production(cur, conn)} rows")
    print(f"  fact_execution:     {etl_fact_execution(cur, conn)} rows")
    print(f"  fact_quality:       {etl_fact_quality(cur, conn)} rows")
    print(f"  fact_sensors:       {etl_fact_sensors(cur, conn)} rows")
    print(f"  fact_maintenance:   {etl_fact_maintenance(cur, conn)} rows")

    cur.close()
    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
