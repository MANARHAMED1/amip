# AMIP — AMM Manufacturing Intelligence Platform

> End-to-end  platform simulating a real **CNC machining workshop**.
> Generates a realistic industrial dataset (~1.09M rows), loads it into **PostgreSQL**, transforms it into a **Data Warehouse star schema**, serves it through a **FastAPI** REST API with **7 trained ML models**, and visualizes it with a **React** frontend and a **Streamlit** BI dashboard.

![Database](https://img.shields.io/badge/PostgreSQL-16-blue) ![API](https://img.shields.io/badge/API-FastAPI-brightgreen) ![ML](https://img.shields.io/badge/ML-XGBoost-orange) ![Frontend](https://img.shields.io/badge/Frontend-React%2019-blueviolet) ![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-red) ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Dataset](#dataset)
- [Database Schema](#database-schema)
- [Data Warehouse](#data-warehouse)
- [REST API](#rest-api)
- [Machine Learning Models](#machine-learning-models)
- [Frontend](#frontend)
- [BI Dashboard](#bi-dashboard)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [License](#license)

---

## Overview

**AMM (Atelier Micro-Mécanique)** is a precision CNC machining workshop. This platform simulates the complete industrial lifecycle of the shop:

- **6** workshop sectors (turning, milling, precision machining, quality, maintenance)
- **12** real CNC machines (HANQI-CNC, Hartford, FANUC controllers)
- **50** operators, **40** raw materials, **150** tools, **300** finished parts
- **~1.09M** rows of realistic operational data: production orders, phase executions, quality inspections, maintenance records, and **1M IoT sensor readings**

The platform demonstrates the full modern data stack: realistic data generation → normalized PostgreSQL database → dimensional ETL into a star-schema Data Warehouse → analytics REST API → predictive ML models → real-time BI dashboards.

---

## Features

### Data Engineering
- **19-table normalized PostgreSQL schema** (3NF) with foreign keys, constraints, and performance indexes
- **1,087,211 rows** of coherent industrial data (sensor time-series, production, quality, maintenance)
- **Star-schema Data Warehouse** (`dwh` schema): 9 dimensions + 5 fact tables + 7 analytics views
- **OEE (Overall Equipment Effectiveness)** computed at the phase level (availability × performance × quality)
- **ETL pipeline** that populates the warehouse from the transactional database
- **Docker Compose** deployment for the whole stack

### Backend & API
- **FastAPI** REST API with **JWT authentication** and role-based users
- 10 route groups: executive KPIs, machines, production, quality, inventory, tools, maintenance, sensors, and **Excel/PDF report export**
- **WebSocket** live notifications + **SMTP email alerts** for critical events (machine downtime, stock thresholds, quality issues)
- Swagger interactive docs at `/docs`

### Machine Learning (7 models)
| # | Model | Type |
|---|-------|------|
| ML-01 | **Scrap Prediction** | XGBoost Classifier |
| ML-02 | **Machining Time Estimation** | XGBoost Regressor |
| ML-03 | **Predictive Maintenance** (days-until-failure) | XGBoost Regressor |
| ML-04 | **Machine Anomaly Detection** | IsolationForest |
| ML-05 | **Tool Wear Prediction** (remaining useful life) | XGBoost Regressor |
| ML-06 | **Production Duration Prediction** | XGBoost Regressor |
| ML-07 | **Inventory Forecasting** (stock-out date) | Trend projection |

### Frontend & Dashboard
- **React 19 + Vite + TypeScript + Tailwind** SPA: executive overview, machines, production, quality, inventory, tools, maintenance, sensors, and ML pages
- **Streamlit BI dashboard** (French UI) with role-based login, global filters, and live charts

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        DATA GENERATION (offline)                          │
│   generated_data/*.csv  ── 19 CSV files, ~1.09M rows (committed in repo)  │
└───────────────────────────────┬───────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          POSTGRESQL (OLTP)                                │
│                database/schema.sql  ─ 19 normalized tables               │
└───────────────────────────────┬───────────────────────────────────────────┘
                                │ ETL (etl/run_etl.py)
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    DATA WAREHOUSE (OLAP, schema `dwh`)                     │
│            warehouse/schema.sql  ─ star schema: 9 dims + 5 facts          │
│            warehouse/views.sql   ─ 7 analytics views (OEE, scrap, ...)     │
└───────────────────────────────┬───────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│              FASTAPI REST API  +  ML MODELS (api/)                         │
│        JWT auth, 10 routers, WebSocket alerts, Excel/PDF reports           │
└───────────────┬───────────────────────────────┬───────────────────────────┘
                ▼                               ▼
┌──────────────────────────────┐   ┌──────────────────────────────┐
│   REACT FRONTEND (frontend/) │   │   STREAMLIT DASHBOARD         │
│   Vite + TS + Tailwind       │   │   (dashboard/)  - French UI   │
└──────────────────────────────┘   └──────────────────────────────┘
```

---

## Project Structure

```
amip/
├── api/                        # FastAPI backend
│   ├── main.py                 # App entrypoint (routers + WebSocket + lifespan)
│   ├── auth.py                 # JWT login / verify token
│   ├── database.py             # psycopg2 connection helpers
│   ├── ws_manager.py           # WebSocket notifications + alert background task
│   ├── ml/
│   │   ├── train.py            # Trains all 7 ML models (from the DB)
│   │   ├── predict.py          # Model inference helpers
│   │   └── models/             # Trained .joblib artifacts + metrics.json
│   └── routers/                # executive, machine, production, quality,
│                               # inventory, tool, maintenance, sensors, reports
├── backend/
│   └── Dockerfile
├── config/
│   └── settings.py             # Shared configuration constants
├── dashboard/                  # Streamlit BI dashboard (French UI)
│   ├── app.py                  # Entrypoint + login + global layout
│   ├── components.py           # Sidebar, filters, alerts banner
│   ├── api_client.py           # API calls
│   ├── charts.py, icons.py
│   └── modules/                # executive, machine, production, quality,
│                               # inventory, tool, maintenance, sensors
├── database/
│   ├── schema.sql              # PostgreSQL DDL - all 19 tables + indexes
│   └── data_inserts.sql        # [not committed] full INSERT dump (~106 MB,
│                               # exceeds GitHub's 100 MB file limit)
├── docker/
│   ├── init-all.sh             # DB bootstrap (auto-loads CSVs if the SQL dump is absent)
│   ├── init.sql                # amip_user table + default admin/viewer accounts
│   ├── 01b-fix-actif.sql       # BOOLEAN → INTEGER compatibility fix
│   └── 06-run-remaining.sh
├── docs/                       # ER diagram, data dictionary, KPI specs, dashboards
├── etl/                        # ETL pipeline (OLTP → warehouse)
│   ├── run_etl.py              # Orchestrator (waits for DB, runs ETL)
│   ├── populate_dwh.py         # Populates star-schema dimensions + facts
│   └── Dockerfile
├── frontend/                   # React 19 + Vite + TypeScript SPA
│   └── src/pages/              # Login, Overview, Machine, Production, Quality,
│                               # Inventory, Tool, Maintenance, Sensors, ML
├── generated_data/             # 19 CSV datasets (committed) - ~1.09M rows total
├── tests/                      # Data + DB validation scripts
├── warehouse/
│   ├── schema.sql              # Star schema (schema `dwh`)
│   └── views.sql               # OEE, scrap, quality, sensor, maintenance views
├── docker-compose.yml          # db + backend + frontend + etl + mailhog
├── .env.example                # Environment variable template
└── requirements.txt
```

> **Note:** The data **generator** scripts (`generator/`) are intentionally **not** committed to this repository. The generated dataset is provided directly as CSV files in [`generated_data/`](generated_data). To rebuild the dataset yourself, run the original generator and convert the CSVs with `generator/csv_to_sql.py`.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Database | PostgreSQL 16 |
| API | FastAPI, Uvicorn, psycopg2, PyJWT, bcrypt |
| ML | scikit-learn, XGBoost, joblib |
| Frontend | React 19, Vite 6, TypeScript 5, Tailwind CSS, Recharts |
| BI Dashboard | Streamlit, Plotly |
| Reports | ReportLab (PDF), openpyxl (Excel) |
| Data | pandas, numpy |
| Deployment | Docker, Docker Compose |

---

## Dataset

All data is provided as **CSV files** in `generated_data/` (committed to the repo). The full SQL INSERT dump (`database/data_inserts.sql`, ~106 MB) exceeds GitHub's per-file limit and is therefore **not** committed — the Docker bootstrap automatically loads the CSVs via `\copy` instead.

| # | Table | Description | Rows |
|---|-------|-------------|------|
| 1 | `secteur` | Workshop sectors | 6 |
| 2 | `machine` | CNC machines | 12 |
| 3 | `operateur` | Operators / workers | 50 |
| 4 | `matiere` | Raw materials | 40 |
| 5 | `outil` | Tools | 150 |
| 6 | `stock_outil` | Tool inventory | 150 |
| 7 | `piece` | Finished parts | 300 |
| 8 | `programme_usinage` | CNC programs | 400 |
| 9 | `gamme_usinage` | Machining routings | 500 |
| 10 | `phase_gamme` | Routing phases | 2,500 |
| 11 | `ordre_fabrication` | Production orders | 5,000 |
| 12 | `execution_phase` | Phase executions | 25,000 |
| 13 | `execution_outil` | Tool usage | 25,000 |
| 14 | `cause_rebut` | Scrap causes | 12 |
| 15 | `controle_qualite` | Quality inspections | 25,000 |
| 16 | `maintenance` | Maintenance records | 3,000 |
| 17 | `sensor_data` | IoT sensor readings | 1,000,000 |
| 18 | `stock_piece` | Parts inventory | 300 |
| 19 | `stock_matiere` | Material inventory | 40 |
| | | **Total** | **~1,089,600** |

**Data coherence:** realistic 6:00–18:00 machine schedules, monotonically increasing tool wear, gradually evolving sensor values, quality defects correlated with tool wear, realistic maintenance costs, and production orders that respect routing and part dependencies.

---

## Database Schema

The **OLTP schema** (`database/schema.sql`) is fully normalized (3NF) with:

- Foreign keys on every relationship
- `CHECK` constraints on all business rules (statuses, quantities, machine specs)
- Performance indexes on all `WHERE`/`JOIN` columns (critical for the 1M-row sensor table)

**Design rules:**
- No direct `MACHINE`–`TOOL` relationship — `PHASE_GAMME` defines *planned* machine + tool, while `EXECUTION_PHASE` records the *actual* machine + tool.
- No circular dependencies.

See [docs/er_diagram.md](docs/er_diagram.md) for the Mermaid ER diagram and [docs/data_dictionary.xlsx](docs/data_dictionary.xlsx) for the full data dictionary.

---

## Data Warehouse

The `dwh` schema (OLAP) is a classic **star schema**:

**Dimensions (9):** `dim_date`, `dim_machine`, `dim_part`, `dim_material`, `dim_tool`, `dim_sector`, `dim_production_order`, `dim_operateur`, `dim_maintenance_type`, `dim_quality_result`

**Facts (5):** `fact_production`, `fact_execution` (with **OEE**), `fact_quality`, `fact_sensors`, `fact_maintenance`

**Analytics views (7):** `v_oee_machine_daily`, `v_oee_monthly`, `v_scrap_by_part`, `v_maintenance_cost`, `v_production_summary`, `v_quality_by_cause`, `v_sensor_summary`

The ETL pipeline (`etl/populate_dwh.py`) deletes and rebuilds the dimensions/facts idempotently, computing KPIs such as scrap rate, yield, and OEE.

---

## REST API

Base URL: `http://localhost:8000` · Interactive docs at `http://localhost:8000/docs`

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/login` | POST | Returns a JWT (24h expiry) |
| `/api/auth/me` | GET | Current user profile |

### Route groups
| Group | Base path | Highlights |
|-------|-----------|------------|
| Executive | `/api/executive` | KPIs, machine status, alerts, production trend, OEE by machine, scrap by family |
| Machine | `/api/machine` | Machine list/details, performance, OEE history, maintenance, sensors, tool history, **anomaly detection** |
| Production | `/api/production` | Order KPIs/list, order phases, efficiency, **duration prediction** |
| Quality | `/api/quality` | Quality KPIs, causes, by machine/operator/part/material, evolution, **scrap prediction** |
| Inventory | `/api/inventory` | Overview, stock by type, alerts, consumption trend, **stock-out forecast** |
| Tools | `/api/tool` | Tool list, detail, **wear prediction** |
| Maintenance | `/api/maintenance` | List, KPIs, cost evolution, next maintenance |
| Sensors | `/api/sensors` | Live values, stats, history, heatmaps, correlation |
| Reports | `/api/reports` | **Excel & PDF** exports for quality, maintenance, production |

**Realtime:** `ws://localhost:8000/ws/notifications` (WebSocket) + SMTP email alerts for critical events.

---

## Machine Learning Models

Training: `python -m api.ml.train` (reads directly from PostgreSQL, saves to `api/ml/models/`). Inference is exposed through the `/api/machine/{code}/anomaly`, `/api/quality/scrap-prediction`, `/api/production/prediction/duration`, `/api/tool/{code}/wear-prediction`, and `/api/inventory/stockout-forecast` endpoints.

Pre-trained artifacts are committed in `api/ml/models/` (`.joblib` + feature lists + `metrics.json`).

---

## Frontend

React 19 SPA (Vite + TypeScript + Tailwind). Pages:

- **Login** — JWT authentication
- **Overview** — executive KPIs, alerts, production vs plan, OEE by machine
- **Machine** — per-machine performance, OEE history, maintenance timeline, sensor trends, anomaly
- **Production** — order list, phases, efficiency, duration prediction
- **Quality** — conformité, scrap causes, by machine/operator/material, scrap prediction
- **Inventory** — stock overview, alerts, stock-out forecast
- **Tool** — tool wear, remaining life
- **Maintenance** — records, costs, next maintenance
- **Sensors** — live sensor table, heatmaps, correlations
- **ML** — model cards and metrics

---

## BI Dashboard

Streamlit app (French UI) in `dashboard/`:

- Role-based **login** (JWT against the API)
- Sidebar navigation: Vue d'ensemble (overview), Machines, Production, Qualité, Inventaire, Outillage, Maintenance
- Global date/machine filters, critical-alerts banner, KPI cards, Plotly charts

---

## Getting Started

### Option 1 — Docker Compose (recommended)

Prerequisites: [Docker](https://docs.docker.com/get-docker/) with Compose.

```bash
git clone <your-repo-url>
cd amip

# 1. Configure environment
cp .env.example .env        # adjust passwords / SMTP if needed

# 2. Start the whole stack (PostgreSQL + ETL + API + Frontend + MailHog)
docker compose up --build -d
```

The DB bootstrap (`docker/init-all.sh`) creates the schema, loads the data (from `data_inserts.sql` if present, otherwise **directly from the CSVs**), builds the warehouse, and creates the default users.

| Service | URL |
|---------|-----|
| Frontend | http://localhost |
| API docs | http://localhost:8000/docs |
| API health | http://localhost:8000/health |
| MailHog | http://localhost:8025 |

### Option 2 — Manual / local development

#### 1. Database (PostgreSQL)

```bash
# Create the database
psql -U postgres -c "CREATE DATABASE amip;"

# Load schema
psql -U postgres -d amip -f database/schema.sql
psql -U postgres -d amip -f docker/01b-fix-actif.sql

# Load data — Option A: direct CSV import (CSV headers match the schema)
for f in secteur machine operateur matiere outil stock_outil piece \
         programme_usinage gamme_usinage phase_gamme ordre_fabrication \
         execution_phase execution_outil cause_rebut controle_qualite \
         maintenance sensor_data stock_piece stock_matiere; do
  psql -U postgres -d amip -c "\copy $f FROM 'generated_data/$f.csv' WITH CSV HEADER;"
done

# Load data — Option B: with the full SQL dump (if you generated it locally)
psql -U postgres -d amip -f database/data_inserts.sql
```

#### 2. Backend + ML models

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

# Optional: retrain the 7 ML models from the DB
python -m api.ml.train

# Start the API
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

#### 3. Data Warehouse (optional)

```bash
psql -U postgres -d amip -f warehouse/schema.sql
psql -U postgres -d amip -f warehouse/views.sql
python etl/run_etl.py        # or: python etl/populate_dwh.py
```

#### 4. Frontend

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173
# production build: npm run build && npm run preview
```

#### 5. BI Dashboard

```bash
streamlit run dashboard/app.py    # http://localhost:8501
```

### Default accounts

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Administrator |
| `viewer` | `viewer123` | Viewer (read-only) |

---

## Configuration

All secrets/credentials are read from environment variables (see [.env.example](.env.example)):

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | `amip` / `postgres` / `change_me_in_production` | PostgreSQL DB container |
| `AMIP_DB_HOST` / `AMIP_DB_PORT` | `db` / `5432` | Backend DB connection |
| `AMIP_DB_NAME` / `AMIP_DB_USER` / `AMIP_DB_PASSWORD` | `amip` / `postgres` / `change_me_in_production` | Backend DB credentials |
| `AMIP_JWT_SECRET` | random | JWT signing secret |
| `SMTP_HOST` / `SMTP_PORT` | `mailhog` / `1025` | Outbound email server |
| `SMTP_USER` / `SMTP_PASSWORD` | empty | SMTP credentials (Gmail app password) |
| `NOTIFY_EMAIL` | `admin@amm.local` | Alert recipient |

> **Security:** never commit real credentials. Rotate any key you may have previously committed to a public repo.

---

## Documentation

All specifications live in [`docs/`](docs):

- [ER Diagram (Mermaid)](docs/er_diagram.md)
- [Data Dictionary (Excel)](docs/data_dictionary.xlsx)
- [KPI Specification](docs/kpi_specification.md) + [KPI Catalog](docs/kpi_catalog.md)
- [Dashboard Specification](docs/dashboard_specification.md)
- [Sample data (Excel)](docs/amip_data.xlsx)

---

## License

This project is provided for educational and demonstration purposes.
