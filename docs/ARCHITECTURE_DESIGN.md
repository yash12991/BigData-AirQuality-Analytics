# System Architecture & Technical Design Specification

**Project:** Distributed Urban Air Quality Analytics and AQI Forecasting  
**Architecture Track:** Track B — Machine Learning at Scale: $\text{HDFS} \rightarrow \text{Spark} \rightarrow \text{Spark MLlib}$  
**Standard Compliance:** Central Pollution Control Board (CPCB) NAQI (2014)  

---

## 1. High-Level Architecture Overview

The system processes multi-year, multi-station ambient air quality sensor telemetry spanning criteria pollutants ($\text{PM}_{2.5}$, $\text{PM}_{10}$, $\text{NO}_2$, $\text{SO}_2$, $\text{CO}$, $\text{O}_3$) across major Indian urban hubs.

```
+-----------------------------------------------------------------------------------+
| 1. DATA INGESTION TIER (Python 3.12 Engine)                                      |
|    - OpenAQ API v3 Client with Throttling & Rate-Limit Tracking (60 req/min)      |
|    - Checkpointed Resumable Pagination                                            |
|    - Raw JSON Lineage Stored in data/raw/responses/                               |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------+-----------------------------------------+
| 2. DISTRIBUTED STORAGE TIER (Hadoop 3.3.6 HDFS)                                   |
|    - hdfs:///air_quality/raw/         -> Raw JSONL streams (47.3 MB ingested)    |
|    - hdfs:///air_quality/processed/   -> Partitioned Parquet (city=X/year=Y)     |
|    - hdfs:///air_quality/analytics/   -> Aggregated metric tables & summaries     |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------+-----------------------------------------+
| 3. DISTRIBUTED ETL & COMPUTATION (Apache Spark 4.2.0 Engine)                     |
|    - Schema Validation & Deduplication (location_id, sensor_id, timestamp)        |
|    - Unit Harmonization (ppb/ppm -> µg/m³, mg/m³ at 25°C, 1 atm)                 |
|    - Temporal Alignment & Multi-Pollutant Pivot per Station-Hour                  |
|    - Rolling Exposure Windows (24-hour & 8-hour) with 16h Validity Gate          |
|    - Vectorized CPCB Sub-Index and NAQI Max-Operator Calculation                 |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------+-----------------------------------------+
| 4. DISTRIBUTED ML & ANALYTICS (Spark MLlib Pipeline)                              |
|    - Leak-Free Chronological Block Train/Test Partitioning (80/20)               |
|    - Multi-Scale Temporal Lags (t-1, t-2, t-3, t-6, t-12, t-24)                   |
|    - Task 1: 24h Ahead PM2.5 Regression (RF, GBT, LinearRegression)              |
|    - Task 2: 24h Ahead CPCB Hazard Classification (RandomForestClassifier)       |
|    - Benchmarking vs. Naive Persistence Baseline                                 |
+-----------------------------------------------------------------------------------+
```

---

## 2. Distributed Storage Architecture (HDFS)

Data in HDFS is partitioned according to access patterns to optimize predicate pushdown and minimize executor I/O shuffle overhead:

1. **Raw Storage Zone (`/air_quality/raw/`):**
   - Stores raw OpenAQ observations in append-only JSONL format (`raw_hourly_measurements.jsonl`).
   - Retains original sensor-level metadata, timestamp tags, and quality flags.
2. **Processed Storage Zone (`/air_quality/processed/hourly_aqi_parquet/`):**
   - Stored in columnar Apache Parquet format with snappy compression.
   - Partitioned by:
     - `city` (e.g., `city=Delhi NCR`, `city=Bengaluru`, `city=Hyderabad`)
     - `year` (e.g., `year=2025`, `year=2026`)
   - Incorporates all harmonized pollutants, 24-hour moving averages, sub-indices, composite AQI, and health categories.
