# Distributed Urban Air Quality Analytics and AQI Forecasting

A production-grade distributed Big Data and Machine Learning system for urban air quality telemetry analysis and forecasting.

Built strictly according to **Track B (Machine Learning at Scale: HDFS → Spark → Spark MLlib)** and adhering to the official **CPCB National Air Quality Index (NAQI)** regulatory framework.

---

## 🏗️ Architecture Pipeline

```
OpenAQ API v3  ──>  data/raw/  ──>  Hadoop HDFS (/air_quality/raw)  ──>  Apache Spark 4.2.0 (ETL)  ──>  HDFS Parquet (/air_quality/processed)  ──>  Spark MLlib (Regression & Classification)
```

1. **Ingestion Tier (`scripts/ingest_openaq.py`):**
   - Extracts real-world continuous ambient air quality observations via OpenAQ API v3.
   - Respects 60 req/min rate limit with automatic token tracking, exponential backoff, and checkpointed resumable pagination.
2. **Distributed Storage Tier (Hadoop 3.3.6 HDFS):**
   - Staged in dedicated HDFS zones: `/air_quality/raw/`, `/air_quality/processed/`, `/air_quality/analytics/`.
3. **Distributed ETL Tier (`scripts/spark_etl.py`):**
   - Cleanses, deduplicates, and harmonizes gaseous units ($\text{ppb} \rightarrow \mu\text{g/m}^3$).
   - Pivots multi-pollutant measurements into station-hour time series.
   - Enforces CPCB 16-hour validity rules across 24h moving exposure windows.
   - Calculates CPCB sub-indices and overall composite NAQI with the maximum operator.
   - Stores columnar partitioned Parquet (`city=XXX/year=YYYY`).
4. **Analytics Tier (`scripts/run_analytics.py`):**
   - Computes distributed Spark SQL queries across cities and stations.
   - Evaluates diurnal and day-of-week patterns and health hazard category distributions.
   - Generates publication-ready figures in `reports/figures/`.
5. **Distributed Machine Learning Tier (`scripts/train_forecasting_models.py`, `scripts/train_classification_model.py`):**
   - Strict chronological block splitting (80% past history, 20% future horizon) to prevent temporal leakage.
   - Generates multi-scale historical lags ($t-1, t-2, t-3, t-6, t-12, t-24$).
   - Trains distributed regression models (`RandomForestRegressor`, `GBTRegressor`, `LinearRegression`) against a standard **Persistence Baseline** ($\hat{y}_{t+24} = y_t$).
   - Trains multiclass CPCB hazard tier classification (`RandomForestClassifier`) evaluated with weighted F1, accuracy, and confusion matrices.

---

## 📊 Key Results & Benchmarks

### 1. 24-Hour Ahead PM2.5 Forecasting (Spark MLlib Regression)

| Model Architecture | RMSE (µg/m³) | MAE (µg/m³) | $R^2$ Score | Improvement vs Baseline | Training Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Naive Persistence Baseline** | 42.16 | 15.56 | 0.003 | Baseline (0.0%) | — |
| **Linear Regression (ElasticNet)** | 37.86 | 17.92 | 0.196 | +10.2% | 1.51s |
| **Gradient-Boosted Trees (GBT)** | 37.61 | 16.07 | 0.206 | +10.8% | 5.26s |
| **Random Forest Regressor** | **35.17** | **14.47** | **0.306** | **+16.6%** | **1.68s** |

### 2. 24-Hour Ahead CPCB Hazard Classification (Spark MLlib)
- **Model:** `RandomForestClassifier` (50 trees, maxDepth=8)
- **Test Accuracy:** **70.21%**
- **Weighted F1-Score:** **0.676**
- **Weighted Precision:** **0.674**
- **Weighted Recall:** **0.702**
- **Distributed Training Duration:** **3.55 seconds**

---

## 🚀 Quickstart & Reproducibility

### 1. Prerequisites
- macOS or Linux with **Java 17** (for Spark 4.2.0) and **Java 11** (for Hadoop 3.3.6).
- Python 3.10+ (Python 3.12 configured in `.venv/`).
- Running Hadoop HDFS instance (`hdfs://localhost:9000`).

### 2. Setup Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Credentials
Copy `.env.example` to `.env` (or place your API key into `apikey.md`):
```bash
cp .env.example .env
# Edit .env with your personal OpenAQ API Key
```

### 4. Execute the End-to-End Pipeline
Run the master automated runner script:
```bash
./run_pipeline.sh
```

Or execute individual stages:
```bash
# Phase 1: Audit & Discovery
python3 scripts/audit_openaq.py

# Phase 2: Ingestion
python3 scripts/ingest_openaq.py --sample

# Phase 3: Spark ETL
python3 scripts/spark_etl.py

# Phase 4: Spark SQL Analytics
python3 scripts/run_analytics.py

# Phase 5: MLlib Regression & Forecasting
python3 scripts/train_forecasting_models.py

# Phase 5: MLlib Hazard Classification
python3 scripts/train_classification_model.py
```

---

## 📁 Repository Structure

```
.
├── README.md                           # Master documentation
├── requirements.txt                    # Python dependencies
├── .env.example                        # Credentials template
├── run_pipeline.sh                     # End-to-end execution runner
├── scripts/
│   ├── audit_openaq.py                 # OpenAQ API v3 audit & discovery
│   ├── ingest_openaq.py                # Resumable, rate-limited ingestion engine
│   ├── cpcb_aqi.py                     # Regulatory CPCB NAQI calculation engine
│   ├── spark_etl.py                    # Distributed Spark ETL (HDFS -> Parquet)
│   ├── run_analytics.py                # Distributed Spark SQL analytics & plotting
│   ├── train_forecasting_models.py     # Spark MLlib regression benchmarking
│   └── train_classification_model.py   # Spark MLlib hazard category classification
├── docs/
│   ├── REFERENCE_ANALYSIS_REPORT.md    # Phase 0: Literature review & API analysis
│   ├── DATA_AUDIT_REPORT.md            # Phase 1: Station coverage & sensor audit
│   ├── ARCHITECTURE_DESIGN.md          # Complete technical design & data zoning
│   ├── ANALYTICS_REPORT.md             # Phase 4: Statistical summary & trends
│   ├── MODEL_EVALUATION_REPORT.md      # Phase 5: Regression benchmarking report
│   ├── CLASSIFICATION_EVALUATION_REPORT.md # Phase 5: Category classification report
│   └── FINAL_PROJECT_REPORT.md         # Master final project report
├── reports/figures/
│   ├── diurnal_pm25_trends.png         # Diurnal PM2.5 cycle plot
│   ├── cpcb_category_distribution.png  # Health category distribution bar chart
│   ├── city_aqi_boxplots.png           # Multi-city AQI boxplot comparison
│   ├── model_forecast_actual_vs_pred.png # 24h forecast vs ground truth time series
│   └── cpcb_classification_confusion_matrix.png # MLlib classification confusion matrix
└── data/
    ├── raw/                            # Raw JSON responses and JSONL streams
    └── processed/                      # Cleaned partitioned Parquet dataset
```
