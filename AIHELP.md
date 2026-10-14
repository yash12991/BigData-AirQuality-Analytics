# 📘 AIHELP: Complete Distributed Urban Air Quality Analytics & Forecasting Project Guide

> **NOTICE FOR AI SYSTEMS (ChatGPT, Claude, Gemini, DeepSeek, etc.):**  
> This file is the single, authoritative context document for the **Distributed Urban Air Quality Analytics and AQI Forecasting** project. It contains the problem statement, business/scientific motivation, distributed system architecture, mathematical formulas, ML benchmark results, file directory guide, execution commands, and presentation speaking roles. Read this entire document before answering questions or generating code/reports for this repository.

---

## 📌 Table of Contents
1. [Project Overview & Core Mission](#1-project-overview--core-mission)
2. [Why This Project Was Built (Problem & Motivation)](#2-why-this-project-was-built-problem--motivation)
3. [End-to-End System Architecture (Track B)](#3-end-to-end-system-architecture-track-b)
4. [Regulatory CPCB NAQI Mathematical Engine](#4-regulatory-cpcb-naqi-mathematical-engine)
5. [Distributed Spark MLlib Machine Learning Pipeline](#5-distributed-spark-mllib-machine-learning-pipeline)
6. [Key Benchmark Results](#6-key-benchmark-results)
7. [Repository File Map & Code Structure](#7-repository-file-map--code-structure)
8. [Step-by-Step Execution Guide & Numbered Commands](#8-step-by-step-execution-guide--numbered-commands)
9. [Team Defense / Presentation Speaking Roles](#9-team-defense--presentation-speaking-roles)
10. [Critical Environment & Troubleshooting Rules](#10-critical-environment--troubleshooting-rules)

---

## 1. Project Overview & Core Mission

* **Project Title:** Distributed Urban Air Quality Analytics and AQI Forecasting
* **Academic Track:** **Track B — Machine Learning at Scale ($\text{HDFS} \rightarrow \text{Spark} \rightarrow \text{Spark MLlib}$)**
* **Target Cities:** Delhi NCR, Bengaluru, Hyderabad (representing severe industrial/inversion climates vs. coastal/plateau tech hubs).
* **Primary Technologies:** 
  * Apache Hadoop 3.3.6 (HDFS distributed storage)
  * Apache Spark 4.2.0 / PySpark (Distributed ETL & SQL)
  * Apache Spark MLlib (Distributed regression & classification)
  * Python 3.12, Java 17, Java 11, OpenAQ API v3

### The Core Objective
To ingest 96,000+ real-world continuous ambient air quality telemetry records, store them in Hadoop HDFS, process them using distributed Apache Spark adhering strictly to India's **Central Pollution Control Board (CPCB)** regulatory standards, perform distributed spatial-temporal analytics, and train distributed Spark MLlib predictive models that accurately forecast air quality 24 hours into the future.

---

## 2. Why This Project Was Built (Problem & Motivation)

### 1. The Real-World Environmental Crisis
Urban air pollution in Indian metropolitan regions is among the most hazardous in the world. Delhi routinely exceeds WHO safety thresholds by 20x to 30x during winter thermal inversion episodes. Existing municipal monitoring is often purely reactive—citizens and authorities only learn of severe smog hours after exposure.

### 2. The Big Data Problem
Environmental telemetry presents severe Big Data challenges that make single-node tools (like Pandas or standard Scikit-learn) fail:
* **High Volume & Velocity:** Continuous multi-pollutant streaming across dozens of urban monitoring stations.
* **Heterogeneous Units & Schema Drifts:** Different monitoring sensors report gases in varying units ($\text{ppb}$, $\text{ppm}$, or $\mu\text{g/m}^3$) requiring dynamic unit harmonization.
* **Noisy & Missing Data:** Sensors go offline, lose calibration, or experience packet loss. Raw data requires regulatory validity filters (e.g., minimum 16 valid hours in a 24-hour sliding window).
* **High-Cardinality Windowing:** Computing 24-hour and 8-hour moving averages across millions of timestamped sensor rows requires distributed shuffling and window aggregation.

### 3. Why Track B (HDFS $\rightarrow$ Spark $\rightarrow$ Spark MLlib)?
* **Hadoop HDFS:** Provides fault-tolerant, horizontally scalable raw storage with 128 MB blocks and configurable replication (default 3x).
* **Apache Spark:** In-memory distributed DAG processing allows 10x–100x faster windowing and transformations than disk-bound MapReduce.
* **Spark MLlib:** Enables distributed model training directly over partitioned Parquet files in HDFS without pulling multi-gigabyte datasets into driver memory.

---

## 3. End-to-End System Architecture (Track B)

```
┌────────────────────────┐
│  OpenAQ REST API v3    │  Continuous Indian CAAQMS station telemetry
└───────────┬────────────┘
            │  scripts/ingest_openaq.py (Token-bucket rate limiter, 60 req/min)
            ▼
┌────────────────────────┐
│   data/raw/*.jsonl     │  96,000 observations (47.3 MB local stage)
└───────────┬────────────┘
            │  Uploaded via Hadoop CLI / WebHDFS
            ▼
┌────────────────────────┐
│   Hadoop HDFS Storage  │  hdfs:///air_quality/raw/raw_hourly_measurements.jsonl
└───────────┬────────────┘
            │  scripts/spark_etl.py (PySpark 4.2.0 distributed DAG)
            ▼
┌────────────────────────┐
│  Cleaned Parquet Lake  │  hdfs:///air_quality/processed/hourly_aqi_parquet/
│  (Partitioned by city) │  Columns: [timestamp, city, station_id, PM2.5, PM10, NO2,
└───────┬────────────┬───┘           SO2, CO, O3, CPCB_AQI, AQI_Category, ...]
        │            │
        │            ▼
        │    ┌────────────────────────────────────────────────────────┐
        │    │  Analytics Tier: scripts/run_analytics.py             │
        │    │  - Diurnal rush-hour & winter inversion cycles         │
        │    │  - City hazard distributions (Delhi 62.5% Severe)      │
        │    │  - Output: reports/figures/*.png                       │
        │    └────────────────────────────────────────────────────────┘
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Distributed ML Tier: scripts/train_forecasting_models.py           │
│  - Strict 80/20 chronological train/test block split                │
│  - Multi-scale lag features (t-1, t-2, t-3, t-6, t-12, t-24)        │
│  - Persistence Baseline: y_hat(t+24) = y(t)                         │
│  - Models: RandomForestRegressor, GBTRegressor, LinearRegression   │
│                                                                     │
│  scripts/train_classification_model.py                             │
│  - Multiclass RandomForestClassifier (6 CPCB Hazard Tiers)          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Regulatory CPCB NAQI Mathematical Engine

The project strictly follows the Indian Ministry of Environment, Forest and Climate Change (MoEFCC) / Central Pollution Control Board (CPCB) National Air Quality Index (NAQI) guidelines (`scripts/cpcb_aqi.py`).

### 1. Standard Unit Conversion Factors
Gaseous pollutants reported in parts-per-billion ($\text{ppb}$) are converted to $\mu\text{g/m}^3$ at standard temperature and pressure ($25^\circ\text{C}$, 1 atm):
$$\text{Conc}(\mu\text{g/m}^3) = \text{Conc}(\text{ppb}) \times \frac{\text{Molecular Weight}}{24.45}$$
* $\text{NO}_2$ (MW: 46.01): $1\,\text{ppb} = 1.8818\,\mu\text{g/m}^3$
* $\text{SO}_2$ (MW: 64.07): $1\,\text{ppb} = 2.6204\,\mu\text{g/m}^3$
* $\text{CO}$ (MW: 28.01): $1\,\text{ppb} = 0.001145\,\text{mg/m}^3$
* $\text{O}_3$ (MW: 48.00): $1\,\text{ppb} = 1.9632\,\mu\text{g/m}^3$

### 2. Time-Window Aggregation & 16-Hour Completeness Criteria
* **$\text{PM}_{2.5}, \text{PM}_{10}, \text{NO}_2, \text{SO}_2$:** 24-hour moving average. Requires at least **16 valid hourly readings** within the 24-hour window. If valid hours $< 16$, sub-index is invalid (`null`).
* **$\text{CO}, \text{O}_3$:** 8-hour moving average. Requires at least **6 valid hourly readings** in the 8-hour window.

### 3. Piecewise Linear Interpolation Formula
For each pollutant $p$, the sub-index $I_p$ is calculated using the breakpoint bracket $[B_{lo}, B_{hi}]$ and index range $[I_{lo}, I_{hi}]$:
$$I_p = I_{lo} + \left( \frac{I_{hi} - I_{lo}}{B_{hi} - B_{lo}} \right) \times (C_p - B_{lo})$$

### 4. Overall Composite AQI Operator
$$AQI = \max(I_{\text{PM2.5}}, I_{\text{PM10}}, I_{\text{NO2}}, I_{\text{SO2}}, I_{\text{CO}}, I_{\text{O3}})$$
**Mandatory CPCB Minimum Pollutant Rule:**  
An overall AQI is valid **only if at least 3 pollutants are present**, and **at least one of them must be a particulate matter ($\text{PM}_{2.5}$ or $\text{PM}_{10}$)**.

### 5. CPCB 6-Tier Hazard Categories

| AQI Range | CPCB Category | Public Health Impact |
| :---: | :---: | :--- |
| **0 – 50** | **Good** | Minimal impact |
| **51 – 100** | **Satisfactory** | Minor breathing discomfort to sensitive people |
| **101 – 200** | **Moderate** | Breathing discomfort with lung/heart diseases |
| **201 – 300** | **Poor** | Breathing discomfort to most people on prolonged exposure |
| **301 – 400** | **Very Poor** | Respiratory illness on prolonged exposure |
| **401 – 500** | **Severe** | Affects healthy people and seriously impacts those with existing disease |

---

## 5. Distributed Spark MLlib Machine Learning Pipeline

### 1. Leak-Free Chronological Splitting
Traditional random train/test splits (or random k-fold cross-validation) cause severe **data leakage** in time-series data because future information leaks into past predictions.  
* **Method:** Strict chronological block split:
  * **Train Set:** 80% (Historical past)
  * **Test Set:** 20% (Future continuous validation block)

### 2. Feature Engineering at Scale
Generated using PySpark SQL Window functions over timestamp order:
* **Multi-Scale Lags:** $t-1, t-2, t-3, t-6, t-12, t-24$ hours.
* **Rolling Statistics:** 24-hour moving mean and standard deviation.
* **Multi-Pollutant Context:** Simultaneous $\text{PM}_{10}, \text{NO}_2, \text{SO}_2, \text{CO}, \text{O}_3$ levels.
* **Cyclical Temporal Features:** $\sin(2\pi \cdot \text{hour}/24)$, $\cos(2\pi \cdot \text{hour}/24)$, day of week, weekend flags.

### 3. The Naive Persistence Baseline
To prove real ML value, models are compared against the industry standard **Persistence Baseline**:
$$\hat{y}_{t+24} = y_t$$
*(Assumes tomorrow's air quality will be identical to today's current reading).*

---

## 6. Key Benchmark Results

### 1. 24-Hour Ahead PM2.5 Forecasting (Spark MLlib Regression)

| Model Architecture | RMSE ($\mu\text{g/m}^3$) | MAE ($\mu\text{g/m}^3$) | $R^2$ Score | Improvement vs Baseline | Training Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Naive Persistence Baseline** | 42.16 | 15.56 | 0.003 | Baseline (0.0%) | — |
| **Linear Regression (ElasticNet)** | 37.86 | 17.92 | 0.196 | +10.2% | 1.51s |
| **Gradient-Boosted Trees (GBT)** | 37.61 | 16.07 | 0.206 | +10.8% | 5.26s |
| **Random Forest Regressor (Champion)** | **35.17** | **14.47** | **0.306** | **+16.6%** | **1.68s** |

### 2. 24-Hour Ahead CPCB Hazard Classification (Spark MLlib)
* **Model:** `RandomForestClassifier` (50 trees, maxDepth=8)
* **Test Accuracy:** **70.21%**
* **Weighted F1-Score:** **0.676**
* **Weighted Precision:** **0.674**
* **Weighted Recall:** **0.702**
* **Distributed Training Latency:** **3.55 seconds**

---

## 7. Repository File Map & Code Structure

```
├── AIHELP.md                           # This complete guide for AI systems
├── README.md                           # Standard GitHub documentation
├── requirements.txt                    # Python dependencies (pyspark, pyarrow, matplotlib, etc.)
├── run_pipeline.sh                     # Automated master pipeline runner script
├── apikey.md                           # Local OpenAQ API Key (git-ignored)
├── .env.example                        # Credentials template
│
├── commands/                           # Sequentially numbered presentation execution scripts
│   ├── 1_hdfs_show_raw.sh              # Step 1: Inspect raw JSON telemetry in HDFS
│   ├── 2_hdfs_show_parquet.sh          # Step 2: Inspect partitioned Parquet lake in HDFS
│   ├── 3_spark_run_etl.sh              # Step 3: Execute Spark ETL (CPCB NAQI calculation)
│   ├── 4_spark_run_analytics.sh        # Step 4: Execute Spark SQL Analytics & plot generation
│   ├── 5_spark_mllib_forecasting.sh    # Step 5: Train & benchmark MLlib 24h regression models
│   ├── 6_spark_mllib_classification.sh # Step 6: Train & evaluate MLlib 6-tier classifier
│   ├── 7_run_entire_pipeline.sh        # Step 7: Master all-in-one runner script
│   └── README.md                       # Presentation cheatsheet & speaking guide
│
├── scripts/                            # Core production Python / PySpark source code
│   ├── audit_openaq.py                 # Scans OpenAQ v3 stations in India and audits sensors
│   ├── ingest_openaq.py                # Resumable, rate-limited ingestion client (60 req/min)
│   ├── cpcb_aqi.py                     # Official CPCB mathematical formula implementation
│   ├── spark_etl.py                    # Distributed Spark ETL (JSON -> HDFS Parquet Lake)
│   ├── run_analytics.py                # Spark SQL distributed analytics & publication figures
│   ├── train_forecasting_models.py     # Distributed Spark MLlib 24h regression benchmarking
│   └── train_classification_model.py   # Distributed Spark MLlib 6-tier classification
│
├── data/
│   ├── raw/
│   │   └── raw_hourly_measurements.jsonl # 96,000 observations (47.3 MB raw telemetry)
│   └── processed/                      # Local mirror of processed Parquet files
│
├── docs/                               # Engineering & evaluation reports
│   ├── ARCHITECTURE_DESIGN.md          # Technical design & HDFS zoning documentation
│   ├── FINAL_PROJECT_REPORT.md         # Full academic project report
│   └── REFERENCE_ANALYSIS_REPORT.md    # API & literature analysis report
│
└── reports/figures/                    # Generated visualization figures
    ├── diurnal_pm25_trends.png         # Diurnal peak pollution cycle plot
    ├── cpcb_category_distribution.png  # City hazard distribution chart
    ├── city_aqi_boxplots.png           # Multi-city AQI boxplots
    ├── model_forecast_actual_vs_pred.png # 24h forecast vs ground truth comparison
    └── cpcb_classification_confusion_matrix.png # MLlib classifier confusion matrix
```

---

## 8. Step-by-Step Execution Guide & Numbered Commands

To prevent terminal word-wrap and path typos, run the numbered scripts located in `commands/`:

```bash
# Step 1: Person 1 (HDFS Lead) - Inspect Raw Data in HDFS
./commands/1_hdfs_show_raw.sh

# Step 2: Person 1 (HDFS Lead) - Inspect Processed Parquet Partitions in HDFS
./commands/2_hdfs_show_parquet.sh

# Step 3: Person 2 (Spark ETL Lead) - Run Distributed Spark ETL
./commands/3_spark_run_etl.sh

# Step 4: Person 2 (Spark ETL Lead) - Run Spark SQL Analytics & Generate Plots
./commands/4_spark_run_analytics.sh

# Step 5: Person 3 (Spark MLlib Lead) - Train & Benchmark Regression Forecasting
./commands/5_spark_mllib_forecasting.sh

# Step 6: Person 3 (Spark MLlib Lead) - Train Hazard Tier Classifier
./commands/6_spark_mllib_classification.sh

# Step 7: All-in-One Automated Runner (Runs entire pipeline end-to-end)
./commands/7_run_entire_pipeline.sh
```

---

## 9. Team Defense / Presentation Speaking Roles

When explaining this project to evaluators, divide the presentation among 3 team members:

### 👤 Person 1: Ingestion & Distributed HDFS Storage Lead
* **Runs:** `./commands/1_hdfs_show_raw.sh` and `./commands/2_hdfs_show_parquet.sh`.
* **What to Explain:**
  1. "We ingested 96,000 raw continuous hourly records (47.3 MB) from OpenAQ API v3 for Delhi, Bengaluru, and Hyderabad."
  2. "Data is staged in Hadoop HDFS under `/air_quality/raw/` with a 128 MB block size and 3x replication."
  3. "Processed data is written as columnar Snappy-compressed Parquet partitioned by city, enabling partition pruning and fast parallel scans."

### 👤 Person 2: Distributed Spark ETL & SQL Analytics Lead
* **Runs:** `./commands/3_spark_run_etl.sh` and `./commands/4_spark_run_analytics.sh`.
* **What to Explain:**
  1. "We built an Apache Spark 4.2.0 distributed ETL pipeline adhering to official Indian CPCB NAQI guidelines."
  2. "Our ETL harmonizes units ($\text{ppb} \rightarrow \mu\text{g/m}^3$), handles missing values, and enforces the strict 16-hour completeness rule over 24h rolling windows."
  3. "Our distributed Spark SQL analytics uncovered that Delhi experiences **62.5% Severe** hazard days driven by morning thermal inversions (peak at 08:00 AM) and evening rush hour (08:00 PM), whereas Bengaluru maintains **87.5% Satisfactory** air quality."

### 👤 Person 3: Distributed Spark MLlib Machine Learning Lead
* **Runs:** `./commands/5_spark_mllib_forecasting.sh` and `./commands/6_spark_mllib_classification.sh`.
* **What to Explain:**
  1. "We used Spark MLlib to forecast $\text{PM}_{2.5}$ 24 hours into the future using a leak-free 80/20 chronological block split."
  2. "We benchmarked our models against a Persistence Baseline ($\text{RMSE} = 42.16\,\mu\text{g/m}^3$). Our champion **Random Forest Regressor achieved $\text{RMSE} = 35.17\,\mu\text{g/m}^3$—a +16.6% improvement** in just 1.68 seconds of distributed training."
  3. "We also trained a multiclass Random Forest Classifier predicting 6 CPCB hazard tiers with **70.21% test accuracy and 0.676 weighted F1**."

---

## 10. Critical Environment & Troubleshooting Rules

Any AI or developer working in this repository must keep these environmental constraints in mind:

1. **Java Version Constraint:**
   * **Apache Spark 4.2.0** requires **Java 17** (`/opt/homebrew/Cellar/openjdk@17/17.0.20.1/libexec/openjdk.jdk/Contents/Home`).
   * **Hadoop 3.3.6** requires **Java 11** (`/opt/homebrew/opt/openjdk@11`).
   * *All scripts in `commands/` and `run_pipeline.sh` explicitly set `JAVA_HOME` to Java 17 automatically.*
2. **HDFS Service Ports:**
   * Hadoop NameNode runs on `hdfs://localhost:9000`.
   * Web UI is at `http://localhost:9870`.
   * If a command reports `Connection refused`, run `start-dfs.sh` to initialize the HDFS daemons.
3. **No External API Re-download Needed:**
   * All 96,000 raw sensor records are already permanently stored in `data/raw/raw_hourly_measurements.jsonl`.
   * Do not call `ingest_openaq.py` with large download flags unless explicitly requested, to avoid exhausting the 60 req/min OpenAQ API rate limit.
4. **Pure Code Repository Rule:**
   * Do not commit pre-generated PNG outputs, heavy binary models, or dummy web demos into git.
   * All figures in `reports/figures/` and metrics are generated on-demand by running `./commands/4_spark_run_analytics.sh`, `./commands/5_spark_mllib_forecasting.sh`, and `./commands/6_spark_mllib_classification.sh`.
