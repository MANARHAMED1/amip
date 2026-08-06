# AMIP — Catalogue des KPI du Dashboard

**Version:** 1.0
**Date:** 2026-07-15
**Statut:** Catalogue métier — En attente de validation par l'ingénieur AMM
**Nombre total de KPI:** 132

---

## Conventions

Chaque KPI suit ce modèle :

| Champ | Description |
|-------|-------------|
| **KPI ID** | Identifiant unique (ex: `EXEC-001`) |
| **Nom** | Nom lisible par un non-technique |
| **Module** | Module du dashboard concerné |
| **Question métier** | Ce que l'ingénieur veut savoir |
| **Inputs requis** | Ce que l'ingénieur sélectionne |
| **Information retournée** | Ce que le système affiche |
| **Formule** | Comment c'est calculé |
| **Visualisation** | Type de graphique ou carte |
| **Interprétation** | Ce que la valeur signifie opérationnellement |
| **Seuil vert** | Zone de performance acceptable |
| **Seuil orange** | Zone d'attention |
| **Seuil rouge** | Zone d'alerte |
| **Configurable** | Oui/Non — l'ingénieur peut modifier le seuil |
| **Source de données** | Tables et colonnes utilisées |
| **Utilisation ML** | Prédiction future (le cas échéant) |

### Abréviations modules

| Code | Module |
|------|--------|
| `EXEC` | Vue Exécutive |
| `MCH` | Machine |
| `OF` | Ordre de Fabrication |
| `QUA` | Qualité |
| `INV` | Inventaire |
| `TL` | Outil |
| `MNT` | Maintenance |
| `SEN` | Capteurs |

---

## Module 1 — Vue Exécutive

---

### EXEC-001 — OEE Global

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-001 |
| **Nom** | OEE Global de l'atelier |
| **Module** | Vue Exécutive |
| **Question métier** | Comment se porte l'efficacité globale de mon atelier ? |
| **Inputs requis** | Période |
| **Information retournée** | Moyenne pondérée de tous les OEE machines |
| **Formule** | `AVG(dwh.fact_execution.oee) × 100` |
| **Visualisation** | Carte avec jauge |
| **Interprétation** | Indicateur synthétique de la performance globale |
| **Seuil vert** | ≥ 75% |
| **Seuil orange** | 60% — 75% |
| **Seuil rouge** | < 60% |
| **Configurable** | Oui |
| **Source de données** | `dwh.fact_execution.oee` |
| **Utilisation ML** | — |

---

### EXEC-002 — Disponibilité Globale

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-002 |
| **Nom** | Disponibilité globale |
| **Module** | Vue Exécutive |
| **Question métier** | Quel pourcentage de temps mes machines sont-elles disponibles ? |
| **Inputs requis** | Période |
| **Information retournée** | Moyenne de la disponibilité de toutes les machines |
| **Formule** | `AVG(dwh.fact_execution.taux_disponibilite) × 100` |
| **Visualisation** | Carte |
| **Interprétation** | Capacité de production réelle vs temps total |
| **Seuil vert** | ≥ 85% |
| **Seuil orange** | 70% — 85% |
| **Seuil rouge** | < 70% |
| **Configurable** | Oui |
| **Source de données** | `dwh.fact_execution.taux_disponibilite` |
| **Utilisation ML** | — |

---

### EXEC-003 — Performance Globale

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-003 |
| **Nom** | Performance globale |
| **Module** | Vue Exécutive |
| **Question métier** | Mes machines produisent-elles au rythme prévu ? |
| **Inputs requis** | Période |
| **Information retournée** | Moyenne de la performance |
| **Formule** | `AVG(dwh.fact_execution.taux_performance) × 100` |
| **Visualisation** | Carte |
| **Interprétation** | Vitesse de production réelle vs théorique |
| **Seuil vert** | ≥ 90% |
| **Seuil orange** | 75% — 90% |
| **Seuil rouge** | < 75% |
| **Configurable** | Oui |
| **Source de données** | `dwh.fact_execution.taux_performance` |
| **Utilisation ML** | — |

---

### EXEC-004 — Qualité Globale

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-004 |
| **Nom** | Taux de conformité global |
| **Module** | Vue Exécutive |
| **Question métier** | Quel est le pourcentage de pièces conformes dans mon atelier ? |
| **Inputs requis** | Période |
| **Information retournée** | Taux de conformité moyen |
| **Formule** | `AVG(dwh.fact_execution.taux_qualite) × 100` |
| **Visualisation** | Carte |
| **Interprétation** | Qualité globale de production |
| **Seuil vert** | ≥ 98% |
| **Seuil orange** | 95% — 98% |
| **Seuil rouge** | < 95% |
| **Configurable** | Oui |
| **Source de données** | `dwh.fact_execution.taux_qualite` |
| **Utilisation ML** | — |

---

### EXEC-005 — Production Totale

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-005 |
| **Nom** | Nombre total de pièces produites |
| **Module** | Vue Exécutive |
| **Question métier** | Combien de pièces mon atelier a-t-il produites sur la période ? |
| **Inputs requis** | Période |
| **Information retournée** | Somme des pièces produites |
| **Formule** | `SUM(dwh.fact_execution.nb_pieces_produites)` |
| **Visualisation** | Carte |
| **Interprétation** | Volume de production global |
| **Seuil vert** | ≥ Objectif planifié |
| **Seuil orange** | 80% — 100% objectif |
| **Seuil rouge** | < 80% objectif |
| **Configurable** | Oui |
| **Source de données** | `dwh.fact_execution.nb_pieces_produites` |
| **Utilisation ML** | — |

---

### EXEC-006 — Rebut Total

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-006 |
| **Nom** | Nombre total de pièces rebutées |
| **Module** | Vue Exécutive |
| **Question métier** | Combien de pièces ai-je perdues sur la période ? |
| **Inputs requis** | Période |
| **Information retournée** | Somme des rebuts |
| **Formule** | `SUM(dwh.fact_execution.nb_pieces_rebut)` |
| **Visualisation** | Carte |
| **Interprétation** | Perte de production |
| **Seuil vert** | ≤ 2% de la production |
| **Seuil orange** | 2% — 5% |
| **Seuil rouge** | > 5% |
| **Configurable** | Oui |
| **Source de données** | `dwh.fact_execution.nb_pieces_rebut` |
| **Utilisation ML** | — |

---

### EXEC-007 — Taux de Rebut Global

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-007 |
| **Nom** | Taux de rebut global |
| **Module** | Vue Exécutive |
| **Question métier** | Quel est le pourcentage de rebuts dans mon atelier ? |
| **Inputs requis** | Période |
| **Information retournée** | Pourcentage de rebuts |
| **Formule** | `SUM(nb_pieces_rebut) / SUM(nb_pieces_produites) × 100` |
| **Visualisation** | Carte avec jauge |
| **Interprétation** | Indicateur qualité global |
| **Seuil vert** | ≤ 2% |
| **Seuil orange** | 2% — 5% |
| **Seuil rouge** | > 5% |
| **Configurable** | Oui |
| **Source de données** | `dwh.fact_execution.nb_pieces_rebut`, `dwh.fact_execution.nb_pieces_produites` |
| **Utilisation ML** | — |

---

### EXEC-008 — Nombre d'OFs Actifs

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-008 |
| **Nom** | Nombre d'ordres de fabrication en cours |
| **Module** | Vue Exécutive |
| **Question métier** | Combien d'OFs sont actuellement en production ? |
| **Inputs requis** | Période |
| **Information retournée** | Nombre d'OFs avec statut EN_COURS |
| **Formule** | `COUNT(DWH.dim_production_order) WHERE statut = 'EN_COURS'` |
| **Visualisation** | Carte |
| **Interprétation** | Charge de production actuelle |
| **Seuil vert** | Selon capacité |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `dwh.dim_production_order.statut` |
| **Utilisation ML** | — |

---

### EXEC-009 — Machines Disponibles

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-009 |
| **Nom** | Nombre de machines en état RUNNING |
| **Module** | Vue Exécutive |
| **Question métier** | Combien de machines sont opérationnelles ? |
| **Inputs requis** | — |
| **Information retournée** | Nombre de machines avec statut RUNNING |
| **Formule** | `COUNT(dwh.dim_machine) WHERE statut = 'RUNNING'` |
| **Visualisation** | Carte (sur 12) |
| **Interprétation** | Capacité opérationnelle |
| **Seuil vert** | ≥ 10/12 |
| **Seuil orange** | 7/12 — 9/12 |
| **Seuil rouge** | < 7/12 |
| **Configurable** | Oui |
| **Source de données** | `dwh.dim_machine.statut` |
| **Utilisation ML** | — |

---

### EXEC-010 — Nombre d'Alertes Critiques

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-010 |
| **Nom** | Nombre d'alertes critiques actives |
| **Module** | Vue Exécutive |
| **Question métier** | Y a-t-il des situations urgentes à traiter ? |
| **Inputs requis** | — |
| **Information retournée** | Nombre d'alertes de sévérité critique |
| **Formule** | `COUNT(alerts WHERE severity = 'Critique')` |
| **Visualisation** | Carte (avec icône rouge) |
| **Interprétation** | Urgences à traiter immédiatement |
| **Seuil vert** | 0 |
| **Seuil orange** | 1 — 3 |
| **Seuil rouge** | > 3 |
| **Configurable** | Oui |
| **Source de données** | Système d'alertes (calculé) |
| **Utilisation ML** | — |

---

### EXEC-011 — Production vs Plan

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-011 |
| **Nom** | Production réalisée vs planifiée |
| **Module** | Vue Exécutive |
| **Question métier** | Suis-je en retard sur mon plan de production ? |
| **Inputs requis** | Période |
| **Information retournée** | Quantité produite vs quantité demandée |
| **Formule** | `SUM(quantite_produite) / SUM(quantite_demandee) × 100` |
| **Visualisation** | Barres comparatives |
| **Interprétation** | Respect du planning |
| **Seuil vert** | ≥ 100% |
| **Seuil orange** | 80% — 100% |
| **Seuil rouge** | < 80% |
| **Configurable** | Oui |
| **Source de données** | `dwh.fact_production.quantite_produite`, `dwh.fact_production.quantite_demandee` |
| **Utilisation ML** | — |

---

### EXEC-012 — OFs en Retard

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-012 |
| **Nom** | Nombre d'OFs en retard |
| **Module** | Vue Exécutive |
| **Question métier** | Combien d'OFs ont dépassé leur date de fin prévue ? |
| **Inputs requis** | Période |
| **Information retournée** | Nombre d'OFs avec date_fin_reelle > date_fin_prevue |
| **Formule** | `COUNT(OF WHERE date_fin_reelle > date_fin_prevue)` |
| **Visualisation** | Carte |
| **Interprétation** | Retards de production |
| **Seuil vert** | 0 |
| **Seuil orange** | 1 — 5 |
| **Seuil rouge** | > 5 |
| **Configurable** | Oui |
| **Source de données** | `dwh.dim_production_order.date_fin_prevue`, `dwh.dim_production_order.date_fin_reelle` |
| **Utilisation ML** | — |

