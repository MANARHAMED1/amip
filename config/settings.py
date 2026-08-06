import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
GENERATED_DATA_DIR = BASE_DIR / "generated_data"
DATABASE_DIR = BASE_DIR / "database"
DOCS_DIR = BASE_DIR / "docs"

GENERATED_DATA_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42

TARGET_ROWS = {
    "secteur": 6,
    "machine": 12,
    "operateur": 50,
    "matiere": 40,
    "outil": 150,
    "stock_outil": 150,
    "piece": 300,
    "programme_usinage": 400,
    "gamme_usinage": 500,
    "phase_gamme": 2500,
    "ordre_fabrication": 5000,
    "execution_phase": 25000,
    "execution_outil": 25000,
    "cause_rebut": 12,
    "controle_qualite": 25000,
    "maintenance": 3000,
    "sensor_data": 1000000,
    "stock_piece": 300,
    "stock_matiere": 40,
}

MACHINE_DATA = [
    {
        "code": "M001", "nom": "Tour CNC Precision 1", "type": "Tour CNC",
        "marque": "HANQI-CNC", "modele": "CNC-1660",
        "controller": "FANUC Series 0i-TF", "axes": 2, "rpm_max": 4500,
        "tool_capacity": 0, "statut": "RUNNING", "secteur_nom": "Tournage",
    },
    {
        "code": "M002", "nom": "Tour CNC Precision 2", "type": "Tour CNC",
        "marque": "HANQI-CNC", "modele": "CNE-20",
        "controller": "FANUC Series 0i-TF", "axes": 2, "rpm_max": 6000,
        "tool_capacity": 0, "statut": "RUNNING", "secteur_nom": "Tournage",
    },
    {
        "code": "M003", "nom": "Centre usinage CN3", "type": "Centre usinage CNC",
        "marque": "Hartford", "modele": "SMC-5",
        "controller": "HARTROL-FANUC AI100", "axes": 3, "rpm_max": 8000,
        "tool_capacity": 20, "statut": "RUNNING", "secteur_nom": "Usinage CNC",
    },
    {
        "code": "M004", "nom": "Centre usinage CN4", "type": "Centre usinage CNC",
        "marque": "Hartford", "modele": "SMC-5",
        "controller": "HARTROL-FANUC AI100", "axes": 3, "rpm_max": 8000,
        "tool_capacity": 20, "statut": "RUNNING", "secteur_nom": "Usinage CNC",
    },
    {
        "code": "M005", "nom": "Tour CNC Precision 3", "type": "Tour CNC",
        "marque": "HANQI-CNC", "modele": "CNC-1660",
        "controller": "FANUC Series 0i-TF", "axes": 2, "rpm_max": 4500,
        "tool_capacity": 0, "statut": "RUNNING", "secteur_nom": "Tournage",
    },
    {
        "code": "M006", "nom": "Fraiseuse CNC 1", "type": "Fraiseuse CNC",
        "marque": "Hartford", "modele": "SMC-5",
        "controller": "HARTROL-FANUC AI100", "axes": 3, "rpm_max": 8000,
        "tool_capacity": 24, "statut": "RUNNING", "secteur_nom": "Fraisage",
    },
    {
        "code": "M007", "nom": "Tour CNC Precision 4", "type": "Tour CNC",
        "marque": "HANQI-CNC", "modele": "CNE-20",
        "controller": "FANUC Series 0i-TF", "axes": 2, "rpm_max": 6000,
        "tool_capacity": 0, "statut": "STOPPED", "secteur_nom": "Tournage",
    },
    {
        "code": "M008", "nom": "Centre usinage CN8", "type": "Centre usinage CNC",
        "marque": "Hartford", "modele": "SMC-5",
        "controller": "HARTROL-FANUC AI100", "axes": 3, "rpm_max": 8000,
        "tool_capacity": 20, "statut": "STOPPED", "secteur_nom": "Usinage CNC",
    },
    {
        "code": "M009", "nom": "Fraiseuse CNC 2", "type": "Fraiseuse CNC",
        "marque": "Hartford", "modele": "SMC-5",
        "controller": "HARTROL-FANUC AI100", "axes": 3, "rpm_max": 8000,
        "tool_capacity": 24, "statut": "STOPPED", "secteur_nom": "Fraisage",
    },
    {
        "code": "M010", "nom": "Tour CNC Precision 5", "type": "Tour CNC",
        "marque": "HANQI-CNC", "modele": "CNC-1660",
        "controller": "FANUC Series 0i-TF", "axes": 2, "rpm_max": 4500,
        "tool_capacity": 0, "statut": "MAINTENANCE", "secteur_nom": "Tournage",
    },
    {
        "code": "M011", "nom": "Centre usinage CN11", "type": "Centre usinage CNC",
        "marque": "Hartford", "modele": "SMC-5",
        "controller": "HARTROL-FANUC AI100", "axes": 3, "rpm_max": 8000,
        "tool_capacity": 20, "statut": "MAINTENANCE", "secteur_nom": "Usinage CNC",
    },
    {
        "code": "M012", "nom": "CHC-22120", "type": "Machine CNC",
        "marque": "HANQI-CNC", "modele": "CNC-1660",
        "controller": "FANUC Series 0i-TF", "axes": 2, "rpm_max": 4500,
        "tool_capacity": 0, "statut": "BROKEN", "secteur_nom": "Tournage",
    },
]

