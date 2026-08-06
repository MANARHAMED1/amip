-- ============================================================
-- AMIP - AMM Manufacturing Intelligence Platform
-- PostgreSQL Database Schema
-- Version: 1.0
-- Date: 2026-07-12
-- ============================================================

-- Drop existing tables (in reverse dependency order)
DROP TABLE IF EXISTS sensor_data CASCADE;
DROP TABLE IF EXISTS mouvement_stock CASCADE;
DROP TABLE IF EXISTS stock_matiere CASCADE;
DROP TABLE IF EXISTS stock_piece CASCADE;
DROP TABLE IF EXISTS stock_outil CASCADE;
DROP TABLE IF EXISTS controle_qualite CASCADE;
DROP TABLE IF EXISTS cause_rebut CASCADE;
DROP TABLE IF EXISTS execution_outil CASCADE;
DROP TABLE IF EXISTS execution_phase CASCADE;
DROP TABLE IF EXISTS maintenance CASCADE;
DROP TABLE IF EXISTS phase_gamme CASCADE;
DROP TABLE IF EXISTS programme_usinage CASCADE;
DROP TABLE IF EXISTS gamme_usinage CASCADE;
DROP TABLE IF EXISTS ordre_fabrication CASCADE;
DROP TABLE IF EXISTS piece CASCADE;
DROP TABLE IF EXISTS outil CASCADE;
DROP TABLE IF EXISTS matiere CASCADE;
DROP TABLE IF EXISTS operateur CASCADE;
DROP TABLE IF EXISTS machine CASCADE;
DROP TABLE IF EXISTS secteur CASCADE;

