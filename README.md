# IRIS-Airflow-Provider 
## Overview

This project demonstrates an implementation of InterSystems IRIS integration with Apache Airflow. It contains:

- A minimal **IRIS Airflow provider** (hook + operator) that uses `sqlalchemy-iris`.
- **Three DAGs**:
  1. HL7 ingestion pipeline (file → parse → IRIS table).
  2. FHIR resource count & export (calls IRIS FHIR endpoints and produces a CSV).
  3. Vector search demo (store embeddings in IRIS and run nearest-neighbor queries).
- A Docker Compose setup to run IRIS and Airflow locally for development/demo.

--

## Why Airflow + IRIS?

### What is Apache Airflow?
Apache Airflow is an open-source workflow orchestration and scheduling platform that defines workflows as code (Python DAGs). It is widely used to build, schedule, and monitor data pipelines. :contentReference[oaicite:10]{index=10}

### Advantages of using Airflow with IRIS
- **Orchestration**: schedule and monitor ETL, HL7/FHIR conversions, and analytics tasks that involve IRIS.
- **Reproducibility**: pipelines are defined in code (DAGs) — easy to version and test.
- **Extensibility**: create custom hooks/operators to reuse IRIS connectivity across DAGs.
- **Interoperability**: combine IRIS’s healthcare features (FHIR, HL7, vector search) with Airflow’s scheduling and observability. :contentReference[oaicite:11]{index=11}

---

## What this repo contains
- `dags/providers/iris/iris_hook.py` — simple SQLAlchemy-based hook (uses `sqlalchemy-iris`)
- `dags/providers/iris/iris_operator.py` — query operator for IRIS
- `dags/hl7_ingest_dag.py`
- `dags/fhir_count_and_export_dag.py`
- `dags/vector_search_demo_dag.py`
- `docker-compose.yml` — to run IRIS + Airflow in development (example)
- `README.md` (this file)

---

## Prerequisites

- Docker & Docker Compose
- `python >= 3.10` (for local scripts)
- `pip install -r requirements.txt` for any locally-run helpers (optional)

**Python packages used**
- `sqlalchemy-iris` (IRIS dialect for SQLAlchemy). See usage and examples in the package docs. :contentReference[oaicite:12]{index=12}
- `requests`, `pandas`, etc., for helper scripts.

---

## Setup & Run (development)

1. Clone this repo.
2. Edit `docker-compose.yml` network/hostnames if needed. Ensure Airflow can reach IRIS at `iris:1972` or `host.docker.internal:1972`.
3. Start containers:
   ```bash
   docker-compose up --build -d