SECTEUR_DATA = [
    {"code": "T01", "nom": "Tournage", "description": "Secteur de tournage CNC"},
    {"code": "T02", "nom": "Fraisage", "description": "Secteur de fraisage CNC"},
    {"code": "T03", "nom": "Usinage CNC", "description": "Secteur d''usinage sur centre"},
    {"code": "T04", "nom": "Controle qualite", "description": "Secteur de controle qualite"},
    {"code": "T05", "nom": "Maintenance", "description": "Secteur de maintenance"},
    {"code": "T06", "nom": "Stock", "description": "Secteur de stockage"},
]

PHASE_TYPES = [
    {
        "type": "DEBIT",
        "designation": "Débit / Tronçonnage",
        "machine_types": ["Tour CNC", "Centre usinage CNC", "Machine CNC"],
        "temps_usinage_range": (3, 15),
        "temps_reglage_range": (2, 8),
        "exigences": ["Cote brute ±0.5mm", "Longueur ±1mm", "Planarite 0.3mm", ""],
        "weight": 1,
        "position": "first",
    },
    {
        "type": "REGLEMENT",
        "designation": "Réglement / Montage",
        "machine_types": ["Tour CNC", "Centre usinage CNC", "Fraiseuse CNC"],
        "temps_usinage_range": (2, 10),
        "temps_reglage_range": (5, 20),
        "exigences": ["Centrage ±0.02mm", "Parallélisme 0.01mm", "Perpendicularité 0.02mm", ""],
        "weight": 1,
        "position": "first",
    },
    {
        "type": "TOURNAGE",
        "designation": "Tournage",
        "machine_types": ["Tour CNC"],
        "temps_usinage_range": (10, 60),
        "temps_reglage_range": (3, 15),
        "exigences": ["Surface Ra 1.6µm", "Cylindricité 0.02mm", "Concentricité 0.01mm", "Diamètre ±0.01mm"],
        "weight": 3,
        "position": "middle",
    },
    {
        "type": "FRAISAGE",
        "designation": "Fraisage",
        "machine_types": ["Fraiseuse CNC"],
        "temps_usinage_range": (10, 50),
        "temps_reglage_range": (3, 15),
        "exigences": ["Surface Ra 3.2µm", "Parallélisme 0.03mm", "Planéité 0.02mm", "Profondeur ±0.05mm"],
        "weight": 3,
        "position": "middle",
    },
    {
        "type": "PERCAGE",
        "designation": "Perçage",
        "machine_types": ["Centre usinage CNC"],
        "temps_usinage_range": (5, 25),
        "temps_reglage_range": (2, 10),
        "exigences": ["Diamètre ±0.02mm", "Perpendicularité 0.05mm", "Alésage H7", "Taraudage M6"],
        "weight": 2,
        "position": "middle",
    },
    {
        "type": "RECTIFICATION",
        "designation": "Rectification",
        "machine_types": ["Tour CNC", "Centre usinage CNC", "Fraiseuse CNC"],
        "temps_usinage_range": (8, 30),
        "temps_reglage_range": (3, 10),
        "exigences": ["Surface Ra 0.8µm", "Cylindricité 0.005mm", "Parallélisme 0.01mm", ""],
        "weight": 1,
        "position": "middle",
    },
    {
        "type": "EBAVURAGE",
        "designation": "Ébavurage",
        "machine_types": ["Tour CNC", "Centre usinage CNC", "Fraiseuse CNC"],
        "temps_usinage_range": (3, 12),
        "temps_reglage_range": (1, 5),
        "exigences": ["Pas d'arêtes vives", "Rayon R0.2 max", ""],
        "weight": 1,
        "position": "last",
    },
    {
        "type": "CONTROLE",
        "designation": "Contrôle qualité",
        "machine_types": ["Tour CNC", "Centre usinage CNC", "Fraiseuse CNC"],
        "temps_usinage_range": (5, 20),
        "temps_reglage_range": (2, 8),
        "exigences": ["PDT 100%", "Mesure 3 points", "Contrôle dimensionnel", ""],
        "weight": 1,
        "position": "last",
    },
]