-- ============================================================
-- 1. SECTEUR (Workshop Sectors)
-- ============================================================
CREATE TABLE secteur (
    secteur_id SERIAL PRIMARY KEY,
    code VARCHAR(10) NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE secteur IS 'Secteurs de l''atelier AMM';
COMMENT ON COLUMN secteur.code IS 'Code court du secteur';
COMMENT ON COLUMN secteur.nom IS 'Nom du secteur';

-- ============================================================
-- 2. MACHINE (CNC Machines)
-- ============================================================
CREATE TABLE machine (
    machine_id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    marque VARCHAR(50) NOT NULL,
    modele VARCHAR(50) NOT NULL,
    controller VARCHAR(50),
    axes INTEGER,
    rpm_max INTEGER,
    tool_capacity INTEGER DEFAULT 0,
    statut VARCHAR(20) NOT NULL DEFAULT 'RUNNING',
    secteur_id INTEGER NOT NULL REFERENCES secteur(secteur_id),
    date_installation DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_machine_statut CHECK (statut IN ('RUNNING', 'STOPPED', 'MAINTENANCE', 'BROKEN')),
    CONSTRAINT chk_machine_axes CHECK (axes > 0 AND axes <= 6),
    CONSTRAINT chk_machine_rpm CHECK (rpm_max > 0)
);

COMMENT ON TABLE machine IS 'Machines CNC de l''atelier AMM';
COMMENT ON COLUMN machine.statut IS 'Etat: RUNNING, STOPPED, MAINTENANCE, BROKEN';

-- ============================================================
-- 3. OPERATEUR (Operators/Workers)
-- ============================================================
CREATE TABLE operateur (
    operateur_id SERIAL PRIMARY KEY,
    matricule VARCHAR(20) NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    poste VARCHAR(50),
    niveau_competence VARCHAR(20),
    date_embauche DATE,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_competence CHECK (niveau_competence IN ('Junior', 'Confirme', 'Senior') OR niveau_competence IS NULL)
);

COMMENT ON TABLE operateur IS 'Operateurs et personnel technique';

-- ============================================================
-- 4. MATIERE (Raw Materials)
-- ============================================================
CREATE TABLE matiere (
    matiere_id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    designation VARCHAR(100) NOT NULL,
    type_matiere VARCHAR(50),
    nuance VARCHAR(50),
    densite DECIMAL(6,3),
    prix_kg DECIMAL(10,2),
    unite VARCHAR(10) DEFAULT 'kg',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE matiere IS 'Matieres premieres pour usinage';

-- ============================================================
-- 5. OUTIL (Tools)
-- ============================================================
CREATE TABLE outil (
    outil_id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    designation VARCHAR(100) NOT NULL,
    type_outil VARCHAR(50) NOT NULL,
    diametre DECIMAL(8,3),
    matiere_outil VARCHAR(50),
    duree_vie_totale INTEGER NOT NULL,
    usure_actuelle INTEGER DEFAULT 0,
    duree_vie_restante INTEGER NOT NULL,
    cout_achat DECIMAL(10,2),
    cout_remplacement DECIMAL(10,2),
    disponible BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_outil_usure CHECK (usure_actuelle >= 0),
    CONSTRAINT chk_outil_vie CHECK (duree_vie_restante >= 0),
    CONSTRAINT chk_outil_vie_totale CHECK (duree_vie_totale > 0)
);

COMMENT ON TABLE outil IS 'Outillage de usinage (forets, fraises, etc.)';
COMMENT ON COLUMN outil.duree_vie_totale IS 'Duree de vie totale en minutes';
COMMENT ON COLUMN outil.usure_actuelle IS 'Usure actuelle en minutes';
COMMENT ON COLUMN outil.duree_vie_restante IS 'Duree de vie restante en minutes';

-- ============================================================
-- 6. STOCK_OUTIL (Tool Inventory)
-- ============================================================
CREATE TABLE stock_outil (
    stock_outil_id SERIAL PRIMARY KEY,
    outil_id INTEGER NOT NULL UNIQUE REFERENCES outil(outil_id),
    quantite_stock INTEGER NOT NULL DEFAULT 0,
    emplacement VARCHAR(50),
    seuil_alerte INTEGER DEFAULT 5,
    date_derniere_maj TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_stock_outil_qte CHECK (quantite_stock >= 0)
);

COMMENT ON TABLE stock_outil IS 'Stock d''outillage';

-- ============================================================
-- 7. PIECE (Finished Parts)
-- ============================================================
CREATE TABLE piece (
    piece_id SERIAL PRIMARY KEY,
    reference VARCHAR(30) NOT NULL UNIQUE,
    designation VARCHAR(150) NOT NULL,
    famille VARCHAR(50),
    matiere_id INTEGER REFERENCES matiere(matiere_id),
    poids DECIMAL(10,4),
    dimensions VARCHAR(100),
    tolerances VARCHAR(100),
    prix_revient DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE piece IS 'Pieces finies usinees';

-- ============================================================
-- 8. PROGRAMME_USINAGE (CNC Programs)
-- ============================================================
CREATE TABLE programme_usinage (
    programme_id SERIAL PRIMARY KEY,
    code_programme VARCHAR(30) NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL,
    version VARCHAR(10),
    description TEXT,
    duree_estimee INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE programme_usinage IS 'Programmes CNC de usinage';

-- ============================================================
-- 9. GAMME_USINAGE (Machining Routings)
-- ============================================================
CREATE TABLE gamme_usinage (
    gamme_id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    designation VARCHAR(100) NOT NULL,
    piece_id INTEGER NOT NULL REFERENCES piece(piece_id),
    nb_phases INTEGER,
    duree_totale_estimee INTEGER,
    version VARCHAR(10) DEFAULT '1.0',
    statut VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_gamme_statut CHECK (statut IN ('ACTIVE', 'OBSOLETE')),
    CONSTRAINT chk_gamme_phases CHECK (nb_phases > 0 OR nb_phases IS NULL)
);

COMMENT ON TABLE gamme_usinage IS 'Gammes d''usinage (routings)';

-- ============================================================
-- 10. PHASE_GAMME (Routing Phases)
-- ============================================================
CREATE TABLE phase_gamme (
    phase_gamme_id SERIAL PRIMARY KEY,
    gamme_id INTEGER NOT NULL REFERENCES gamme_usinage(gamme_id),
    numero_phase INTEGER NOT NULL,
    designation VARCHAR(100),
    machine_id INTEGER NOT NULL REFERENCES machine(machine_id),
    outil_id INTEGER NOT NULL REFERENCES outil(outil_id),
    programme_id INTEGER REFERENCES programme_usinage(programme_id),
    temps_usinage_prevu INTEGER NOT NULL,
    temps_reglage_prevu INTEGER NOT NULL,
    exigence_technique TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_phase_numero CHECK (numero_phase > 0),
    CONSTRAINT chk_phase_temps_usinage CHECK (temps_usinage_prevu >= 0),
    CONSTRAINT chk_phase_temps_reglage CHECK (temps_reglage_prevu >= 0),
    CONSTRAINT uq_phase_gamme UNIQUE (gamme_id, numero_phase)
);

COMMENT ON TABLE phase_gamme IS 'Phases d''une gamme d''usinage';
COMMENT ON COLUMN phase_gamme.temps_usinage_prevu IS 'Temps d''usinage prevu en minutes';
COMMENT ON COLUMN phase_gamme.temps_reglage_prevu IS 'Temps de reglage prevu en minutes';

-- ============================================================
-- 11. ORDRE_FABRICATION (Production Orders)
-- ============================================================
CREATE TABLE ordre_fabrication (
    ordre_fabrication_id SERIAL PRIMARY KEY,
    numero_of VARCHAR(20) NOT NULL UNIQUE,
    piece_id INTEGER NOT NULL REFERENCES piece(piece_id),
    gamme_id INTEGER NOT NULL REFERENCES gamme_usinage(gamme_id),
    quantite_demandee INTEGER NOT NULL,
    quantite_produite INTEGER DEFAULT 0,
    quantite_rebut INTEGER DEFAULT 0,
    date_debut_prevue DATE NOT NULL,
    date_fin_prevue DATE,
    date_debut_reelle DATE,
    date_fin_reelle DATE,
    priorite VARCHAR(20) DEFAULT 'NORMALE',
    statut VARCHAR(20) NOT NULL DEFAULT 'EN_ATTENTE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_of_quantite CHECK (quantite_demandee > 0),
    CONSTRAINT chk_of_priorite CHECK (priorite IN ('HAUTE', 'NORMALE', 'BASSE')),
    CONSTRAINT chk_of_statut CHECK (statut IN ('EN_ATTENTE', 'EN_COURS', 'TERMINE', 'ANNULE'))
);

COMMENT ON TABLE ordre_fabrication IS 'Ordres de fabrication (OF)';

-- ============================================================
-- 12. EXECUTION_PHASE (Phase Execution Records)
-- ============================================================
CREATE TABLE execution_phase (
    execution_id SERIAL PRIMARY KEY,
    ordre_fabrication_id INTEGER NOT NULL REFERENCES ordre_fabrication(ordre_fabrication_id),
    phase_gamme_id INTEGER NOT NULL REFERENCES phase_gamme(phase_gamme_id),
    machine_id INTEGER NOT NULL REFERENCES machine(machine_id),
    outil_id INTEGER REFERENCES outil(outil_id),
    operateur_id INTEGER REFERENCES operateur(operateur_id),
    programme_id INTEGER REFERENCES programme_usinage(programme_id),
    date_debut TIMESTAMP NOT NULL,
    date_fin TIMESTAMP,
    temps_usinage_reel INTEGER,
    temps_reglage_reel INTEGER,
    nb_pieces_produites INTEGER DEFAULT 0,
    nb_pieces_rebut INTEGER DEFAULT 0,
    vitesse_coupe DECIMAL(10,2),
    avance DECIMAL(10,3),
    profondeur_passe DECIMAL(8,3),
    statut VARCHAR(20) DEFAULT 'EN_COURS',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_exec_temps_usinage CHECK (temps_usinage_reel >= 0 OR temps_usinage_reel IS NULL),
    CONSTRAINT chk_exec_statut CHECK (statut IN ('EN_COURS', 'TERMINE', 'ARRET'))
);

COMMENT ON TABLE execution_phase IS 'Executions reelles des phases d''usinage';
COMMENT ON COLUMN execution_phase.vitesse_coupe IS 'Vitesse de coupe en m/min';
COMMENT ON COLUMN execution_phase.avance IS 'Avance en mm/tr';
COMMENT ON COLUMN execution_phase.profondeur_passe IS 'Profondeur de passe en mm';

-- ============================================================
-- 13. EXECUTION_OUTIL (Tool Usage per Execution)
-- ============================================================
CREATE TABLE execution_outil (
    execution_outil_id SERIAL PRIMARY KEY,
    execution_id INTEGER NOT NULL REFERENCES execution_phase(execution_id),
    outil_id INTEGER NOT NULL REFERENCES outil(outil_id),
    usure_debut INTEGER,
    usure_fin INTEGER,
    duree_utilisation INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_exec_outil_usure CHECK (usure_debut >= 0 OR usure_debut IS NULL),
    CONSTRAINT chk_exec_outil_duree CHECK (duree_utilisation >= 0 OR duree_utilisation IS NULL)
);

COMMENT ON TABLE execution_outil IS 'Consommation d''outils par execution';

-- ============================================================
-- 14. CAUSE_REBUT (Scrap Causes)
-- ============================================================
CREATE TABLE cause_rebut (
    cause_rebut_id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    categorie VARCHAR(50) NOT NULL,
    description VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_cause_categorie CHECK (categorie IN ('Materiel', 'Outil', 'Machine', 'Programmation', 'Operateur', 'Autre'))
);

COMMENT ON TABLE cause_rebut IS 'Causes de rebut (defauts)';

-- ============================================================
-- 15. CONTROLE_QUALITE (Quality Inspections)
-- ============================================================
CREATE TABLE controle_qualite (
    controle_id SERIAL PRIMARY KEY,
    execution_id INTEGER NOT NULL REFERENCES execution_phase(execution_id),
    piece_id INTEGER NOT NULL REFERENCES piece(piece_id),
    cause_rebut_id INTEGER REFERENCES cause_rebut(cause_rebut_id),
    date_controle TIMESTAMP NOT NULL,
    resultat VARCHAR(20) NOT NULL,
    nb_controles INTEGER DEFAULT 0,
    nb_conformes INTEGER DEFAULT 0,
    nb_non_conformes INTEGER DEFAULT 0,
    dimension_mesuree DECIMAL(10,3),
    dimension_cible DECIMAL(10,3),
    tolerance_plus DECIMAL(10,3),
    tolerance_moins DECIMAL(10,3),
    rugosite_mesuree DECIMAL(6,3),
    commentaire TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_qte_resultat CHECK (resultat IN ('CONFORME', 'NON_CONFORME', 'EN_ATTENTE')),
    CONSTRAINT chk_qte_controles CHECK (nb_controles >= 0),
    CONSTRAINT chk_qte_conformes CHECK (nb_conformes >= 0),
    CONSTRAINT chk_qte_non_conformes CHECK (nb_non_conformes >= 0)
);

COMMENT ON TABLE controle_qualite IS 'Controles qualite des pieces';

-- ============================================================
-- 16. MAINTENANCE
-- ============================================================
CREATE TABLE maintenance (
    maintenance_id SERIAL PRIMARY KEY,
    machine_id INTEGER NOT NULL REFERENCES machine(machine_id),
    type_maintenance VARCHAR(30) NOT NULL,
    description TEXT NOT NULL,
    date_debut TIMESTAMP NOT NULL,
    date_fin TIMESTAMP,
    duree INTEGER,
    cout DECIMAL(10,2),
    operateur_id INTEGER REFERENCES operateur(operateur_id),
    statut VARCHAR(20) DEFAULT 'PLANIFIEE',
    cree_par VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_maint_type CHECK (type_maintenance IN (
        'Preventive', 'Corrective', 'Changement huile',
        'Nettoyage', 'Inspection', 'Remplacement roulement',
        'Changement liquide', 'Alignement machine'
    )),
    CONSTRAINT chk_maint_statut CHECK (statut IN ('PLANIFIEE', 'EN_COURS', 'TERMINEE')),
    CONSTRAINT chk_maint_duree CHECK (duree >= 0 OR duree IS NULL),
    CONSTRAINT chk_maint_cout CHECK (cout >= 0 OR cout IS NULL)
);

COMMENT ON TABLE maintenance IS 'Interventions de maintenance';

-- ============================================================
-- 17. SENSOR_DATA (IoT Sensor Readings)
-- ============================================================
CREATE TABLE sensor_data (
    sensor_id BIGSERIAL PRIMARY KEY,
    machine_id INTEGER NOT NULL REFERENCES machine(machine_id),
    timestamp TIMESTAMP NOT NULL,
    temperature DECIMAL(6,2),
    vibration DECIMAL(6,3),
    rpm INTEGER,
    charge_frappe DECIMAL(6,2),
    puissance DECIMAL(8,2),
    vitesse_avance DECIMAL(8,2),
    statut_machine VARCHAR(20),
    temps_cycle DECIMAL(8,2),
    CONSTRAINT chk_sensor_statut CHECK (statut_machine IN ('RUNNING', 'STOPPED', 'MAINTENANCE', 'BROKEN') OR statut_machine IS NULL),
    CONSTRAINT chk_sensor_rpm CHECK (rpm >= 0 OR rpm IS NULL),
    CONSTRAINT chk_sensor_temp CHECK (temperature >= -20 AND temperature <= 200)
);

COMMENT ON TABLE sensor_data IS 'Donnees capteurs IoT des machines (time-series)';
COMMENT ON COLUMN sensor_data.temperature IS 'Temperature broche en C';
COMMENT ON COLUMN sensor_data.vibration IS 'Vibration en mm/s';
COMMENT ON COLUMN sensor_data.charge_frappe IS 'Charge broche en %';
COMMENT ON COLUMN sensor_data.puissance IS 'Consommation electrique en kW';

-- ============================================================
-- 18. STOCK_PIECE (Finished Parts Inventory)
-- ============================================================
CREATE TABLE stock_piece (
    stock_piece_id SERIAL PRIMARY KEY,
    piece_id INTEGER NOT NULL UNIQUE REFERENCES piece(piece_id),
    quantite_stock INTEGER NOT NULL DEFAULT 0,
    emplacement VARCHAR(50),
    date_derniere_maj TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_stock_piece_qte CHECK (quantite_stock >= 0)
);

COMMENT ON TABLE stock_piece IS 'Stock de pieces finies';

-- ============================================================
-- 19. STOCK_MATIERE (Raw Material Inventory)
-- ============================================================
CREATE TABLE stock_matiere (
    stock_matiere_id SERIAL PRIMARY KEY,
    matiere_id INTEGER NOT NULL UNIQUE REFERENCES matiere(matiere_id),
    quantite_stock DECIMAL(12,3) NOT NULL DEFAULT 0,
    emplacement VARCHAR(50),
    seuil_alerte DECIMAL(12,3),
    date_derniere_maj TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_stock_matiere_qte CHECK (quantite_stock >= 0)
);

COMMENT ON TABLE stock_matiere IS 'Stock de matieres premieres';

-- ============================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================

-- Machine
CREATE INDEX idx_machine_secteur ON machine(secteur_id);
CREATE INDEX idx_machine_statut ON machine(statut);
CREATE INDEX idx_machine_code ON machine(code);

-- Phase Gamme
CREATE INDEX idx_phase_gamme_gamme ON phase_gamme(gamme_id);
CREATE INDEX idx_phase_gamme_machine ON phase_gamme(machine_id);
CREATE INDEX idx_phase_gamme_outil ON phase_gamme(outil_id);

-- Ordre Fabrication
CREATE INDEX idx_of_piece ON ordre_fabrication(piece_id);
CREATE INDEX idx_of_gamme ON ordre_fabrication(gamme_id);
CREATE INDEX idx_of_statut ON ordre_fabrication(statut);
CREATE INDEX idx_of_date_debut ON ordre_fabrication(date_debut_prevue);
CREATE INDEX idx_of_numero ON ordre_fabrication(numero_of);

-- Execution Phase
CREATE INDEX idx_exec_of ON execution_phase(ordre_fabrication_id);
CREATE INDEX idx_exec_phase_gamme ON execution_phase(phase_gamme_id);
CREATE INDEX idx_exec_machine ON execution_phase(machine_id);
CREATE INDEX idx_exec_outil ON execution_phase(outil_id);
CREATE INDEX idx_exec_operateur ON execution_phase(operateur_id);
CREATE INDEX idx_exec_date_debut ON execution_phase(date_debut);
CREATE INDEX idx_exec_statut ON execution_phase(statut);

-- Execution Outil
CREATE INDEX idx_exec_outil_exec ON execution_outil(execution_id);
CREATE INDEX idx_exec_outil_outil ON execution_outil(outil_id);

-- Controle Qualite
CREATE INDEX idx_cq_execution ON controle_qualite(execution_id);
CREATE INDEX idx_cq_piece ON controle_qualite(piece_id);
CREATE INDEX idx_cq_cause ON controle_qualite(cause_rebut_id);
CREATE INDEX idx_cq_resultat ON controle_qualite(resultat);
CREATE INDEX idx_cq_date ON controle_qualite(date_controle);

-- Maintenance
CREATE INDEX idx_maint_machine ON maintenance(machine_id);
CREATE INDEX idx_maint_operateur ON maintenance(operateur_id);
CREATE INDEX idx_maint_type ON maintenance(type_maintenance);
CREATE INDEX idx_maint_date ON maintenance(date_debut);
CREATE INDEX idx_maint_statut ON maintenance(statut);

-- Sensor Data (critical for time-series)
CREATE INDEX idx_sensor_machine_time ON sensor_data(machine_id, timestamp);
CREATE INDEX idx_sensor_timestamp ON sensor_data(timestamp);
CREATE INDEX idx_sensor_statut ON sensor_data(statut_machine);

-- Stock
CREATE INDEX idx_stock_outil_outil ON stock_outil(outil_id);
CREATE INDEX idx_stock_piece_piece ON stock_piece(piece_id);
CREATE INDEX idx_stock_matiere_matiere ON stock_matiere(matiere_id);

-- Piece
CREATE INDEX idx_piece_matiere ON piece(matiere_id);
CREATE INDEX idx_piece_reference ON piece(reference);
CREATE INDEX idx_piece_famille ON piece(famille);

-- Gamme
CREATE INDEX idx_gamme_piece ON gamme_usinage(piece_id);

-- Operateur
CREATE INDEX idx_operateur_matricule ON operateur(matricule);
CREATE INDEX idx_operateur_actif ON operateur(actif);

-- Outil
CREATE INDEX idx_outil_type ON outil(type_outil);
CREATE INDEX idx_outil_disponible ON outil(disponible);
