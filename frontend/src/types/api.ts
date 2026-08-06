// ── Auth ──

export interface LoginRequest {
  username: string;
  password: string;
}

export interface AuthUser {
  user_id: number;
  username: string;
  full_name: string;
  role: string;
}

export interface LoginResponse {
  token: string;
  user: AuthUser;
}

// ── Executive / Overview ──

export interface ExecutiveKPI {
  oee: {
    oee_global: number;
    taux_rebut: number;
    qualite: number;
  };
  machines: {
    running: number;
    stopped: number;
    maintenance: number;
  };
  ordres_fabrication: {
    en_cours: number;
    en_attente: number;
    termine: number;
  };
  retards: number;
}

export interface MachineStatus {
  code: string;
  nom: string;
  type: string;
  marque: string;
  modele: string;
  statut: string;
  secteur: string;
}

export interface AlertItem {
  type: "CRITICAL" | "WARNING";
  message: string;
  detail?: string;
}

export interface ProductionTrend {
  date: string;
  produites: number;
  rebuts: number;
}

export interface OEEByMachine {
  code: string;
  nom: string;
  disponibilite: number;
  performance: number;
  qualite: number;
  oee: number;
  production: number;
}

export interface ProductionVsPlan {
  date: string;
  planifie: number;
  reel: number;
}

export interface ScrapByFamily {
  famille: string;
  nb_rebut: number;
  nb_produites: number;
  taux_rebut: number;
}

export interface ActiveOrder {
  numero_of: string;
  piece_ref: string;
  piece_nom: string;
  quantite_demandee: number;
  quantite_produite: number;
  quantite_rebut: number;
  statut: string;
  priorite: string;
  avancement_pct: number;
  retard_jours: number | null;
}

// ── Machine ──

export interface Machine {
  machine_id: number;
  code: string;
  nom: string;
  type: string;
  marque: string;
  modele: string;
  controller: string;
  axes: number;
  rpm_max: number;
  tool_capacity: number;
  statut: string;
  date_installation: string;
  secteur: string;
}

export interface MachineDetail {
  machine: Machine;
  of_actuel: Record<string, unknown> | null;
  operateur: Record<string, unknown> | null;
  outil_actuel: Record<string, unknown> | null;
}

export interface MachinePerformance {
  disponibilite: number;
  performance: number;
  qualite: number;
  oee: number;
  total_produites: number;
  total_rebut: number;
  temps_usinage_total: number;
  temps_reglage_total: number;
}

export interface OEEHistory {
  date: string;
  oee: number;
  disponibilite: number;
  performance: number;
  qualite: number;
}

export interface MachineMaintenance {
  type_maintenance: string;
  description: string;
  date_debut: string;
  date_fin: string;
  duree: number;
  cout: number;
  statut: string;
}

export interface MachineMaintenanceKPI {
  stats: {
    nb_interventions: number;
    cout_total: number;
    cout_moyen: number;
    duree_totale_min: number;
    duree_moyenne_min: number;
    nb_preventive: number;
    nb_corrective: number;
  };
  mtbf_mttr: {
    mtbf_heures: number;
    mttr_heures: number;
  };
}

export interface MachineSensors {
  current: {
    temperature: number;
    vibration: number;
    rpm: number;
    charge_frappe: number;
    puissance: number;
    vitesse_avance: number;
    temps_cycle: number;
    statut_machine: string;
    timestamp: string;
  } | null;
  stats: {
    temp_moy: number;
    temp_max: number;
    temp_min: number;
    vib_moy: number;
    vib_max: number;
    vib_min: number;
    rpm_moy: number;
    rpm_max: number;
    charge_moy: number;
    charge_max: number;
    puissance_moy: number;
    puissance_max: number;
    nb_readings: number;
    alertes_temp: number;
    alertes_vibration: number;
  } | null;
}

export interface PhaseTimeline {
  numero_phase: string;
  phase_name: string;
  machine_code: string;
  outil_code: string;
  temps_usinage_prevu: number;
  temps_usinage_reel: number;
  date_debut: string;
  date_fin: string;
  statut: string;
  duree: number;
}

// ── Production ──

export interface ProductionKPI {
  total: number;
  en_cours: number;
  termine: number;
  en_attente: number;
  annule: number;
  en_retard: number;
}