---

### EXEC-013 — Coût Maintenance Total

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-013 |
| **Nom** | Coût total de maintenance de l'atelier |
| **Module** | Vue Exécutive |
| **Question métier** | Combien coûte la maintenance de mon atelier ? |
| **Inputs requis** | Période |
| **Information retournée** | Somme des coûts de maintenance |
| **Formule** | `SUM(dwh.fact_maintenance.cout)` |
| **Visualisation** | Carte |
| **Interprétation** | Budget maintenance consommé |
| **Seuil vert** | ≤ Budget |
| **Seuil orange** | 100% — 120% Budget |
| **Seuil rouge** | > 120% Budget |
| **Configurable** | Oui |
| **Source de données** | `dwh.fact_maintenance.cout` |
| **Utilisation ML** | — |

---

### EXEC-014 — OEE par Machine (Top/Bottom)

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-014 |
| **Nom** | Classement des machines par OEE |
| **Module** | Vue Exécutive |
| **Question métier** | Quelles sont mes meilleures et moins bonnes machines ? |
| **Inputs requis** | Période |
| **Information retournée** | Liste des machines classées par OEE |
| **Formule** | `AVG(oee) par machine ORDER BY oee DESC/ASC` |
| **Visualisation** | Barres horizontales |
| **Interprétation** | Identification des goulots d'étranglement |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `dwh.fact_execution.oee`, `dwh.dim_machine.code` |
| **Utilisation ML** | — |

---

### EXEC-015 — Tendance Production Quotidienne

| Champ | Valeur |
|-------|--------|
| **KPI ID** | EXEC-015 |
| **Nom** | Évolution de la production quotidienne |
| **Module** | Vue Exécutive |
| **Question métier** | La production est-elle en hausse ou en baisse ? |
| **Inputs requis** | Période |
| **Information retournée** | Nombre de pièces produites par jour |
| **Formule** | `SUM(nb_pieces_produites) GROUP BY date` |
| **Visualisation** | Courbe |
| **Interprétation** | Tendance de production |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `dwh.fact_execution.nb_pieces_produites`, `dwh.dim_date` |
| **Utilisation ML** | — |

---

## Module 2 — Machine

---

### MCH-001 — Statut Machine

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-001 |
| **Nom** | Statut actuel de la machine |
| **Module** | Machine |
| **Question métier** | La machine est-elle en marche, arrêtée, en maintenance ou en panne ? |
| **Inputs requis** | Machine |
| **Information retournée** | RUNNING / STOPPED / MAINTENANCE / BROKEN |
| **Formule** | `machine.statut` |
| **Visualisation** | Carte avec indicateur coloré |
| **Interprétation** | État opérationnel |
| **Seuil vert** | RUNNING |
| **Seuil orange** | STOPPED, MAINTENANCE |
| **Seuil rouge** | BROKEN |
| **Configurable** | Non |
| **Source de données** | `machine.statut` |
| **Utilisation ML** | — |

---

### MCH-002 — OF Actuel

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-002 |
| **Nom** | Ordre de fabrication en cours |
| **Module** | Machine |
| **Question métier** | Quel OF est en cours sur cette machine ? |
| **Inputs requis** | Machine |
| **Information retournée** | Numéro OF, pièce, quantité |
| **Formule** | `SELECT numero_of FROM ordre_fabrication JOIN execution_phase WHERE machine_id = X AND statut = 'EN_COURS'` |
| **Visualisation** | Carte |
| **Interprétation** | Production en cours |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `ordre_fabrication`, `execution_phase` |
| **Utilisation ML** | — |

---

### MCH-003 — Opérateur Actuel

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-003 |
| **Nom** | Opérateur sur la machine |
| **Module** | Machine |
| **Question métier** | Qui pilote la machine ? |
| **Inputs requis** | Machine |
| **Information retournée** | Nom, prénom, niveau de compétence |
| **Formule** | `SELECT nom, prenom, niveau_competence FROM operateur WHERE operateur_id = (SELECT operateur_id FROM execution_phase WHERE machine_id = X AND statut = 'EN_COURS')` |
| **Visualisation** | Carte |
| **Interprétation** | Affectation opérateur |
| **Seuil vert** | Senior / Confirme |
| **Seuil orange** | — |
| **Seuil rouge** | Junior sur phase critique |
| **Configurable** | Oui |
| **Source de données** | `operateur`, `execution_phase` |
| **Utilisation ML** | — |

---

### MCH-004 — Outil Actuel

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-004 |
| **Nom** | Outil en cours d'utilisation |
| **Module** | Machine |
| **Question métier** | Quel outil est utilisé ? |
| **Inputs requis** | Machine |
| **Information retournée** | Code outil, type, usure |
| **Formule** | `SELECT code, type_outil, usure_actuelle FROM outil WHERE outil_id = (SELECT outil_id FROM execution_phase WHERE machine_id = X AND statut = 'EN_COURS')` |
| **Visualisation** | Carte |
| **Interprétation** | Outil en service |
| **Seuil vert** | Usure < 50% |
| **Seuil orange** | Usure 50% — 80% |
| **Seuil rouge** | Usure > 80% |
| **Configurable** | Oui |
| **Source de données** | `outil`, `execution_phase` |
| **Utilisation ML** | ML-05: Prédiction usure outil |

---

### MCH-005 — Temps d'Usinage Prévu

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-005 |
| **Nom** | Temps d'usinage prévu total |
| **Module** | Machine |
| **Question métier** | Combien de temps la production est-elle prévue ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Somme des temps d'usinage prévus (minutes) |
| **Formule** | `SUM(phase_gamme.temps_usinage_prevu)` |
| **Visualisation** | Carte |
| **Interprétation** | Capacité planifiée |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `phase_gamme.temps_usinage_prevu` |
| **Utilisation ML** | ML-02: Estimation temps d'usinage |

---

### MCH-006 — Temps d'Usinage Réel

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-006 |
| **Nom** | Temps d'usinage réel total |
| **Module** | Machine |
| **Question métier** | Combien de temps la machine a-t-elle réellement usiné ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Somme des temps d'usinage réels (minutes) |
| **Formule** | `SUM(execution_phase.temps_usinage_reel)` |
| **Visualisation** | Carte + comparaison avec prévu |
| **Interprétation** | Temps réel consommé |
| **Seuil vert** | ≤ 105% du prévu |
| **Seuil orange** | 105% — 120% du prévu |
| **Seuil rouge** | > 120% du prévu |
| **Configurable** | Oui |
| **Source de données** | `execution_phase.temps_usinage_reel` |
| **Utilisation ML** | ML-02: Estimation temps d'usinage |

---

### MCH-007 — Temps de Réglage Prévu

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-007 |
| **Nom** | Temps de réglage prévu |
| **Module** | Machine |
| **Question métier** | Combien de temps de réglage est prévu ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Somme des temps de réglage prévus (minutes) |
| **Formule** | `SUM(phase_gamme.temps_reglage_prevu)` |
| **Visualisation** | Carte |
| **Interprétation** | Temps non productif planifié |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `phase_gamme.temps_reglage_prevu` |
| **Utilisation ML** | — |

---

### MCH-008 — Temps de Réglage Réel

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-008 |
| **Nom** | Temps de réglage réel |
| **Module** | Machine |
| **Question métier** | Combien de temps de réglage réellement consommé ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Somme des temps de réglage réels (minutes) |
| **Formule** | `SUM(execution_phase.temps_reglage_reel)` |
| **Visualisation** | Carte + comparaison |
| **Interprétation** | Temps non productif réel |
| **Seuil vert** | ≤ 105% du prévu |
| **Seuil orange** | 105% — 120% du prévu |
| **Seuil rouge** | > 120% du prévu |
| **Configurable** | Oui |
| **Source de données** | `execution_phase.temps_reglage_reel` |
| **Utilisation ML** | — |

---

### MCH-009 — Disponibilité Machine

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-009 |
| **Nom** | Disponibilité de la machine |
| **Module** | Machine |
| **Question métier** | La machine est-elle disponible ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Pourcentage de disponibilité |
| **Formule** | `temps_usinage_reel / (temps_usinage_reel + temps_reglage_reel) × 100` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Capacité à produire |
| **Seuil vert** | ≥ 85% |
| **Seuil orange** | 70% — 85% |
| **Seuil rouge** | < 70% |
| **Configurable** | Oui |
| **Source de données** | `execution_phase.temps_usinage_reel`, `execution_phase.temps_reglage_reel` |
| **Utilisation ML** | — |

---

### MCH-010 — Performance Machine

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-010 |
| **Nom** | Performance de la machine |
| **Module** | Machine |
| **Question métier** | La machine produit-elle au rythme prévu ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Pourcentage de performance |
| **Formule** | `(temps_usinage_prevu × nb_pieces_produites) / temps_usinage_reel × 100` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Efficacité de production |
| **Seuil vert** | ≥ 90% |
| **Seuil orange** | 75% — 90% |
| **Seuil rouge** | < 75% |
| **Configurable** | Oui |
| **Source de données** | `execution_phase`, `phase_gamme` |
| **Utilisation ML** | — |

---

### MCH-011 — Qualité Machine

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-011 |
| **Nom** | Taux de qualité de la machine |
| **Module** | Machine |
| **Question métier** | La machine produit-elle des pièces conformes ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Pourcentage de qualité |
| **Formule** | `(nb_pieces_produites - nb_pieces_rebut) / nb_pieces_produites × 100` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Qualité de production |
| **Seuil vert** | ≥ 98% |
| **Seuil orange** | 95% — 98% |
| **Seuil rouge** | < 95% |
| **Configurable** | Oui |
| **Source de données** | `execution_phase.nb_pieces_produites`, `execution_phase.nb_pieces_rebut` |
| **Utilisation ML** | — |

---

### MCH-012 — OEE Machine

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-012 |
| **Nom** | OEE de la machine |
| **Module** | Machine |
| **Question métier** | Quel est l'OEE de cette machine ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | OEE en pourcentage |
| **Formule** | `Disponibilité × Performance × Qualité × 100` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Efficacité globale de la machine |
| **Seuil vert** | ≥ 75% |
| **Seuil orange** | 60% — 75% |
| **Seuil rouge** | < 60% |
| **Configurable** | Oui |
| **Source de données** | MCH-009, MCH-010, MCH-011 |
| **Utilisation ML** | — |

---

