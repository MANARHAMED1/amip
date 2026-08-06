-- ============================================================
-- AMIP Data Warehouse - Star Schema
-- ============================================================

DROP SCHEMA IF EXISTS dwh CASCADE;
CREATE SCHEMA dwh;

-- ============================================================
-- DIMENSION TABLES
-- ============================================================

-- dim_date
CREATE TABLE dwh.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    week INTEGER NOT NULL,
    day_of_month INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    year_month VARCHAR(7) NOT NULL
);

COMMENT ON TABLE dwh.dim_date IS 'Dimension temps - calendrier';

-- dim_machine
CREATE TABLE dwh.dim_machine (
    machine_key SERIAL PRIMARY KEY,
    machine_id INTEGER NOT NULL,
    code VARCHAR(20) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    marque VARCHAR(50) NOT NULL,
    modele VARCHAR(50) NOT NULL,
    controller VARCHAR(50),
    axes INTEGER,
    rpm_max INTEGER,
    statut VARCHAR(20) NOT NULL,
    secteur_code VARCHAR(10),
    secteur_nom VARCHAR(100)
);

COMMENT ON TABLE dwh.dim_machine IS 'Dimension machines CNC';

-- dim_part
CREATE TABLE dwh.dim_part (
    part_key SERIAL PRIMARY KEY,
    piece_id INTEGER NOT NULL,
    reference VARCHAR(30) NOT NULL,
    designation VARCHAR(150) NOT NULL,
    famille VARCHAR(50),
    matiere_code VARCHAR(20),
    matiere_designation VARCHAR(100),
    matiere_type VARCHAR(50),
    matiere_nuance VARCHAR(50),
    poids DECIMAL(10,4),
    dimensions VARCHAR(100)
);

COMMENT ON TABLE dwh.dim_part IS 'Dimension pieces finies';

-- dim_material
CREATE TABLE dwh.dim_material (
    material_key SERIAL PRIMARY KEY,
    matiere_id INTEGER NOT NULL,
    code VARCHAR(20) NOT NULL,
    designation VARCHAR(100) NOT NULL,
    type_matiere VARCHAR(50),
    nuance VARCHAR(50),
    densite DECIMAL(6,3),
    prix_kg DECIMAL(10,2)
);

COMMENT ON TABLE dwh.dim_material IS 'Dimension matieres premieres';

-- dim_tool
CREATE TABLE dwh.dim_tool (
    tool_key SERIAL PRIMARY KEY,
    outil_id INTEGER NOT NULL,
    code VARCHAR(20) NOT NULL,
    designation VARCHAR(100) NOT NULL,
    type_outil VARCHAR(50) NOT NULL,
    diametre DECIMAL(8,3),
    matiere_outil VARCHAR(50),
    duree_vie_totale INTEGER NOT NULL,
    cout_achat DECIMAL(10,2),
    cout_remplacement DECIMAL(10,2)
);

COMMENT ON TABLE dwh.dim_tool IS 'Dimension outillage';

-- dim_sector
CREATE TABLE dwh.dim_sector (
    sector_key SERIAL PRIMARY KEY,
    secteur_id INTEGER NOT NULL,
    code VARCHAR(10) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    description TEXT
);

COMMENT ON TABLE dwh.dim_sector IS 'Dimension secteurs';

-- dim_production_order
CREATE TABLE dwh.dim_production_order (
    order_key SERIAL PRIMARY KEY,
    ordre_fabrication_id INTEGER NOT NULL,
    numero_of VARCHAR(20) NOT NULL,
    priorite VARCHAR(20),
    statut VARCHAR(20) NOT NULL,
    date_debut_prevue DATE,
    date_fin_prevue DATE,
    date_debut_reelle DATE,
    date_fin_reelle DATE
);

COMMENT ON TABLE dwh.dim_production_order IS 'Dimension ordres de fabrication';

-- dim_operateur
CREATE TABLE dwh.dim_operateur (
    operateur_key SERIAL PRIMARY KEY,
    operateur_id INTEGER NOT NULL,
    matricule VARCHAR(20) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    poste VARCHAR(50),
    niveau_competence VARCHAR(20)
);

COMMENT ON TABLE dwh.dim_operateur IS 'Dimension operateurs';

-- dim_maintenance_type
CREATE TABLE dwh.dim_maintenance_type (
    maint_type_key SERIAL PRIMARY KEY,
    type_maintenance VARCHAR(30) NOT NULL,
    categorie VARCHAR(30)
);

COMMENT ON TABLE dwh.dim_maintenance_type IS 'Dimension types de maintenance';

-- dim_quality_result
CREATE TABLE dwh.dim_quality_result (
    quality_result_key SERIAL PRIMARY KEY,
    resultat VARCHAR(20) NOT NULL,
    est_conforme BOOLEAN NOT NULL,
    cause_categorie VARCHAR(50),
    cause_description VARCHAR(200)
);

COMMENT ON TABLE dwh.dim_quality_result IS 'Dimension resultats qualite';

-- ============================================================
-- FACT TABLES
-- ============================================================

-- fact_production
CREATE TABLE dwh.fact_production (
    production_key SERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL REFERENCES dwh.dim_date(date_key),
    part_key INTEGER NOT NULL REFERENCES dwh.dim_part(part_key),
    material_key INTEGER NOT NULL REFERENCES dwh.dim_material(material_key),
    order_key INTEGER NOT NULL REFERENCES dwh.dim_production_order(order_key),
    sector_key INTEGER NOT NULL REFERENCES dwh.dim_sector(sector_key),
    quantite_demandee INTEGER NOT NULL,
    quantite_produite INTEGER NOT NULL,
    quantite_rebut INTEGER NOT NULL,
    taux_rebut DECIMAL(5,4),
    taux_rendement DECIMAL(5,4),
    duree_prevue_jours INTEGER,
    duree_reelle_jours INTEGER,
    ecart_duree_jours INTEGER
);

