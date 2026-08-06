# AMIP - KPI Specification Document

**Version:** 1.0
**Date:** 2026-07-14
**Status:** Phase 1 - Specification Only (No Implementation)
**Scope:** All KPIs calculable from the current operational database schema

---

## Table of Contents

1. [Production KPIs](#1-production-kpis)
2. [Quality KPIs](#2-quality-kpis)
3. [OEE KPIs](#3-oee-kpis)
4. [Machine Performance KPIs](#4-machine-performance-kpis)
5. [Tool Management KPIs](#5-tool-management-kpis)
6. [Inventory KPIs](#6-inventory-kpis)
7. [Maintenance KPIs](#7-maintenance-kpis)
8. [Sensor KPIs](#8-sensor-kpis)
9. [Cost KPIs](#9-cost-kpis)
10. [Future KPIs - Phase 2](#10-future-kpis---phase-2)
11. [Machine Learning Feature Mapping](#11-machine-learning-feature-mapping)

---

## Conventions

Each KPI entry follows this template:

| Field | Description |
|---|---|
| **KPI ID** | Unique identifier for traceability |
| **Business Objective** | Why this KPI is needed |
| **Formula** | Mathematical expression using database columns |
| **Source Tables** | Tables from the public schema required |
| **Source Columns** | Exact column names consumed |
| **Output** | Data type and meaning of the result |
| **Unit** | Measure unit |
| **Business Interpretation** | What the value means operationally |
| **Typical Values** | Realistic range for a CNC workshop |
| **Dashboard Visual** | Suggested chart type |
| **Refresh** | How often this should be computed |

---

## 1. Production KPIs

### KPI-PRD-001 - Estimated Machining Time per OF

| Field | Value |
|---|---|
| **Business Objective** | Know the total planned machining time before production starts |
| **Formula** | `SUM(pg.temps_usinage_prevu)` grouped by `of.gamme_id` |
| **Source Tables** | `phase_gamme`, `ordre_fabrication` |
| **Source Columns** | `phase_gamme.temps_usinage_prevu`, `phase_gamme.gamme_id`, `ordre_fabrication.gamme_id` |
| **Output** | Integer - total estimated machining minutes for one OF |
| **Unit** | Minutes |
| **Business Interpretation** | Baseline for comparing actual performance. Used for scheduling and capacity planning |
| **Typical Values** | 30-300 min depending on part complexity and number of phases |
| **Dashboard Visual** | Card (per OF) |
| **Refresh** | On OF creation |

---

### KPI-PRD-002 - Real Machining Time per OF

| Field | Value |
|---|---|
| **Business Objective** | Measure actual machining time after execution |
| **Formula** | `SUM(ep.temps_usinage_reel)` WHERE `ep.ordre_fabrication_id = OF` AND `ep.statut = 'TERMINE'` |
| **Source Tables** | `execution_phase` |
| **Source Columns** | `temps_usinage_reel`, `ordre_fabrication_id`, `statut` |
| **Output** | Integer - total real machining minutes for one OF |
| **Unit** | Minutes |
| **Business Interpretation** | Real time consumed. Compare with KPI-PRD-001 to evaluate estimation accuracy |
| **Typical Values** | 35-350 min (usually 5-20% above estimate) |
| **Dashboard Visual** | Card + comparison bar (estimated vs real) |
| **Refresh** | After each OF completion |

---

### KPI-PRD-003 - Estimated Setup Time per OF

| Field | Value |
|---|---|
| **Business Objective** | Track planned non-productive preparation time |
| **Formula** | `SUM(pg.temps_reglage_prevu)` grouped by gamme |
| **Source Tables** | `phase_gamme`, `ordre_fabrication` |
| **Source Columns** | `phase_gamme.temps_reglage_prevu`, `phase_gamme.gamme_id` |
| **Output** | Integer - estimated setup minutes |
| **Unit** | Minutes |
| **Business Interpretation** | Setup is non-value-added time. Reducing setup is a lean manufacturing priority |
| **Typical Values** | 5-60 min per OF |
| **Dashboard Visual** | Card |
| **Refresh** | On OF creation |

---

### KPI-PRD-004 - Real Setup Time per OF

| Field | Value |
|---|---|
| **Business Objective** | Measure actual setup time |
| **Formula** | `SUM(ep.temps_reglage_reel)` grouped by `ep.ordre_fabrication_id` |
| **Source Tables** | `execution_phase` |
| **Source Columns** | `temps_reglage_reel`, `ordre_fabrication_id` |
| **Output** | Integer - real setup minutes |
| **Unit** | Minutes |
| **Business Interpretation** | Compare with KPI-PRD-003. Excess setup time indicates tooling or process issues |
| **Typical Values** | 5-80 min |
| **Dashboard Visual** | Card + comparison bar |
| **Refresh** | After each OF completion |

---

### KPI-PRD-005 - Total Production Time per OF

| Field | Value |
|---|---|
| **Business Objective** | Total machine time consumed by a production order |
| **Formula** | `SUM(ep.temps_usinage_reel + ep.temps_reglage_reel)` WHERE `ep.ordre_fabrication_id = OF` AND `ep.statut = 'TERMINE'` |
| **Source Tables** | `execution_phase` |
| **Source Columns** | `temps_usinage_reel`, `temps_reglage_reel`, `ordre_fabrication_id`, `statut` |
| **Output** | Integer - total machine minutes |
| **Unit** | Minutes |
| **Business Interpretation** | Core input for cost calculations and machine utilization |
| **Typical Values** | 40-400 min |
| **Dashboard Visual** | Card |
| **Refresh** | After each OF completion |

---

### KPI-PRD-006 - Production Duration (Calendar)

| Field | Value |
|---|---|
| **Business Objective** | Measure elapsed calendar time of an OF |
| **Formula** | `OF.date_fin_reelle - OF.date_debut_reelle` |
| **Source Tables** | `ordre_fabrication` |
| **Source Columns** | `date_fin_reelle`, `date_debut_reelle` |
| **Output** | Integer - calendar days |
| **Unit** | Days |
| **Business Interpretation** | Includes non-working time (weekends, nights). Compare with planned duration for delivery tracking |
| **Typical Values** | 3-30 days |
| **Dashboard Visual** | Bar chart (planned vs actual) |
| **Refresh** | On OF completion |

---

### KPI-PRD-007 - Cycle Time per Execution Phase

| Field | Value |
|---|---|
| **Business Objective** | Time to produce one piece in a specific phase |
| **Formula** | `ep.temps_usinage_reel / ep.nb_pieces_produites` WHERE `nb_pieces_produites > 0` |
| **Source Tables** | `execution_phase` |
| **Source Columns** | `temps_usinage_reel`, `nb_pieces_produites` |
| **Output** | Decimal - minutes per piece |
| **Unit** | min/pc |
| **Business Interpretation** | Core metric for capacity planning. Increasing cycle time over time indicates degradation |
| **Typical Values** | 0.5-15 min/piece |
| **Dashboard Visual** | Line chart (trend over time) |
| **Refresh** | After each execution |

---

### KPI-PRD-008 - Production Efficiency

| Field | Value |
|---|---|
| **Business Objective** | Compare estimated vs real machining time |
| **Formula** | `SUM(pg.temps_usinage_prevu) / SUM(ep.temps_usinage_reel) * 100` per OF |
| **Source Tables** | `phase_gamme`, `execution_phase` |
| **Source Columns** | `phase_gamme.temps_usinage_prevu`, `execution_phase.temps_usinage_reel` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | 100% = exactly as planned. > 100% = faster than planned. < 100% = overruns. Low values trigger routing review |
| **Typical Values** | 85-120% |
| **Dashboard Visual** | Gauge + trend line |
| **Refresh** | After OF completion |

---

### KPI-PRD-009 - Production Yield

| Field | Value |
|---|---|
| **Business Objective** | Proportion of good parts vs total produced |
| **Formula** | `(SUM(ep.nb_pieces_produites) - SUM(ep.nb_pieces_rebut)) / SUM(ep.nb_pieces_produites) * 100` per OF or per period |
| **Source Tables** | `execution_phase` |
| **Source Columns** | `nb_pieces_produites`, `nb_pieces_rebut` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | Direct measure of manufacturing quality. Target > 95% |
| **Typical Values** | 88-99% |
| **Dashboard Visual** | Gauge |
| **Refresh** | Daily |

---

### KPI-PRD-010 - Production Throughput

| Field | Value |
|---|---|
| **Business Objective** | Output rate - good pieces per hour of production |
| **Formula** | `SUM(ep.nb_pieces_produites - ep.nb_pieces_rebut) / (SUM(ep.temps_usinage_reel + ep.temps_reglage_reel) / 60)` per machine or workshop per period |
| **Source Tables** | `execution_phase` |
| **Source Columns** | `nb_pieces_produites`, `nb_pieces_rebut`, `temps_usinage_reel`, `temps_reglage_reel` |
| **Output** | Decimal - pieces per hour |
| **Unit** | pcs/h |
| **Business Interpretation** | Key capacity indicator. Used for production planning and bottleneck detection |
| **Typical Values** | 10-100 pcs/h depending on complexity |
| **Dashboard Visual** | Bar chart (by machine, by period) |
| **Refresh** | Daily |

---

### KPI-PRD-011 - Production Capacity Utilization

| Field | Value |
|---|---|
| **Business Objective** | How much of available production time is actually used |
| **Formula** | `SUM(ep.temps_usinage_reel + ep.temps_reglage_reel) / available_time * 100` per machine per period |
| **Source Tables** | `execution_phase` |
| **Source Columns** | `temps_usinage_reel`, `temps_reglage_reel`, `machine_id`, `date_debut` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | Available time = total hours in period minus weekends/nights. Low values = idle machines |
| **Typical Values** | 60-85% |
| **Dashboard Visual** | Heatmap (machine x day) |
| **Refresh** | Daily |
| **Assumption** | Available time requires shift schedule configuration. Default: single shift 8h/day, 22 working days/month |

---

### KPI-PRD-012 - OF Delay

| Field | Value |
|---|---|
| **Business Objective** | Measure delivery delay for production orders |
| **Formula** | `OF.date_fin_reelle - OF.date_fin_prevue` (both cast to date) |
| **Source Tables** | `ordre_fabrication` |
| **Source Columns** | `date_fin_reelle`, `date_fin_prevue` |
| **Output** | Integer - days (positive = late, negative = early) |
| **Unit** | Days |
| **Business Interpretation** | Critical for customer satisfaction. Negative values mean early delivery |
| **Typical Values** | -5 to +10 days |
| **Dashboard Visual** | Bar chart (distribution of delays) |
| **Refresh** | Weekly |

---

## 2. Quality KPIs

### KPI-QLT-001 - Scrap Rate

| Field | Value |
|---|---|
| **Business Objective** | Proportion of defective parts in total production |
| **Formula** | `SUM(cq.nb_non_conformes) / SUM(cq.nb_controles) * 100` per period, per machine, per part, etc. |
| **Source Tables** | `controle_qualite` |
| **Source Columns** | `nb_non_conformes`, `nb_controles` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | Primary quality metric. > 5% triggers investigation. Can be sliced by machine, tool, material, operator |
| **Typical Values** | 2-8% in precision machining |
| **Dashboard Visual** | Gauge + line chart (trend) |
| **Refresh** | Daily |

---

### KPI-QLT-002 - First Pass Yield (FPY)

| Field | Value |
|---|---|
| **Business Objective** | Parts passing quality control on first attempt |
| **Formula** | `(SUM(cq.nb_controles) - SUM(cq.nb_non_conformes)) / SUM(cq.nb_controles) * 100` |
| **Source Tables** | `controle_qualite` |
| **Source Columns** | `nb_controles`, `nb_non_conformes` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | Measures process capability without rework. Higher FPY = lower rework cost |
| **Typical Values** | 90-98% |
| **Dashboard Visual** | Gauge |
| **Refresh** | Daily |

---

### KPI-QLT-003 - Conformity Rate

| Field | Value |
|---|---|
| **Business Objective** | Proportion of inspected parts conforming to specifications |
| **Formula** | `SUM(cq.nb_conformes) / SUM(cq.nb_controles) * 100` |
| **Source Tables** | `controle_qualite` |
| **Source Columns** | `nb_conformes`, `nb_controles` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | Inverse of non-conformity. Tracked per period, per machine, per operator |
| **Typical Values** | 92-99% |
| **Dashboard Visual** | Gauge + trend |
| **Refresh** | Daily |

---

### KPI-QLT-004 - Dimensional Accuracy

| Field | Value |
|---|---|
| **Business Objective** | Measure how close parts are to target dimensions |
| **Formula** | `ABS(cq.dimension_mesuree - cq.dimension_cible)` WHERE both are NOT NULL |
| **Source Tables** | `controle_qualite` |
| **Source Columns** | `dimension_mesuree`, `dimension_cible` |
| **Output** | Decimal - absolute deviation |
| **Unit** | mm |
| **Business Interpretation** | Should stay within tolerance limits (tolerance_plus / tolerance_moins). Average and max deviation tracked over time |
| **Typical Values** | 0.001-0.05 mm |
| **Dashboard Visual** | Box plot or scatter chart |
| **Refresh** | Daily |

---

### KPI-QLT-005 - Surface Roughness

| Field | Value |
|---|---|
| **Business Objective** | Track surface finish quality |
| **Formula** | `AVG(cq.rugosite_mesuree)` WHERE `rugosite_mesuree IS NOT NULL` grouped by machine, part, period |
| **Source Tables** | `controle_qualite` |
| **Source Columns** | `rugosite_mesuree` |
| **Output** | Decimal - average roughness |
| **Unit** | Ra (um) |
| **Business Interpretation** | Lower Ra = smoother surface. Increasing trend indicates tool wear or machine issues |
| **Typical Values** | 0.4-6.3 um |
| **Dashboard Visual** | Line chart (trend) |
| **Refresh** | Daily |

---

### KPI-QLT-006 - Defects by Machine

| Field | Value |
|---|---|
| **Business Objective** | Identify machines with highest defect rates |
| **Formula** | `SUM(cq.nb_non_conformes) GROUP BY ep.machine_id` via `cq.execution_id = ep.execution_id` |
| **Source Tables** | `controle_qualite`, `execution_phase` |
| **Source Columns** | `controle_qualite.nb_non_conformes`, `controle_qualite.execution_id`, `execution_phase.machine_id` |
| **Output** | Table - machine_id, defect_count, defect_rate |
| **Unit** | Count / % |
| **Business Interpretation** | Identifies problematic machines. High defect rate = maintenance or calibration needed |
| **Dashboard Visual** | Bar chart (top machines by defect count) |
| **Refresh** | Weekly |

---

### KPI-QLT-007 - Defects by Tool

| Field | Value |
|---|---|
| **Business Objective** | Identify tools causing the most defects |
| **Formula** | `SUM(cq.nb_non_conformes) GROUP BY ep.outil_id` via `cq.execution_id = ep.execution_id` |
| **Source Tables** | `controle_qualite`, `execution_phase` |
| **Source Columns** | `nb_non_conformes`, `execution_id`, `outil_id` |
| **Output** | Table - outil_id, defect_count |
| **Unit** | Count |
| **Business Interpretation** | Tools nearing end of life produce more defects. Correlate with tool wear data |
| **Dashboard Visual** | Bar chart |
| **Refresh** | Weekly |

---

### KPI-QLT-008 - Defects by Material

| Field | Value |
|---|---|
| **Business Objective** | Identify materials with highest defect rates |
| **Formula** | `SUM(cq.nb_non_conformes) GROUP BY p.matiere_id` via `cq.piece_id = p.piece_id` |
| **Source Tables** | `controle_qualite`, `piece` |
| **Source Columns** | `nb_non_conformes`, `piece_id`, `piece.matiere_id` |
| **Output** | Table - matiere_id, material_type, defect_count |
| **Unit** | Count |
| **Business Interpretation** | Some materials are harder to machine. Informs material selection and process planning |
| **Dashboard Visual** | Bar chart or pie chart |
| **Refresh** | Monthly |

---

### KPI-QLT-009 - Defects by Operator

| Field | Value |
|---|---|
| **Business Objective** | Identify operators associated with defects |
| **Formula** | `SUM(cq.nb_non_conformes) GROUP BY ep.operateur_id` via `cq.execution_id = ep.execution_id` |
| **Source Tables** | `controle_qualite`, `execution_phase` |
| **Source Columns** | `nb_non_conformes`, `execution_id`, `operateur_id` |
| **Output** | Table - operateur_id, nom, defect_count |
| **Unit** | Count |
| **Business Interpretation** | May indicate training needs. Cross-reference with operator competence level |
| **Dashboard Visual** | Bar chart |
| **Refresh** | Monthly |

---

### KPI-QLT-010 - Defects by Cause Category

| Field | Value |
|---|---|
| **Business Objective** | Classify defects by root cause |
| **Formula** | `SUM(cq.nb_non_conformes) GROUP BY cr.categorie` via `cq.cause_rebut_id = cr.cause_rebut_id` WHERE `cause_rebut_id IS NOT NULL` |
| **Source Tables** | `controle_qualite`, `cause_rebut` |
| **Source Columns** | `nb_non_conformes`, `cause_rebut_id`, `cause_rebut.categorie` |
| **Output** | Table - categorie (Materiel, Outil, Machine, Programmation, Operateur, Autre), defect_count |
| **Unit** | Count |
| **Business Interpretation** | Identifies systemic root causes. Highest category gets priority for corrective action |
| **Dashboard Visual** | Pie chart + bar chart |
| **Refresh** | Monthly |

---

### KPI-QLT-011 - Defects by Production Order

| Field | Value |
|---|---|
| **Business Objective** | Identify OFs with highest scrap |
| **Formula** | `SUM(cq.nb_non_conformes) GROUP BY ep.ordre_fabrication_id` |
| **Source Tables** | `controle_qualite`, `execution_phase` |
| **Source Columns** | `nb_non_conformes`, `execution_id`, `ordre_fabrication_id` |
| **Output** | Table - numero_of, defect_count |
| **Unit** | Count |
| **Business Interpretation** | Flags problematic production runs for root cause analysis |
| **Dashboard Visual** | Bar chart (top 10 OFs by scrap) |
| **Refresh** | Weekly |

---

## 3. OEE KPIs

### KPI-OEE-001 - Availability

| Field | Value |
|---|---|
| **Business Objective** | Proportion of planned time the machine is actually running |
| **Formula** | `SUM(ep.temps_usinage_reel + ep.temps_reglage_reel) / (SUM(ep.temps_usinage_reel + ep.temps_reglage_reel) + maintenance_downtime + idle_time) * 100` per machine per period |
| **Source Tables** | `execution_phase`, `maintenance`, `sensor_data` |
| **Source Columns** | `execution_phase.temps_usinage_reel`, `execution_phase.temps_reglage_reel`, `execution_phase.machine_id`, `maintenance.duree`, `maintenance.machine_id`, `sensor_data.statut_machine` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | Low availability = too much downtime or maintenance. Target > 85% |
| **Typical Values** | 80-95% |
| **Dashboard Visual** | Gauge |
| **Refresh** | Daily |
| **Assumption** | maintenance_downtime = sum of maintenance.duree for the machine in the period. idle_time estimated from sensor readings where statut_machine = 'STOPPED' |

---

### KPI-OEE-002 - Performance

| Field | Value |
|---|---|
| **Business Objective** | Speed efficiency - running at optimal speed? |
| **Formula** | `SUM(pg.temps_usinage_prevu) / SUM(ep.temps_usinage_reel) * 100` WHERE `ep.statut = 'TERMINE'` per machine per period |
| **Source Tables** | `execution_phase`, `phase_gamme` |
| **Source Columns** | `phase_gamme.temps_usinage_prevu`, `execution_phase.temps_usinage_reel`, `execution_phase.phase_gamme_id` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | > 100% = running faster than planned. < 85% = machine or process slowdown |
| **Typical Values** | 85-110% |
| **Dashboard Visual** | Gauge |
| **Refresh** | Daily |

---

### KPI-OEE-003 - Quality Rate

| Field | Value |
|---|---|
| **Business Objective** | Proportion of good parts out of total production |
| **Formula** | `(SUM(ep.nb_pieces_produites) - SUM(ep.nb_pieces_rebut)) / SUM(ep.nb_pieces_produites) * 100` per machine per period |
| **Source Tables** | `execution_phase` |
| **Source Columns** | `nb_pieces_produites`, `nb_pieces_rebut`, `machine_id` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | Target > 98%. Low quality rate pulls down overall OEE significantly |
| **Typical Values** | 92-99% |
| **Dashboard Visual** | Gauge |
| **Refresh** | Daily |

---

### KPI-OEE-004 - Overall Equipment Effectiveness (OEE)

| Field | Value |
|---|---|
| **Business Objective** | Single metric combining availability, performance, and quality |
| **Formula** | `(KPI-OEE-001 / 100) * (KPI-OEE-002 / 100) * (KPI-OEE-003 / 100) * 100` |
| **Source Tables** | Derived from KPI-OEE-001, KPI-OEE-002, KPI-OEE-003 |
| **Source Columns** | (Indirect) all columns from Availability, Performance, Quality |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | World-class target = 85%. < 65% = significant improvement opportunity. 65-80% = good. > 80% = excellent |
| **Typical Values** | 50-75% |
| **Dashboard Visual** | Gauge (primary KPI) + trend line |
| **Refresh** | Daily |

---

## 4. Machine Performance KPIs

### KPI-MCH-001 - Machine Running Time

| Field | Value |
|---|---|
| **Business Objective** | Total productive time for a machine in a period |
| **Formula** | `SUM(ep.temps_usinage_reel + ep.temps_reglage_reel)` WHERE `ep.machine_id = M` AND `ep.statut = 'TERMINE'` AND `ep.date_debut` IN [period] |
| **Source Tables** | `execution_phase` |
| **Source Columns** | `temps_usinage_reel`, `temps_reglage_reel`, `machine_id`, `statut`, `date_debut` |
| **Output** | Integer - minutes |
| **Unit** | Minutes |
| **Business Interpretation** | Foundation for utilization and OEE calculations |
| **Dashboard Visual** | Card + bar chart (by machine) |
| **Refresh** | Daily |

---

### KPI-MCH-002 - Machine Downtime (Sensor-Based)

| Field | Value |
|---|---|
| **Business Objective** | Time machine was stopped or broken based on sensor data |
| **Formula** | `COUNT(*) * 30 / 60` WHERE `sd.statut_machine IN ('STOPPED', 'BROKEN')` AND `sd.machine_id = M` AND `sd.timestamp` IN [period] |
| **Source Tables** | `sensor_data` |
| **Source Columns** | `statut_machine`, `machine_id`, `timestamp` |
| **Output** | Decimal - hours |
| **Unit** | Hours |
| **Business Interpretation** | High downtime = production bottleneck. Compare across machines to find worst performers |
| **Dashboard Visual** | Bar chart |
| **Refresh** | Daily |
| **Assumption** | Sensor data is recorded at 30-second intervals. Each STOPPED/BROKEN reading = 30 seconds of downtime |

---

### KPI-MCH-003 - Machine Maintenance Time

| Field | Value |
|---|---|
| **Business Objective** | Total time machine was under maintenance |
| **Formula** | `SUM(m.duree)` WHERE `m.machine_id = M` AND `m.date_debut` IN [period] |
| **Source Tables** | `maintenance` |
| **Source Columns** | `duree`, `machine_id`, `date_debut` |
| **Output** | Integer - minutes |
| **Unit** | Minutes |
| **Business Interpretation** | High maintenance time = unreliable machine. Track trends to predict replacement need |
| **Dashboard Visual** | Card + bar chart |
| **Refresh** | Monthly |

---

### KPI-MCH-004 - Machine Average Cycle Time

| Field | Value |
|---|---|
| **Business Objective** | Average time to produce one piece on a specific machine |
| **Formula** | `SUM(ep.temps_usinage_reel) / SUM(ep.nb_pieces_produites)` WHERE `ep.machine_id = M` AND `nb_pieces_produites > 0` |
| **Source Tables** | `execution_phase` |
| **Source Columns** | `temps_usinage_reel`, `nb_pieces_produites`, `machine_id` |
| **Output** | Decimal - minutes per piece |
| **Unit** | min/pc |
| **Business Interpretation** | Increasing trend over time = machine degradation or tool wear. Compare across machines of same type |
| **Dashboard Visual** | Line chart (trend) + bar chart (comparison) |
| **Refresh** | Weekly |

---

### KPI-MCH-005 - Machine Efficiency

| Field | Value |
|---|---|
| **Business Objective** | Compare estimated vs actual production time per machine |
| **Formula** | `SUM(pg.temps_usinage_prevu) / SUM(ep.temps_usinage_reel) * 100` WHERE `ep.machine_id = M` |
| **Source Tables** | `execution_phase`, `phase_gamme` |
| **Source Columns** | `phase_gamme.temps_usinage_prevu`, `execution_phase.temps_usinage_reel`, `phase_gamme_id`, `machine_id` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | > 100% = machine running faster than planned. < 85% = investigate (tool wear, mechanical issue, operator) |
| **Typical Values** | 85-120% |
| **Dashboard Visual** | Bar chart (by machine) |
| **Refresh** | Monthly |

---

## 5. Tool Management KPIs

### KPI-TOL-001 - Tool Wear per Execution

| Field | Value |
|---|---|
| **Business Objective** | Measure tool lifetime consumed during one execution |
| **Formula** | `eo.usure_fin - eo.usure_debut` |
| **Source Tables** | `execution_outil` |
| **Source Columns** | `usure_debut`, `usure_fin` |
| **Output** | Integer - minutes of tool life consumed |
| **Unit** | Minutes |
| **Business Interpretation** | High wear per execution = aggressive machining parameters or hard material |
| **Dashboard Visual** | Line chart (trend per tool) |
| **Refresh** | After each execution |

---

### KPI-TOL-002 - Cumulative Tool Consumption

| Field | Value |
|---|---|
| **Business Objective** | Total lifetime consumed across all uses of a tool |
| **Formula** | `SUM(eo.usure_fin - eo.usure_debut)` GROUP BY `eo.outil_id` |
| **Source Tables** | `execution_outil` |
| **Source Columns** | `usure_debut`, `usure_fin`, `outil_id` |
| **Output** | Integer - total minutes consumed |
| **Unit** | Minutes |
| **Business Interpretation** | Compare with outil.duree_vie_totale to determine remaining life percentage |
| **Dashboard Visual** | Bar chart (top tools by consumption) |
| **Refresh** | Weekly |

---

### KPI-TOL-003 - Tool Lifetime Percentage

| Field | Value |
|---|---|
| **Business Objective** | How much of a tool's life has been consumed |
| **Formula** | `o.usure_actuelle / o.duree_vie_totale * 100` |
| **Source Tables** | `outil` |
| **Source Columns** | `usure_actuelle`, `duree_vie_totale` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | > 80% = replacement needed soon. 100% = tool exhausted. Track distribution across inventory |
| **Dashboard Visual** | Histogram (distribution of tool life % across inventory) |
| **Refresh** | Weekly |

---

### KPI-TOL-004 - Tool Replacement Indicator

| Field | Value |
|---|---|
| **Business Objective** | Flag tools that need replacement |
| **Formula** | `CASE WHEN duree_vie_restante <= duree_vie_totale * 0.10 THEN 'REPLACE' WHEN duree_vie_restante <= duree_vie_totale * 0.25 THEN 'WARNING' ELSE 'OK' END` |
| **Source Tables** | `outil` |
| **Source Columns** | `duree_vie_restante`, `duree_vie_totale` |
| **Output** | String - REPLACE, WARNING, or OK |
| **Unit** | Category |
| **Business Interpretation** | Tools at REPLACE should be swapped immediately. WARNING tools should be scheduled for replacement |
| **Dashboard Visual** | Pie chart (OK / WARNING / REPLACE distribution) |
| **Refresh** | Weekly |

---

### KPI-TOL-005 - Average Tool Lifetime by Type

| Field | Value |
|---|---|
| **Business Objective** | Benchmark tool durability by type |
| **Formula** | `AVG(o.duree_vie_totale) GROUP BY o.type_outil` |
| **Source Tables** | `outil` |
| **Source Columns** | `duree_vie_totale`, `type_outil` |
| **Output** | Decimal - average lifetime in minutes |
| **Unit** | Minutes |
| **Business Interpretation** | Helps compare brands and materials. Low average for a type = consider alternative suppliers |
| **Dashboard Visual** | Bar chart |
| **Refresh** | Monthly |

---

### KPI-TOL-006 - Tool Utilization Rate

| Field | Value |
|---|---|
| **Business Objective** | How actively each tool type is being used |
| **Formula** | `COUNT(DISTINCT eo.execution_id WHERE t.type_outil = X) / COUNT(DISTINCT eo.execution_id) * 100` |
| **Source Tables** | `execution_outil`, `outil` |
| **Source Columns** | `execution_id`, `outil_id`, `outil.type_outil` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | Low utilization = excess inventory or wrong tool selection. High utilization = potential bottleneck |
| **Dashboard Visual** | Bar chart |
| **Refresh** | Monthly |

---

## 6. Inventory KPIs

### KPI-INV-001 - Current Stock Level (Parts)

| Field | Value |
|---|---|
| **Business Objective** | Know how many finished parts are in stock |
| **Formula** | `sp.quantite_stock` |
| **Source Tables** | `stock_piece` |
| **Source Columns** | `quantite_stock`, `piece_id` |
| **Output** | Integer - quantity per part reference |
| **Unit** | Pieces |
| **Business Interpretation** | Zero = stockout risk. Very high = excess inventory tying up capital |
| **Dashboard Visual** | Table with conditional formatting |
| **Refresh** | Daily |

---

### KPI-INV-002 - Current Stock Level (Materials)

| Field | Value |
|---|---|
| **Business Objective** | Know raw material quantities available |
| **Formula** | `sm.quantite_stock` |
| **Source Tables** | `stock_matiere` |
| **Source Columns** | `quantite_stock`, `matiere_id` |
| **Output** | Decimal - kg per material |
| **Unit** | kg |
| **Business Interpretation** | Critical for production planning. Below threshold = reorder needed |
| **Dashboard Visual** | Table with conditional formatting |
| **Refresh** | Daily |

---

### KPI-INV-003 - Current Stock Level (Tools)

| Field | Value |
|---|---|
| **Business Objective** | Know tool inventory quantities |
| **Formula** | `so.quantite_stock` |
| **Source Tables** | `stock_outil` |
| **Source Columns** | `quantite_stock`, `outil_id` |
| **Output** | Integer - quantity per tool reference |
| **Unit** | Pieces |
| **Business Interpretation** | Below threshold = urgent reorder to avoid production stoppage |
| **Dashboard Visual** | Table with conditional formatting |
| **Refresh** | Daily |

---

### KPI-INV-004 - Stock Status

| Field | Value |
|---|---|
| **Business Objective** | Classify inventory health |
| **Formula** | `CASE WHEN quantite_stock <= 0 THEN 'OUT_OF_STOCK' WHEN quantite_stock <= seuil_alerte THEN 'LOW' WHEN quantite_stock > seuil_alerte * 3 THEN 'OVERSTOCK' ELSE 'NORMAL' END` (applied to stock_matiere, stock_outil, stock_piece with appropriate thresholds) |
| **Source Tables** | `stock_matiere`, `stock_outil`, `stock_piece` |
| **Source Columns** | `quantite_stock`, `seuil_alerte` |
| **Output** | String - OUT_OF_STOCK, LOW, NORMAL, OVERSTOCK |
| **Unit** | Category |
| **Business Interpretation** | OUT_OF_STOCK = immediate action. LOW = schedule reorder. OVERSTOCK = reduce next order |
| **Dashboard Visual** | Donut chart (distribution across status categories) |
| **Refresh** | Daily |

---

### KPI-INV-005 - Material Consumption (Estimated)

| Field | Value |
|---|---|
| **Business Objective** | Estimate material consumed based on production output |
| **Formula** | `SUM(p.poids * ep.nb_pieces_produites)` GROUP BY `p.matiere_id` WHERE `ep.statut = 'TERMINE'` |
| **Source Tables** | `piece`, `execution_phase`, `ordre_fabrication` |
| **Source Columns** | `piece.poids`, `piece.piece_id`, `execution_phase.nb_pieces_produites`, `execution_phase.ordre_fabrication_id`, `ordre_fabrication.piece_id` |
| **Output** | Decimal - estimated kg consumed per material |
| **Unit** | kg |
| **Business Interpretation** | Estimated from pieces produced x piece weight. Does not account for machining waste (chips, cut-offs) |
| **Dashboard Visual** | Bar chart (by material type) |
| **Refresh** | Weekly |
| **Assumption** | This is an estimate. Actual consumption includes machining waste factor (typically 1.1-1.3x net weight). Precise tracking requires mouvement_stock table (Phase 2) |

---

### KPI-INV-006 - Reorder Indicator

| Field | Value |
|---|---|
| **Business Objective** | Flag items that need reordering |
| **Formula** | `quantite_stock <= seuil_alerte` (applied to stock_matiere and stock_outil) |
| **Source Tables** | `stock_matiere`, `stock_outil` |
| **Source Columns** | `quantite_stock`, `seuil_alerte` |
| **Output** | Boolean - TRUE = needs reorder |
| **Unit** | Boolean |
| **Business Interpretation** | Operational trigger for purchasing department |
| **Dashboard Visual** | Alert list / table |
| **Refresh** | Daily |

---

### KPI-INV-007 - Finished Parts Stock Value

| Field | Value |
|---|---|
| **Business Objective** | Estimate inventory value of finished parts |
| **Formula** | `SUM(sp.quantite_stock * p.prix_revient)` |
| **Source Tables** | `stock_piece`, `piece` |
| **Source Columns** | `stock_piece.quantite_stock`, `stock_piece.piece_id`, `piece.prix_revient`, `piece.piece_id` |
| **Output** | Decimal - total EUR value |
| **Unit** | EUR |
| **Business Interpretation** | Financial indicator for inventory management. High value = capital tied up in stock |
| **Dashboard Visual** | Card + bar chart (by part family) |
| **Refresh** | Monthly |

---

## 7. Maintenance KPIs

### KPI-MNT-001 - Maintenance Count by Machine

| Field | Value |
|---|---|
| **Business Objective** | Track how many maintenance events per machine |
| **Formula** | `COUNT(*) GROUP BY m.machine_id` WHERE `m.date_debut` IN [period] |
| **Source Tables** | `maintenance` |
| **Source Columns** | `machine_id`, `date_debut` |
| **Output** | Integer - count per machine |
| **Unit** | Count |
| **Business Interpretation** | High count = unreliable machine. Compare across machines of same age and type |
| **Dashboard Visual** | Bar chart |
| **Refresh** | Monthly |

---

### KPI-MNT-002 - Preventive Maintenance Ratio

| Field | Value |
|---|---|
| **Business Objective** | Proportion of planned vs unplanned maintenance |
| **Formula** | `COUNT(CASE WHEN m.type_maintenance IN ('Preventive','Changement huile','Nettoyage','Inspection','Changement liquide','Alignement machine') THEN 1 END) / COUNT(*) * 100` |
| **Source Tables** | `maintenance` |
| **Source Columns** | `type_maintenance` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | Target > 70%. Low ratio = reactive maintenance culture, higher costs, more unplanned downtime |
| **Typical Values** | 50-80% |
| **Dashboard Visual** | Gauge |
| **Refresh** | Monthly |

---

### KPI-MNT-003 - Corrective Maintenance Ratio

| Field | Value |
|---|---|
| **Business Objective** | Proportion of unplanned corrective interventions |
| **Formula** | `COUNT(CASE WHEN m.type_maintenance IN ('Corrective','Remplacement roulement') THEN 1 END) / COUNT(*) * 100` |
| **Source Tables** | `maintenance` |
| **Source Columns** | `type_maintenance` |
| **Output** | Decimal - percentage |
| **Unit** | % |
| **Business Interpretation** | Target < 30%. High ratio = unreliable machines or insufficient preventive program |
| **Typical Values** | 20-50% |
| **Dashboard Visual** | Gauge |
| **Refresh** | Monthly |

---

### KPI-MNT-004 - Machine Downtime (from Maintenance)

| Field | Value |
|---|---|
| **Business Objective** | Total downtime caused by maintenance events |
| **Formula** | `SUM(m.duree)` WHERE `m.machine_id = M` AND `m.date_debut` IN [period] |
| **Source Tables** | `maintenance` |
| **Source Columns** | `duree`, `machine_id`, `date_debut` |
| **Output** | Integer - total minutes |
| **Unit** | Minutes |
| **Business Interpretation** | Directly reduces availability for OEE calculation. Breakdown by type reveals root causes |
| **Dashboard Visual** | Stacked bar (by type) |
| **Refresh** | Monthly |

---

### KPI-MNT-005 - Mean Time Between Failures (MTBF)

| Field | Value |
|---|---|
| **Business Objective** | Average operating time between consecutive machine failures |
| **Formula** | `SUM(ep.temps_usinage_reel + ep.temps_reglage_reel) / COUNT(CASE WHEN m.type_maintenance IN ('Corrective','Remplacement roulement') THEN 1 END)` per machine |
| **Source Tables** | `execution_phase`, `maintenance` |
| **Source Columns** | `execution_phase.temps_usinage_reel`, `execution_phase.temps_reglage_reel`, `maintenance.type_maintenance`, `maintenance.machine_id` |
| **Output** | Decimal - hours of operation between failures |
| **Unit** | Hours |
| **Business Interpretation** | Higher = more reliable. Declining trend = machine aging. Used for replacement planning |
| **Typical Values** | 200-2000 hours |
| **Dashboard Visual** | Card + line chart (trend) |
| **Refresh** | Monthly |
| **Assumption** | Only Corrective and Remplacement roulement count as failures. Operating time from execution_phase (not calendar time) |

---

### KPI-MNT-006 - Mean Time To Repair (MTTR)

| Field | Value |
|---|---|
| **Business Objective** | Average duration of a corrective repair |
| **Formula** | `AVG(m.duree) WHERE m.type_maintenance IN ('Corrective','Remplacement roulement')` per machine |
| **Source Tables** | `maintenance` |
| **Source Columns** | `duree`, `type_maintenance` |
| **Output** | Decimal - average repair duration |
| **Unit** | Minutes |
| **Business Interpretation** | Lower = faster repairs (better spare parts availability, more skilled technicians) |
| **Typical Values** | 60-360 min |
| **Dashboard Visual** | Card + bar chart (by machine) |
| **Refresh** | Monthly |

---

### KPI-MNT-007 - Maintenance Cost per Machine

| Field | Value |
|---|---|
| **Business Objective** | Total maintenance expenditure per machine |
| **Formula** | `SUM(m.cout)` WHERE `m.machine_id = M` AND `m.date_debut` IN [period] |
| **Source Tables** | `maintenance` |
| **Source Columns** | `cout`, `machine_id`, `date_debut` |
| **Output** | Decimal - total EUR |
| **Unit** | EUR |
| **Business Interpretation** | High cost + old machine = replacement candidate. Track cost trends over time |
| **Dashboard Visual** | Bar chart + line chart (trend) |
| **Refresh** | Monthly |

---

### KPI-MNT-008 - Maintenance Frequency

| Field | Value |
|---|---|
| **Business Objective** | How often maintenance occurs per machine per month |
| **Formula** | `COUNT(*) / number_of_months` WHERE `m.machine_id = M` AND `m.date_debut` IN [period] |
| **Source Tables** | `maintenance` |
| **Source Columns** | `machine_id`, `date_debut` |
| **Output** | Decimal - events per month |
| **Unit** | events/month |
| **Business Interpretation** | High frequency = unreliable machine. Sudden increase = impending failure |
| **Dashboard Visual** | Line chart (trend per machine) |
| **Refresh** | Monthly |

---

## 8. Sensor KPIs

### KPI-SNS-001 - Temperature Status

| Field | Value |
|---|---|
| **Business Objective** | Monitor spindle temperature health |
| **Formula** | `CASE WHEN sd.temperature > 55 THEN 'CRITICAL' WHEN sd.temperature > 45 THEN 'WARNING' ELSE 'NORMAL' END` |
| **Source Tables** | `sensor_data` |
| **Source Columns** | `temperature` |
| **Output** | String - NORMAL, WARNING, CRITICAL |
| **Unit** | Category (deg C) |
| **Business Interpretation** | Normal: 20-40 deg C. Warning: > 45 = approaching limit. Critical: > 55 = stop machine |
| **Dashboard Visual** | Gauge (latest) + line chart (trend with threshold lines) |
| **Refresh** | Real-time |

---

### KPI-SNS-002 - Vibration Status

| Field | Value |
|---|---|
| **Business Objective** | Monitor machine vibration health |
| **Formula** | `CASE WHEN sd.vibration > 2.5 THEN 'CRITICAL' WHEN sd.vibration > 1.5 THEN 'WARNING' ELSE 'NORMAL' END` |
| **Source Tables** | `sensor_data` |
| **Source Columns** | `vibration` |
| **Output** | String - NORMAL, WARNING, CRITICAL |
| **Unit** | Category (mm/s) |
| **Business Interpretation** | Normal: 0.1-1.0. Warning: > 1.5 = bearing wear. Critical: > 2.5 = risk of damage |
| **Dashboard Visual** | Gauge + line chart with thresholds |
| **Refresh** | Real-time |

---

### KPI-SNS-003 - Spindle Load Status

| Field | Value |
|---|---|
| **Business Objective** | Monitor machine load |
| **Formula** | `CASE WHEN sd.charge_frappe > 90 THEN 'CRITICAL' WHEN sd.charge_frappe > 80 THEN 'WARNING' ELSE 'NORMAL' END` |
| **Source Tables** | `sensor_data` |
| **Source Columns** | `charge_frappe` |
| **Output** | String - NORMAL, WARNING, CRITICAL |
| **Unit** | Category (%) |
| **Business Interpretation** | Normal: 25-70%. Warning: > 80 = near capacity. Critical: > 90 = tool breakage risk |
| **Dashboard Visual** | Gauge + line chart |
| **Refresh** | Real-time |

---

### KPI-SNS-004 - Anomaly Composite Score

| Field | Value |
|---|---|
| **Business Objective** | Single composite indicator combining multiple sensor readings |
| **Formula** | `(temp_flag * 1) + (vib_flag * 2) + (load_flag * 1.5) + (rpm_flag * 1.5)` where each flag = 0 if NORMAL, 1 if WARNING, 2 if CRITICAL |
| **Source Tables** | `sensor_data`, `machine` |
| **Source Columns** | `temperature`, `vibration`, `charge_frappe`, `rpm`, `machine.rpm_max` |
| **Output** | Decimal - composite index (0-7 scale) |
| **Unit** | Index |
| **Business Interpretation** | Score >= 3 = MACHINE AT RISK. Triggers preventive maintenance check. Vibration weighted highest |
| **Dashboard Visual** | Gauge + heatmap (machine x time) |
| **Refresh** | Real-time |
| **Assumption** | RPM flag: CRITICAL if > 95% of rpm_max, WARNING if < 20% while RUNNING |

---

## 9. Cost KPIs

### KPI-CST-001 - Material Cost per OF

| Field | Value |
|---|---|
| **Business Objective** | Raw material cost for a production order |
| **Formula** | `p.poids * mat.prix_kg * of.quantite_produite` via `of.piece_id = p.piece_id` AND `p.matiere_id = mat.matiere_id` |
| **Source Tables** | `ordre_fabrication`, `piece`, `matiere` |
| **Source Columns** | `piece.poids`, `piece.matiere_id`, `matiere.prix_kg`, `ordre_fabrication.quantite_produite`, `ordre_fabrication.piece_id` |
| **Output** | Decimal - EUR |
| **Unit** | EUR |
| **Business Interpretation** | Largest cost component typically. Drives material purchasing decisions |
| **Dashboard Visual** | Card + bar chart (by OF, by material) |
| **Refresh** | Per OF |

---

### KPI-CST-002 - Tool Cost per OF

| Field | Value |
|---|---|
| **Business Objective** | Tool consumption cost for a production order |
| **Formula** | `SUM(eo.duree_utilisation / o.duree_vie_totale * o.cout_remplacement)` per OF |
| **Source Tables** | `execution_outil`, `outil`, `execution_phase` |
| **Source Columns** | `execution_outil.duree_utilisation`, `execution_outil.execution_id`, `outil.duree_vie_totale`, `outil.cout_remplacement`, `execution_phase.ordre_fabrication_id` |
| **Output** | Decimal - EUR |
| **Unit** | EUR |
| **Business Interpretation** | Fraction of tool lifetime consumed multiplied by replacement cost |
| **Dashboard Visual** | Card |
| **Refresh** | Per OF |

---

### KPI-CST-003 - Machining Cost per OF

| Field | Value |
|---|---|
| **Business Objective** | Cost of machine time for a production order |
| **Formula** | `SUM(ep.temps_usinage_reel + ep.temps_reglage_reel) / 60 * hourly_machine_rate` per OF |
| **Source Tables** | `execution_phase` |
| **Source Columns** | `temps_usinage_reel`, `temps_reglage_reel`, `ordre_fabrication_id` |
| **Output** | Decimal - EUR |
| **Unit** | EUR |
| **Business Interpretation** | hourly_machine_rate is an external parameter (30-80 EUR/h depending on machine type). Not stored in DB |
| **Dashboard Visual** | Card |
| **Refresh** | Per OF |
| **Assumption** | Machine hourly rates are external configuration parameters, not in the database. Default assumed: Tour CNC = 35 EUR/h, Centre usinage = 55 EUR/h, Fraiseuse = 50 EUR/h |

---

### KPI-CST-004 - Maintenance Cost by Machine

| Field | Value |
|---|---|
| **Business Objective** | Total maintenance expenditure per machine (same as KPI-MNT-007, referenced here for cost context) |
| **Formula** | `SUM(m.cout)` WHERE `m.machine_id = M` AND `m.date_debut` IN [period] |
| **Source Tables** | `maintenance` |
| **Source Columns** | `cout`, `machine_id`, `date_debut` |
| **Output** | Decimal - EUR |
| **Unit** | EUR |
| **Business Interpretation** | Part of total production cost. High cost relative to machine value = replacement candidate |
| **Dashboard Visual** | Bar chart + trend line |
| **Refresh** | Monthly |

---

### KPI-CST-005 - Cost per Part

| Field | Value |
|---|---|
| **Business Objective** | Unit cost of manufacturing one good piece |
| **Formula** | `(KPI-CST-001 + KPI-CST-002 + KPI-CST-003 + allocated KPI-CST-004) / (of.quantite_produite - of.quantite_rebut)` |
| **Source Tables** | Derived from KPI-CST-001 through KPI-CST-004, `ordre_fabrication` |
| **Source Columns** | `ordre_fabrication.quantite_produite`, `ordre_fabrication.quantite_rebut` |
| **Output** | Decimal - EUR per piece |
| **Unit** | EUR/pc |
| **Business Interpretation** | Key financial metric. Compare with piece.prix_revient for margin analysis |
| **Dashboard Visual** | Card + trend line |
| **Refresh** | Per OF |
| **Assumption** | Maintenance cost allocation to OF is proportional to machine time used by that OF |

---

## 10. Future KPIs - Phase 2

The following KPIs cannot be calculated with the current database schema. They require additional tables or data sources not yet implemented.

### KPI-FUT-001 - Inventory Turnover Rate

| Field | Value |
|---|---|
| **Reason for Phase 2** | Requires `mouvement_stock` table to track historical stock movements (entries, exits, consumption). Current schema only has snapshot stock levels |
| **Required Addition** | `mouvement_stock` table with `type_mouvement`, `quantite`, `date_mouvement`, `piece_id`/`matiere_id`/`outil_id` |
| **Formula (planned)** | `SUM(consumption_movements) / AVG(stock_level)` per period |

---

### KPI-FUT-002 - Stock Coverage (Days of Stock)

| Field | Value |
|---|---|
| **Reason for Phase 2** | Requires historical consumption rate over time. Current estimate (KPI-INV-005) is rough and does not account for waste |
| **Required Addition** | `mouvement_stock` table or production schedule forecasting |
| **Formula (planned)** | `current_stock / average_daily_consumption` |

---

### KPI-FUT-003 - Power Consumption Cost

| Field | Value |
|---|---|
| **Reason for Phase 2** | `sensor_data.puissance` exists but no electricity cost rate or energy meter mapping in the database |
| **Required Addition** | Configuration table for electricity rates (EUR/kWh) and machine power profiles |
| **Formula (planned)** | `SUM(puissance * interval_hours) * electricity_rate` per machine per period |

---

### KPI-FUT-004 - Overall Factory OEE

| Field | Value |
|---|---|
| **Reason for Phase 2** | KPI-OEE-004 works per machine. A plant-wide OEE requires weighted aggregation across all machines, which needs shift schedule data and planned production time per machine |
| **Required Addition** | Shift schedule configuration table, planned_production_time per machine per day |
| **Formula (planned)** | `SUM(available_time_all_machines) / SUM(planned_time_all_machines) * SUM(perf_all_machines) * SUM(quality_all_machines)` |

---

### KPI-FUT-005 - Planned Maintenance Compliance

| Field | Value |
|---|---|
| **Reason for Phase 2** | Requires a `maintenance_plan` table defining scheduled preventive maintenance dates. Current data only records actual maintenance events, not planned ones |
| **Required Addition** | `maintenance_plan` table with `prochaine_intervention` dates |
| **Formula (planned)** | `COUNT(on-time maintenance events) / COUNT(planned maintenance events) * 100` |

---

### KPI-FUT-006 - Scrap Cost

| Field | Value |
|---|---|
| **Reason for Phase 2** | Requires material cost + machining cost allocated to scrap parts specifically. Partially calculable but needs proper cost allocation logic |
| **Formula (planned)** | `SUM(nb_pieces_rebut * (material_cost_per_part + machining_cost_per_part))` |

---

### KPI-FUT-007 - Tool Cost per Part

| Field | Value |
|---|---|
| **Reason for Phase 2** | Requires linking tool consumption to specific parts, which needs the OF -> piece -> execution -> tool chain fully costed |
| **Formula (planned)** | `tool_cost_per_of / quantity_good_produced` |

---

## 11. Machine Learning Feature Mapping

This section describes how existing database columns and calculated KPIs will serve as inputs (features) or outputs (targets) for future ML models. No additional predictive KPIs are defined here.

---

### 11.1 Model: Scrap Prediction

| Field | Description |
|---|---|
| **Objective** | Predict whether a production execution will produce defective parts |
| **Target Variable** | `execution_phase.nb_pieces_rebut > 0` (binary classification) or `nb_pieces_rebut / nb_pieces_produites` (regression) |
| **Features** | |

| Feature | Source Table | Source Column | Type |
|---|---|---|---|
| Cutting speed | `execution_phase` | `vitesse_coupe` | Continuous |
| Feed rate | `execution_phase` | `avance` | Continuous |
| Depth of cut | `execution_phase` | `profondeur_passe` | Continuous |
| Tool wear at start | `execution_outil` | `usure_debut` | Integer |
| Tool wear at end | `execution_outil` | `usure_fin` | Integer |
| Tool remaining life % | `outil` | `duree_vie_restante / duree_vie_totale` | Continuous |
| Tool type | `outil` | `type_outil` | Categorical |
| Machine type | `machine` | `type` | Categorical |
| Machine age (days) | `machine` | `date_installation` | Derived |
| Operator competence | `operateur` | `niveau_competence` | Categorical |
| Material type | `matiere` | `type_matiere` | Categorical |
| Material nuance | `matiere` | `nuance` | Categorical |
| Part weight | `piece` | `poids` | Continuous |
| Phases in routing | `gamme_usinage` | `nb_phases` | Integer |
| Avg temperature (last 100) | `sensor_data` | Rolling AVG of `temperature` | Continuous |
| Avg vibration (last 100) | `sensor_data` | Rolling AVG of `vibration` | Continuous |
| Avg spindle load (last 100) | `sensor_data` | Rolling AVG of `charge_frappe` | Continuous |

---

### 11.2 Model: Machining Time Estimation

| Field | Description |
|---|---|
| **Objective** | Predict actual machining time from planned parameters and context |
| **Target Variable** | `execution_phase.temps_usinage_reel` |
| **Features** | |

| Feature | Source Table | Source Column | Type |
|---|---|---|---|
| Planned machining time | `phase_gamme` | `temps_usinage_prevu` | Integer |
| Planned setup time | `phase_gamme` | `temps_reglage_prevu` | Integer |
| Machine type | `machine` | `type` | Categorical |
| Machine RPM max | `machine` | `rpm_max` | Integer |
| Tool type | `outil` | `type_outil` | Categorical |
| Tool diameter | `outil` | `diametre` | Continuous |
| Material type | `matiere` | `type_matiere` | Categorical |
| Material density | `matiere` | `densite` | Continuous |
| Part weight | `piece` | `poids` | Continuous |
| Operator competence | `operateur` | `niveau_competence` | Categorical |
| Number of phases | `gamme_usinage` | `nb_phases` | Integer |

---

### 11.3 Model: Predictive Maintenance

| Field | Description |
|---|---|
| **Objective** | Predict when a machine will need maintenance |
| **Target Variable** | `maintenance.date_debut` (time-to-event) or binary: maintenance needed within next N days |
| **Features** | |

| Feature | Source Table | Source Column | Type |
|---|---|---|---|
| Rolling avg temperature (100 readings) | `sensor_data` | AVG of `temperature` | Continuous |
| Rolling std temperature | `sensor_data` | STDDEV of `temperature` | Continuous |
| Rolling avg vibration (100 readings) | `sensor_data` | AVG of `vibration` | Continuous |
| Rolling std vibration | `sensor_data` | STDDEV of `vibration` | Continuous |
| Rolling avg spindle load | `sensor_data` | AVG of `charge_frappe` | Continuous |
| Time since last maintenance | `maintenance` | MAX(`date_debut`) per machine | Derived |
| Machine age (days) | `machine` | `date_installation` | Derived |
| Cumulative running hours | `execution_phase` | SUM of `temps_usinage_reel + temps_reglage_reel` | Derived |
| Maintenance count (total) | `maintenance` | COUNT per machine | Derived |
| Maintenance cost (total) | `maintenance` | SUM of `cout` per machine | Derived |
| Corrective maintenance count | `maintenance` | COUNT WHERE type = 'Corrective' | Derived |

---

### 11.4 Model: Machine Failure Prediction

| Field | Description |
|---|---|
| **Objective** | Predict imminent machine breakdown |
| **Target Variable** | `sensor_data.statut_machine = 'BROKEN'` within next N sensor readings |
| **Features** | |

| Feature | Source Table | Source Column | Type |
|---|---|---|---|
| Temperature trend (slope) | `sensor_data` | Linear regression slope of `temperature` | Continuous |
| Vibration trend (slope) | `sensor_data` | Linear regression slope of `vibration` | Continuous |
| Anomaly composite score | `sensor_data` | KPI-SNS-004 computed value | Continuous |
| Time since last corrective maintenance | `maintenance` | Derived | Continuous |
| Machine utilization rate | `execution_phase` | Derived from running_time / available_time | Continuous |
| RPM stability (std dev) | `sensor_data` | STDDEV of `rpm` over window | Continuous |
| Power consumption trend | `sensor_data` | AVG of `puissance` over window | Continuous |
| Number of WARNING readings (last 100) | `sensor_data` | COUNT WHERE status != NORMAL | Integer |

---

### 11.5 Model: Tool Wear Prediction

| Field | Description |
|---|---|
| **Objective** | Predict remaining tool life given current usage patterns |
| **Target Variable** | `outil.duree_vie_restante` (regression) or `execution_outil.usure_fin` for next usage |
| **Features** | |

| Feature | Source Table | Source Column | Type |
|---|---|---|---|
| Tool type | `outil` | `type_outil` | Categorical |
| Tool diameter | `outil` | `diametre` | Continuous |
| Tool material | `outil` | `matiere_outil` | Categorical |
| Cumulative usage count | `execution_outil` | COUNT per outil_id | Derived |
| Recent wear rate (last 5 uses) | `execution_outil` | AVG(usure_fin - usure_debut) | Derived |
| Cutting speed | `execution_phase` | `vitesse_coupe` | Continuous |
| Feed rate | `execution_phase` | `avance` | Continuous |
| Depth of cut | `execution_phase` | `profondeur_passe` | Continuous |
| Material being machined | `piece` -> `matiere` | `type_matiere` | Categorical |
| Part weight | `piece` | `poids` | Continuous |

---

### 11.6 Model: Production Duration Prediction

| Field | Description |
|---|---|
| **Objective** | Predict total calendar duration of a production order |
| **Target Variable** | `ordre_fabrication.date_fin_reelle - ordre_fabrication.date_debut_reelle` (in days) |
| **Features** | |

| Feature | Source Table | Source Column | Type |
|---|---|---|---|
| Quantity demanded | `ordre_fabrication` | `quantite_demandee` | Integer |
| Number of phases in routing | `gamme_usinage` | `nb_phases` | Integer |
| Estimated total time | `gamme_usinage` | `duree_totale_estimee` | Integer |
| Number of distinct machines | `phase_gamme` | COUNT DISTINCT `machine_id` | Derived |
| Average operator competence | `operateur` | `niveau_competence` (encoded) | Categorical |
| Material type | `matiere` | `type_matiere` | Categorical |
| Machine current status | `machine` | `statut` | Categorical |
| Priority | `ordre_fabrication` | `priorite` | Categorical |

---

### 11.7 Model: Inventory Forecasting

| Field | Description |
|---|---|
| **Objective** | Forecast future stock levels and predict stockout dates |
| **Target Variable** | `stock_matiere.quantite_stock` or `stock_piece.quantite_stock` at future dates |
| **Features** | |

| Feature | Source | Column | Type |
|---|---|---|---|
| Current stock level | `stock_matiere` / `stock_piece` | `quantite_stock` | Continuous |
| Estimated daily consumption | `execution_phase` + `piece` | Derived from production data | Continuous |
| Number of active OFs requiring this material | `ordre_fabrication` | COUNT WHERE statut IN ('EN_ATTENTE','EN_COURS') | Integer |
| Reorder threshold | `stock_matiere` / `stock_outil` | `seuil_alerte` | Continuous |
| Historical consumption (weekly) | `execution_phase` + `piece` | SUM(poids * qty_produced) per week | Time-series |

---

### 11.8 Feature Engineering Summary

All features used by ML models are derived from these existing database columns:

| Feature Category | Source Tables | Key Columns |
|---|---|---|
| **Machining parameters** | `execution_phase` | `vitesse_coupe`, `avance`, `profondeur_passe` |
| **Machine state** | `machine` | `statut`, `date_installation`, `type`, `rpm_max` |
| **Sensor readings** | `sensor_data` | `temperature`, `vibration`, `rpm`, `charge_frappe`, `puissance` |
| **Tool state** | `outil`, `execution_outil` | `usure_actuelle`, `duree_vie_restante`, `usure_debut`, `usure_fin` |
| **Operator** | `operateur` | `niveau_competence`, `date_embauche` |
| **Material** | `matiere`, `piece` | `type_matiere`, `nuance`, `densite`, `poids` |
| **Routing complexity** | `gamme_usinage`, `phase_gamme` | `nb_phases`, `duree_totale_estimee` |
| **Production history** | `ordre_fabrication` | `quantite_demandee`, `statut`, dates |
| **Maintenance history** | `maintenance` | `type_maintenance`, `duree`, `cout`, `date_debut` |
| **Quality history** | `controle_qualite`, `cause_rebut` | `resultat`, `nb_non_conformes`, `categorie` |

No new tables, columns, or database modifications are required for ML feature extraction. All features can be computed from the existing operational schema.

---

## Appendix A - KPI Summary Table

| KPI ID | Name | Section | Unit | Refresh |
|---|---|---|---|---|
| KPI-PRD-001 | Estimated Machining Time | Production | min | On OF creation |
| KPI-PRD-002 | Real Machining Time | Production | min | After OF completion |
| KPI-PRD-003 | Estimated Setup Time | Production | min | On OF creation |
| KPI-PRD-004 | Real Setup Time | Production | min | After OF completion |
| KPI-PRD-005 | Total Production Time | Production | min | After OF completion |
| KPI-PRD-006 | Production Duration | Production | days | On OF completion |
| KPI-PRD-007 | Cycle Time | Production | min/pc | After execution |
| KPI-PRD-008 | Production Efficiency | Production | % | After OF completion |
| KPI-PRD-009 | Production Yield | Production | % | Daily |
| KPI-PRD-010 | Production Throughput | Production | pcs/h | Daily |
| KPI-PRD-011 | Capacity Utilization | Production | % | Daily |
| KPI-PRD-012 | OF Delay | Production | days | Weekly |
| KPI-QLT-001 | Scrap Rate | Quality | % | Daily |
| KPI-QLT-002 | First Pass Yield | Quality | % | Daily |
| KPI-QLT-003 | Conformity Rate | Quality | % | Daily |
| KPI-QLT-004 | Dimensional Accuracy | Quality | mm | Daily |
| KPI-QLT-005 | Surface Roughness | Quality | Ra (um) | Daily |
| KPI-QLT-006 | Defects by Machine | Quality | Count | Weekly |
| KPI-QLT-007 | Defects by Tool | Quality | Count | Weekly |
| KPI-QLT-008 | Defects by Material | Quality | Count | Monthly |
| KPI-QLT-009 | Defects by Operator | Quality | Count | Monthly |
| KPI-QLT-010 | Defects by Cause | Quality | Count | Monthly |
| KPI-QLT-011 | Defects by OF | Quality | Count | Weekly |
| KPI-OEE-001 | Availability | OEE | % | Daily |
| KPI-OEE-002 | Performance | OEE | % | Daily |
| KPI-OEE-003 | Quality Rate | OEE | % | Daily |
| KPI-OEE-004 | OEE | OEE | % | Daily |
| KPI-MCH-001 | Machine Running Time | Machine | min | Daily |
| KPI-MCH-002 | Machine Downtime | Machine | h | Daily |
| KPI-MCH-003 | Machine Maintenance Time | Machine | min | Monthly |
| KPI-MCH-004 | Machine Avg Cycle Time | Machine | min/pc | Weekly |
| KPI-MCH-005 | Machine Efficiency | Machine | % | Monthly |
| KPI-TOL-001 | Tool Wear per Execution | Tool | min | After execution |
| KPI-TOL-002 | Cumulative Tool Consumption | Tool | min | Weekly |
| KPI-TOL-003 | Tool Lifetime % | Tool | % | Weekly |
| KPI-TOL-004 | Tool Replacement Indicator | Tool | Category | Weekly |
| KPI-TOL-005 | Avg Tool Lifetime by Type | Tool | min | Monthly |
| KPI-TOL-006 | Tool Utilization Rate | Tool | % | Monthly |
| KPI-INV-001 | Stock Level (Parts) | Inventory | pcs | Daily |
| KPI-INV-002 | Stock Level (Materials) | Inventory | kg | Daily |
| KPI-INV-003 | Stock Level (Tools) | Inventory | pcs | Daily |
| KPI-INV-004 | Stock Status | Inventory | Category | Daily |
| KPI-INV-005 | Material Consumption | Inventory | kg | Weekly |
| KPI-INV-006 | Reorder Indicator | Inventory | Boolean | Daily |
| KPI-INV-007 | Stock Value (Parts) | Inventory | EUR | Monthly |
| KPI-MNT-001 | Maintenance Count | Maintenance | Count | Monthly |
| KPI-MNT-002 | Preventive Ratio | Maintenance | % | Monthly |
| KPI-MNT-003 | Corrective Ratio | Maintenance | % | Monthly |
| KPI-MNT-004 | Machine Downtime | Maintenance | min | Monthly |
| KPI-MNT-005 | MTBF | Maintenance | hours | Monthly |
| KPI-MNT-006 | MTTR | Maintenance | min | Monthly |
| KPI-MNT-007 | Maintenance Cost | Maintenance | EUR | Monthly |
| KPI-MNT-008 | Maintenance Frequency | Maintenance | events/month | Monthly |
| KPI-SNS-001 | Temperature Status | Sensor | Category | Real-time |
| KPI-SNS-002 | Vibration Status | Sensor | Category | Real-time |
| KPI-SNS-003 | Spindle Load Status | Sensor | Category | Real-time |
| KPI-SNS-004 | Anomaly Score | Sensor | Index | Real-time |
| KPI-CST-001 | Material Cost per OF | Cost | EUR | Per OF |
| KPI-CST-002 | Tool Cost per OF | Cost | EUR | Per OF |
| KPI-CST-003 | Machining Cost per OF | Cost | EUR | Per OF |
| KPI-CST-004 | Maintenance Cost per Machine | Cost | EUR | Monthly |
| KPI-CST-005 | Cost per Part | Cost | EUR/pc | Per OF |

**Total: 62 KPIs** (55 calculable now, 7 deferred to Phase 2)