### MCH-013 — Température Actuelle

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-013 |
| **Nom** | Température actuelle de la broche |
| **Module** | Machine |
| **Question métier** | La température est-elle dans les normes ? |
| **Inputs requis** | Machine |
| **Information retournée** | Dernière lecture température (°C) |
| **Formule** | `DERNIERE(sensor_data.temperature)` |
| **Visualisation** | Carte + courbe |
| **Interprétation** | État thermique |
| **Seuil vert** | < 60°C |
| **Seuil orange** | 60°C — 80°C |
| **Seuil rouge** | > 80°C |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.temperature` |
| **Utilisation ML** | ML-04: Prédiction panne machine |

---

### MCH-014 — Vibration Actuelle

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-014 |
| **Nom** | Vibration actuelle |
| **Module** | Machine |
| **Question métier** | La vibration est-elle excessive ? |
| **Inputs requis** | Machine |
| **Information retournée** | Dernière lecture vibration (mm/s) |
| **Formule** | `DERNIERE(sensor_data.vibration)` |
| **Visualisation** | Carte + courbe |
| **Interprétation** | État mécanique |
| **Seuil vert** | < 2.5 mm/s |
| **Seuil orange** | 2.5 — 4.5 mm/s |
| **Seuil rouge** | > 4.5 mm/s |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.vibration` |
| **Utilisation ML** | ML-04: Prédiction panne machine |

---

### MCH-015 — RPM Actuel

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-015 |
| **Nom** | Vitesse de rotation broche |
| **Module** | Machine |
| **Question métier** | La broche tourne-t-elle à la vitesse correcte ? |
| **Inputs requis** | Machine |
| **Information retournée** | Dernière lecture RPM |
| **Formule** | `DERNIERE(sensor_data.rpm)` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Vitesse de rotation |
| **Seuil vert** | Dans la plage prévue |
| **Seuil orange** | Légère déviation |
| **Seuil rouge** | Déviation majeure |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.rpm` |
| **Utilisation ML** | — |

---

### MCH-016 — Puissance Consommée

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-016 |
| **Nom** | Puissance électrique consommée |
| **Module** | Machine |
| **Question métier** | La consommation est-elle normale ? |
| **Inputs requis** | Machine |
| **Information retournée** | Dernière lecture puissance (kW) |
| **Formule** | `DERNIERE(sensor_data.puissance)` |
| **Visualisation** | Carte + courbe |
| **Interprétation** | Consommation énergétique |
| **Seuil vert** | Dans la plage normale |
| **Seuil orange** | Légère augmentation |
| **Seuil rouge** | Consommation anormale |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.puissance` |
| **Utilisation ML** | — |

---

### MCH-017 — Score d'Anomalie

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-017 |
| **Nom** | Score d'anomalie basé sur les capteurs |
| **Module** | Machine |
| **Question métier** | La machine présente-t-elle des anomalies ? |
| **Inputs requis** | Machine |
| **Information retournée** | Score de 0 à 100 |
| **Formule** | `Calcul basé sur l'écart de température, vibration, puissance par rapport aux seuils` |
| **Visualisation** | Carte avec jauge colorée |
| **Interprétation** | État de santé global |
| **Seuil vert** | < 30 |
| **Seuil orange** | 30 — 60 |
| **Seuil rouge** | > 60 |
| **Configurable** | Oui |
| **Source de données** | `sensor_data` (calculé) |
| **Utilisation ML** | ML-04: Détection d'anomalie |

---