MATERIAL_TYPES = {
    "Acier": [
        ("C45", 7.85, 2.50), ("C45E", 7.85, 2.80), ("20MnCr5", 7.85, 3.20),
        ("42CrMo4", 7.85, 3.80), ("16MnCr5", 7.85, 2.90), ("34CrNiMo6", 7.85, 4.50),
        ("100Cr6", 7.85, 4.00), ("X40CrMoV5", 7.85, 5.20), ("S355J2", 7.85, 2.10),
        ("E360", 7.85, 2.00),
    ],
    "Inox": [
        ("304L", 7.90, 8.50), ("316L", 7.98, 9.20), ("310S", 7.98, 10.00),
        ("410", 7.75, 6.00), ("420", 7.75, 5.50), ("17-4PH", 7.78, 12.00),
    ],
    "Aluminium": [
        ("5083", 2.66, 4.50), ("6061", 2.70, 3.80), ("6082", 2.71, 3.90),
        ("7075", 2.81, 7.50), ("2017", 2.79, 4.20), ("5754", 2.66, 4.00),
    ],
    "Cuivre": [
        ("CuZn39Pb3", 8.47, 7.00), ("CuSn8", 8.78, 9.50), ("CuAl10Ni5Fe5", 7.60, 11.00),
        ("E-Cu57", 8.90, 8.00),
    ],
    "Plastique": [
        ("PA66", 1.14, 3.50), ("POM", 1.41, 2.80), ("PTFE", 2.15, 12.00),
        ("PEEK", 1.30, 85.00), ("POM-C", 1.41, 3.00),
    ],
}

TOOL_TYPES = {
    "Foret": [
        ("HSS", [3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 20.0]),
        ("Carbure", [6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 20.0, 25.0]),
    ],
    "Fraise": [
        ("Carbure", [6.0, 8.0, 10.0, 12.0, 16.0, 20.0, 25.0]),
        ("HSS", [8.0, 10.0, 12.0, 16.0]),
    ],
    "Alesoir": [
        ("Carbure", [10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 25.0]),
    ],
    "Taraud": [
        ("HSS", [4.0, 5.0, 6.0, 8.0, 10.0, 12.0]),
        ("Carbure", [6.0, 8.0, 10.0]),
    ],
    "Plateau": [
        ("Acier", [200.0, 250.0, 300.0]),
    ],
    "Mandrin": [
        ("Acier", [80.0, 100.0, 125.0, 160.0]),
    ],
    "Mandrin serrage": [
        ("Acier", [50.0, 63.0, 80.0]),
    ],
}

TOOL_MANUFACTURERS = [
    "Sandvik Coromant", "Kennametal", "Mitsubishi Materials",
    "Iscar", "Walter", "Seco Tools", "OSG", "Kyocera",
    "Sumitomo", "Mapal", "Horn", "Gühring",
]

OPERATEUR_POSTES = ["Operateur CNC", "Controleur qualite", "Technicien maintenance"]
COMPETENCES = ["Junior", "Confirme", "Senior"]

PART_FAMILLES = [
    "Arbre", "Douille", "Bague", "Rond", "Plaque",
    "Flasque", "Coussinet", "Engrenage", "Pignon", "Manivelle",
    "Support", "Palier", "Ressort", "Clavette", "Ecrou",
]

MAINTENANCE_TYPES = [
    "Preventive", "Preventive", "Preventive", "Preventive",
    "Corrective", "Corrective",
    "Changement huile", "Changement huile",
    "Nettoyage", "Nettoyage",
    "Inspection",
    "Remplacement roulement",
    "Changement liquide",
    "Alignement machine",
]

CAUSE_REBUT_DATA = [
    ("C01", "Materiel", "Defaut matiere premiere"),
    ("C02", "Materiel", "Non-conformite nuance"),
    ("C03", "Outil", "Usure outil excessive"),
    ("C04", "Outil", "Cassage foret"),
    ("C05", "Machine", "Defaut machine"),
    ("C06", "Machine", "Vibration excessive"),
    ("C07", "Programmation", "Programme errone"),
    ("C08", "Programmation", "Offset incorrect"),
    ("C09", "Operateur", "Erreur manipulation"),
    ("C10", "Operateur", "Reglage incorrect"),
    ("C11", "Autre", "Contamination"),
    ("C12", "Autre", "Autre cause"),
]
