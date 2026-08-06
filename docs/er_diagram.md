# AMIP - ER Diagram

## Entity Relationship Diagram

```mermaid
erDiagram

    SECTEUR {
        SERIAL secteur_id PK
        VARCHAR code UK
        VARCHAR nom
        TEXT description
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    MACHINE {
        SERIAL machine_id PK
        VARCHAR code UK
        VARCHAR nom
        VARCHAR type
        VARCHAR marque
        VARCHAR modele
        VARCHAR controller
        INTEGER axes
        INTEGER rpm_max
        INTEGER tool_capacity
        VARCHAR statut
        INTEGER secteur_id FK
        DATE date_installation
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    OPERATEUR {
        SERIAL operateur_id PK
        VARCHAR matricule UK
        VARCHAR nom
        VARCHAR prenom
        VARCHAR poste
        VARCHAR niveau_competence
        DATE date_embauche
        BOOLEAN actif
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    MATIERE {
        SERIAL matiere_id PK
        VARCHAR code UK
        VARCHAR designation
        VARCHAR type_matiere
        VARCHAR nuance
        DECIMAL densite
        DECIMAL prix_kg
        VARCHAR unite
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    OUTIL {
        SERIAL outil_id PK
        VARCHAR code UK
        VARCHAR designation
        VARCHAR type_outil
        DECIMAL diametre
        VARCHAR matiere_outil
        INTEGER duree_vie_totale
        INTEGER usure_actuelle
        INTEGER duree_vie_restante
        DECIMAL cout_achat
        DECIMAL cout_remplacement
        BOOLEAN disponible
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    STOCK_OUTIL {
        SERIAL stock_outil_id PK
        INTEGER outil_id FK
        INTEGER quantite_stock
        VARCHAR emplacement
        INTEGER seuil_alerte
        TIMESTAMP date_derniere_maj
    }

    PIECE {
        SERIAL piece_id PK
        VARCHAR reference UK
        VARCHAR designation
        VARCHAR famille
        INTEGER matiere_id FK
        DECIMAL poids
        VARCHAR dimensions
        VARCHAR tolerances
        DECIMAL prix_revient
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    PROGRAMME_USINAGE {
        SERIAL programme_id PK
        VARCHAR code_programme UK
        VARCHAR nom
        VARCHAR version
        TEXT description
        INTEGER duree_estimee
    }

    GAMME_USINAGE {
        SERIAL gamme_id PK
        VARCHAR code UK
        VARCHAR designation
        INTEGER piece_id FK
        INTEGER nb_phases
        INTEGER duree_totale_estimee
        VARCHAR version
        VARCHAR statut
    }

    PHASE_GAMME {
        SERIAL phase_gamme_id PK
        INTEGER gamme_id FK
        INTEGER numero_phase
        VARCHAR designation
        INTEGER machine_id FK
        INTEGER outil_id FK
        INTEGER programme_id FK
        INTEGER temps_usinage_prevu
        INTEGER temps_reglage_prevu
        TEXT exigence_technique
    }

    ORDRE_FABRICATION {
        SERIAL ordre_fabrication_id PK
        VARCHAR numero_of UK
        INTEGER piece_id FK
        INTEGER gamme_id FK
        INTEGER quantite_demandee
        INTEGER quantite_produite
        INTEGER quantite_rebut
        DATE date_debut_prevue
        DATE date_fin_prevue
        DATE date_debut_reelle
        DATE date_fin_reelle
        VARCHAR priorite
        VARCHAR statut
    }

    EXECUTION_PHASE {
        SERIAL execution_id PK
        INTEGER ordre_fabrication_id FK
        INTEGER phase_gamme_id FK
        INTEGER machine_id FK
        INTEGER outil_id FK
        INTEGER operateur_id FK
        INTEGER programme_id FK
        TIMESTAMP date_debut
        TIMESTAMP date_fin
        INTEGER temps_usinage_reel
        INTEGER temps_reglage_reel
        INTEGER nb_pieces_produites
        INTEGER nb_pieces_rebut
        DECIMAL vitesse_coupe
        DECIMAL avance
        DECIMAL profondeur_passe
        VARCHAR statut
    }

    EXECUTION_OUTIL {
        SERIAL execution_outil_id PK
        INTEGER execution_id FK
        INTEGER outil_id FK
        INTEGER usure_debut
        INTEGER usure_fin
        INTEGER duree_utilisation
    }

    CAUSE_REBUT {
        SERIAL cause_rebut_id PK
        VARCHAR code UK
        VARCHAR categorie
        VARCHAR description
    }

    CONTROLE_QUALITE {
        SERIAL controle_id PK
        INTEGER execution_id FK
        INTEGER piece_id FK
        INTEGER cause_rebut_id FK
        TIMESTAMP date_controle
        VARCHAR resultat
        INTEGER nb_controles
        INTEGER nb_conformes
        INTEGER nb_non_conformes
        DECIMAL dimension_mesuree
        DECIMAL dimension_cible
        DECIMAL tolerance_plus
        DECIMAL tolerance_moins
        DECIMAL rugosite_mesuree
        TEXT commentaire
    }

    MAINTENANCE {
        SERIAL maintenance_id PK
        INTEGER machine_id FK
        VARCHAR type_maintenance
        TEXT description
        TIMESTAMP date_debut
        TIMESTAMP date_fin
        INTEGER duree
        DECIMAL cout
        INTEGER operateur_id FK
        VARCHAR statut
        VARCHAR cree_par
    }

    SENSOR_DATA {
        BIGSERIAL sensor_id PK
        INTEGER machine_id FK
        TIMESTAMP timestamp
        DECIMAL temperature
        DECIMAL vibration
        INTEGER rpm
        DECIMAL charge_frappe
        DECIMAL puissance
        DECIMAL vitesse_avance
        VARCHAR statut_machine
        DECIMAL temps_cycle
    }

    STOCK_PIECE {
        SERIAL stock_piece_id PK
        INTEGER piece_id FK
        INTEGER quantite_stock
        VARCHAR emplacement
        TIMESTAMP date_derniere_maj
    }

    STOCK_MATIERE {
        SERIAL stock_matiere_id PK
        INTEGER matiere_id FK
        DECIMAL quantite_stock
        VARCHAR emplacement
        DECIMAL seuil_alerte
        TIMESTAMP date_derniere_maj
    }

    SECTEUR ||--o{ MACHINE : "contient"
    SECTEUR ||--o{ MAINTENANCE : "secteur"

    MACHINE ||--o{ PHASE_GAMME : "machine planifiee"
    MACHINE ||--o{ EXECUTION_PHASE : "machine reelle"
    MACHINE ||--o{ MAINTENANCE : "maintenue"
    MACHINE ||--o{ SENSOR_DATA : "genere capteurs"

    OPERATEUR ||--o{ EXECUTION_PHASE : "execute"
    OPERATEUR ||--o{ MAINTENANCE : "intervient"

    MATIERE ||--o{ PIECE : "compose"
    MATIERE ||--o{ STOCK_MATIERE : "stockee"

    OUTIL ||--o{ PHASE_GAMME : "outil planifie"
    OUTIL ||--o{ EXECUTION_OUTIL : "outil utilise"
    OUTIL ||--o{ STOCK_OUTIL : "stocke"

    PIECE ||--o{ GAMME_USINAGE : "a gamme"
    PIECE ||--o{ ORDRE_FABRICATION : "fabriquee"
    PIECE ||--o{ STOCK_PIECE : "stockee"
    PIECE ||--o{ CONTROLE_QUALITE : "controlee"

    PROGRAMME_USINAGE ||--o{ PHASE_GAMME : "programme phase"
    PROGRAMME_USINAGE ||--o{ EXECUTION_PHASE : "programme execution"

    GAMME_USINAGE ||--o{ PHASE_GAMME : "contient phases"
    GAMME_USINAGE ||--o{ ORDRE_FABRICATION : "suivie par OF"

    PHASE_GAMME ||--o{ EXECUTION_PHASE : "executee"

    ORDRE_FABRICATION ||--o{ EXECUTION_PHASE : "contient executions"

    EXECUTION_PHASE ||--o{ EXECUTION_OUTIL : "consomme outils"
    EXECUTION_PHASE ||--o{ CONTROLE_QUALITE : "controlee"

    CAUSE_REBUT ||--o{ CONTROLE_QUALITE : "cause defeaut"

    STOCK_OUTIL ||--o{ STOCK_OUTIL : "inventaire"
    STOCK_PIECE ||--o{ STOCK_PIECE : "inventaire"
    STOCK_MATIERE ||--o{ STOCK_MATIERE : "inventaire"
```

