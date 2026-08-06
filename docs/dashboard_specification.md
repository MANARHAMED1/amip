# AMIP — Spécification du Dashboard de Décision Industrielle

**Version:** 1.0
**Date:** 2026-07-15
**Statut:** Spécification métier — En attente de validation par l'ingénieur AMM
**Portée:** Système de support à la décision pour l'atelier d'usinage CNC

---

## Table des matières

1. [Vue d'ensemble du système](#1-vue-densemble-du-système)
2. [Navigation globale et filtres](#2-navigation-globale-et-filtres)
3. [Module 1 — Vue Exécutive](#3-module-1--vue-exécutive)
4. [Module 2 — Machine](#4-module-2--machine)
5. [Module 3 — Ordre de Fabrication](#5-module-3--ordre-de-fabrication)
6. [Module 4 — Qualité](#6-module-4--qualité)
7. [Module 5 — Inventaire](#7-module-5--inventaire)
8. [Module 6 — Outil](#8-module-6--outil)
9. [Module 7 — Maintenance](#9-module-7--maintenance)
10. [Module 8 — Capteurs](#10-module-8--capteurs)
11. [Système d'alertes](#11-système-dalertes)
12. [Navigation inter-modules](#12-navigation-inter-modules)
13. [Prédictions Machine Learning](#13-prédictions-machine-learning)
14. [Roadmap de mise en œuvre](#14-roadmap-de-mise-en-œuvre)

---

## 1. Vue d'ensemble du système

### 1.1 Qu'est-ce qu'AMIP ?

AMIP (AMM Manufacturing Intelligence Platform) est une **plateforme intelligente de support à la décision** pour un atelier d'usinage CNC. Elle ne se limite pas à afficher des graphiques : elle analyse la base de données opérationnelle, calcule des KPI industriels, détecte des anomalies, et (dans une phase ultérieure) utilise le Machine Learning pour fournir des prédictions et des recommandations.

### 1.2 À qui s'adresse le dashboard ?

Le dashboard est destiné à :

| Rôle | Utilisation principale |
|------|----------------------|
| **Ingénieur AMM** | Superviser la production, analyser la qualité, prendre des décisions |
| **Chef d'atelier** | Suivre l'avancement des OFs, gérer les priorités |
| **Technicien maintenance** | Consulter l'historique, planifier les interventions |
| **Responsable qualité** | Analyser les rebuts, identifier les causes racines |
| **Responsable stock** | Surveiller les niveaux de stock, planifier les réapprovisionnements |

### 1.3 Comment l'ingénieur interagit avec le système

Le dashboard suit un workflow d'interaction :

```
L'ingénieur sélectionne une information
            ↓
Le système recherche dans la base de données opérationnelle
            ↓
Le système calcule les KPI
            ↓
Le système analyse les données historiques
            ↓
(dans une phase ultérieure) Les modèles ML font des prédictions
            ↓
Le dashboard retourne des réponses industrielles, alertes et recommandations
```

### 1.4 Flux de données

```
PostgreSQL (base opérationnelle)
    ↓ ETL
Data Warehouse (schéma en étoile)
    ↓ Requêtes
FastAPI (backend)
    ↓ JSON
Dashboard Streamlit (frontend)
    ↓ Affichage
Ingénieur AMM (décision)
```

### 1.5 Données disponibles

| Donnée | Volume | Période |
|--------|--------|---------|
| Machines | 12 machines CNC | — |
| Opérateurs | 50 opérateurs | — |
| Matières premières | 31 matières | — |
| Outils | 150 outils | — |
| Pièces | 300 pièces | — |
| Ordres de fabrication | 5 000 OFs | 2025-2026 |
| Phases exécutées | 25 000 exécutions | 2025-2026 |
| Contrôles qualité | 25 000 inspections | 2025-2026 |
| Maintenances | 3 000 interventions | 2025-2026 |
| Données capteurs | 1 000 000 relevés | 2025-2026 |

---

## 2. Navigation globale et filtres

### 2.1 Filtres globaux

Le dashboard dispose de filtres accessibles depuis tous les modules :

| Filtre | Type | Description |
|--------|------|-------------|
| **Période** | Sélecteur de dates | Date de début et date de fin |
| **Secteur** | Liste déroulante | Tournage, Fraisage, Usinage CNC, etc. |
| **Machine** | Multi-sélection | Filtrer par une ou plusieurs machines |
| **Statut** | Cases à cocher | RUNNING, STOPPED, MAINTENANCE, BROKEN |

### 2.2 Barre latérale d'alertes

Une barre latérale permanente affiche les alertes actives :

| Sévérité | Couleur | Exemple |
|----------|---------|---------|
| **Critique** | Rouge | Machine en panne, stock critique |
| **Avertissement** | Orange | OEE < 60%, vibration élevée |
| **Information** | Bleu | Maintenance planifiée, OF en retard |

### 2.3 Navigation entre modules

Le dashboard est organisé en **8 modules** accessibles par un menu horizontal ou latéral. Chaque module peut être atteint par :

- Le menu principal
- Un clic sur une donnée dans un autre module (navigation croisée)
- Une alerte cliquable

---

## 3. Module 1 — Vue Exécutive

### 3.1 Objectif métier

Donner à l'ingénieur AMM une **vision globale de l'atelier** en un coup d'œil. Répondre à la question : « Comment se porte mon atelier aujourd'hui ? »

### 3.2 Questions de l'ingénieur

- Quel est l'OEE global de l'atelier ?
- Combien de machines sont en fonctionnement ?
- Combien d'OFs sont en cours ?
- Y a-t-il des retards de production ?
- Quel est le taux de rebut global ?
- Quelles sont les alertes critiques ?
- Comment la production évolue-t-elle ce mois-ci ?

### 3.3 Inputs requis

| Input | Type | Obligatoire |
|-------|------|-------------|
| Période | Date début / date fin | Oui (défaut : mois en cours) |
| Secteur | Liste déroulante | Non (défaut : tous) |

### 3.4 Informations retournées

#### 3.4.1 KPIs en haut de page (Cartes)

| Carte | Description |
|-------|-------------|
| **OEE Global** | Moyenne pondérée de tous les OEE machines |
| **Production totale** | Nombre total de pièces produites |
| **Taux de rebut** | Pourcentage global de rebuts |
| **OFs actifs** | Nombre d'OFs en cours |
| **Machines disponibles** | Nombre de machines en état RUNNING |
| **Alertes critiques** | Nombre d'alertes de niveau critique |

#### 3.4.2 Grille de statut des machines

Affiche les 12 machines sous forme de cartes colorées :

| État | Couleur | Signification |
|------|---------|---------------|
| RUNNING | Vert | Machine en production |
| STOPPED | Gris | Machine arrêtée |
| MAINTENANCE | Orange | En intervention |
| BROKEN | Rouge | En panne |

Chaque carte machine affiche :
- Code machine (ex: M005)
- Nom (ex: Tour CNC Precision 3)
- Type (ex: Tour CNC)
- OF actuel (si applicable)
- OEE du jour

#### 3.4.3 Graphiques

| Graphique | Type | Description |
|-----------|------|-------------|
| Production vs Plan | Barres comparatives | Quantité produite vs demandée par jour |
| OEE par machine | Barres horizontales | OEE de chaque machine |
| Taux de rebut par famille | Camembert | Répartition des rebuts par famille de pièce |
| Tendance production | Courbe | Production quotidienne sur la période |
| Coûts de maintenance | Barres | Coûts par type de maintenance |

#### 3.4.4 Tableau des OFs actifs

| Colonne | Description |
|---------|-------------|
| Numéro OF | Référence OF |
| Pièce | Référence pièce |
| Quantité | Produite / Demandée |
| Statut | EN_COURS, TERMINE, etc. |
| Avancement | Pourcentage de complétion |
| Retard | Nombre de jours de retard (si applicable) |

---

## 4. Module 2 — Machine

### 4.1 Objectif métier

Fournir une **vision complète d'une machine CNC** : statut actuel, performance, capteurs, maintenance, outils. C'est le module le plus riche car il croise des données de sources multiples.

### 4.2 Questions de l'ingénieur

- Comment se porte la machine M005 ?
- Quel est son OEE aujourd'hui ?
- Quel OF est en cours sur cette machine ?
- Quel opérateur la pilote ?
- Quel outil est utilisé ?
- Les capteurs sont-ils normaux ?
- Quand a eu lieu la dernière maintenance ?
- Quel est le coût de maintenance ?
- La machine risque-t-elle de tomber en panne ?

### 4.3 Inputs requis

| Input | Type | Obligatoire |
|-------|------|-------------|
| Machine | Sélection unique (M001-M012) | Oui |
| Période | Date début / date fin | Non (défaut : aujourd'hui) |

### 4.4 Informations retournées

#### 4.4.1 Section Statut

| Information | Source | Description |
|-------------|--------|-------------|
| Statut actuel | `machine.statut` | RUNNING / STOPPED / MAINTENANCE / BROKEN |
| OF actuel | `execution_phase` | Numéro OF en cours |
| Opérateur | `operateur` | Nom et prénom |
| Outil actuel | `execution_outil` | Code et type d'outil |
| Programme CNC | `programme_usinage` | Code programme |
| Date installation | `machine.date_installation` | Depuis combien de temps en service |

#### 4.4.2 Section Performance

| Information | Source | Description |
|-------------|--------|-------------|
| Temps d'usinage prévu | `phase_gamme.temps_usinage_prevu` | Somme des temps prévus |
| Temps d'usinage réel | `execution_phase.temps_usinage_reel` | Somme des temps réels |
| Temps de réglage prévu | `phase_gamme.temps_reglage_prevu` | Somme des temps de réglage prévus |
| Temps de réglage réel | `execution_phase.temps_reglage_reel` | Somme des temps de réglage réels |
| Disponibilité | Calculé | Temps utile / Temps total |
| Performance | Calculé | (Taux × Nombre pièces) / Temps utile |
| Qualité | Calculé | (Pièces bonnes / Pièces totales) |
| OEE | Calculé | Disponibilité × Performance × Qualité |
| Ecart temps | Calculé | Temps réel - Temps prévu |

#### 4.4.3 Section Capteurs

| Information | Source | Description |
|-------------|--------|-------------|
| Température actuelle | `sensor_data.temperature` | Dernière lecture |
| Vibration actuelle | `sensor_data.vibration` | Dernière lecture |
| RPM | `sensor_data.rpm` | Dernière lecture |
| Charge broche | `sensor_data.charge_frappe` | Dernière lecture |
| Puissance | `sensor_data.puissance` | Dernière lecture |
| Vitesse d'avance | `sensor_data.vitesse_avance` | Dernière lecture |
| Temps de cycle | `sensor_data.temps_cycle` | Dernière lecture |
| Score d'anomalie | Calculé | Basé sur les seuils |

#### 4.4.4 Section Maintenance

| Information | Source | Description |
|-------------|--------|-------------|
| Dernière maintenance | `maintenance.date_debut` | Date de la dernière intervention |
| Type dernière maintenance | `maintenance.type_maintenance` | Préventive / Corrective |
| MTBF | Calculé | Temps moyen entre pannes |
| MTTR | Calculé | Temps moyen de réparation |
| Coût maintenance total | `maintenance.cout` | Somme des coûts |
| Nombre d'interventions | `maintenance.maintenance_id` | Comptage |
| Prochaine maintenance | Planifié | Date prévue |

#### 4.4.5 Section Outils

| Information | Source | Description |
|-------------|--------|-------------|
| Outil actuel | `execution_outil` | Code, type, usure |
| Pourcentage d'usure | Calculé | usure_actuelle / duree_vie_totale |
| Durée de vie restante | `outil.duree_vie_restante` | En minutes |
| Indicateur de remplacement | Calculé | Si usure > 80% → WARNING |

#### 4.4.6 Graphiques

| Graphique | Type | Description |
|-----------|------|-------------|
| OEE historique | Courbe | OEE journalier sur la période |
| Température | Courbe | Évolution temporelle |
| Vibration | Courbe | Évolution temporelle |
| Coût maintenance | Barres | Coûts mensuels |
| Phases exécutées | Frise | Timeline des phases |

#### 4.4.7 Prédictions ML (Phase 4)

| Prédiction | Description |
|------------|-------------|
| Probabilité de panne | Chance de panne dans les 7 prochains jours |
| Durée de vie utile restante | Estimation du temps avant panne |
| Date de maintenance recommandée | Quand planifier la prochaine intervention |

---

## 5. Module 3 — Ordre de Fabrication

### 5.1 Objectif métier

Suivre l'**avancement d'un ordre de fabrication** du début à la fin. Répondre à la question : « Mon OF est-il en retard ? Combien reste-t-il ? »

### 5.2 Questions de l'ingénieur

- Comment avance l'OF-2025-001 ?
- Combien de pièces restent à produire ?
- Y a-t-il un retard ?
- Quelle machine est utilisée ?
- Quel opérateur travaille dessus ?
- Quel est le taux de rebut ?
- Les phases précédentes sont-elles terminées ?

### 5.3 Inputs requis

| Input | Type | Obligatoire |
|-------|------|-------------|
| Numéro OF | Sélection ou recherche | Oui |
| OU Pièce | Sélection pièce | Non |
| OU Période | Date début / date fin | Non |

### 5.4 Informations retournées

#### 5.4.1 Section Résumé OF

| Information | Source | Description |
|-------------|--------|-------------|
| Numéro OF | `ordre_fabrication.numero_of` | Référence |
| Pièce produite | `piece.reference` | Référence et désignation |
| Famille | `piece.famille` | Catégorie de pièce |
| Matière | `matiere.designation` | Matière première |
| Gamme | `gamme_usinage.code` | Code gamme |
| Priorité | `ordre_fabrication.priorite` | HAUTE / NORMALE / BASSE |
| Statut | `ordre_fabrication.statut` | EN_ATTENTE / EN_COURS / TERMINE / ANNULE |

#### 5.4.2 Section Quantités

| Information | Source | Description |
|-------------|--------|-------------|
| Quantité demandée | `ordre_fabrication.quantite_demandee` | Objectif |
| Quantité produite | `ordre_fabrication.quantite_produite` | Réalisé |
| Pièces bonnes | Calculé | Produite - Rebut |
| Pièces rebutées | `ordre_fabrication.quantite_rebut` | Perdues |
| Taux de rebut | Calculé | Rebut / Produite |
| Pourcentage avancement | Calculé | Produite / Demandée |

#### 5.4.3 Section Planning

| Information | Source | Description |
|-------------|--------|-------------|
| Date début prévue | `ordre_fabrication.date_debut_prevue` | Planifié |
| Date fin prévue | `ordre_fabrication.date_fin_prevue` | Planifié |
| Date début réelle | `ordre_fabrication.date_debut_reelle` | Effectif |
| Date fin réelle | `ordre_fabrication.date_fin_reelle` | Effectif |
| Durée prévue | Calculé | Fin prévue - Début prévu |
| Durée réelle | Calculé | Fin réelle - Début réelle |
| Retard | Calculé | Réelle - Prévue (en jours) |
| Statut retard | Logique | À l'heure / En retard / Terminé en avance |

#### 5.4.4 Section Exécution par phase

| Information | Source | Description |
|-------------|--------|-------------|
| Liste des phases | `phase_gamme` | Numéro, désignation |
| Machine par phase | `phase_gamme.machine_id` | Code machine |
| Outil par phase | `phase_gamme.outil_id` | Code outil |
| Temps prévu par phase | `phase_gamme.temps_usinage_prevu` | Minutes |
| Temps réel par phase | `execution_phase.temps_usinage_reel` | Minutes |
| Statut par phase | `execution_phase.statut` | EN_COURS / TERMINE / ARRET |
| Opérateur par phase | `execution_phase.operateur_id` | Nom |
| Pièces produites par phase | `execution_phase.nb_pieces_produites` | Nombre |
| Rebut par phase | `execution_phase.nb_pieces_rebut` | Nombre |

#### 5.4.5 Section Efficacité

| Information | Source | Description |
|-------------|--------|-------------|
| Efficacité globale | Calculé | Quantité produite / Quantité demandée |
| Efficacité temps | Calculé | Temps prévu / Temps réel |
| Efficacité par phase | Calculé | Temps prévu / Temps réel par phase |

#### 5.4.6 Graphiques

| Graphique | Type | Description |
|-----------|------|-------------|
| Avancement | Jauge | Pourcentage de complétion |
| Phases | Barres horizontales | Temps prévu vs réel par phase |
| Planning | Diagramme de Gantt simplifié | Frise des phases |
| Quantités | Barres comparatives | Demandée vs Produite vs Rebut |

---

## 6. Module 4 — Qualité

### 6.1 Objectif métier

Analyser la **qualité de production** : taux de conformité, causes de rebuts, évolution dans le temps. Répondre à la question : « Ma qualité est-elle sous contrôle ? »

### 6.2 Questions de l'ingénieur

- Quel est le taux de rebut de la pièce P025 ?
- Combien de pièces ont été rejetées ?
- Quelles sont les principales causes de défauts ?
- La qualité s'améliore-t-elle ou se dégrade-t-elle ?
- Quelle machine produit le plus de rebuts ?
- Quel opérateur a le meilleur taux de conformité ?
- Les dimensions sont-elles dans les tolérances ?

### 6.3 Inputs requis

| Input | Type | Obligatoire |
|-------|------|-------------|
| Pièce | Sélection pièce | Non |
| Machine | Sélection machine | Non |
| OF | Sélection OF | Non |
| Période | Date début / date fin | Oui (défaut : mois en cours) |

### 6.4 Informations retournées

#### 6.4.1 Section KPIs qualité (Cartes)

| Carte | Description |
|-------|-------------|
| **Nombre d'inspections** | Total des contrôles effectués |
| **Pièces conformes** | Nombre de pièces conformes |
| **Pièces non conformes** | Nombre de pièces rejetées |
| **Taux de conformité** | Conformes / Total inspections |
| **Taux de rebut** | Non conformes / Total produites |
| **FPY (First Pass Yield)** | Pièces conformes au premier contrôle |

#### 6.4.2 Section Analyse des causes

| Information | Source | Description |
|-------------|--------|-------------|
| Défauts par catégorie | `cause_rebut.categorie` | Materiel, Outil, Machine, Programmation, Operateur |
| Top causes | `cause_rebut.description` | Classement par fréquence |
| Pareto des causes | Calculé | 80/20 des causes |

#### 6.4.3 Section Défauts par dimension

| Information | Source | Description |
|-------------|--------|-------------|
| Dimension mesurée | `controle_qualite.dimension_mesuree` | Valeur |
| Dimension cible | `controle_qualite.dimension_cible` | Objectif |
| Tolérance + | `controle_qualite.tolerance_plus` | Limite haute |
| Tolérance - | `controle_qualite.tolerance_moins` | Limite basse |
| Écart | Calculé | Mesurée - Cible |
| Rugosité | `controle_qualite.rugosite_mesuree` | Ra |

#### 6.4.4 Section Analyse croisée

| Information | Source | Description |
|-------------|--------|-------------|
| Qualité par machine | `execution_phase.machine_id` | Taux de rebut par machine |
| Qualité par opérateur | `execution_phase.operateur_id` | Taux de rebut par opérateur |
| Qualité par outil | `execution_phase.outil_id` | Taux de rebut par outil |
| Qualité par matière | `matiere.type_matiere` | Taux de rebut par type de matière |

#### 6.4.5 Graphiques

| Graphique | Type | Description |
|-----------|------|-------------|
| Évolution du taux de rebut | Courbe | Taux journalier sur la période |
| Causes de défauts | Camembert | Répartition par catégorie |
| Pareto des causes | Barres + courbe | Top causes (80/20) |
| Qualité par machine | Barres horizontales | Comparaison machines |
| Qualité par opérateur | Barres horizontales | Comparaison opérateurs |
| Évolution dimension | Courbe + tolérances | Mesures vs cible avec bandes de tolérance |

---

## 7. Module 5 — Inventaire

### 7.1 Objectif métier

Surveiller les **niveaux de stock** de matières premières, d'outils et de pièces finies. Détecter les situations critiques et planifier les réapprovisionnements.

### 7.2 Questions de l'ingénieur

- Mon stock de matière X est-il suffisant ?
- Dois-je passer une commande de réapprovisionnement ?
- Combien de jours de stock me reste-t-il ?
- Quelle est la valeur de mon inventaire ?
- Quels articles sont en stock critique ?
- Quels outils doivent être remplacés ?

### 7.3 Inputs requis

| Input | Type | Obligatoire |
|-------|------|-------------|
| Type de stock | Matière / Outil / Pièce | Oui |
| Article | Sélection ou recherche | Non (défaut : tous les critiques) |
| Période | Date début / date fin | Non |

### 7.4 Informations retournées

#### 7.4.1 Section Vue d'ensemble des stocks

| Information | Source | Description |
|-------------|--------|-------------|
| Nombre d'articles critiques | `stock_matiere`, `stock_outil`, `stock_piece` | Stock ≤ seuil |
| Nombre d'articles en alerte | Calculé | Stock ≤ 1.5 × seuil |
| Nombre d'articles OK | Calculé | Stock > seuil |
| Valeur totale inventaire | Calculé | Quantité × Prix unitaire |

#### 7.4.2 Section Détail par article

| Information | Source | Description |
|-------------|--------|-------------|
| Stock actuel | `stock_*.quantite_stock` | Quantité en stock |
| Seuil d'alerte | `stock_*.seuil_alerte` | Limite basse |
| Seuil max (calculé) | Calculé | 2 × consommation moyenne |
| Statut stock | Logique | Critique / Bas / Normal / Surstock |
| Emplacement | `stock_*.emplacement` | Position physique |
| Dernière mise à jour | `stock_*.date_derniere_maj` | Horodatage |

#### 7.4.3 Section Matières premières

| Information | Source | Description |
|-------------|--------|-------------|
| Code matière | `matiere.code` | Référence |
| Désignation | `matiere.designation` | Nom |
| Type | `matiere.type_matiere` | Acier, Inox, Aluminium, etc. |
| Nuance | `matiere.nuance` | Nuance spécifique |
| Prix au kg | `matiere.prix_kg` | Coût unitaire |
| Stock en kg | `stock_matiere.quantite_stock` | Quantité |
| Seuil alerte | `stock_matiere.seuil_alerte` | Limite |

#### 7.4.4 Section Outils en stock

| Information | Source | Description |
|-------------|--------|-------------|
| Code outil | `outil.code` | Référence |
| Type outil | `outil.type_outil` | Foret, Fraise, etc. |
| Quantité en stock | `stock_outil.quantite_stock` | Nombre d'unités |
| Seuil alerte | `stock_outil.seuil_alerte` | Limite |
| Indicateur remplacement | Calculé | Si outil en usage usé > 80% |

#### 7.4.5 Section Pièces finies en stock

| Information | Source | Description |
|-------------|--------|-------------|
| Référence pièce | `piece.reference` | Code |
| Désignation | `piece.designation` | Nom |
| Famille | `piece.famille` | Catégorie |
| Quantité en stock | `stock_piece.quantite_stock` | Nombre |
| Prix de revient | `piece.prix_revient` | Coût unitaire |
| Valeur stock | Calculé | Quantité × Prix |

#### 7.4.6 Graphiques

| Graphique | Type | Description |
|-----------|------|-------------|
| Statut des stocks | Camembert | Répartition Critique / Bas / Normal / Surstock |
| Consommation matière | Courbe | Tendance de consommation |
| Top articles critiques | Barres | Articles les plus en alerte |
| Valeur inventaire | Camembert | Par catégorie |

---

## 8. Module 6 — Outil

### 8.1 Objectif métier

Suivre l'**état de chaque outil** : usure, durée de vie, exécutions, coût. Répondre à la question : « Dois-je remplacer cet outil ? »

### 8.2 Questions de l'ingénieur

- Quel est l'état d'usure de l'outil T014 ?
- Combien de temps reste-t-il ?
- Combien de fois a-t-il été utilisé ?
- Dois-je le remplacer ?
- Quel est le coût de cet outil ?
- Sur quelle machine est-il utilisé ?

### 8.3 Inputs requis

| Input | Type | Obligatoire |
|-------|------|-------------|
| Outil | Sélection ou recherche | Oui |
| OU Type d'outils | Filtre par type | Non |

### 8.4 Informations retournées

#### 8.4.1 Section KPIs outil (Cartes)

| Carte | Description |
|-------|-------------|
| **Pourcentage d'usure** | usure_actuelle / duree_vie_totale × 100 |
| **Durée de vie restante** | duree_vie_restante (en minutes) |
| **Nombre d'exécutions** | Comptage dans execution_outil |
| **Coût par exécution** | cout_achat / nombre_exécutions |
| **Indicateur remplacement** | Vert / Orange / Rouge |

#### 8.4.2 Section Détails outil

| Information | Source | Description |
|-------------|--------|-------------|
| Code | `outil.code` | Référence |
| Désignation | `outil.designation` | Nom |
| Type | `outil.type_outil` | Foret, Fraise, etc. |
| Diamètre | `outil.diametre` | En mm |
| Matière outil | `outil.matiere_outil` | HSS, Carbure, etc. |
| Durée de vie totale | `outil.duree_vie_totale` | Minutes |
| Usure actuelle | `outil.usure_actuelle` | Minutes utilisées |
| Durée de vie restante | `outil.duree_vie_restante` | Minutes restantes |
| Coût d'achat | `outil.cout_achat` | EUR |
| Coût de remplacement | `outil.cout_remplacement` | EUR |
| Disponible | `outil.disponible` | Oui / Non |

#### 8.4.3 Section Utilisation

| Information | Source | Description |
|-------------|--------|-------------|
| Machine actuelle | `execution_phase` | Machine où l'outil est utilisé |
| Dernière utilisation | `execution_outil` | Date dernière exécution |
| Usure début (dernière exécution) | `execution_outil.usure_debut` | Minutes |
| Usure fin (dernière exécution) | `execution_outil.usure_fin` | Minutes |
| Usure par exécution | Calculé | Fin - Début |
| Historique des usures | `execution_outil` | Courbe d'usure |

#### 8.4.4 Section Stock

| Information | Source | Description |
|-------------|--------|-------------|
| Quantité en stock | `stock_outil.quantite_stock` | Nombre |
| Seuil d'alerte | `stock_outil.seuil_alerte` | Limite |
| Emplacement | `stock_outil.emplacement` | Position |

#### 8.4.5 Graphiques

| Graphique | Type | Description |
|-----------|------|-------------|
| Usure | Jauge | Pourcentage d'usure |
| Historique usure | Courbe | Usure au fil des exécutions |
| Coût | Barres | Coût cumulé d'utilisation |

#### 8.4.6 Prédictions ML (Phase 4)

| Prédiction | Description |
|------------|-------------|
| Durée de vie utile restante | Estimation du temps avant usure critique |
| Date de remplacement recommandée | Quand remplacer l'outil |

---

## 9. Module 7 — Maintenance

### 9.1 Objectif métier

Gérer les **interventions de maintenance** : historique, coûts, temps d'arrêt, planification. Répondre à la question : « Comment gérer la maintenance de ma machine M003 ? »

### 9.2 Questions de l'ingénieur

- Quel est l'historique de maintenance de M003 ?
- Combien coûte la maintenance de cette machine ?
- Quel est le MTBF ?
- Quel est le MTTR ?
- Combien de temps la machine est-elle à l'arrêt ?
- Quelle est la fréquence des interventions ?
- Dois-je planifier une maintenance ?

### 9.3 Inputs requis

| Input | Type | Obligatoire |
|-------|------|-------------|
| Machine | Sélection machine | Oui |
| Période | Date début / date fin | Non (défaut : 12 derniers mois) |
| Type maintenance | Filtre | Non |

### 9.4 Informations retournées

#### 9.4.1 Section KPIs maintenance (Cartes)

| Carte | Description |
|-------|-------------|
| **MTBF** | Mean Time Between Failures (heures) |
| **MTTR** | Mean Time To Repair (heures) |
| **Disponibilité** | MTBF / (MTBF + MTTR) |
| **Nombre d'interventions** | Total sur la période |
| **Coût total maintenance** | Somme des coûts |
| **Coût moyen par intervention** | Coût total / Nombre |
| **Durée totale d'arrêt** | Somme des durées (heures) |

#### 9.4.2 Section Historique des interventions

| Colonne | Description |
|---------|-------------|
| Date début | `maintenance.date_debut` |
| Date fin | `maintenance.date_fin` |
| Type | `maintenance.type_maintenance` |
| Catégorie | Préventive / Corrective |
| Description | `maintenance.description` |
| Durée | `maintenance.duree` (minutes) |
| Coût | `maintenance.cout` (EUR) |
| Opérateur | `maintenance.operateur_id` |
| Statut | `maintenance.statut` |

#### 9.4.3 Section Analyse par type

| Information | Source | Description |
|-------------|--------|-------------|
| Préventif vs Correctif | `maintenance.type_maintenance` | Nombre et coût |
| Répartition par type | Calculé | 8 types de maintenance |
| Coût par type | Calculé | Somme des coûts par type |
| Durée par type | Calculé | Moyenne des durées par type |

#### 9.4.4 Section Calcul MTBF / MTTR

| KPI | Formule | Description |
|-----|---------|-------------|
| MTBF | Temps total de fonctionnement / Nombre de pannes | Temps moyen entre pannes |
| MTTR | Temps total de réparation / Nombre de pannes | Temps moyen de réparation |
| Disponibilité | MTBF / (MTBF + MTTR) × 100 | % de temps disponible |

#### 9.4.5 Graphiques

| Graphique | Type | Description |
|-----------|------|-------------|
| Historique maintenance | Frise | Timeline des interventions |
| Coûts mensuels | Barres | Coût par mois |
| Répartition par type | Camembert | Répartition des types |
| Coût cumulé | Courbe | Coût cumulé dans le temps |
| Fréquence | Barres | Nombre d'interventions par mois |

#### 9.4.6 Prédictions ML (Phase 4)

| Prédiction | Description |
|------------|-------------|
| Probabilité de panne | Chance de panne dans les N prochains jours |
| Date de maintenance recommandée | Quand planifier la prochaine intervention |
| Coût de maintenance prévu | Estimation du coût futur |

---

## 10. Module 8 — Capteurs

### 10.1 Objectif métier

Suivre les **données capteurs en temps réel** (ou quasi-réel) : température, vibration, RPM, puissance. Détecter les anomalies et alerter.

### 10.2 Questions de l'ingénieur

- Les valeurs de capteurs sont-elles normales ?
- La température est-elle excessive ?
- La vibration est-elle dans les limites ?
- Y a-t-il des anomalies détectées ?
- Comment les capteurs ont-ils évolué aujourd'hui ?

### 10.3 Inputs requis

| Input | Type | Obligatoire |
|-------|------|-------------|
| Machine | Sélection machine | Oui |
| Période | Date début / date fin | Non (défaut : aujourd'hui) |
| Capteur | Filtre capteur | Non (défaut : tous) |

### 10.4 Informations retournées

#### 10.4.1 Section KPIs capteurs (Cartes)

| Carte | Description |
|-------|-------------|
| **Température actuelle** | Dernière lecture (°C) |
| **Vibration actuelle** | Dernière lecture (mm/s) |
| **RPM actuel** | Dernière lecture |
| **Charge broche** | Dernière lecture (%) |
| **Puissance** | Dernière lecture (kW) |
| **Score d'anomalie** | Calculé (0-100) |
| **Niveau d'alerte** | Normal / Attention / Alerte |

#### 10.4.2 Section Détails des capteurs

| Information | Source | Description |
|-------------|--------|-------------|
| Température moyenne | `sensor_data.temperature` | Moyenne sur la période |
| Température max | `sensor_data.temperature` | Maximum sur la période |
| Température min | `sensor_data.temperature` | Minimum sur la période |
| Vibration moyenne | `sensor_data.vibration` | Moyenne sur la période |
| Vibration max | `sensor_data.vibration` | Maximum sur la période |
| RPM moyen | `sensor_data.rpm` | Moyenne sur la période |
| Charge moyenne | `sensor_data.charge_frappe` | Moyenne sur la période |
| Puissance moyenne | `sensor_data.puissance` | Moyenne sur la période |
| Temps de cycle moyen | `sensor_data.temps_cycle` | Moyenne sur la période |

#### 10.4.3 Section Détection d'anomalies

| Information | Source | Description |
|-------------|--------|-------------|
| Seuil température | Configurable | Vert < 60°C, Orange 60-80°C, Rouge > 80°C |
| Seuil vibration | Configurable | Vert < 2.5 mm/s, Orange 2.5-4.5, Rouge > 4.5 |
| Score d'anomalie | Calculé | Basé sur l'écart aux seuils |
| Nombre d'alertes | Calculé | Dépassements de seuil |

#### 10.4.4 Section État machine (basé sur capteurs)

| Information | Source | Description |
|-------------|--------|-------------|
| Statut machine | `sensor_data.statut_machine` | RUNNING / STOPPED / MAINTENANCE / BROKEN |
| Nombre de changements de statut | Calculé | Transitions dans la période |
| Temps d'arrêt détecté | Calculé | Périodes avec statut != RUNNING |

#### 10.4.5 Graphiques

| Graphique | Type | Description |
|-----------|------|-------------|
| Température | Courbe | Évolution temporelle avec seuils |
| Vibration | Courbe | Évolution temporelle avec seuils |
| RPM | Courbe | Évolution temporelle |
| Puissance | Courbe | Évolution temporelle |
| Charge broche | Courbe | Évolution temporelle |
| Heatmap capteurs | Heatmap | Valeurs par heure de la journée |
| Corrélation température/vibration | Scatter | Relation entre capteurs |

#### 10.4.6 Prédictions ML (Phase 4)

| Prédiction | Description |
|------------|-------------|
| Prédiction de panne machine | Basé sur les tendances capteurs |
| Détection d'anomalie | Score ML d'anomalie |
| Prédiction température | Tendance future |

---

## 11. Système d'alertes

### 11.1 Types d'alertes

| # | Alerte | Sévérité | Condition | Action recommandée |
|---|--------|----------|-----------|-------------------|
| A01 | Machine en panne | Critique | `machine.statut = 'BROKEN'` | Appeler le technicien maintenance |
| A02 | Stock matière critique | Critique | `stock.quantite_stock ≤ seuil_alerte` | Passer commande de réapprovisionnement |
| A03 | Stock outil critique | Critique | `stock_outil.quantite_stock ≤ seuil_alerte` | Commander nouvel outil |
| A04 | Vibrations excessives | Critique | `vibration > 4.5 mm/s` | Arrêter la machine, inspecter |
| A05 | Température excessive | Avertissement | `temperature > 80°C` | Vérifier le refroidissement |
| A06 | OEE bas | Avertissement | `OEE < 60%` | Analyser les causes |
| A07 | Taux de rebut élevé | Avertissement | `taux_rebut > 5%` | Vérifier qualité, outil, réglage |
| A08 | Outil usé | Avertissement | `usure > 80%` | Planifier remplacement outil |
| A09 | OF en retard | Information | `date_fin_reelle > date_fin_prevue` | Réorganiser planning |
| A10 | Maintenance en retard | Information | Date prévue dépassée | Planifier intervention |
| A11 | Opérateur non qualifié | Information | Junior sur phase critique | Superviser |

### 11.2 Niveaux de sévérité

| Niveau | Couleur | Action | Notification |
|--------|---------|--------|-------------|
| **Critique** | Rouge | Intervention immédiate | Push + email |
| **Avertissement** | Orange | Action requise bientôt | Email |
| **Information** | Bleu | À noter | Dashboard uniquement |

### 11.3 Seuils configurables

Tous les seuils d'alerte sont **configurables** par l'ingénieur AMM via une page de paramètres. Les valeurs par défaut sont basées sur les standards de l'industrie CNC.

---

## 12. Navigation inter-modules

### 12.1 Connexions entre modules

Le dashboard permet de naviguer d'un module à l'autre en cliquant sur des données :

| De | Vers | Action |
|----|------|--------|
| Vue Exécutive | Machine | Cliquer sur une carte machine |
| Vue Exécutive | OF | Cliquer sur un OF dans le tableau |
| Vue Exécutive | Maintenance | Cliquer sur une alerte maintenance |
| Machine | OF | Cliquer sur l'OF en cours |
| Machine | Outil | Cliquer sur l'outil actuel |
| Machine | Maintenance | Cliquer sur l'historique maintenance |
| Machine | Capteurs | Cliquer sur un capteur |
| OF | Machine | Cliquer sur la machine utilisée |
| OF | Pièce | Cliquer sur la référence pièce |
| Qualité | Machine | Cliquer sur la machine |
| Qualité | OF | Cliquer sur l'OF |
| Qualité | Outil | Cliquer sur l'outil |
| Inventaire | Matière | Cliquer sur la matière |
| Inventaire | Outil | Cliquer sur l'outil |
| Inventaire | Pièce | Cliquer sur la pièce |
| Maintenance | Machine | Cliquer sur la machine |
| Capteurs | Machine | Sélection machine |

### 12.2 Fil d'Ariane

Chaque page affiche un fil d'Ariane permettant de revenir aux modules précédents :

Exemple : `Vue Exécutive > Machine M005 > Outil OUT0034`

---

## 13. Prédictions Machine Learning

### 13.1 Phase 4 — Modèles à intégrer

| # | Modèle | Module cible | Prédiction | Variables d'entrée |
|---|--------|-------------|------------|-------------------|
| ML01 | Scrap Prediction | Qualité | Probabilité de rebut | Paramètres coupe, outil, capteurs, opérateur |
| ML02 | Machining Time Estimation | OF | Temps d'usinage réel estimé | Gamme, machine, outil, matière |
| ML03 | Predictive Maintenance | Maintenance | Temps avant prochaine panne | Capteurs, historique maintenance, âge machine |
| ML04 | Machine Failure Prediction | Machine | Probabilité de panne (7 jours) | Capteurs tendances, maintenance, exécution |
| ML05 | Tool Wear Prediction | Outil | Usure restante prédite | Type outil, exécutions, paramètres coupe |
| ML06 | Production Duration Prediction | OF | Durée totale prédite | Quantité, gamme, opérateur, matière |
| ML07 | Inventory Forecasting | Inventaire | Date de rupture stock | Stock actuel, consommation, OFs actifs |

### 13.2 Intégration dans le dashboard

Chaque prédiction ML apparaît dans le module correspondant sous forme de :

| Élément | Description |
|---------|-------------|
| **Carte de prédiction** | Valeur prédite avec icône ML |
| **Intervalle de confiance** | Fourchette de valeurs possibles |
| **Recommandation** | Action suggérée basée sur la prédiction |
| **Tendance** | Si la prédiction s'aggrave ou s'améliore |

### 13.3 Indicateur de confiance ML

| Confiance | Couleur | Signification |
|-----------|---------|---------------|
| ≥ 80% | Vert | Prédiction fiable |
| 60-80% | Orange | Prédiction à valider |
| < 60% | Rouge | Prédiction peu fiable, consulter un expert |

---

## 14. Roadmap de mise en œuvre

| Phase | Livrables | Priorité |
|-------|-----------|----------|
| **Phase 1** (actuelle) | Spécification métier + Catalogue KPI + Validation ingénieur | Haute |
| **Phase 2** | Backend API (FastAPI) | Haute |
| **Phase 3** | Dashboard interactif (Streamlit) | Haute |
| **Phase 4** | Intégration Machine Learning (scikit-learn + XGBoost) | Moyenne |
| **Phase 5** | Dockerisation complète | Moyenne |

---

## Annexe A — Glossaire

| Terme | Définition |
|-------|-----------|
| **OEE** | Overall Equipment Effectiveness — Efficacité Globale des Équipements |
| **MTBF** | Mean Time Between Failures — Temps Moyen Entre Pannes |
| **MTTR** | Mean Time To Repair — Temps Moyen de Réparation |
| **FPY** | First Pass Yield — Rendement au Premier Passage |
| **OF** | Ordre de Fabrication |
| **CNC** | Computer Numerical Control — Commande Numérique par Ordinateur |
| **RUL** | Remaining Useful Life — Durée de Vie Utile Restante |
| **Pareto** | Principe 80/20 — 80% des effets viennent de 20% des causes |
| **MES** | Manufacturing Execution System — Système d'Exécution de Production |
| **BI** | Business Intelligence — Intelligence Économique |

---

**Document validé par :** ________________ (Ingénieur AMM)
**Date :** ________________
**Signature :** ________________