3. **Analytics Storage Zone (`/air_quality/analytics/`):**
   - Aggregated summary statistics, diurnal trends, and health category distributions.

---

## 3. Distributed Processing Pipeline (Spark Core & DataFrames)

### 3.1 Schema Enforcement & Cleaning
Raw sensor records are parsed with an explicit `StructType` schema. Records with unphysical negative concentrations ($< 0$) or extreme hardware errors ($\ge 5000\,\mu\text{g/m}^3$) are filtered. Duplicate entries are eliminated by checking `(location_id, sensor_id, datetime_from_utc)`.

### 3.2 Unit Harmonization
Under CPCB specifications, particulate pollutants use mass concentration ($\mu\text{g/m}^3$), while gaseous analyzers often report in parts per billion ($\text{ppb}$). The Spark pipeline converts all gases to CPCB-standard units at NTP conditions ($25^\circ\text{C}, 1\text{ atm}$):
$$\text{NO}_2\,(\mu\text{g/m}^3) = \text{ppb} \times 1.88$$
$$\text{SO}_2\,(\mu\text{g/m}^3) = \text{ppb} \times 2.62$$
$$\text{CO}\,(\text{mg/m}^3) = \text{ppb} \times 0.001145$$
$$\text{O}_3\,(\mu\text{g/m}^3) = \text{ppb} \times 1.96$$

### 3.3 CPCB NAQI Engine
For each station-hour observation:
1. A sliding 24-hour chronological window calculates the 24-hour rolling averages for $\text{PM}_{2.5}$, $\text{PM}_{10}$, $\text{NO}_2$, and $\text{SO}_2$, and an 8-hour window for $\text{CO}$ and $\text{O}_3$.
2. **Data Completeness Rule:** A 24-hour average is marked valid only if $\ge 16$ valid hourly readings exist.
3. **Sub-Index Formula:**
   $$I_p = \frac{I_{HI} - I_{LO}}{B_{HI} - B_{LO}} \times (C_p - B_{LO}) + I_{LO}$$
4. **Overall AQI:**
   $$\text{NAQI} = \max(I_1, I_2, \dots, I_k)$$
   Requires $\ge 3$ valid pollutants, with at least one particulate parameter ($\text{PM}_{2.5}$ or $\text{PM}_{10}$).

---

## 4. Distributed Machine Learning Pipeline (Spark MLlib)

### 4.1 Chronological Split (No Future Leakage)
In time-series forecasting, standard K-Fold random splitting leaks future values into past training iterations. This system applies a strict timestamp cutoff ($T_{\text{split}}$):
- **Training Set (80%):** All observations where $t \le T_{\text{split}}$
- **Held-Out Test Set (20%):** All observations where $t > T_{\text{split}}$

### 4.2 Feature Space
- Multi-scale lags: $t-1\text{h}$, $t-2\text{h}$, $t-3\text{h}$, $t-6\text{h}$, $t-12\text{h}$, $t-24\text{h}$
- Particulate lag interactions: $\text{PM}_{10}(t-1)$, $\text{PM}_{10}(t-24)$, $\text{NO}_2(t-1)$
- Temporal covariates: `hour` (0–23), `day_of_week` (1–7), `is_weekend` (0/1)
- Meteorological variables: `temperature`, `relativehumidity`
- Pipeline: `VectorAssembler(handleInvalid="skip")` $\rightarrow$ `StandardScaler(withMean=True, withStd=True)` $\rightarrow$ `Estimator`

### 4.3 Models Evaluated
1. **Naive Persistence Benchmark:** $\hat{y}_{t+24} = y_t$
2. **Linear Regression (ElasticNet):** Regularized linear baseline.
3. **Random Forest Regressor:** Distributed ensemble (40 trees, depth 7).
4. **Gradient-Boosted Trees (GBTRegressor):** Distributed boosting (40 iterations, depth 5).
5. **Random Forest Classifier:** 6-tier CPCB hazard classification (50 trees, depth 8).