## Data Flow Diagram

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│  SECTEUR    │────>│   MACHINE    │────>│ SENSOR_DATA   │
└─────────────┘     └──────┬───────┘     └───────────────┘
                           │
                           │
┌─────────────┐     ┌──────┴───────┐     ┌───────────────┐
│  OPERATEUR  │────>│ EXECUTION    │────>│CONTROLE       │
└─────────────┘     │ _PHASE       │     │_QUALITE       │
                    └──────┬───────┘     └───────────────┘
                           │
                    ┌──────┴───────┐
                    │EXECUTION     │
                    │_OUTIL        │
                    └──────────────┘

┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│  MATIERE    │────>│    PIECE     │────>│GAMME_USINAGE  │
└─────────────┘     └──────┬───────┘     └───────┬───────┘
                           │                     │
                    ┌──────┴───────┐     ┌───────┴───────┐
                    │ORDRE_FABRIF. │     │ PHASE_GAMME   │
                    └──────────────┘     └───────────────┘

┌─────────────┐     ┌──────────────┐
│    OUTIL    │────>│ STOCK_OUTIL  │
└─────────────┘     └──────────────┘
```

## Dependency Order (Generation)

```
1. SECTEUR
2. MACHINE (depends on SECTEUR)
3. OPERATEUR
4. MATIERE
5. OUTIL
6. STOCK_OUTIL (depends on OUTIL)
7. PIECE (depends on MATIERE)
8. PROGRAMME_USINAGE
9. GAMME_USINAGE (depends on PIECE)
10. PHASE_GAMME (depends on GAMME, MACHINE, OUTIL, PROGRAMME)
11. ORDRE_FABRICATION (depends on PIECE, GAMME)
12. EXECUTION_PHASE (depends on OF, PHASE_GAMME, MACHINE, OUTIL, OPERATEUR)
13. EXECUTION_OUTIL (depends on EXECUTION, OUTIL)
14. CAUSE_REBUT
15. CONTROLE_QUALITE (depends on EXECUTION, PIECE, CAUSE_REBUT)
16. MAINTENANCE (depends on MACHINE, OPERATEUR)
17. SENSOR_DATA (depends on MACHINE)
18. STOCK_PIECE (depends on PIECE)
19. STOCK_MATIERE (depends on MATIERE)
```