### MCH-018 — Nombre d'Interventions Maintenance

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-018 |
| **Nom** | Nombre d'interventions de maintenance |
| **Module** | Machine |
| **Question métier** | Combien de fois cette machine a-t-elle été maintenue ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Nombre d'interventions |
| **Formule** | `COUNT(maintenance WHERE machine_id = X)` |
| **Visualisation** | Carte |
| **Interprétation** | Fréquence de maintenance |
| **Seuil vert** | Faible (moins d'interventions = mieux) |
| **Seuil orange** | — |
| **Seuil rouge** | Trop fréquent |
| **Configurable** | Oui |
| **Source de données** | `maintenance` |
| **Utilisation ML** | — |

---

### MCH-019 — Coût Maintenance Machine

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-019 |
| **Nom** | Coût total de maintenance de la machine |
| **Module** | Machine |
| **Question métier** | Combien coûte la maintenance de cette machine ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Somme des coûts de maintenance |
| **Formule** | `SUM(maintenance.cout WHERE machine_id = X)` |
| **Visualisation** | Carte + courbe |
| **Interprétation** | Budget maintenance machine |
| **Seuil vert** | ≤ Budget |
| **Seuil orange** | 100% — 120% Budget |
| **Seuil rouge** | > 120% Budget |
| **Configurable** | Oui |
| **Source de données** | `maintenance.cout` |
| **Utilisation ML** | — |

---

### MCH-020 — MTBF (Mean Time Between Failures)

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MCH-020 |
| **Nom** | Temps moyen entre pannes |
| **Module** | Machine |
| **Question métier** | Quel est le temps moyen entre les pannes de cette machine ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | MTBF en heures |
| **Formule** | `Temps total de fonctionnement / Nombre de pannes (maintenance corrective)` |
| **Visualisation** | Carte |
| **Interprétation** | Fiabilité de la machine |
| **Seuil vert** | ≥ 200 heures |
| **Seuil orange** | 100 — 200 heures |
| **Seuil rouge** | < 100 heures |
| **Configurable** | Oui |
| **Source de données** | `maintenance`, `sensor_data.statut_machine` |
| **Utilisation ML** | ML-03: Maintenance prédictive |

---

## Module 3 — Ordre de Fabrication

---

### OF-001 — Statut OF

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-001 |
| **Nom** | Statut de l'ordre de fabrication |
| **Module** | Ordre de Fabrication |
| **Question métier** | Mon OF est-il en attente, en cours, terminé ou annulé ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | EN_ATTENTE / EN_COURS / TERMINE / ANNULE |
| **Formule** | `ordre_fabrication.statut` |
| **Visualisation** | Carte avec indicateur coloré |
| **Interprétation** | État de l'OF |
| **Seuil vert** | TERMINE |
| **Seuil orange** | EN_COURS |
| **Seuil rouge** | ANNULE |
| **Configurable** | Non |
| **Source de données** | `ordre_fabrication.statut` |
| **Utilisation ML** | — |

---

### OF-002 — Quantité Demandée

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-002 |
| **Nom** | Quantité commandée |
| **Module** | Ordre de Fabrication |
| **Question métier** | Combien de pièces doit-on produire ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | Nombre de pièces demandées |
| **Formule** | `ordre_fabrication.quantite_demandee` |
| **Visualisation** | Carte |
| **Interprétation** | Objectif de production |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `ordre_fabrication.quantite_demandee` |
| **Utilisation ML** | — |

---

### OF-003 — Quantité Produite

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-003 |
| **Nom** | Quantité effectivement produite |
| **Module** | Ordre de Fabrication |
| **Question métier** | Combien de pièces ont été produites ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | Nombre de pièces produites |
| **Formule** | `ordre_fabrication.quantite_produite` |
| **Visualisation** | Carte |
| **Interprétation** | Réalisation |
| **Seuil vert** | ≥ Quantité demandée |
| **Seuil orange** | 80% — 100% |
| **Seuil rouge** | < 80% |
| **Configurable** | Oui |
| **Source de données** | `ordre_fabrication.quantite_produite` |
| **Utilisation ML** | ML-06: Prédiction durée production |

---

### OF-004 — Pièces Bonnes

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-004 |
| **Nom** | Nombre de pièces conformes |
| **Module** | Ordre de Fabrication |
| **Question métier** | Combien de bonnes pièces ai-je ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | Quantité produite - Quantité rebut |
| **Formule** | `quantite_produite - quantite_rebut` |
| **Visualisation** | Carte |
| **Interprétation** | Production utile |
| **Seuil vert** | ≥ Quantité demandée |
| **Seuil orange** | 80% — 100% |
| **Seuil rouge** | < 80% |
| **Configurable** | Oui |
| **Source de données** | `ordre_fabrication` |
| **Utilisation ML** | — |

---

### OF-005 — Pièces Rebutées

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-005 |
| **Nom** | Nombre de pièces rejetées |
| **Module** | Ordre de Fabrication |
| **Question métier** | Combien de pièces ai-je perdues ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | Nombre de rebuts |
| **Formule** | `ordre_fabrication.quantite_rebut` |
| **Visualisation** | Carte |
| **Interprétation** | Perte |
| **Seuil vert** | 0 |
| **Seuil orange** | 1% — 5% |
| **Seuil rouge** | > 5% |
| **Configurable** | Oui |
| **Source de données** | `ordre_fabrication.quantite_rebut` |
| **Utilisation ML** | ML-01: Prédiction rebut |

---

### OF-006 — Taux de Rebut OF

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-006 |
| **Nom** | Pourcentage de rebut de l'OF |
| **Module** | Ordre de Fabrication |
| **Question métier** | Quel est le taux de perte de cet OF ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | Pourcentage de rebut |
| **Formule** | `quantite_rebut / quantite_produite × 100` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Qualité de l'OF |
| **Seuil vert** | ≤ 2% |
| **Seuil orange** | 2% — 5% |
| **Seuil rouge** | > 5% |
| **Configurable** | Oui |
| **Source de données** | `ordre_fabrication` |
| **Utilisation ML** | ML-01: Prédiction rebut |

---

### OF-007 — Avancement OF

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-007 |
| **Nom** | Pourcentage d'avancement |
| **Module** | Ordre de Fabrication |
| **Question métier** | Où en est l'avancement de l'OF ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | Pourcentage de complétion |
| **Formule** | `quantite_produite / quantite_demandee × 100` |
| **Visualisation** | Jauge |
| **Interprétation** | Progression |
| **Seuil vert** | ≥ 100% |
| **Seuil orange** | 50% — 100% |
| **Seuil rouge** | < 50% |
| **Configurable** | Oui |
| **Source de données** | `ordre_fabrication` |
| **Utilisation ML** | — |

---

### OF-008 — Durée Prévue

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-008 |
| **Nom** | Durée prévue de l'OF |
| **Module** | Ordre de Fabrication |
| **Question métier** | Combien de temps l'OF devrait-il durer ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | Nombre de jours |
| **Formule** | `date_fin_prevue - date_debut_prevue` |
| **Visualisation** | Carte |
| **Interprétation** | Planning |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `ordre_fabrication.date_debut_prevue`, `ordre_fabrication.date_fin_prevue` |
| **Utilisation ML** | ML-06: Prédiction durée |

---

### OF-009 — Durée Réelle

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-009 |
| **Nom** | Durée réelle de l'OF |
| **Module** | Ordre de Fabrication |
| **Question métier** | Combien de temps l'OF a-t-il réellement duré ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | Nombre de jours réels |
| **Formule** | `date_fin_reelle - date_debut_reelle` |
| **Visualisation** | Carte + comparaison |
| **Interprétation** | Réel vs prévu |
| **Seuil vert** | ≤ Prévu |
| **Seuil orange** | 100% — 120% du prévu |
| **Seuil rouge** | > 120% du prévu |
| **Configurable** | Oui |
| **Source de données** | `ordre_fabrication.date_debut_reelle`, `ordre_fabrication.date_fin_reelle` |
| **Utilisation ML** | ML-06: Prédiction durée |

---

### OF-010 — Retard

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-010 |
| **Nom** | Retard de l'OF |
| **Module** | Ordre de Fabrication |
| **Question métier** | L'OF est-il en retard ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | Nombre de jours de retard |
| **Formule** | `date_fin_reelle - date_fin_prevue` (si positif = retard) |
| **Visualisation** | Carte |
| **Interprétation** | Retard |
| **Seuil vert** | ≤ 0 (à l'heure ou en avance) |
| **Seuil orange** | 1 — 3 jours |
| **Seuil rouge** | > 3 jours |
| **Configurable** | Oui |
| **Source de données** | `ordre_fabrication` |
| **Utilisation ML** | — |

---

### OF-011 — Machine Utilisée

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-011 |
| **Nom** | Machine(s) utilisée(s) pour l'OF |
| **Module** | Ordre de Fabrication |
| **Question métier** | Quelle machine est utilisée ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | Liste des codes machines |
| **Formule** | `SELECT DISTINCT machine.code FROM machine JOIN execution_phase WHERE ordre_fabrication_id = X` |
| **Visualisation** | Tableau |
| **Interprétation** | Affectation machine |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `machine`, `execution_phase` |
| **Utilisation ML** | — |

---

### OF-012 — Opérateur(s)

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-012 |
| **Nom** | Opérateur(s) affecté(s) |
| **Module** | Ordre de Fabrication |
| **Question métier** | Qui travaille sur cet OF ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | Liste des opérateurs |
| **Formule** | `SELECT DISTINCT operateur.nom, prenom FROM operateur JOIN execution_phase WHERE ordre_fabrication_id = X` |
| **Visualisation** | Tableau |
| **Interprétation** | Affectation opérateur |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `operateur`, `execution_phase` |
| **Utilisation ML** | — |

---

### OF-013 — Efficacité OF

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-013 |
| **Nom** | Efficacité globale de l'OF |
| **Module** | Ordre de Fabrication |
| **Question métier** | L'OF a-t-il été efficace ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | Efficacité en % |
| **Formule** | `quantite_produite / quantite_demandee × (temps_prevu / temps_reel) × 100` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Efficacité composite |
| **Seuil vert** | ≥ 90% |
| **Seuil orange** | 75% — 90% |
| **Seuil rouge** | < 75% |
| **Configurable** | Oui |
| **Source de données** | `ordre_fabrication`, `execution_phase` |
| **Utilisation ML** | — |

---

### OF-014 — Priorité OF

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-014 |
| **Nom** | Priorité de l'ordre de fabrication |
| **Module** | Ordre de Fabrication |
| **Question métier** | Quelle est la priorité de cet OF ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | HAUTE / NORMALE / BASSE |
| **Formule** | `ordre_fabrication.priorite` |
| **Visualisation** | Carte avec badge coloré |
| **Interprétation** | Priorité |
| **Seuil vert** | NORMALE, BASSE |
| **Seuil orange** | — |
| **Seuil rouge** | HAUTE (si en retard) |
| **Configurable** | Non |
| **Source de données** | `ordre_fabrication.priorite` |
| **Utilisation ML** | — |

---

### OF-015 — Phases par Ordre

| Champ | Valeur |
|-------|--------|
| **KPI ID** | OF-015 |
| **Nom** | Nombre de phases exécutées |
| **Module** | Ordre de Fabrication |
| **Question métier** | Combien de phases l'OF a-t-il nécessitées ? |
| **Inputs requis** | Numéro OF |
| **Information retournée** | Nombre de phases, phases terminées, en cours |
| **Formule** | `COUNT(execution_phase WHERE ordre_fabrication_id = X)` |
| **Visualisation** | Frise ou tableau |
| **Interprétation** | Complexité de l'OF |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `execution_phase`, `phase_gamme` |
| **Utilisation ML** | — |

---

## Module 4 — Qualité

---

### QUA-001 — Nombre d'Inspections

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-001 |
| **Nom** | Nombre total d'inspections qualité |
| **Module** | Qualité |
| **Question métier** | Combien de contrôles qualité ai-je effectués ? |
| **Inputs requis** | Période, (Pièce / Machine / OF) |
| **Information retournée** | Nombre de contrôles |
| **Formule** | `COUNT(controle_qualite)` |
| **Visualisation** | Carte |
| **Interprétation** | Activité de contrôle |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `controle_qualite` |
| **Utilisation ML** | — |

---

### QUA-002 — Pièces Conformes

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-002 |
| **Nom** | Nombre de pièces conformes |
| **Module** | Qualité |
| **Question métier** | Combien de pièces sont conformes ? |
| **Inputs requis** | Période, (Pièce / Machine / OF) |
| **Information retournée** | Nombre de pièces conformes |
| **Formule** | `SUM(controle_qualite.nb_conformes)` |
| **Visualisation** | Carte |
| **Interprétation** | Production conforme |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `controle_qualite.nb_conformes` |
| **Utilisation ML** | — |

---

### QUA-003 — Pièces Non Conformes

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-003 |
| **Nom** | Nombre de pièces non conformes |
| **Module** | Qualité |
| **Question métier** | Combien de pièces sont rejetées ? |
| **Inputs requis** | Période, (Pièce / Machine / OF) |
| **Information retournée** | Nombre de non-conformes |
| **Formule** | `SUM(controle_qualite.nb_non_conformes)` |
| **Visualisation** | Carte |
| **Interprétation** | Perte qualité |
| **Seuil vert** | 0 |
| **Seuil orange** | — |
| **Seuil rouge** | > Seuil |
| **Configurable** | Oui |
| **Source de données** | `controle_qualite.nb_non_conformes` |
| **Utilisation ML** | ML-01: Prédiction rebut |

---

### QUA-004 — Taux de Conformité

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-004 |
| **Nom** | Taux de conformité |
| **Module** | Qualité |
| **Question métier** | Quel % de mes pièces sont conformes ? |
| **Inputs requis** | Période, (Pièce / Machine / OF) |
| **Information retournée** | Pourcentage de conformité |
| **Formule** | `SUM(nb_conformes) / SUM(nb_controles) × 100` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Qualité globale |
| **Seuil vert** | ≥ 98% |
| **Seuil orange** | 95% — 98% |
| **Seuil rouge** | < 95% |
| **Configurable** | Oui |
| **Source de données** | `controle_qualite` |
| **Utilisation ML** | — |

---

### QUA-005 — Taux de Rebut

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-005 |
| **Nom** | Taux de rebut |
| **Module** | Qualité |
| **Question métier** | Quel % de mes pièces sont rejetées ? |
| **Inputs requis** | Période, (Pièce / Machine / OF) |
| **Information retournée** | Pourcentage de rebut |
| **Formule** | `SUM(nb_non_conformes) / SUM(nb_controles) × 100` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Perte qualité |
| **Seuil vert** | ≤ 2% |
| **Seuil orange** | 2% — 5% |
| **Seuil rouge** | > 5% |
| **Configurable** | Oui |
| **Source de données** | `controle_qualite` |
| **Utilisation ML** | ML-01: Prédiction rebut |

---

### QUA-006 — FPY (First Pass Yield)

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-006 |
| **Nom** | Rendement au premier passage |
| **Module** | Qualité |
| **Question métier** | Combien de pièces sont conformes dès le premier contrôle ? |
| **Inputs requis** | Période, (Pièce / Machine / OF) |
| **Information retournée** | Pourcentage FPY |
| **Formule** | `Nombre de pièces conformes au 1er contrôle / Total pièces × 100` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Qualité du processus |
| **Seuil vert** | ≥ 95% |
| **Seuil orange** | 90% — 95% |
| **Seuil rouge** | < 90% |
| **Configurable** | Oui |
| **Source de données** | `controle_qualite` |
| **Utilisation ML** | — |

---

### QUA-007 — Défauts par Catégorie

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-007 |
| **Nom** | Répartition des défauts par catégorie |
| **Module** | Qualité |
| **Question métier** | Quelles sont les grandes causes de défauts ? |
| **Inputs requis** | Période |
| **Information retournée** | Nombre par catégorie (Materiel, Outil, Machine, Programmation, Operateur, Autre) |
| **Formule** | `COUNT(cq) GROUP BY cause_rebut.categorie` |
| **Visualisation** | Camembert |
| **Interprétation** | Analyse Pareto des causes |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `controle_qualite`, `cause_rebut` |
| **Utilisation ML** | — |

---

### QUA-008 — Top 5 Causes de Défauts

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-008 |
| **Nom** | Les 5 causes principales de défauts |
| **Module** | Qualité |
| **Question métier** | Quelles sont les causes les plus fréquentes ? |
| **Inputs requis** | Période |
| **Information retournée** | Top 5 des descriptions de causes |
| **Formule** | `COUNT(cq) GROUP BY cause_rebut.description ORDER BY COUNT DESC LIMIT 5` |
| **Visualisation** | Barres horizontales (Pareto) |
| **Interprétation** | Priorisation des actions correctives |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `controle_qualite`, `cause_rebut` |
| **Utilisation ML** | — |

---

### QUA-009 — Évolution du Taux de Rebut

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-009 |
| **Nom** | Évolution du taux de rebut dans le temps |
| **Module** | Qualité |
| **Question métier** | La qualité s'améliore-t-elle ? |
| **Inputs requis** | Période |
| **Information retournée** | Taux de rebut par jour/semaine/mois |
| **Formule** | `SUM(nb_non_conformes) / SUM(nb_controles) × 100 GROUP BY date` |
| **Visualisation** | Courbe |
| **Interprétation** | Tendance qualité |
| **Seuil vert** | Tendance à la baisse |
| **Seuil orange** | Stable |
| **Seuil rouge** | Tendance à la hausse |
| **Configurable** | Oui |
| **Source de données** | `controle_qualite` |
| **Utilisation ML** | — |

---

### QUA-010 — Qualité par Machine

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-010 |
| **Nom** | Taux de rebut par machine |
| **Module** | Qualité |
| **Question métier** | Quelle machine produit le plus de rebuts ? |
| **Inputs requis** | Période |
| **Information retournée** | Taux de rebut par machine |
| **Formule** | `SUM(nb_non_conformes) / SUM(nb_controles) × 100 GROUP BY machine.code` |
| **Visualisation** | Barres horizontales |
| **Interprétation** | Performance machine en qualité |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `controle_qualite`, `execution_phase`, `machine` |
| **Utilisation ML** | — |

---

### QUA-011 — Qualité par Opérateur

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-011 |
| **Nom** | Taux de rebut par opérateur |
| **Module** | Qualité |
| **Question métier** | Quel opérateur a le meilleur taux de conformité ? |
| **Inputs requis** | Période |
| **Information retournée** | Taux de rebut par opérateur |
| **Formule** | `SUM(nb_non_conformes) / SUM(nb_controles) × 100 GROUP BY operateur.nom` |
| **Visualisation** | Barres horizontales |
| **Interprétation** | Performance opérateur |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `controle_qualite`, `execution_phase`, `operateur` |
| **Utilisation ML** | — |

---

### QUA-012 — Qualité par Outil

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-012 |
| **Nom** | Taux de rebut par outil |
| **Module** | Qualité |
| **Question métier** | Quel outil cause le plus de défauts ? |
| **Inputs requis** | Période |
| **Information retournée** | Taux de rebut par outil |
| **Formule** | `SUM(nb_non_conformes) / SUM(nb_controles) × 100 GROUP BY outil.code` |
| **Visualisation** | Barres horizontales |
| **Interprétation** | Impact outil sur qualité |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `controle_qualite`, `execution_phase`, `outil` |
| **Utilisation ML** | — |

---

### QUA-013 — Qualité par Matière

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-013 |
| **Nom** | Taux de rebut par type de matière |
| **Module** | Qualité |
| **Question métier** | Quelle matière cause le plus de défauts ? |
| **Inputs requis** | Période |
| **Information retournée** | Taux de rebut par matière |
| **Formule** | `SUM(nb_non_conformes) / SUM(nb_controles) × 100 GROUP BY matiere.type_matiere` |
| **Visualisation** | Barres |
| **Interprétation** | Impact matière sur qualité |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `controle_qualite`, `piece`, `matiere` |
| **Utilisation ML** | — |

---

### QUA-014 — Écart Dimensionnel Moyen

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-014 |
| **Nom** | Écart dimensionnel moyen |
| **Module** | Qualité |
| **Question métier** | Mes pièces sont-elles dans les tolérances ? |
| **Inputs requis** | Période, Pièce |
| **Information retournée** | Écart moyen (mesurée - cible) |
| **Formule** | `AVG(dimension_mesuree - dimension_cible)` |
| **Visualisation** | Carte |
| **Interprétation** | Précision du processus |
| **Seuil vert** | Dans tolérance |
| **Seuil orange** | Proche des limites |
| **Seuil rouge** | Hors tolérance |
| **Configurable** | Oui |
| **Source de données** | `controle_qualite.dimension_mesuree`, `controle_qualite.dimension_cible` |
| **Utilisation ML** | — |

---

### QUA-015 — Rugosité Moyenne

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-015 |
| **Nom** | Rugosité moyenne mesurée |
| **Module** | Qualité |
| **Question métier** | La finition de surface est-elle acceptable ? |
| **Inputs requis** | Période, Pièce |
| **Information retournée** | Rugosité moyenne (Ra) |
| **Formule** | `AVG(rugosite_mesuree)` |
| **Visualisation** | Carte |
| **Interprétation** | Qualité de surface |
| **Seuil vert** | Selon spécification |
| **Seuil orange** | Proche limite |
| **Seuil rouge** | Hors spécification |
| **Configurable** | Oui |
| **Source de données** | `controle_qualite.rugosite_mesuree` |
| **Utilisation ML** | — |

---

### QUA-016 — Qualité par Pièce

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-016 |
| **Nom** | Taux de rebut par pièce |
| **Module** | Qualité |
| **Question métier** | Quelle pièce a le plus de défauts ? |
| **Inputs requis** | Période |
| **Information retournée** | Taux de rebut par référence pièce |
| **Formule** | `SUM(nb_non_conformes) / SUM(nb_controles) × 100 GROUP BY piece.reference` |
| **Visualisation** | Barres horizontales |
| **Interprétation** | Pièces à problèmes |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `controle_qualite`, `piece` |
| **Utilisation ML** | — |

---

### QUA-017 — Taux de Défauts par Famille

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-017 |
| **Nom** | Taux de défauts par famille de pièces |
| **Module** | Qualité |
| **Question métier** | Quelle famille de pièces pose le plus de problèmes ? |
| **Inputs requis** | Période |
| **Information retournée** | Taux de rebut par famille |
| **Formule** | `SUM(nb_non_conformes) / SUM(nb_controles) × 100 GROUP BY piece.famille` |
| **Visualisation** | Barres |
| **Interprétation** | Tendance par famille |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `controle_qualite`, `piece` |
| **Utilisation ML** | — |

---

### QUA-018 — Ratio Préventif/Correctif Qualité

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-018 |
| **Nom** | Nombre de contrôles conformes vs non conformes |
| **Module** | Qualité |
| **Question métier** | Quel est le ratio conformes/non conformes ? |
| **Inputs requis** | Période |
| **Information retournée** | Ratio |
| **Formule** | `SUM(nb_conformes) / SUM(nb_non_conformes)` |
| **Visualisation** | Camembert |
| **Interprétation** | Équilibre qualité |
| **Seuil vert** | ≥ 20:1 |
| **Seuil orange** | 10:1 — 20:1 |
| **Seuil rouge** | < 10:1 |
| **Configurable** | Oui |
| **Source de données** | `controle_qualite` |
| **Utilisation ML** | — |

---

### QUA-019 — Nombre de Contrôles par Inspection

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-019 |
| **Nom** | Nombre moyen de contrôles par inspection |
| **Module** | Qualité |
| **Question métier** | Combien de mesures par contrôle ? |
| **Inputs requis** | Période |
| **Information retournée** | Moyenne de nb_controles |
| **Formule** | `AVG(nb_controles)` |
| **Visualisation** | Carte |
| **Interprétation** | Profondeur du contrôle |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `controle_qualite.nb_controles` |
| **Utilisation ML** | — |

---

### QUA-020 — Dernière Inspection

| Champ | Valeur |
|-------|--------|
| **KPI ID** | QUA-020 |
| **Nom** | Date de dernière inspection |
| **Module** | Qualité |
| **Question métier** | Quand a eu lieu le dernier contrôle qualité ? |
| **Inputs requis** | Pièce |
| **Information retournée** | Date de la dernière inspection |
| **Formule** | `MAX(date_controle)` |
| **Visualisation** | Carte |
| **Interprétation** | Fraîcheur du contrôle |
| **Seuil vert** | < 7 jours |
| **Seuil orange** | 7 — 30 jours |
| **Seuil rouge** | > 30 jours |
| **Configurable** | Oui |
| **Source de données** | `controle_qualite.date_controle` |
| **Utilisation ML** | — |

---

## Module 5 — Inventaire

---

### INV-001 — Stock Actuel Matière

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-001 |
| **Nom** | Quantité en stock de matière première |
| **Module** | Inventaire |
| **Question métier** | Combien de matière ai-je en stock ? |
| **Inputs requis** | Matière |
| **Information retournée** | Quantité en kg |
| **Formule** | `stock_matiere.quantite_stock` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Niveau de stock |
| **Seuil vert** | > seuil_alerte × 1.5 |
| **Seuil orange** | seuil_alerte — seuil × 1.5 |
| **Seuil rouge** | ≤ seuil_alerte |
| **Configurable** | Oui |
| **Source de données** | `stock_matiere.quantite_stock`, `stock_matiere.seuil_alerte` |
| **Utilisation ML** | ML-07: Prévision stock |

---

### INV-002 — Statut Stock Matière

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-002 |
| **Nom** | Statut du stock de matière |
| **Module** | Inventaire |
| **Question métier** | Mon stock est-il critique, bas, normal ou en excès ? |
| **Inputs requis** | Matière |
| **Information retournée** | Critique / Bas / Normal / Surstock |
| **Formule** | `Si stock ≤ seuil → Critique; Si stock ≤ 1.5×seuil → Bas; Si stock > seuil×3 → Surstock; Sinon → Normal` |
| **Visualisation** | Carte avec badge coloré |
| **Interprétation** | État du stock |
| **Seuil vert** | Normal |
| **Seuil orange** | Bas, Surstock |
| **Seuil rouge** | Critique |
| **Configurable** | Oui |
| **Source de données** | `stock_matiere` |
| **Utilisation ML** | ML-07: Prévision stock |

---

### INV-003 — Seuil d'Alerte Matière

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-003 |
| **Nom** | Seuil d'alerte matière première |
| **Module** | Inventaire |
| **Question métier** | Quel est le seuil minimum pour cette matière ? |
| **Inputs requis** | Matière |
| **Information retournée** | Seuil d'alerte |
| **Formule** | `stock_matiere.seuil_alerte` |
| **Visualisation** | Carte |
| **Interprétation** | Limite basse |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Oui |
| **Source de données** | `stock_matiere.seuil_alerte` |
| **Utilisation ML** | — |

---

### INV-004 — Valeur Stock Matière

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-004 |
| **Nom** | Valeur du stock de matière première |
| **Module** | Inventaire |
| **Question métier** | Combien vaut mon stock de matière ? |
| **Inputs requis** | Matière |
| **Information retournée** | Valeur en EUR |
| **Formule** | `quantite_stock × prix_kg` |
| **Visualisation** | Carte |
| **Interprétation** | Investissement stock |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `stock_matiere.quantite_stock`, `matiere.prix_kg` |
| **Utilisation ML** | — |

---

### INV-005 — Stock Outil

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-005 |
| **Nom** | Quantité d'outils en stock |
| **Module** | Inventaire |
| **Question métier** | Combien d'outils ai-je en stock ? |
| **Inputs requis** | Outil |
| **Information retournée** | Nombre d'unités |
| **Formule** | `stock_outil.quantite_stock` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Disponibilité outils |
| **Seuil vert** | > seuil_alerte |
| **Seuil orange** | = seuil_alerte |
| **Seuil rouge** | < seuil_alerte |
| **Configurable** | Oui |
| **Source de données** | `stock_outil` |
| **Utilisation ML** | — |

---

### INV-006 — Statut Stock Outil

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-006 |
| **Nom** | Statut du stock d'outils |
| **Module** | Inventaire |
| **Question métier** | Mon stock d'outils est-il suffisant ? |
| **Inputs requis** | Outil |
| **Information retournée** | Critique / Bas / Normal / Surstock |
| **Formule** | `Si stock ≤ seuil → Critique; Si stock ≤ 1.5×seuil → Bas; Si stock > seuil×3 → Surstock; Sinon → Normal` |
| **Visualisation** | Carte avec badge coloré |
| **Interprétation** | État du stock |
| **Seuil vert** | Normal |
| **Seuil orange** | Bas, Surstock |
| **Seuil rouge** | Critique |
| **Configurable** | Oui |
| **Source de données** | `stock_outil` |
| **Utilisation ML** | — |

---

### INV-007 — Stock Pièces Finies

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-007 |
| **Nom** | Quantité de pièces finies en stock |
| **Module** | Inventaire |
| **Question métier** | Combien de pièces finies ai-je en stock ? |
| **Inputs requis** | Pièce |
| **Information retournée** | Nombre d'unités |
| **Formule** | `stock_piece.quantite_stock` |
| **Visualisation** | Carte |
| **Interprétation** | Stock fini |
| **Seuil vert** | > 0 |
| **Seuil orange** | = 0 |
| **Seuil rouge** | — |
| **Configurable** | Oui |
| **Source de données** | `stock_piece` |
| **Utilisation ML** | — |

---

### INV-008 — Statut Stock Pièces

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-008 |
| **Nom** | Statut du stock de pièces finies |
| **Module** | Inventaire |
| **Question métier** | Le stock de pièces finies est-il suffisant ? |
| **Inputs requis** | Pièce |
| **Information retournée** | Critique / Bas / Normal / Surstock |
| **Formule** | `Basé sur la consommation moyenne` |
| **Visualisation** | Carte avec badge coloré |
| **Interprétation** | État du stock |
| **Seuil vert** | Normal |
| **Seuil orange** | Bas, Surstock |
| **Seuil rouge** | Critique |
| **Configurable** | Oui |
| **Source de données** | `stock_piece` |
| **Utilisation ML** | — |

---

### INV-009 — Jours de Stock Restants (Matière)

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-009 |
| **Nom** | Nombre de jours de stock restants |
| **Module** | Inventaire |
| **Question métier** | Combien de jours de stock me reste-t-il ? |
| **Inputs requis** | Matière |
| **Information retournée** | Nombre de jours |
| **Formule** | `stock_actuel / consommation_moyenne_journée` |
| **Visualisation** | Carte |
| **Interprétation** | Durée avant rupture |
| **Seuil vert** | > 30 jours |
| **Seuil orange** | 15 — 30 jours |
| **Seuil rouge** | < 15 jours |
| **Configurable** | Oui |
| **Source de données** | `stock_matiere`, `execution_phase` (consommation) |
| **Utilisation ML** | ML-07: Prévision stock |

---

### INV-010 — Valeur Totale Inventaire

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-010 |
| **Nom** | Valeur totale de l'inventaire |
| **Module** | Inventaire |
| **Question métier** | Combien vaut l'ensemble de mon inventaire ? |
| **Inputs requis** | — |
| **Information retournée** | Valeur totale en EUR |
| **Formule** | `SUM(stock_matiere.quantite_stock × matiere.prix_kg) + SUM(stock_outil.quantite_stock × outil.cout_achat) + SUM(stock_piece.quantite_stock × piece.prix_revient)` |
| **Visualisation** | Carte + camembert |
| **Interprétation** | Investissement total |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `stock_matiere`, `stock_outil`, `stock_piece`, `matiere`, `outil`, `piece` |
| **Utilisation ML** | — |

---

### INV-011 — Nombre d'Articles Critiques

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-011 |
| **Nom** | Nombre d'articles en stock critique |
| **Module** | Inventaire |
| **Question métier** | Combien d'articles nécessitent une réapprovisionnement urgent ? |
| **Inputs requis** | — |
| **Information retournée** | Nombre d'articles critiques |
| **Formule** | `COUNT(articles WHERE stock ≤ seuil)` |
| **Visualisation** | Carte (avec icône rouge) |
| **Interprétation** | Urgences réapprovisionnement |
| **Seuil vert** | 0 |
| **Seuil orange** | 1 — 3 |
| **Seuil rouge** | > 3 |
| **Configurable** | Oui |
| **Source de données** | `stock_matiere`, `stock_outil` |
| **Utilisation ML** | ML-07: Prévision stock |

---

### INV-012 — Emplacement Stock

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-012 |
| **Nom** | Emplacement physique du stock |
| **Module** | Inventaire |
| **Question métier** | Où se trouve le stock ? |
| **Inputs requis** | Article |
| **Information retournée** | Code emplacement |
| **Formule** | `stock_*.emplacement` |
| **Visualisation** | Carte |
| **Interprétation** | Localisation |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `stock_*.emplacement` |
| **Utilisation ML** | — |

---

### INV-013 — Dernière Mise à Jour Stock

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-013 |
| **Nom** | Date de dernière mise à jour du stock |
| **Module** | Inventaire |
| **Question métier** | Le stock est-il à jour ? |
| **Inputs requis** | Article |
| **Information retournée** | Date de dernière mise à jour |
| **Formule** | `stock_*.date_derniere_maj` |
| **Visualisation** | Carte |
| **Interprétation** | Fraîcheur des données |
| **Seuil vert** | < 24h |
| **Seuil orange** | 24h — 7 jours |
| **Seuil rouge** | > 7 jours |
| **Configurable** | Oui |
| **Source de données** | `stock_*.date_derniere_maj` |
| **Utilisation ML** | — |

---

### INV-014 — Coût Matière par Pièce

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-014 |
| **Nom** | Coût matière par pièce finie |
| **Module** | Inventaire |
| **Question métier** | Combien coûte la matière pour une pièce ? |
| **Inputs requis** | Pièce |
| **Information retournée** | Coût en EUR |
| **Formule** | `piece.poids × matiere.prix_kg` |
| **Visualisation** | Carte |
| **Interprétation** | Coût matière unitaire |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `piece.poids`, `matiere.prix_kg` |
| **Utilisation ML** | — |

---

### INV-015 — Taux de Rotation Stock

| Champ | Valeur |
|-------|--------|
| **KPI ID** | INV-015 |
| **Nom** | Taux de rotation des stocks |
| **Module** | Inventaire |
| **Question métier** | Le stock tourne-t-il suffisamment ? |
| **Inputs requis** | Article, Période |
| **Information retournée** | Nombre de rotations |
| **Formule** | `Consommation totale / Stock moyen` |
| **Visualisation** | Carte |
| **Interprétation** | Efficacité de gestion stock |
| **Seuil vert** | ≥ 6 fois/an |
| **Seuil orange** | 3 — 6 fois/an |
| **Seuil rouge** | < 3 fois/an |
| **Configurable** | Oui |
| **Source de données** | `stock_matiere`, `execution_phase` (consommation) |
| **Utilisation ML** | — |

---

## Module 6 — Outil

---

### TL-001 — Pourcentage d'Usure

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-001 |
| **Nom** | Pourcentage d'usure de l'outil |
| **Module** | Outil |
| **Question métier** | À quel point l'outil est-il usé ? |
| **Inputs requis** | Outil |
| **Information retournée** | Pourcentage d'usure |
| **Formule** | `usure_actuelle / duree_vie_totale × 100` |
| **Visualisation** | Jauge |
| **Interprétation** | Usure |
| **Seuil vert** | < 50% |
| **Seuil orange** | 50% — 80% |
| **Seuil rouge** | > 80% |
| **Configurable** | Oui |
| **Source de données** | `outil.usure_actuelle`, `outil.duree_vie_totale` |
| **Utilisation ML** | ML-05: Prédiction usure |

---

### TL-002 — Durée de Vie Restante

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-002 |
| **Nom** | Durée de vie restante de l'outil |
| **Module** | Outil |
| **Question métier** | Combien de temps l'outil va-t-il durer ? |
| **Inputs requis** | Outil |
| **Information retournée** | Minutes restantes |
| **Formule** | `outil.duree_vie_restante` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Vie restante |
| **Seuil vert** | > 50% de la vie totale |
| **Seuil orange** | 20% — 50% |
| **Seuil rouge** | < 20% |
| **Configurable** | Oui |
| **Source de données** | `outil.duree_vie_restante`, `outil.duree_vie_totale` |
| **Utilisation ML** | ML-05: Prédiction usure |

---

### TL-003 — Nombre d'Exécutions

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-003 |
| **Nom** | Nombre d'utilisations de l'outil |
| **Module** | Outil |
| **Question métier** | Combien de fois cet outil a-t-il été utilisé ? |
| **Inputs requis** | Outil |
| **Information retournée** | Nombre d'exécutions |
| **Formule** | `COUNT(execution_outil WHERE outil_id = X)` |
| **Visualisation** | Carte |
| **Interprétation** | Utilisation |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `execution_outil` |
| **Utilisation ML** | — |

---

### TL-004 — Coût par Exécution

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-004 |
| **Nom** | Coût unitaire par utilisation |
| **Module** | Outil |
| **Question métier** | Combien coûte chaque utilisation de cet outil ? |
| **Inputs requis** | Outil |
| **Information retournée** | Coût en EUR |
| **Formule** | `cout_achat / nombre_exécutions` |
| **Visualisation** | Carte |
| **Interprétation** | Coût unitaire |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `outil.cout_achat`, `execution_outil` |
| **Utilisation ML** | — |

---

### TL-005 — Indicateur de Remplacement

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-005 |
| **Nom** | Indicateur de remplacement |
| **Module** | Outil |
| **Question métier** | Dois-je remplacer cet outil ? |
| **Inputs requis** | Outil |
| **Information retournée** | OK / WARNING / CRITICAL |
| **Formule** | `Si usure > 80% → CRITICAL; Si usure > 60% → WARNING; Sinon → OK` |
| **Visualisation** | Carte avec indicateur coloré |
| **Interprétation** | Nécessité de remplacement |
| **Seuil vert** | OK |
| **Seuil orange** | WARNING |
| **Seuil rouge** | CRITICAL |
| **Configurable** | Oui |
| **Source de données** | `outil.usure_actuelle`, `outil.duree_vie_totale` |
| **Utilisation ML** | ML-05: Prédiction usure |

---

### TL-006 — Machine Actuelle

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-006 |
| **Nom** | Machine où l'outil est utilisé |
| **Module** | Outil |
| **Question métier** | Sur quelle machine cet outil est-il monté ? |
| **Inputs requis** | Outil |
| **Information retournée** | Code machine |
| **Formule** | `SELECT machine.code FROM machine JOIN execution_phase JOIN execution_outil WHERE outil_id = X AND statut = 'EN_COURS'` |
| **Visualisation** | Carte |
| **Interprétation** | Affectation |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `machine`, `execution_phase`, `execution_outil` |
| **Utilisation ML** | — |

---

### TL-007 — Usure par Exécution

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-007 |
| **Nom** | Usure moyenne par exécution |
| **Module** | Outil |
| **Question métier** | Combien l'out-il s'use-t-il à chaque utilisation ? |
| **Inputs requis** | Outil |
| **Information retournée** | Minutes d'usure par exécution |
| **Formule** | `AVG(usure_fin - usure_debut)` |
| **Visualisation** | Courbe |
| **Interprétation** | Taux d'usure |
| **Seuil vert** | Faible |
| **Seuil orange** | — |
| **Seuil rouge** | Élevé |
| **Configurable** | Oui |
| **Source de données** | `execution_outil.usure_debut`, `execution_outil.usure_fin` |
| **Utilisation ML** | ML-05: Prédiction usure |

---

### TL-008 — Coût d'Achat

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-008 |
| **Nom** | Coût d'achat de l'outil |
| **Module** | Outil |
| **Question métier** | Combien coûte cet outil ? |
| **Inputs requis** | Outil |
| **Information retournée** | Coût en EUR |
| **Formule** | `outil.cout_achat` |
| **Visualisation** | Carte |
| **Interprétation** | Investissement |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `outil.cout_achat` |
| **Utilisation ML** | — |

---

### TL-009 — Coût de Remplacement

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-009 |
| **Nom** | Coût de remplacement de l'outil |
| **Module** | Outil |
| **Question métier** | Combien coûtera le remplacement ? |
| **Inputs requis** | Outil |
| **Information retournée** | Coût en EUR |
| **Formule** | `outil.cout_remplacement` |
| **Visualisation** | Carte |
| **Interprétation** | Coût de remplacement |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `outil.cout_remplacement` |
| **Utilisation ML** | — |

---

### TL-010 — Indicateur Disponibilité

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-010 |
| **Nom** | Disponibilité de l'outil |
| **Module** | Outil |
| **Question métier** | L'outil est-il disponible ? |
| **Inputs requis** | Outil |
| **Information retournée** | Disponible / Indisponible |
| **Formule** | `outil.disponible` |
| **Visualisation** | Carte avec indicateur |
| **Interprétation** | Disponibilité |
| **Seuil vert** | Disponible |
| **Seuil rouge** | Indisponible |
| **Configurable** | Non |
| **Source de données** | `outil.disponible` |
| **Utilisation ML** | — |

---

### TL-011 — Type d'Outil

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-011 |
| **Nom** | Type d'outil |
| **Module** | Outil |
| **Question métier** | Quel type d'outil est-ce ? |
| **Inputs requis** | Outil |
| **Information retournée** | Type (Foret, Fraise, Taraud, etc.) |
| **Formule** | `outil.type_outil` |
| **Visualisation** | Carte |
| **Interprétation** | Catégorie |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `outil.type_outil` |
| **Utilisation ML** | — |

---

### TL-012 — Diamètre

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-012 |
| **Nom** | Diamètre de l'outil |
| **Module** | Outil |
| **Question métier** | Quel est le diamètre ? |
| **Inputs requis** | Outil |
| **Information retournée** | Diamètre en mm |
| **Formule** | `outil.diametre` |
| **Visualisation** | Carte |
| **Interprétation** | Spécification |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `outil.diametre` |
| **Utilisation ML** | — |

---

### TL-013 — Dernière Utilisation

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-013 |
| **Nom** | Date de dernière utilisation |
| **Module** | Outil |
| **Question métier** | Quand l'outil a-t-il été utilisé pour la dernière fois ? |
| **Inputs requis** | Outil |
| **Information retournée** | Date |
| **Formule** | `MAX(execution_outil.created_at)` |
| **Visualisation** | Carte |
| **Interprétation** | Fraîcheur d'utilisation |
| **Seuil vert** | < 30 jours |
| **Seuil orange** | 30 — 90 jours |
| **Seuil rouge** | > 90 jours |
| **Configurable** | Oui |
| **Source de données** | `execution_outil` |
| **Utilisation ML** | — |

---

### TL-014 — Historique des Usures

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-014 |
| **Nom** | Courbe d'usure dans le temps |
| **Module** | Outil |
| **Question métier** | Comment l'usure évolue-t-elle ? |
| **Inputs requis** | Outil |
| **Information retournée** | Usure fin par exécution |
| **Formule** | `usure_fin GROUP BY date` |
| **Visualisation** | Courbe |
| **Interprétation** | Tendance d'usure |
| **Seuil vert** | Linéaire |
| **Seuil orange** | Accéléré |
| **Seuil rouge** | Extrapolation critique |
| **Configurable** | Oui |
| **Source de données** | `execution_outil` |
| **Utilisation ML** | ML-05: Prédiction usure |

---

### TL-015 — Coût Cumulé d'Utilisation

| Champ | Valeur |
|-------|--------|
| **KPI ID** | TL-015 |
| **Nom** | Coût total d'utilisation de l'outil |
| **Module** | Outil |
| **Question métier** | Combien cet outil a-t-il coûté au total ? |
| **Inputs requis** | Outil |
| **Information retournée** | Coût cumulé |
| **Formule** | `cout_achat + (nombre_remplacements × cout_remplacement)` |
| **Visualisation** | Barres cumulées |
| **Interprétation** | Coût total de possession |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `outil` |
| **Utilisation ML** | — |

---

## Module 7 — Maintenance

---

### MNT-001 — MTBF

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-001 |
| **Nom** | Temps moyen entre pannes (MTBF) |
| **Module** | Maintenance |
| **Question métier** | Quel est le temps moyen entre les pannes ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | MTBF en heures |
| **Formule** | `Temps total de fonctionnement / Nombre de pannes (maintenance corrective)` |
| **Visualisation** | Carte |
| **Interprétation** | Fiabilité |
| **Seuil vert** | ≥ 200 heures |
| **Seuil orange** | 100 — 200 heures |
| **Seuil rouge** | < 100 heures |
| **Configurable** | Oui |
| **Source de données** | `maintenance`, `sensor_data.statut_machine` |
| **Utilisation ML** | ML-03: Maintenance prédictive |

---

### MNT-002 — MTTR

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-002 |
| **Nom** | Temps moyen de réparation (MTTR) |
| **Module** | Maintenance |
| **Question métier** | Combien de temps faut-il pour réparer ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | MTTR en heures |
| **Formule** | `Somme des durées de réparation / Nombre de réparations` |
| **Visualisation** | Carte |
| **Interprétation** | Réparabilité |
| **Seuil vert** | ≤ 2 heures |
| **Seuil orange** | 2 — 4 heures |
| **Seuil rouge** | > 4 heures |
| **Configurable** | Oui |
| **Source de données** | `maintenance.duree` |
| **Utilisation ML** | — |

---

### MNT-003 — Disponibilité Maintenance

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-003 |
| **Nom** | Disponibilité (basée sur MTBF/MTTR) |
| **Module** | Maintenance |
| **Question métier** | La machine est-elle disponible ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Pourcentage de disponibilité |
| **Formule** | `MTBF / (MTBF + MTTR) × 100` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | Capacité opérationnelle |
| **Seuil vert** | ≥ 95% |
| **Seuil orange** | 90% — 95% |
| **Seuil rouge** | < 90% |
| **Configurable** | Oui |
| **Source de données** | MNT-001, MNT-002 |
| **Utilisation ML** | — |

---

### MNT-004 — Nombre d'Interventions

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-004 |
| **Nom** | Nombre total d'interventions |
| **Module** | Maintenance |
| **Question métier** | Combien d'interventions de maintenance ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Nombre d'interventions |
| **Formule** | `COUNT(maintenance)` |
| **Visualisation** | Carte |
| **Interprétation** | Activité maintenance |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `maintenance` |
| **Utilisation ML** | — |

---

### MNT-005 — Coût Total Maintenance

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-005 |
| **Nom** | Coût total de maintenance |
| **Module** | Maintenance |
| **Question métier** | Combien coûte la maintenance ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Somme des coûts |
| **Formule** | `SUM(maintenance.cout)` |
| **Visualisation** | Carte |
| **Interprétation** | Budget consommé |
| **Seuil vert** | ≤ Budget |
| **Seuil orange** | 100% — 120% Budget |
| **Seuil rouge** | > 120% Budget |
| **Configurable** | Oui |
| **Source de données** | `maintenance.cout` |
| **Utilisation ML** | ML-03: Coût maintenance prévu |

---

### MNT-006 — Coût Moyen par Intervention

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-006 |
| **Nom** | Coût moyen par intervention |
| **Module** | Maintenance |
| **Question métier** | Combien coûte en moyenne une intervention ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Coût moyen |
| **Formule** | `SUM(cout) / COUNT(maintenance)` |
| **Visualisation** | Carte |
| **Interprétation** | Coût unitaire |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `maintenance` |
| **Utilisation ML** | — |

---

### MNT-007 — Durée Totale d'Arrêt

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-007 |
| **Nom** | Durée totale d'arrêt pour maintenance |
| **Module** | Maintenance |
| **Question métier** | Combien de temps la machine a-t-elle été à l'arrêt ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Durée totale en heures |
| **Formule** | `SUM(maintenance.duree) / 60` |
| **Visualisation** | Carte |
| **Interprétation** | Temps perdu |
| **Seuil vert** | ≤ 5% du temps total |
| **Seuil orange** | 5% — 10% |
| **Seuil rouge** | > 10% |
| **Configurable** | Oui |
| **Source de données** | `maintenance.duree` |
| **Utilisation ML** | — |

---

### MNT-008 — Ratio Préventif/Correctif

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-008 |
| **Nom** | Ratio maintenance préventive / corrective |
| **Module** | Maintenance |
| **Question métier** | Quel est le ratio préventif vs correctif ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Ratio |
| **Formule** | `COUNT(Préventive) / COUNT(Corrective)` |
| **Visualisation** | Camembert |
| **Interprétation** | Stratégie maintenance |
| **Seuil vert** | ≥ 3:1 |
| **Seuil orange** | 1:1 — 3:1 |
| **Seuil rouge** | < 1:1 |
| **Configurable** | Oui |
| **Source de données** | `maintenance.type_maintenance` |
| **Utilisation ML** | — |

---

### MNT-009 — Répartition par Type

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-009 |
| **Nom** | Répartition des interventions par type |
| **Module** | Maintenance |
| **Question métier** | Quels types de maintenance dominent ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Nombre par type |
| **Formule** | `COUNT(maintenance) GROUP BY type_maintenance` |
| **Visualisation** | Camembert |
| **Interprétation** | Profil maintenance |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `maintenance.type_maintenance` |
| **Utilisation ML** | — |

---

### MNT-010 — Coût par Type

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-010 |
| **Nom** | Coût par type de maintenance |
| **Module** | Maintenance |
| **Question métier** | Quel type de maintenance coûte le plus ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Coût par type |
| **Formule** | `SUM(cout) GROUP BY type_maintenance` |
| **Visualisation** | Barres |
| **Interprétation** | Distribution des coûts |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `maintenance` |
| **Utilisation ML** | — |

---

### MNT-011 — Coût Cumulé

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-011 |
| **Nom** | Coût cumulé de maintenance |
| **Module** | Maintenance |
| **Question métier** | Combien le budget maintenance a-t-il consommé ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Coût cumulé mensuel |
| **Formule** | `SUM(cout) cumulé par mois` |
| **Visualisation** | Courbe |
| **Interprétation** | Consommation budget |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `maintenance` |
| **Utilisation ML** | ML-03: Coût prévu |

---

### MNT-012 — Dernière Maintenance

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-012 |
| **Nom** | Date de la dernière intervention |
| **Module** | Maintenance |
| **Question métier** | Quand a eu lieu la dernière maintenance ? |
| **Inputs requis** | Machine |
| **Information retournée** | Date |
| **Formule** | `MAX(maintenance.date_debut)` |
| **Visualisation** | Carte |
| **Interprétation** | Fraîcheur maintenance |
| **Seuil vert** | < 30 jours |
| **Seuil orange** | 30 — 90 jours |
| **Seuil rouge** | > 90 jours |
| **Configurable** | Oui |
| **Source de données** | `maintenance.date_debut` |
| **Utilisation ML** | ML-03: Prédiction maintenance |

---

### MNT-013 — Fréquence Maintenance

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-013 |
| **Nom** | Fréquence des interventions (par mois) |
| **Module** | Maintenance |
| **Question métier** | Combien de fois par mois la machine est-elle maintenue ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Nombre d'interventions par mois |
| **Formule** | `COUNT(maintenance) / Nombre de mois` |
| **Visualisation** | Barres |
| **Interprétation** | Fréquence |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `maintenance` |
| **Utilisation ML** | — |

---

### MNT-014 — Durée Moyenne d'Intervention

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-014 |
| **Nom** | Durée moyenne d'intervention |
| **Module** | Maintenance |
| **Question métier** | Combien de temps dure une intervention ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Durée moyenne en minutes |
| **Formule** | `AVG(maintenance.duree)` |
| **Visualisation** | Carte |
| **Interprétation** | Efficacité maintenance |
| **Seuil vert** | ≤ 60 min |
| **Seuil orange** | 60 — 120 min |
| **Seuil rouge** | > 120 min |
| **Configurable** | Oui |
| **Source de données** | `maintenance.duree` |
| **Utilisation ML** | — |

---

### MNT-015 — Historique Maintenance

| Champ | Valeur |
|-------|--------|
| **KPI ID** | MNT-015 |
| **Nom** | Historique des interventions |
| **Module** | Maintenance |
| **Question métier** | Quel est l'historique complet ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Liste chronologique des interventions |
| **Formule** | `SELECT * FROM maintenance WHERE machine_id = X ORDER BY date_debut DESC` |
| **Visualisation** | Tableau + frise |
| **Interprétation** | Historique |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `maintenance` |
| **Utilisation ML** | — |

---

## Module 8 — Capteurs

---

### SEN-001 — Température Actuelle

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-001 |
| **Nom** | Dernière lecture de température |
| **Module** | Capteurs |
| **Question métier** | Quelle est la température actuelle ? |
| **Inputs requis** | Machine |
| **Information retournée** | Température en °C |
| **Formule** | `DERNIERE(sensor_data.temperature)` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | État thermique |
| **Seuil vert** | < 60°C |
| **Seuil orange** | 60°C — 80°C |
| **Seuil rouge** | > 80°C |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.temperature` |
| **Utilisation ML** | ML-04: Prédiction panne |

---

### SEN-002 — Température Moyenne

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-002 |
| **Nom** | Température moyenne |
| **Module** | Capteurs |
| **Question métier** | Quelle est la température moyenne ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Moyenne en °C |
| **Formule** | `AVG(sensor_data.temperature)` |
| **Visualisation** | Carte |
| **Interprétation** | Tendance thermique |
| **Seuil vert** | < 60°C |
| **Seuil orange** | 60°C — 80°C |
| **Seuil rouge** | > 80°C |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.temperature` |
| **Utilisation ML** | ML-04: Prédiction panne |

---

### SEN-003 — Température Max

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-003 |
| **Nom** | Température maximale |
| **Module** | Capteurs |
| **Question métier** | Quelle est la température maximale atteinte ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Max en °C |
| **Formule** | `MAX(sensor_data.temperature)` |
| **Visualisation** | Carte |
| **Interprétation** | Pic de température |
| **Seuil vert** | < 70°C |
| **Seuil orange** | 70°C — 80°C |
| **Seuil rouge** | > 80°C |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.temperature` |
| **Utilisation ML** | ML-04: Prédiction panne |

---

### SEN-004 — Vibration Actuelle

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-004 |
| **Nom** | Dernière lecture de vibration |
| **Module** | Capteurs |
| **Question métier** | Quelle est la vibration actuelle ? |
| **Inputs requis** | Machine |
| **Information retournée** | Vibration en mm/s |
| **Formule** | `DERNIERE(sensor_data.vibration)` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | État mécanique |
| **Seuil vert** | < 2.5 mm/s |
| **Seuil orange** | 2.5 — 4.5 mm/s |
| **Seuil rouge** | > 4.5 mm/s |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.vibration` |
| **Utilisation ML** | ML-04: Prédiction panne |

---

### SEN-005 — Vibration Moyenne

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-005 |
| **Nom** | Vibration moyenne |
| **Module** | Capteurs |
| **Question métier** | Quelle est la vibration moyenne ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Moyenne en mm/s |
| **Formule** | `AVG(sensor_data.vibration)` |
| **Visualisation** | Carte |
| **Interprétation** | Tendance vibration |
| **Seuil vert** | < 2.5 mm/s |
| **Seuil orange** | 2.5 — 4.5 mm/s |
| **Seuil rouge** | > 4.5 mm/s |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.vibration` |
| **Utilisation ML** | ML-04: Prédiction panne |

---

### SEN-006 — Vibration Max

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-006 |
| **Nom** | Vibration maximale |
| **Module** | Capteurs |
| **Question métier** | Quelle est la vibration maximale atteinte ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Max en mm/s |
| **Formule** | `MAX(sensor_data.vibration)` |
| **Visualisation** | Carte |
| **Interprétation** | Pic de vibration |
| **Seuil vert** | < 3.5 mm/s |
| **Seuil orange** | 3.5 — 4.5 mm/s |
| **Seuil rouge** | > 4.5 mm/s |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.vibration` |
| **Utilisation ML** | ML-04: Prédiction panne |

---

### SEN-007 — RPM Moyen

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-007 |
| **Nom** | RPM moyen de la broche |
| **Module** | Capteurs |
| **Question métier** | La broche tourne-t-elle correctement ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | RPM moyen |
| **Formule** | `AVG(sensor_data.rpm)` |
| **Visualisation** | Carte + courbe |
| **Interprétation** | Vitesse broche |
| **Seuil vert** | Dans la plage prévue |
| **Seuil orange** | Légère déviation |
| **Seuil rouge** | Déviation majeure |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.rpm` |
| **Utilisation ML** | — |

---

### SEN-008 — Charge Broche Moyenne

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-008 |
| **Nom** | Charge moyenne de la broche |
| **Module** | Capteurs |
| **Question métier** | La broche est-elle surchargée ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Charge en % |
| **Formule** | `AVG(sensor_data.charge_frappe)` |
| **Visualisation** | Carte + courbe |
| **Interprétation** | Charge mécanique |
| **Seuil vert** | < 80% |
| **Seuil orange** | 80% — 95% |
| **Seuil rouge** | > 95% |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.charge_frappe` |
| **Utilisation ML** | — |

---

### SEN-009 — Puissance Moyenne

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-009 |
| **Nom** | Puissance électrique moyenne |
| **Module** | Capteurs |
| **Question métier** | La consommation est-elle normale ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Puissance en kW |
| **Formule** | `AVG(sensor_data.puissance)` |
| **Visualisation** | Carte + courbe |
| **Interprétation** | Consommation énergétique |
| **Seuil vert** | Dans la plage normale |
| **Seuil orange** | Légère augmentation |
| **Seuil rouge** | Consommation anormale |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.puissance` |
| **Utilisation ML** | — |

---

### SEN-010 — Temps de Cycle Moyen

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-010 |
| **Nom** | Temps de cycle moyen |
| **Module** | Capteurs |
| **Question métier** | Le temps de cycle est-il stable ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Temps en secondes |
| **Formule** | `AVG(sensor_data.temps_cycle)` |
| **Visualisation** | Carte + courbe |
| **Interprétation** | Stabilité du cycle |
| **Seuil vert** | Stable (écart faible) |
| **Seuil orange** | Variable |
| **Seuil rouge** | Très variable |
| **Configurable** | Oui |
| **Source de données** | `sensor_data.temps_cycle` |
| **Utilisation ML** | — |

---

### SEN-011 — Score d'Anomalie

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-011 |
| **Nom** | Score d'anomalie composite |
| **Module** | Capteurs |
| **Question métier** | Y a-t-il des anomalies détectées ? |
| **Inputs requis** | Machine |
| **Information retournée** | Score de 0 à 100 |
| **Formule** | `Calcul basé sur l'écart de température, vibration, puissance par rapport aux seuils historiques` |
| **Visualisation** | Carte + jauge |
| **Interprétation** | État de santé |
| **Seuil vert** | < 30 |
| **Seuil orange** | 30 — 60 |
| **Seuil rouge** | > 60 |
| **Configurable** | Oui |
| **Source de données** | `sensor_data` (calculé) |
| **Utilisation ML** | ML-04: Détection anomalie |

---

### SEN-012 — Nombre d'Alertes Capteurs

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-012 |
| **Nom** | Nombre de dépassements de seuil |
| **Module** | Capteurs |
| **Question métier** | Combien d'alertes capteurs aujourd'hui ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Nombre d'alertes |
| **Formule** | `COUNT(readings WHERE temperature > seuil OR vibration > seuil)` |
| **Visualisation** | Carte |
| **Interprétation** | Anomalies détectées |
| **Seuil vert** | 0 |
| **Seuil orange** | 1 — 5 |
| **Seuil rouge** | > 5 |
| **Configurable** | Oui |
| **Source de données** | `sensor_data` (calculé) |
| **Utilisation ML** | ML-04: Détection anomalie |

---

### SEN-013 — Statut Machine (Capteurs)

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-013 |
| **Nom** | Statut machine basé sur les capteurs |
| **Module** | Capteurs |
| **Question métier** | La machine est-elle en marche ? |
| **Inputs requis** | Machine |
| **Information retournée** | RUNNING / STOPPED / MAINTENANCE / BROKEN |
| **Formule** | `DERNIERE(sensor_data.statut_machine)` |
| **Visualisation** | Carte avec indicateur |
| **Interprétation** | État opérationnel |
| **Seuil vert** | RUNNING |
| **Seuil orange** | STOPPED, MAINTENANCE |
| **Seuil rouge** | BROKEN |
| **Configurable** | Non |
| **Source de données** | `sensor_data.statut_machine` |
| **Utilisation ML** | ML-04: Prédiction panne |

---

### SEN-014 — Courbe Température

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-014 |
| **Nom** | Évolution temporelle de la température |
| **Module** | Capteurs |
| **Question métier** | Comment la température évolue-t-elle ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Série temporelle |
| **Formule** | `temperature GROUP BY timestamp` |
| **Visualisation** | Courbe avec seuils |
| **Interprétation** | Tendance |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `sensor_data` |
| **Utilisation ML** | ML-04: Tendance |

---

### SEN-015 — Courbe Vibration

| Champ | Valeur |
|-------|--------|
| **KPI ID** | SEN-015 |
| **Nom** | Évolution temporelle de la vibration |
| **Module** | Capteurs |
| **Question métier** | Comment la vibration évolue-t-elle ? |
| **Inputs requis** | Machine, Période |
| **Information retournée** | Série temporelle |
| **Formule** | `vibration GROUP BY timestamp` |
| **Visualisation** | Courbe avec seuils |
| **Interprétation** | Tendance mécanique |
| **Seuil vert** | — |
| **Seuil orange** | — |
| **Seuil rouge** | — |
| **Configurable** | Non (informatif) |
| **Source de données** | `sensor_data` |
| **Utilisation ML** | ML-04: Tendance |

---

## Résumé par module

| Module | Code | Nombre de KPI |
|--------|------|---------------|
| Vue Exécutive | EXEC | 15 |
| Machine | MCH | 20 |
| Ordre de Fabrication | OF | 15 |
| Qualité | QUA | 20 |
| Inventaire | INV | 15 |
| Outil | TL | 15 |
| Maintenance | MNT | 15 |
| Capteurs | SEN | 15 |
| **Total** | — | **130** |

---

**Document validé par :** ________________ (Ingénieur AMM)
**Date :** ________________
**Signature :** ________________