export interface ProductionOrder {
  numero_of: string;
  statut: string;
  priorite: string;
  piece_ref: string;
  piece_nom: string;
  quantite_demandee: number;
  quantite_produite: number;
  quantite_rebut: number;
  date_debut_prevue: string;
  date_fin_prevue: string;
  date_debut_reelle: string | null;
  date_fin_reelle: string | null;
  taux_rendement: number;
}

export interface ProductionOrderDetail {
  of: ProductionOrder;
  retard_jours: number | null;
  phases: ProductionPhase[];
}

export interface ProductionPhase {
  numero_phase: string;
  designation: string;
  machine_code: string;
  outil_code: string;
  temps_usinage_prevu: number;
  temps_reglage_prevu: number;
  temps_usinage_reel: number;
  temps_reglage_reel: number;
  nb_pieces_produites: number;
  nb_pieces_rebut: number;
  vitesse_coupe: number;
  avance: number;
  profondeur_passe: number;
  statut: string;
  date_debut: string;
  date_fin: string;
  operateur_nom: string;
  operateur_prenom: string;
}

// ── Quality ──

export interface QualityKPI {
  nb_inspections: number;
  total_controles: number;
  total_conformes: number;
  total_non_conformes: number;
  taux_conformite: number;
  ecart_dimension_moyen: number;
  rugosite_moyenne: number;
}

export interface QualityCause {
  categorie: string;
  description: string;
  nb: number;
  total_rebut: number;
}

export interface QualityByMachine {
  code: string;
  nom: string;
  total_controles: number;
  total_non_conformes: number;
  taux_rebut: number;
}

// ── Inventory ──

export interface InventoryOverview {
  matieres: { total: number; critiques: number; valeur_totale: number };
  outils: { total: number; critiques: number };
  pieces: { total: number; stock_total: number };
}

export interface InventoryAlert {
  type: string;
  code: string;
  designation: string;
  quantite_stock: number;
  seuil_alerte: number;
  statut: "CRITIQUE" | "BAS" | "NORMAL" | "SURSTOCK";
}

// ── Tool ──

export interface Tool {
  outil_id: number;
  code: string;
  designation: string;
  type_outil: string;
  diametre: number;
  matiere_outil: string;
  duree_vie_totale: number;
  usure_actuelle: number;
  duree_vie_restante: number;
  cout_achat: number;
  cout_remplacement: number;
  disponible: boolean;
  pct_usure: number;
  indicateur_remplacement: string;
  stock: number;
}

// ── Maintenance ──

export interface MaintenanceRecord {
  maintenance_id: number;
  machine_code: string;
  machine_nom: string;
  type_maintenance: string;
  description: string;
  date_debut: string;
  date_fin: string;
  duree: number;
  cout: number;
  statut: string;
  operateur_nom: string;
  operateur_prenom: string;
}

export interface MaintenanceKPI {
  stats: {
    nb_interventions: number;
    cout_total: number;
    cout_moyen: number;
    duree_totale_min: number;
    duree_moyenne_min: number;
    nb_preventive: number;
    nb_corrective: number;
  };
  by_type: Array<Record<string, unknown>>;
}

// ── Sensors ──

export interface SensorCurrent {
  temperature: number;
  vibration: number;
  rpm: number;
  charge_frappe: number;
  puissance: number;
  vitesse_avance: number;
  temps_cycle: number;
  statut_machine: string;
  timestamp: string;
}

export interface SensorStats {
  temp_moy: number;
  temp_max: number;
  temp_min: number;
  vib_moy: number;
  vib_max: number;
  vib_min: number;
  rpm_moy: number;
  rpm_max: number;
  charge_moy: number;
  charge_max: number;
  puissance_moy: number;
  puissance_max: number;
  nb_readings: number;
  alertes_temp: number;
  alertes_vibration: number;
}

export interface SensorHistory {
  timestamp: string;
  temperature: number;
  vibration: number;
  rpm: number;
  charge_frappe: number;
  puissance: number;
  temps_cycle: number;
  statut_machine: string;
}

export interface AllMachinesSensor {
  code: string;
  nom: string;
  temperature: number;
  vibration: number;
  rpm: number;
  charge_frappe: number;
  puissance: number;
  statut_machine: string;
  timestamp: string;
}
