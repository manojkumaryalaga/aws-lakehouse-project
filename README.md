# AWS Lakehouse Data Pipeline 🏗️

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![AWS](https://img.shields.io/badge/AWS-Cloud-orange.svg)](https://aws.amazon.com/)
[![dbt](https://img.shields.io/badge/dbt-Core-red.svg)](https://www.getdbt.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-blue.svg)](https://www.sqlite.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML-green.svg)](https://xgboost.readthedocs.io/)
[![LightGBM](https://img.shields.io/badge/LightGBM-ML-brightgreen.svg)](https://lightgbm.readthedocs.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8-orange.svg)](https://scikit-learn.org/)

> **End-to-end AWS data lakehouse processing 1.37M+ NYC taxi records with automated ETL, quality validation, dimensional modeling, and 3 production ML models.**

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Architecture](#️-architecture)
- [Tech Stack](#️-tech-stack)
- [AWS Infrastructure](#-aws-infrastructure)
- [ETL Pipeline](#️-etl-pipeline)
- [dbt Dimensional Models](#-dbt-dimensional-models)
- [CloudWatch Monitoring](#-cloudwatch-monitoring)
- [ML Models](#-ml-models--nyc-taxi-intelligence-layer)
- [Data Quality Results](#-data-quality-results)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Author](#-author)

---

## 🎯 Overview

This project demonstrates **modern data lakehouse architecture** on AWS, implementing enterprise data engineering best practices end-to-end — from raw S3 ingestion through dbt dimensional modeling to a full **ML intelligence layer** with 3 production models.

| Stat | Value |
|------|-------|
| 📊 Raw records ingested | 1,369,765 |
| ✅ Clean records loaded | 1,220,127 |
| 🎯 Data quality pass rate | 89.1% |
| 🤖 ML models trained | 3 |
| ☁️ Cloud provider | AWS (S3, Glue, Athena, CloudWatch) |

---

## 🏛️ Architecture

```
NYC Taxi CSV (120 MB)
        │
        ▼
┌─────────────────┐
│  S3 Bronze      │  raw/yellow_tripdata_2021-01.csv
│  (Raw Layer)    │
└────────┬────────┘
         │  AWS Glue Crawler (auto-detects 18 columns)
         ▼
┌─────────────────┐
│  Glue Catalog   │  lakehouse_db.raw
│  + Athena       │  Serverless SQL · 1.076s · 120MB scanned
└────────┬────────┘
         │  Python ETL (pandas + boto3)
         ▼
┌─────────────────┐
│  S3 Silver      │  processed/yellow_tripdata_cleaned.csv
│  (Cleaned)      │  1,220,127 rows · 89.1% pass rate
└────────┬────────┘
         │  load_to_sqlite.py
         ▼
┌─────────────────┐
│  SQLite + dbt   │  fact_trips · dim_location
│  (Gold Layer)   │  dim_datetime · dim_payment
└────────┬────────┘
         │  nyc_taxi_ml/
         ▼
┌─────────────────┐
│  ML Layer       │  XGBoost · Isolation Forest · LightGBM
│  3 Models       │  Demand · Anomaly · Fare
└─────────────────┘
         │  CloudWatch
         ▼
┌─────────────────┐
│  Monitoring     │  DataQualityScore · RowsProcessed
│  + Alerting     │  LowDataQuality alarm
└─────────────────┘
```

---

## 🛠️ Tech Stack

**Cloud** — Amazon S3 · AWS Glue · Amazon Athena · CloudWatch · IAM

**Data** — Python 3.9+ · pandas · boto3 · dbt-core · SQLite

**ML** — XGBoost · LightGBM · scikit-learn · joblib · matplotlib

**DevOps** — GitHub Actions · Apache Airflow · VS Code

---

## ☁️ AWS Infrastructure

### S3 — `lakehouse-project-manoj`

Single bucket with 4 folders: `raw/` · `processed/` · `athena-results/` · `scripts/`

![S3 Bucket Structure](screenshots/Screenshot%20(192).png)

### AWS Glue — Schema Auto-Discovery

Glue Crawler `lakehouse-crawler` scanned S3 and auto-detected **18 columns** including `vendorid`, `tpep_pickup_datetime`, `trip_distance`, `pulocationid`, `fare_amount` and more.

![Glue Schema 18 Columns](screenshots/Screenshot%20(198).png)

Crawler state: **Ready · Succeeded** · Last run: April 4, 2026 · 1 table created in `lakehouse_db`

![Glue Crawler Succeeded](screenshots/Screenshot%20(202).png)

## 🔄 ETL Scripts — Production Pipeline

**Three Python scripts orchestrate data flow from raw S3 ingestion (1.37M records) to production warehouse with real-time monitoring — achieving 89.1% data quality in 45 seconds.**

---

### Pipeline Scripts

![ETL Scripts Directory](screenshots/Screenshot%20(227).png)

| Script | Purpose | Runtime |
|--------|---------|---------|
| `etl.py` | Extract from S3 → Validate (6 checks) → Clean → Write to S3 Silver | 30s |
| `load_to_sqlite.py` | Download cleaned data → Bulk insert 1.22M rows to SQLite | 12s |
| `cloudwatch_monitor.py` | Calculate quality metrics → Publish to CloudWatch | 3s |

---

### Successful Execution

![Pipeline Success](screenshots/Screenshot%20(228).png)

```python
✅ etl.py
   • Rows before: 1,369,765
   • Rows after:  1,220,127
   • Quality rate: 89.1%
   • Status: Cleaned data uploaded to S3 ✅

✅ load_to_sqlite.py  
   • Loading 1,220,127 rows into SQLite... Done! ✅
   • Insert rate: 101,677 rows/sec

✅ cloudwatch_monitor.py
   • Published 4 metrics to CloudWatch ✅
   • Alarm: LowDataQuality (Status: OK)
```

**Total Runtime:** 45 seconds | **Throughput:** 30,438 records/sec

---

### Data Quality Validation

| Check | Records Removed |
|-------|----------------|
| Null values | 78,432 |
| Duplicates | 12,891 |
| Invalid ranges (fare $0-$500, distance 0-100mi) | 45,219 |
| Type mismatches | 8,744 |
| Schema violations | 4,352 |
| **Total cleaned** | **149,638 (10.9%)** |

**Pass Rate: 89.1%** ✅

---

### dbt materialized views

Pipeline summary — **1,369,765 trips · $12.1 avg fare · $1.656B total revenue · 4.63 mi avg distance** — completed in **1.076 sec**, scanning 120.15 MB.

![dbt view](screenshots/Screenshot%20(213).png)

### Athena Queries

![Athena Top Zones](screenshots/Screenshot%20(207).png)
![Athena Top Zones](screenshots/Screenshot%20(206).png)
![Athena Top Zones](screenshots/Screenshot%20(209).png)
![Athena Top Zones](screenshots/Screenshot%20(208).png)

---

## ⚙️ dbt querying on modeled data

```
Rows before cleaning:  1,369,765
Rows after cleaning:   1,220,127
Cleaned data uploaded to S3 processed/ folder
Loading 1220127 rows into SQLite... Done!
```

![VS Code ETL Run](screenshots/Screenshot%20(196).png)

---

## 🗃️ dbt Dimensional Models

Star schema built with dbt-core (SQLite adapter). Models visible via Datasette at `127.0.0.1:8005`.

### `raw_taxi_trips` — 1,220,127 rows

![raw_taxi_trips](screenshots/Screenshot%20(195).png)

### `fact_trips` — 1,220,127 rows

![fact_trips](screenshots/Screenshot%20(211).png)

---

## 📡 CloudWatch Monitoring

Custom namespace **`LakehousePipeline`** with 4 metrics: `DataQualityScore` · `RowsAfterCleaning` · `RowsDropped` · `RowsProcessed`

![CloudWatch Metrics](screenshots/Screenshot%20(216).png)

Alarm **`LowDataQuality`** fires when `DataQualityScore < 80` for 1 datapoint within 5 minutes.

![CloudWatch Alarm](screenshots/Screenshot%20(218).png)

---

## 🤖 ML Models — NYC Taxi Intelligence Layer

All 3 models trained on **200,000 NYC taxi records** · Python 3.12 · Saved as `.joblib` + `.png` charts

```bash
cd nyc_taxi_ml
pip install -r requirements_ml.txt
python run_all_models.py
```

---

### Model 1 — Demand Forecasting (XGBoost)

**Goal**: Predict hourly trip count per pickup zone

**Features**: Lag features (1h / 2h / 3h / 24h / 168h) + rolling 24h & 7-day averages + hour / day / zone

| MAE | RMSE | R² | MAPE | Train rows | Zones modelled |
|-----|------|----|------|------------|----------------|
| 0.4347 trips/hr | 0.6313 trips/hr | 0.2589 | 29.41% | 117,351 | 20 |

`rolling_24h_avg` (importance 0.38) is the strongest predictor — recent demand drives future demand.

![Model 1 Demand Forecast](screenshots/Screenshot%20(221).png)

---

### Model 2 — Anomaly Detection (Isolation Forest)

**Goal**: Detect suspicious fares, impossible speeds, and fraudulent trips

**Features**: `fare_amount` · `trip_distance` · `speed_mph` · `fare_per_mile` · `tip_pct` · `is_overnight`

| Anomalies | Normal | Rate | Avg Score | High-fare | Impossible speed |
|-----------|--------|------|-----------|-----------|-----------------|
| 10,000 | 190,000 | 5.00% | 0.6441 | 500 | 472 |

**Key insight**: Overnight hours (10pm–6am) show **17–26% anomaly rate** vs 2–5% during daytime.

![Model 2 Anomaly Detection](screenshots/Screenshot%20(223).png)

---

### Model 3 — Fare Estimator (LightGBM)

**Goal**: Predict trip fare from distance, zone, time, and passenger features

**Features**: `trip_distance` · `trip_duration_min` · `pickup_hour` · `pickup_location_id` · `dropoff_location_id` · `pickup_dow` · rush hour flags

| MAE | RMSE | R² | Within $1 | Within $2 | Within $5 |
|-----|------|----|-----------|-----------|-----------|
| $1.16 | $1.44 | **0.9683** | 50.8% | 83.9% | **99.9%** |

Live demo predictions:

| Trip | Predicted Fare |
|------|---------------|
| Midtown → Downtown · 2.5mi · 8am rush | **$10.98** |
| JFK → Manhattan · 15mi · 11pm weekend | **$36.40** |
| Short trip · 0.8mi · midday | **$4.63** |

![Model 3 Fare Estimator](screenshots/Screenshot%20(225).png)

### Live Interactive Predictor

Input any trip parameters → instant LightGBM fare prediction with surge factor breakdown.

![Live Predictor](screenshots/Screenshot%20(220).png)

---

## 📊 Data Quality Results

| Metric | Value |
|--------|-------|
| Total raw records | 1,369,765 |
| Records failing validation | 149,638 (10.9%) |
| **Clean records loaded** | **1,220,127** |
| **Pass rate** | **89.1%** |

Validation checks applied: **Null · Duplicate · Schema · Data Type · Range · Format**

---

## 📁 Project Structure

```
aws-lakehouse-project/
├── .github/workflows/ci.yml         # GitHub Actions CI/CD
├── airflow/lakehouse_dag.py          # Airflow orchestration DAG
├── lakehouse_dbt/
│   ├── models/
│   │   ├── fact_trips.sql            # 1,220,127 rows
│   │   ├── dim_location.sql          # 260 rows
│   │   ├── dim_datetime.sql          # 877,702 rows
│   │   └── schema.yml
│   └── dbt_project.yml
├── lakehouse_sqlite/lakehouse.db     # SQLite data warehouse
├── nyc_taxi_ml/                      # ← ML Intelligence Layer
│   ├── run_all_models.py             # Runs all 3 models
│   ├── models/
│   │   ├── demand_forecast.py        # XGBoost
│   │   ├── anomaly_detection.py      # Isolation Forest
│   │   └── fare_estimator.py         # LightGBM
│   ├── utils/
│   │   ├── db_loader.py
│   │   └── pretty_print.py
│   └── outputs/                      # .joblib models + .png charts
├── scripts/
│   ├── etl.py
│   ├── load_to_sqlite.py
│   └── cloudwatch_monitor.py
├── crawler.json
├── glue-db.json
├── trust-policy.json
└── requirements.txt
```

---

## 🚀 Setup & Installation

### Prerequisites
- AWS Account with IAM permissions (S3, Glue, Athena, CloudWatch)
- Python 3.9+ · AWS CLI configured · dbt CLI · Git

```bash
# 1. Clone
git clone https://github.com/manojkumaryalaga/aws-lakehouse-project.git
cd aws-lakehouse-project

# 2. Install
pip install -r requirements.txt

# 3. Configure AWS
aws configure

# 4. Set up Glue
aws glue create-database --database-input file://glue-db.json
aws glue create-crawler --cli-input-json file://crawler.json

# 5. Run ETL
python scripts/etl.py
python scripts/load_to_sqlite.py

# 6. Run dbt
cd lakehouse_dbt && dbt run --profile lakehouse_sqlite

# 7. Run ML models
cd nyc_taxi_ml
pip install -r requirements_ml.txt
python run_all_models.py
```

---

## 🔮 Future Enhancements

- [ ] Snowflake migration (replace SQLite for production scale)
- [ ] AWS Kinesis real-time streaming ingestion
- [ ] SageMaker hosted ML endpoints
- [ ] Amazon QuickSight executive dashboards
- [ ] AWS Lake Formation data governance + lineage
- [ ] RAG / LLM natural language querying of trip data

---

## 👤 Author

**Manoj Kumar Yalaga**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-mky--sde-blue)](https://linkedin.com/in/mky-sde)
[![GitHub](https://img.shields.io/badge/GitHub-manojkumaryalaga-black)](https://github.com/manojkumaryalaga)
[![Email](https://img.shields.io/badge/Email-manojkyalaga%40gmail.com-red)](mailto:manojkyalaga@gmail.com)

📍 Hollywood, Florida

---

**⭐ If you find this project useful, please give it a star!**

---

**Project Stats:**
- 📊 Records Processed: 1,369,765
- ✅ Data Quality Rate: 89.1%
- 🤖 ML Models: 3 (XGBoost + Isolation Forest + LightGBM)
- ☁️ AWS: S3 · Glue · Athena · CloudWatch
- 🔄 Pipeline Status: Active · Last Updated: May 2026
