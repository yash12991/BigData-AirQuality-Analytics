# Complete Video Call Presentation Script & Project Defense Guide

**Project Title:** Distributed Urban Air Quality Analytics and AQI Forecasting  
**Assigned Track:** Track B — Machine Learning at Scale: HDFS -> Spark -> Spark MLlib  
**Standard Authority:** Central Pollution Control Board (CPCB), Government of India  
**Audience:** Academic Evaluators, Project Review Committee, Technical Interviewers  

---

## 📋 Table of Contents
1. [Executive Cheatsheet (Quick Facts)](#1-executive-cheatsheet-quick-facts)
2. [How to Run the Live Demo (Exact Commands)](#2-how-to-run-the-live-demo-exact-commands)
3. [Word-for-Word Video Call Speaking Script (5–10 Minutes)](#3-word-for-word-video-call-speaking-script-510-minutes)
   - [Part 1: Introduction & Problem Statement (0:00 – 1:30)](#part-1-introduction--problem-statement-000--130)
   - [Part 2: Track B Architecture & HDFS Storage (1:30 – 3:00)](#part-2-track-b-architecture--hdfs-storage-130--300)
   - [Part 3: The CPCB NAQI Regulatory Engine (3:00 – 4:30)](#part-3-the-cpcb-naqi-regulatory-engine-300--430)
   - [Part 4: Spark SQL Analytics & Insights (4:30 – 6:00)](#part-4-spark-sql-analytics--insights-430--600)
   - [Part 5: Distributed Machine Learning with Spark MLlib (6:00 – 8:00)](#part-5-distributed-machine-learning-with-spark-mllib-600--800)
   - [Part 6: Conclusion & Live Demonstration (8:00 – 9:30)](#part-6-conclusion--live-demonstration-800--930)
4. [Anticipated Viva & Evaluator Questions (Q&A Defense)](#4-anticipated-viva--evaluator-questions-qa-defense)
5. [What Every Component in the Repository Does](#5-what-every-component-in-the-repository-does)

---

## 1. Executive Cheatsheet (Quick Facts)

Keep these numbers in mind during your call:
- **Raw Data Volume:** **96,000 raw hourly observations** (47.3 MB JSONL) extracted via OpenAQ API v3.
- **Geographic Scope:** 3 distinct climatic zones in India:
  - **Delhi NCR:** Severe particulate exposure (R K Puram, Anand Vihar)
  - **Bengaluru:** Tech corridor plateau (BTM Layout)
  - **Hyderabad:** Semi-arid Deccan plateau (Central University)
- **Station-Hour Processed Records:** **18,521** records; **12,792** meet the strict CPCB 16-hour validity criteria.
- **Storage:** Hadoop 3.3.6 HDFS (`/air_quality/raw/`, `/air_quality/processed/`, `/air_quality/analytics/`).
- **ETL Performance:** Spark 4.2.0 processes 96,000 records, pivots 8 parameters, calculates rolling windows, and writes Parquet in **~25 seconds**.
- **Forecasting Performance (24h Ahead PM2.5):**
  - **Baseline Persistence:** RMSE = 42.16 µg/m³
  - **Spark MLlib Random Forest:** **RMSE = 35.17 µg/m³ (16.6% improvement over baseline, R² = 0.306)**
- **Classification Performance (24h Ahead CPCB Tier):** **70.21% test accuracy** using Spark MLlib `RandomForestClassifier`.

---

## 2. How to Run the Live Demo (Exact Commands)

Open your Terminal on your Mac and run the following:

```bash
# Navigate to the project directory
cd /Users/yashsonawane/Desktop/BigData

# OPTION A: Run the entire end-to-end pipeline with one command
./run_pipeline.sh
```

If the evaluators ask to see individual stages or inspect HDFS directly:

```bash
# 1. Show HDFS directories and files:
/Users/yashsonawane/bigdata/hadoop/current/bin/hdfs dfs -ls -h /air_quality/raw/
/Users/yashsonawane/bigdata/hadoop/current/bin/hdfs dfs -ls /air_quality/processed/hourly_aqi_parquet/

# 2. Run Spark ETL:
export JAVA_HOME="/opt/homebrew/Cellar/openjdk@17/17.0.20.1/libexec/openjdk.jdk/Contents/Home"
.venv/bin/python3 scripts/spark_etl.py

# 3. Run Distributed Analytics:
.venv/bin/python3 scripts/run_analytics.py

# 4. Run Spark MLlib Regression Training:
.venv/bin/python3 scripts/train_forecasting_models.py

# 5. Run Spark MLlib Hazard Classification:
.venv/bin/python3 scripts/train_classification_model.py
```

---

## 3. Word-for-Word Video Call Speaking Script (5–10 Minutes)

### Part 1: Introduction & Problem Statement (0:00 – 1:30)

> **Say this:**  
> *"Good morning / afternoon, respected professors and evaluators. Today I am presenting our project: **Distributed Urban Air Quality Analytics and AQI Forecasting**.*  
>  
> *Urban air pollution is one of the most pressing public health challenges in India. Continuous Ambient Air Quality Monitoring Stations deployed across our cities generate massive, multi-pollutant, continuous time-series data streams.*  
>  
> *Traditional single-node tools like standard Pandas or Scikit-Learn hit strict computational and memory bottlenecks when attempting to process multi-year, multi-station sensor streams with high-frequency rolling windows. Furthermore, many naive implementations treat raw pollutant concentrations as AQI or use random train/test splits that leak future data into the past.*  
>  
> *To solve this, our project implements **Track B: Machine Learning at Scale**, building an end-to-end distributed data pipeline using **Hadoop HDFS** for distributed storage, **Apache Spark** for distributed ETL and CPCB regulatory compliance, and **Spark MLlib** for scalable distributed machine learning."*

---

### Part 2: Track B Architecture & HDFS Storage (1:30 – 3:00)

> **Say this (Screen share the Architecture Diagram or Terminal):**  
> *"Let me walk you through our architectural design:*  
>  
> *First, for data acquisition, we developed a production-grade ingestion client interfacing with **OpenAQ API version 3**. We extracted **96,000 real-world hourly observations** across four major government-grade CAAQMS stations in **Delhi NCR, Bengaluru, and Hyderabad**, monitoring six criteria pollutants: PM2.5, PM10, NO2, SO2, CO, and O3, along with temperature and humidity.*  
>  
> *Second, as required by Track B, our raw ingested data sits directly in **Hadoop HDFS**. We created three enterprise data zones in HDFS:*  
> 1. `/air_quality/raw/` *where our 47.3 MB raw JSON telemetry resides.*  
> 2. `/air_quality/processed/` *where our cleaned, hourly multi-pollutant dataset is stored in columnar Apache Parquet, partitioned by city and year.*  
> 3. `/air_quality/analytics/` *for pre-aggregated summary tables.*  
>  
> *This structure ensures zero single-node bottleneck and allows Spark workers to parallelize disk I/O directly across HDFS blocks."*

---

### Part 3: The CPCB NAQI Regulatory Engine (3:00 – 4:30)

> **Say this:**  
> *"A foundational contribution of our project is strict adherence to India's official **Central Pollution Control Board (CPCB) National Air Quality Index (NAQI)** methodology.*  
>  
> *There is a critical scientific distinction between **raw concentration** and **AQI**:*  
> - *Concentrations are physical units—like micrograms per cubic meter—which cannot be averaged across different gases.*  
> - *AQI is a dimensionless human-health hazard scale from 0 to 500 based on the **linear segmented principle**.*  
>  
> *In our Spark ETL pipeline:*  
> 1. *We first harmonized all units. Continuous analyzers often report gases in parts-per-billion (ppb). We converted them to mass concentrations at 25°C and 1 atmosphere.*  
> 2. *We applied sliding windows to compute **24-hour averages** for PM2.5, PM10, NO2, and SO2, and **8-hour averages** for CO and O3.*  
> 3. *We strictly enforced CPCB's **16-hour data completeness rule**: an AQI is calculated **only** if at least 16 hours of valid data exist in the 24-hour window, with at least 3 criteria pollutants present, one of which **must** be particulate matter (PM2.5 or PM10). Missing values are **never** replaced with zeros.*  
> 4. *The overall AQI is determined by the **maximum operator**: AQI = max(I1, I2, ... In), and the pollutant with the highest sub-index is flagged as the Prominent Pollutant.*  
>  
> *Our Spark ETL pipeline processes the entire 96,000-record dataset and produces 18,521 station-hour aligned records in just **25 seconds**."*

---

### Part 4: Spark SQL Analytics & Insights (4:30 – 6:00)

> **Say this (Show `reports/figures/diurnal_pm25_trends.png` and `cpcb_category_distribution.png`):**  
> *"Next, we used Spark SQL to run distributed analytics across the partitioned Parquet lake. Here are our three major findings:*  
>  
> *1. **Severe Particulate Loading in Delhi NCR:** Delhi NCR monitoring stations recorded an average PM2.5 concentration of **121.9 µg/m³**, resulting in an average CPCB AQI of **382**, with **62.5% of all monitored hours falling into the 'Severe' category** (>400 AQI).*  
>  
> *2. **The Diurnal Inversion Peak:** In our diurnal analysis chart, you can clearly observe that particulate pollution in Delhi follows a steep bimodal curve. Concentrations spike between **6:00 AM and 9:00 AM IST** due to morning rush-hour traffic trapped by shallow atmospheric boundary layers, and peak again between **9:00 PM and 11:00 PM IST** due to nighttime thermal inversion.*  
>  
> *3. **Regional Comparison:** In contrast, Bengaluru and Hyderabad maintain a baseline PM2.5 around **28 µg/m³**, with over 40% of hours in the 'Satisfactory' health tier."*

---

### Part 5: Distributed Machine Learning with Spark MLlib (6:00 – 8:00)

> **Say this (Show `reports/figures/model_forecast_actual_vs_pred.png` and evaluation tables):**  
> *"Now, let's look at the core requirement of Track B: **Machine Learning at Scale using Spark MLlib**.*  
>  
> *To satisfy the rubric's requirement that the model and evaluation must be **genuinely sound, not just present**, we instituted three critical ML principles:*  
>  
> *First: **Leak-Free Chronological Splitting**. In time-series forecasting, standard random K-fold splits leak future observations into past training sets, causing artificially inflated accuracy. We used a strict chronological cutoff: the first **80% of historical data (10,294 samples)** was used for training, and the remaining **20% strictly future data (2,570 samples)** was held out for testing.*  
>  
> *Second: **Multi-Scale Temporal Lag Features**. Using Spark Window functions, we engineered lag features at t-1h, t-2h, t-3h, t-6h, t-12h, and t-24h, along with meteorological variables and diurnal indicators.*  
>  
> *Third: **Benchmarking against a Naive Persistence Baseline**. In atmospheric science, tomorrow's pollution is often strongly correlated with today's. A naive persistence model yields an RMSE of 42.16 µg/m³.*  
>  
> *We then trained distributed models via Spark MLlib Pipelines:*  
> - *Spark MLlib **Linear Regression with ElasticNet** achieved an RMSE of 37.86 µg/m³ (a 10.2% improvement).*  
> - *Spark MLlib **Gradient-Boosted Trees (GBTRegressor)** achieved an RMSE of 37.61 µg/m³ (a 10.8% improvement).*  
> - *Our best model, Spark MLlib **Random Forest Regressor**, achieved an **RMSE of 35.17 µg/m³ and MAE of 14.47 µg/m³**, delivering a **16.6% error reduction over the persistence baseline** with an R² of 0.306.*  
>  
> *Furthermore, for policy decision-making, we trained a second model: a **Spark MLlib RandomForestClassifier** to forecast the future CPCB hazard tier (Good, Satisfactory, Moderate, Poor, Very Poor, Severe). It achieved **70.21% test accuracy** and a **weighted F1-score of 0.676** across the held-out test horizon."*

---

### Part 6: Conclusion & Live Demonstration (8:00 – 9:30)

> **Say this (Run `./run_pipeline.sh` on terminal):**  
> *"In conclusion, this project demonstrates a complete, reproducible big data solution: from raw API extraction into Hadoop HDFS, distributed cleaning and regulatory CPCB indexing via Spark SQL, to scalable forecasting with Spark MLlib.*  
>  
> *I am now executing `./run_pipeline.sh` in my terminal. As you can see live on screen:*  
> - *HDFS checks active daemons.*  
> - *Spark ETL loads the 96,000 records from HDFS, applies the 16-hour validity rules, and outputs partitioned Parquet in 25 seconds.*  
> - *Spark SQL computes city analytics and renders visualization figures.*  
> - *Spark MLlib fits both the regression and classification pipelines across the cluster.*  
>  
> *Everything is documented in our comprehensive final reports and modular codebase. Thank you, and I am now happy to answer any questions."*

---

## 4. Anticipated Viva & Evaluator Questions (Q&A Defense)

### Q1: "Why did you use Apache Spark and HDFS instead of Pandas and Scikit-Learn?"
> **Answer:**  
> *"Single-node libraries like Pandas and Scikit-learn require loading the entire dataset into RAM on one machine. When scaling to multi-year telemetry across hundreds of stations and thousands of sensors, memory exhaustion occurs. In our architecture, Hadoop HDFS distributes raw data blocks across nodes, and Apache Spark executes distributed transformations in-memory with parallel partitions. Our Spark MLlib pipeline distributes decision-tree node splits and tree evaluations across executor cores simultaneously, training complex ensembles in under 2 seconds."*

### Q2: "How did you calculate AQI? Can't we just take the average of all pollutants?"
> **Answer:**  
> *"No, taking an average of pollutant concentrations is scientifically invalid. Different pollutants have completely different toxicities—for instance, 60 µg/m³ of PM2.5 represents moderate air pollution, whereas 60 µg/m³ of SO2 is completely safe.  
> We implemented the official Central Pollution Control Board (CPCB) National AQI standard:  
> 1. Each pollutant's 24-hour or 8-hour concentration is converted into an independent sub-index via linear segmented interpolation using official CPCB breakpoints.  
> 2. The final AQI is determined by the maximum operator: AQI = max(I1, I2, ... In).  
> 3. We also enforce the CPCB rule that an AQI is valid only if at least 16 hours of data exist in 24 hours and at least 3 criteria pollutants are monitored, one of which must be PM2.5 or PM10."*

### Q3: "Did you use K-Fold Cross-Validation for your ML model?"
> **Answer:**  
> *"We specifically avoided standard random K-fold cross-validation because in time-series forecasting, random splits leak future observations into past training iterations, resulting in artificially inflated accuracy that fails in real life.  
> Instead, we implemented a strict **chronological block split**: the first 80% of historical time-stamped records were used for training, and the final 20% strictly future horizon was held out for testing. This guarantees zero data leakage."*

### Q4: "Why did you compare your model against a Naive Persistence Baseline?"
> **Answer:**  
> *"In atmospheric and environmental science, air pollution exhibits strong autocorrelation: tomorrow's pollution often resembles today's pollution. Simply reporting an R² or RMSE without a baseline is misleading. In the Track B rubric, evaluation must be genuinely sound. We established the persistence baseline (ŷ_{t+24} = y_t), which yielded an RMSE of 42.16 µg/m³. Our Spark MLlib Random Forest model beat this baseline by 16.6%, reducing RMSE to 35.17 µg/m³ and proving that our lag feature engineering extracted genuine meteorological and diurnal patterns."*

### Q5: "How are your Parquet datasets partitioned in HDFS and why?"
> **Answer:**  
> *"Our processed Parquet dataset in HDFS (`/air_quality/processed/hourly_aqi_parquet/`) is partitioned by `city` and `year`. This partitioning aligns with real-world query access patterns: when an analytics query or ML model trains on a specific city or year, Spark applies partition pruning, reading only the relevant directories from HDFS and avoiding expensive full-table scans."*

---

## 5. What Every Component in the Repository Does

| File / Directory | What It Does |
| :--- | :--- |
| `run_pipeline.sh` | **Master Automated Runner:** Sets Java 17, starts HDFS daemons, runs Spark ETL, runs analytics, and trains all MLlib models in sequence. |
| `scripts/audit_openaq.py` | **Phase 1 Data Discovery:** Connects to OpenAQ API v3, checks rate limits, scans Indian stations, and verifies CPCB eligibility. |
| `scripts/ingest_openaq.py` | **Phase 2 Ingestion Engine:** Production client with token tracking (60 req/min), exponential backoff, checkpointing (`.checkpoint.json`), and raw JSON staging (96,000 records). |
| `scripts/cpcb_aqi.py` | **Regulatory Math Engine:** Pure implementation of CPCB sub-index linear interpolation, breakpoint tables, and 16h completeness rules. |
| `scripts/spark_etl.py` | **Phase 3 Spark ETL:** Reads raw JSONL from HDFS, cleans invalid values, harmonizes units (ppb -> µg/m³), computes 24h/8h rolling windows, calculates CPCB AQI, and writes partitioned Parquet to HDFS. |
| `scripts/run_analytics.py` | **Phase 4 Analytics Engine:** Spark SQL queries computing city statistics, diurnal patterns, health category distributions, and generating visual figures. |
| `scripts/train_forecasting_models.py` | **Phase 5 MLlib Regression:** Computes lag features (t-1 to t-24), applies chronological 80/20 split, trains LinearRegression, RandomForest, and GBT against persistence baseline. |
| `scripts/train_classification_model.py` | **Phase 5 MLlib Classification:** Trains distributed RandomForestClassifier on 6-tier CPCB health categories, generating accuracy, F1, and confusion matrix. |
| `docs/FINAL_PROJECT_REPORT.md` | **Master Project Report:** Comprehensive synthesis of Phase 0 to Phase 6 with all data tables, benchmarks, and findings. |
| `docs/ARCHITECTURE_DESIGN.md` | **Architecture Specification:** Complete Track B design document detailing HDFS zoning and Spark execution graphs. |
| `reports/figures/` | **Visualization Assets:** High-resolution figures showing diurnal trends, category bar charts, boxplots, actual vs predicted forecasts, and confusion matrix. |
| `.gitignore` & `.env.example` | **Security Hygiene:** Ensures `apikey.md` and virtual environments are never committed or exposed. |