COMMENT ON TABLE dwh.fact_production IS 'Fait production - OF';

-- fact_execution
CREATE TABLE dwh.fact_execution (
    execution_key SERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL REFERENCES dwh.dim_date(date_key),
    machine_key INTEGER NOT NULL REFERENCES dwh.dim_machine(machine_key),
    part_key INTEGER NOT NULL REFERENCES dwh.dim_part(part_key),
    tool_key INTEGER REFERENCES dwh.dim_tool(tool_key),
    operateur_key INTEGER REFERENCES dwh.dim_operateur(operateur_key),
    order_key INTEGER NOT NULL REFERENCES dwh.dim_production_order(order_key),
    temps_usinage_prevu INTEGER,
    temps_reglage_prevu INTEGER,
    temps_usinage_reel INTEGER,
    temps_reglage_reel INTEGER,
    nb_pieces_produites INTEGER,
    nb_pieces_rebut INTEGER,
    vitesse_coupe DECIMAL(10,2),
    avance DECIMAL(10,3),
    profondeur_passe DECIMAL(8,3),
    temps_disponible_min INTEGER,
    temps_operation_min INTEGER,
    nb_cycles INTEGER,
    taux_disponibilite DECIMAL(5,4),
    taux_performance DECIMAL(5,4),
    taux_qualite DECIMAL(5,4),
    oee DECIMAL(5,4)
);

COMMENT ON TABLE dwh.fact_execution IS 'Fait executions - OEE par phase';

-- fact_quality
CREATE TABLE dwh.fact_quality (
    quality_key SERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL REFERENCES dwh.dim_date(date_key),
    part_key INTEGER NOT NULL REFERENCES dwh.dim_part(part_key),
    quality_result_key INTEGER NOT NULL REFERENCES dwh.dim_quality_result(quality_result_key),
    machine_key INTEGER NOT NULL REFERENCES dwh.dim_machine(machine_key),
    nb_controles INTEGER NOT NULL,
    nb_conformes INTEGER NOT NULL,
    nb_non_conformes INTEGER NOT NULL,
    taux_conformite DECIMAL(5,4),
    dimension_mesuree DECIMAL(10,3),
    dimension_cible DECIMAL(10,3),
    ecart_dimension DECIMAL(10,3),
    rugosite_mesuree DECIMAL(6,3)
);

COMMENT ON TABLE dwh.fact_quality IS 'Fait qualite - inspections';

-- fact_sensors
CREATE TABLE dwh.fact_sensors (
    sensor_key SERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL REFERENCES dwh.dim_date(date_key),
    machine_key INTEGER NOT NULL REFERENCES dwh.dim_machine(machine_key),
    timestamp TIMESTAMP NOT NULL,
    temperature DECIMAL(6,2),
    vibration DECIMAL(6,3),
    rpm INTEGER,
    charge_frappe DECIMAL(6,2),
    puissance DECIMAL(8,2),
    vitesse_avance DECIMAL(8,2),
    statut_machine VARCHAR(20),
    temps_cycle DECIMAL(8,2)
);

COMMENT ON TABLE dwh.fact_sensors IS 'Fait capteurs IoT - time-series';

-- fact_maintenance
CREATE TABLE dwh.fact_maintenance (
    maintenance_key SERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL REFERENCES dwh.dim_date(date_key),
    machine_key INTEGER NOT NULL REFERENCES dwh.dim_machine(machine_key),
    maint_type_key INTEGER NOT NULL REFERENCES dwh.dim_maintenance_type(maint_type_key),
    operateur_key INTEGER REFERENCES dwh.dim_operateur(operateur_key),
    duree_min INTEGER,
    cout DECIMAL(10,2),
    date_debut TIMESTAMP,
    date_fin TIMESTAMP
);

COMMENT ON TABLE dwh.fact_maintenance IS 'Fait maintenance - interventions';

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_fact_prod_date ON dwh.fact_production(date_key);
CREATE INDEX idx_fact_prod_part ON dwh.fact_production(part_key);
CREATE INDEX idx_fact_prod_order ON dwh.fact_production(order_key);

CREATE INDEX idx_fact_exec_date ON dwh.fact_execution(date_key);
CREATE INDEX idx_fact_exec_machine ON dwh.fact_execution(machine_key);
CREATE INDEX idx_fact_exec_part ON dwh.fact_execution(part_key);
CREATE INDEX idx_fact_exec_order ON dwh.fact_execution(order_key);

CREATE INDEX idx_fact_quality_date ON dwh.fact_quality(date_key);
CREATE INDEX idx_fact_quality_part ON dwh.fact_quality(part_key);

CREATE INDEX idx_fact_sensors_date ON dwh.fact_sensors(date_key);
CREATE INDEX idx_fact_sensors_machine ON dwh.fact_sensors(machine_key);
CREATE INDEX idx_fact_sensors_ts ON dwh.fact_sensors(timestamp);

CREATE INDEX idx_fact_maint_date ON dwh.fact_maintenance(date_key);
CREATE INDEX idx_fact_maint_machine ON dwh.fact_maintenance(machine_key);
