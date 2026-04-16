# AWS Lakehouse Data Pipeline 🏗️

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![AWS](https://img.shields.io/badge/AWS-Cloud-orange.svg)](https://aws.amazon.com/)
[![dbt](https://img.shields.io/badge/dbt-Core-red.svg)](https://www.getdbt.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-blue.svg)](https://www.sqlite.org/)

> **End-to-end AWS data lakehouse processing 1.37M+ NYC taxi records with automated ETL, quality validation, and dimensional modeling.**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Key Features](#key-features)
- [Data Quality Results](#data-quality-results)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [What I Learned](#what-i-learned)
- [Future Enhancements](#future-enhancements)

---

## 🎯 Overview

This project demonstrates **modern data lakehouse architecture** on AWS with local data warehouse capabilities, implementing enterprise data engineering best practices:

✅ **Multi-layer data architecture** (Bronze → Silver → Gold)  
✅ **Automated ETL pipelines** with comprehensive data quality validation  
✅ **Dimensional modeling** using dbt for analytics-ready datasets  
✅ **Workflow orchestration** with Apache Airflow  
✅ **Infrastructure as Code** for AWS resource provisioning  
✅ **CI/CD integration** with automated testing  

### Dataset

**NYC Taxi Trip Records** - 1.37M rows of real-world transportation data including:
- Trip timestamps and durations
- Pickup/dropoff locations (latitude/longitude)
- Fare amounts and payment types
- Distance traveled and passenger counts

### Business Value

This pipeline enables:
- **Data Quality Assurance**: 89.1% validation pass rate with automated checks
- **Analytics-Ready Data**: Star schema modeling for efficient querying
- **Scalable Architecture**: Cloud-native design ready for production scaling
- **Reproducible Workflows**: IaC and orchestration for consistent deployments

---

## 🏛️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                   AWS LAKEHOUSE ARCHITECTURE                      │
└──────────────────────────────────────────────────────────────────┘

                           ┌─────────────┐
                           │  Raw Data   │
                           │ (NYC Taxi)  │
                           │  CSV Files  │
                           └──────┬──────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │   S3 Bronze Layer        │
                    │   (Raw Data Storage)     │
                    │   lakehouse-bronze/      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   AWS Glue Crawler       │
                    │   (Auto Schema Discovery)│
                    │   • Scans S3 data        │
                    │   • Detects schema       │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │  AWS Glue Data Catalog   │
                    │  (Metadata Repository)   │
                    │  • Table definitions     │
                    │  • Column types          │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │    Amazon Athena         │
                    │  (SQL Query Engine)      │
                    │  • Serverless queries    │
                    │  • S3 data access        │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │  Python ETL Pipeline     │
                    │  ┌────────────────────┐  │
                    │  │ Data Quality Checks│  │
                    │  ├────────────────────┤  │
                    │  │ • Null validation  │  │
                    │  │ • Duplicate removal│  │
                    │  │ • Schema checks    │  │
                    │  │ • Type enforcement │  │
                    │  │ • Range validation │  │
                    │  └────────────────────┘  │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   S3 Silver Layer        │
                    │   (Cleaned Data)         │
                    │   lakehouse-silver/      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   SQLite Database        │
                    │   (Local Data Warehouse) │
                    │   lakehouse.db           │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   dbt Transformations    │
                    │  ┌────────────────────┐  │
                    │  │ Staging Models     │  │
                    │  │ • stg_taxi_trips   │  │
                    │  ├────────────────────┤  │
                    │  │ Dimensional Models │  │
                    │  │ • fact_trips       │  │
                    │  │ • dim_location     │  │
                    │  │ • dim_datetime     │  │
                    │  │ • dim_payment      │  │
                    │  └────────────────────┘  │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   S3 Gold Layer          │
                    │   (Analytics-Ready)      │
                    │   lakehouse-gold/        │
                    └──────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                          │
└──────────────────────────────────────────────────────────────────┘

    ┌────────────────────┐          ┌─────────────────────┐
    │  Apache Airflow    │          │   CloudWatch        │
    │  • DAG Scheduling  │          │   • Monitoring      │
    │  • Task Deps       │          │   • Logging         │
    │  • Error Handling  │          │   • Alerts          │
    └────────────────────┘          └─────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                         CI/CD AUTOMATION                          │
└──────────────────────────────────────────────────────────────────┘

              ┌──────────────────────────────┐
              │     GitHub Actions           │
              │  • Automated Testing         │
              │  • Code Validation           │
              │  • Deployment Pipeline       │
              └──────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Cloud Services (AWS)
- **Amazon S3** - Multi-layer data lake (Bronze/Silver/Gold)
- **AWS Glue Crawler** - Automated schema discovery and cataloging
- **AWS Glue Data Catalog** - Centralized metadata repository
- **Amazon Athena** - Serverless SQL query engine for S3 data
- **AWS CloudWatch** - Monitoring and logging
- **AWS IAM** - Security and access management

### Data Storage & Warehouse
- **SQLite 3** - Lightweight relational database for local development
  - Zero configuration required
  - Serverless operation
  - ACID compliance
  - Perfect for development and testing

### Data Processing & Transformation
- **Python 3.9+** - Core ETL pipeline
  - `pandas` - Data manipulation and analysis
  - `boto3` - AWS SDK for Python
  - `awswrangler` - Pandas integration with AWS services
  - `sqlite3` - SQLite database interface
- **SQL** - Data querying and transformations
- **dbt (Data Build Tool)** - SQL-based dimensional modeling
  - dbt-core with SQLite adapter
  - Star schema implementation
  - Data quality testing framework

### Orchestration & Workflow
- **Apache Airflow** - Workflow orchestration and scheduling
  - DAG-based pipeline management
  - Task dependency handling
  - Retry logic and monitoring

### Development & CI/CD
- **Git/GitHub** - Version control
- **GitHub Actions** - CI/CD automation

---

## ✨ Key Features

### 1. **Medallion Architecture (Bronze → Silver → Gold)**
```
Raw Data → Validated Data → Analytics-Ready Data
```
- **Bronze Layer (S3)**: Immutable raw data from source
- **Silver Layer (S3)**: Cleaned, validated, deduplicated data
- **Gold Layer (S3 + SQLite)**: Business-level aggregations and star schema

### 2. **Comprehensive Data Quality Framework**

Automated validation pipeline checking:
- ✅ **Null Value Handling** - Identifies and handles missing critical fields
- ✅ **Duplicate Detection** - Removes duplicate trip records
- ✅ **Schema Validation** - Enforces expected column structure and types
- ✅ **Data Type Checks** - Validates numeric, string, and timestamp formats
- ✅ **Business Rules** - Validates fare amounts, distances, timestamps

**Result**: 89.1% of records pass all validation checks

### 3. **Dimensional Modeling with dbt**

Star schema design optimized for analytical queries:
- **Fact Table**: `fact_trips` - Grain: one row per trip
- **Dimension Tables**:
  - `dim_location` - Pickup/dropoff geographic data
  - `dim_datetime` - Trip date/time breakdowns
  - `dim_payment` - Payment type classifications

**Benefits**:
- Optimized query performance
- Intuitive business logic layer
- Reusable SQL transformations
- Built-in data quality tests

### 4. **Serverless Query Engine**

Amazon Athena enables:
- SQL queries directly on S3 data
- Zero infrastructure management
- Pay-per-query pricing
- Integration with Glue Data Catalog

### 5. **Automated Workflow Orchestration**

Apache Airflow provides:
- Scheduled pipeline execution
- Task dependency management
- Automatic retries on failure
- Monitoring and alerting
- Visual workflow tracking

### 6. **Infrastructure as Code**

JSON-based AWS configurations:
- Glue Database definition (`glue-db.json`)
- Glue Crawler configuration (`crawler.json`)
- IAM trust policies (`trust-policy.json`)
- Reproducible deployments
- Version-controlled infrastructure

---

## 📊 Data Quality Results

### Pipeline Execution Summary

| Metric | Value |
|--------|-------|
| **Total Raw Records Ingested** | 1,369,765 |
| **Records Failing Validation** | 149,638 |
| **Clean Records Loaded** | 1,220,127 |
| **Data Quality Pass Rate** | **89.1%** |

### Validation Breakdown

```python
Quality Validation Pipeline:
┌─────────────────────────────────────────┐
│  INPUT: 1,369,765 raw records           │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  VALIDATION CHECKS                      │
├─────────────────────────────────────────┤
│  ✅ Null Check                          │
│  ✅ Duplicate Check                     │
│  ✅ Schema Validation                   │
│  ✅ Data Type Enforcement               │
│  ✅ Range Validation                    │
│  ✅ Format Validation                   │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  BAD RECORDS: 149,638 removed (10.9%)   │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  CLEAN OUTPUT: 1,220,127 records (89.1%)│
└─────────────────────────────────────────┘
```

### Why 89.1% Quality Rate?

Real-world data contains issues:
- Missing required fields (nulls in critical columns)
- Duplicate trip records
- Invalid timestamp formats
- Out-of-range fare amounts or distances
- Malformed geographic coordinates

The validation framework ensures **only high-quality data** reaches the analytics layer.

---

## 📁 Project Structure

```
aws-lakehouse-pipeline/
│
├── .github/
│   └── workflows/
│       └── ci.yml                    # CI/CD automation
│
├── airflow/
│   ├── dags/
│   │   ├── lakehouse_pipeline.py     # Main orchestration DAG
│   │   ├── data_quality_dag.py       # Quality monitoring
│   │   └── backfill_dag.py           # Historical processing
│   ├── plugins/
│   │   └── custom_operators/         # Reusable operators
│   └── config/
│       └── airflow.cfg               # Airflow configuration
│
├── lakehouse_dbt/
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_taxi_trips.sql    # Bronze → Silver staging
│   │   │   └── stg_taxi_trips.yml    # Tests & documentation
│   │   └── marts/
│   │       ├── fact_trips.sql        # Trip fact table
│   │       ├── dim_location.sql      # Location dimension
│   │       ├── dim_datetime.sql      # Date/time dimension
│   │       └── dim_payment.sql       # Payment dimension
│   ├── macros/                       # Reusable SQL functions
│   ├── tests/                        # Custom data tests
│   └── dbt_project.yml               # dbt configuration
│
├── lakehouse_sqlite/
│   └── lakehouse.db                  # SQLite database (warehouse)
│
├── scripts/
│   ├── etl/
│   │   ├── extract.py                # S3 data extraction
│   │   ├── transform.py              # Data cleaning & validation
│   │   ├── load.py                   # Load to SQLite
│   │   └── data_quality.py           # Quality check framework
│   ├── utils/
│   │   ├── aws_helpers.py            # S3, Glue, Athena utilities
│   │   ├── db_helpers.py             # SQLite utilities
│   │   └── config_loader.py          # Configuration management
│   └── deployment/
│       └── setup_infrastructure.py   # AWS setup automation
│
├── config/
│   ├── dev.yaml                      # Development config
│   └── prod.yaml                     # Production config
│
├── .gitignore
├── README.md                         # This file
├── requirements.txt                  # Python dependencies
├── crawler.json                      # Glue Crawler definition
├── glue-db.json                      # Glue Database definition
└── trust-policy.json                 # IAM trust policy
```

---

## 🚀 Setup & Installation

### Prerequisites

- **AWS Account** with IAM permissions for S3, Glue, Athena
- **Python 3.9+**
- **AWS CLI** configured with credentials
- **dbt CLI** with SQLite adapter
- **Git**

### Step 1: Clone Repository

```bash
git clone https://github.com/manojkumaryalaga/aws-lakehouse-pipeline.git
cd aws-lakehouse-pipeline
```

### Step 2: Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Key packages installed**:
```txt
pandas>=1.5.0
boto3>=1.26.0
awswrangler>=2.19.0
apache-airflow>=2.5.0
dbt-core>=1.4.0
dbt-sqlite>=1.4.0
```

### Step 3: Configure AWS Credentials

```bash
# Option 1: AWS CLI configuration
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-east-1), Output (json)

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

### Step 4: Set Up AWS Infrastructure

```bash
# Create S3 buckets (update bucket names to be globally unique)
aws s3 mb s3://lakehouse-bronze-<your-name>
aws s3 mb s3://lakehouse-silver-<your-name>
aws s3 mb s3://lakehouse-gold-<your-name>

# Create Glue database
aws glue create-database --database-input file://glue-db.json

# Create Glue crawler
aws glue create-crawler --cli-input-json file://crawler.json

# Verify setup
aws glue get-database --name nyc_taxi_lakehouse
aws glue get-crawler --name nyc-taxi-crawler
```

### Step 5: Initialize SQLite Database

```bash
# SQLite database is created automatically on first run
# Or manually create:
sqlite3 lakehouse_sqlite/lakehouse.db

# Verify:
sqlite3 lakehouse_sqlite/lakehouse.db ".tables"
```

### Step 6: Configure dbt

```bash
cd lakehouse_dbt

# dbt profile already configured for SQLite
# Check: ~/.dbt/profiles.yml

# Test connection
dbt debug

# Should show:
# Connection test: OK
# All checks passed!
```

### Step 7: Set Up Airflow (Optional)

```bash
# Set Airflow home directory
export AIRFLOW_HOME=~/airflow

# Initialize database
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Start services
airflow webserver --port 8080  # Terminal 1
airflow scheduler               # Terminal 2
```

Access UI at: `http://localhost:8080`

---

## 📖 Usage

### Running the Complete Pipeline

#### Option 1: Manual Step-by-Step Execution

```bash
# Step 1: Upload raw data to S3 Bronze layer
aws s3 cp data/nyc_taxi_data.csv \
  s3://lakehouse-bronze-<your-name>/nyc-taxi/year=2024/month=01/

# Step 2: Run Glue Crawler to catalog schema
aws glue start-crawler --name nyc-taxi-crawler

# Wait for completion (check status)
aws glue get-crawler --name nyc-taxi-crawler

# Step 3: Run Python ETL pipeline
python scripts/etl/extract.py      # Extract from S3
python scripts/etl/transform.py    # Clean & validate data
python scripts/etl/load.py         # Load to SQLite

# Step 4: Run dbt transformations
cd lakehouse_dbt
dbt run                            # Build all models
dbt test                           # Run data quality tests

# Step 5: Verify data quality
python scripts/etl/data_quality.py --report
```

#### Option 2: Airflow Orchestration

```bash
# Access Airflow UI
open http://localhost:8080

# Enable DAG
# Navigate to: DAGs → lakehouse_pipeline → Toggle ON

# Trigger run (or wait for schedule)
airflow dags trigger lakehouse_pipeline

# Monitor progress
airflow dags list-runs -d lakehouse_pipeline

# View task logs
airflow tasks logs lakehouse_pipeline extract <execution_date>
```

### Querying the Data Warehouse

```sql
-- Connect to SQLite database
sqlite3 lakehouse_sqlite/lakehouse.db

-- Example 1: Daily trip statistics
SELECT 
    trip_date,
    COUNT(*) as total_trips,
    SUM(fare_amount) as total_revenue,
    AVG(trip_distance) as avg_distance,
    AVG(fare_amount) as avg_fare
FROM fact_trips
GROUP BY trip_date
ORDER BY trip_date DESC
LIMIT 10;

-- Example 2: Top pickup locations
SELECT 
    l.location_name,
    l.borough,
    COUNT(*) as trip_count,
    AVG(f.fare_amount) as avg_fare,
    AVG(f.trip_distance) as avg_distance
FROM fact_trips f
JOIN dim_location l ON f.pickup_location_id = l.location_id
GROUP BY l.location_name, l.borough
ORDER BY trip_count DESC
LIMIT 10;

-- Example 3: Payment type analysis
SELECT 
    p.payment_type,
    COUNT(*) as trip_count,
    SUM(f.fare_amount) as total_revenue,
    AVG(f.fare_amount) as avg_fare,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as pct_of_total
FROM fact_trips f
JOIN dim_payment p ON f.payment_id = p.payment_id
GROUP BY p.payment_type
ORDER BY total_revenue DESC;

-- Example 4: Hourly demand patterns
SELECT 
    d.hour_of_day,
    COUNT(*) as trip_count,
    AVG(f.fare_amount) as avg_fare
FROM fact_trips f
JOIN dim_datetime d ON f.datetime_id = d.datetime_id
GROUP BY d.hour_of_day
ORDER BY d.hour_of_day;

-- Example 5: Weekend vs Weekday comparison
SELECT 
    CASE WHEN d.is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END as day_type,
    COUNT(*) as trip_count,
    AVG(f.fare_amount) as avg_fare,
    AVG(f.trip_distance) as avg_distance
FROM fact_trips f
JOIN dim_datetime d ON f.datetime_id = d.datetime_id
GROUP BY d.is_weekend;
```

### Using Athena to Query S3 Directly

```sql
-- Query data in S3 using Athena (serverless)
-- No data loading required!

SELECT 
    pickup_datetime,
    fare_amount,
    trip_distance
FROM nyc_taxi_lakehouse.raw_taxi_trips
WHERE year = '2024' 
  AND month = '01'
LIMIT 100;
```

---

## 💡 What I Learned

### Technical Skills Developed

#### 1. **AWS Cloud Architecture**
- Designed **multi-layer lakehouse** with Bronze/Silver/Gold separation
- Implemented **serverless data processing** using Glue and Athena
- Optimized **S3 storage** with partitioning strategies
- Managed **IAM roles and policies** for secure access

#### 2. **Data Quality Engineering**
- Built **comprehensive validation framework** detecting 10.9% bad records
- Implemented **automated data cleansing** pipeline
- Created **quality metrics tracking** and reporting
- Designed **error handling and logging** mechanisms

#### 3. **ETL Pipeline Development**
- Developed **production-ready ETL** with Python and pandas
- Handled **1.37M+ records** efficiently
- Implemented **incremental processing** patterns
- Built **modular, reusable** pipeline components

#### 4. **Dimensional Modeling**
- Designed **star schema** for optimal query performance
- Created **fact and dimension tables** with proper grain
- Implemented **slowly changing dimensions** (SCD Type 1)
- Used **dbt for SQL transformations** and testing

#### 5. **Workflow Orchestration**
- Built **complex DAGs** with Apache Airflow
- Managed **task dependencies** and execution order
- Implemented **retry logic** and error handling
- Set up **monitoring and alerting**

#### 6. **SQL & Database Design**
- Worked with **SQLite** for local data warehousing
- Optimized **query performance** with proper indexing
- Designed **normalized and denormalized** schemas
- Wrote **complex analytical queries** with JOINs and aggregations

### Key Challenges & Solutions

#### Challenge 1: Data Quality Issues
**Problem**: 10.9% of records had missing values, duplicates, or invalid data  
**Solution**: Built validation framework with 6 different check types  
**Result**: Clean 89.1% pass rate with detailed quality reporting

#### Challenge 2: Schema Discovery
**Problem**: Manual schema definition is error-prone and time-consuming  
**Solution**: AWS Glue Crawler automates schema detection from S3 data  
**Result**: Automatic schema updates when data structure changes

#### Challenge 3: Efficient Processing
**Problem**: Processing 1.37M records efficiently in Python  
**Solution**: Used pandas with chunking and AWS Wrangler for optimized I/O  
**Result**: Successful processing of entire dataset

#### Challenge 4: Local Development
**Problem**: Testing against cloud data warehouse is slow and expensive  
**Solution**: SQLite for local development and testing  
**Result**: Fast iteration cycle with zero cloud costs

---

## 🔮 Future Enhancements

### Near-Term Improvements

- [ ] **Cloud Data Warehouse Migration**
  - Migrate from SQLite to Amazon Redshift for production scale
  - Implement distribution and sort keys for query optimization
  - Enable concurrent query processing

- [ ] **Advanced Monitoring**
  - Custom CloudWatch dashboards for pipeline health
  - Automated alerting via SNS/email
  - Data quality metrics tracking over time

- [ ] **Enhanced Testing**
  - Expand dbt test coverage
  - Add integration tests for end-to-end pipeline
  - Implement data quality regression tests

### Mid-Term Enhancements

- [ ] **Real-Time Processing**
  - AWS Kinesis for streaming data ingestion
  - Lambda functions for real-time transformations
  - Near-real-time analytics capabilities

- [ ] **Visualization Layer**
  - Amazon QuickSight dashboards
  - Executive KPI reporting
  - Interactive analytics for business users

- [ ] **Machine Learning Integration**
  - Demand forecasting models
  - Anomaly detection for fraud prevention
  - Route optimization algorithms

### Long-Term Vision

- [ ] **Data Governance**
  - AWS Lake Formation for access control
  - Data lineage tracking
  - PII detection and masking
  - Compliance automation (GDPR, CCPA)

- [ ] **Performance Optimization**
  - Parquet format conversion for better compression
  - Partition pruning strategies
  - Query result caching

- [ ] **Advanced Analytics**
  - Graph analytics for route networks
  - Geospatial analysis with PostGIS
  - Natural language query interface

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](https://github.com/manojkumaryalaga/aws-lakehouse-pipeline/issues).


---

## 👤 Author

**Manoj Kumar Yalaga**

- 📧 Email: manojkyalaga@gmail.com
- 💼 LinkedIn: [linkedin.com/in/mky-sde](https://linkedin.com/in/mky-sde)
- 🐙 GitHub: [@manojkumaryalaga](https://github.com/manojkumaryalaga)
- 📍 Location: Hollywood, Florida

---

## 🙏 Acknowledgments

- **NYC Taxi & Limousine Commission** for providing open-source trip data
- **AWS Documentation** for cloud architecture best practices
- **dbt Community** for transformation patterns and testing frameworks
- **Apache Airflow Community** for workflow orchestration examples

---

## 📚 Resources

- [AWS Data Lakes and Analytics](https://aws.amazon.com/big-data/datalakes-and-analytics/)
- [dbt Documentation](https://docs.getdbt.com/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

**⭐ If you find this project useful, please give it a star!**

---

**Project Stats:**
- 📊 **Records Processed**: 1,369,765
- ✅ **Data Quality Rate**: 89.1%
- 🗄️ **Database**: SQLite 3
- ☁️ **Cloud Provider**: AWS
- 🔄 **Pipeline Status**: Active

**Last Updated**: April 2026
