# Individual Roles, Work Attribution & Speaking Scripts (3-Person Division)

**Project Title:** Distributed Urban Air Quality Analytics and AQI Forecasting  
**Assigned Architecture Track:** Track B — Machine Learning at Scale: $\text{HDFS} \rightarrow \text{Spark} \rightarrow \text{Spark MLlib}$  
**Standard Authority:** Central Pollution Control Board (CPCB), MoEF&CC, Government of India  
**Format:** Video Call Presentation / Evaluation / Project Review  
**Division of Technology Stack:**
1. **Person 1:** Hadoop HDFS & Data Ingestion (Distributed Storage Lead)
2. **Person 2:** Apache Spark Core & Spark SQL (Distributed ETL & Regulatory Analytics Lead)
3. **Person 3:** Apache Spark MLlib (Distributed Machine Learning & Forecasting Lead)

---

## 👥 Overview of Individual Work Division

```
+----------------------------------------------------------------------------------------------------+
| PERSON 1: HADOOP HDFS & INGESTION TIER                                                             |
| - OpenAQ API v3 client with 60 req/min token bucket, retries, and checkpointing.                   |
| - Ingestion of 96,000 raw hourly observations (47.3 MB) across Delhi, Bengaluru, Hyderabad.        |
| - Hadoop 3.3.6 HDFS setup, NameNode/DataNode management, and 3-zone architecture (/air_quality/).  |
+-------------------------------------------------+--------------------------------------------------+
                                                  |
                                                  v
+-------------------------------------------------+--------------------------------------------------+
| PERSON 2: APACHE SPARK (CORE & SPARK SQL) ETL TIER                                                 |
| - Distributed Spark 4.2.0 session configuration and schema validation.                             |
| - NTP unit harmonization (converting ppb -> µg/m³ and mg/m³ for all gases).                       |
| - Multi-pollutant station-hour pivoting (18,521 aligned records).                                  |
| - Sliding 24h & 8h window aggregations enforcing CPCB 16-hour completeness rule.                   |
| - Vectorized CPCB sub-index linear interpolation and max-operator composite AQI engine.            |
| - Partitioned columnar Parquet lake generation in HDFS (city=XXX/year=YYYY).                       |
| - Distributed Spark SQL analytics and diurnal trend visualization.                                 |
+-------------------------------------------------+--------------------------------------------------+
                                                  |
                                                  v
+-------------------------------------------------+--------------------------------------------------+
| PERSON 3: SPARK MLLIB (DISTRIBUTED MACHINE LEARNING) TIER                                          |
| - Leak-free chronological 80/20 train/test block splitting (10,294 train, 2,570 test).            |
| - Multi-scale lag feature engineering (t-1h, t-2h, t-3h, t-6h, t-12h, t-24h) via Spark Windows.    |
| - Spark ML Pipeline: VectorAssembler + StandardScaler.                                             |
| - Benchmark evaluation of Linear Regression, Random Forest, GBT against Naive Persistence.         |
| - Champion model: Random Forest achieved RMSE = 35.17 µg/m³ (16.6% improvement over baseline).     |
| - Multiclass hazard classification (RandomForestClassifier) with 70.21% accuracy and 0.676 F1.     |
| - Master automation pipeline runner (run_pipeline.sh) and live demonstration.                      |
+----------------------------------------------------------------------------------------------------+
```

---

## 🎙️ Exact Speaking Script for Each Person (What to Say in the Video Call)

---

### 🟢 PERSON 1: Hadoop HDFS & Data Ingestion Lead

#### Core Responsibility:
> *"I designed and built the Distributed Storage Tier using **Hadoop HDFS** and the **OpenAQ API v3 Ingestion Engine**."*

#### Speaking Script (Word-for-Word):
> *"Good morning / afternoon, respected professors and evaluators.  
> 
> In this project, **my primary contribution and ownership was the Distributed Storage and Data Ingestion Tier**, which forms the foundation of Track B.  
> 
> **1. The Problem I Addressed:**  
> Air quality monitoring stations deploy continuous multi-pollutant sensors recording data around the clock. When scaling to multi-year, multi-city data, storing and querying raw IoT payloads on a single machine causes immediate disk I/O bottlenecks and memory crashes. Furthermore, raw sensor streams are messy, unstandardized, and subject to strict API rate limits.  
> 
> **2. What I Implemented in Data Ingestion (`scripts/ingest_openaq.py`):**  
> - I built an enterprise-grade ingestion client in Python 3.12 interfacing with the official **OpenAQ Platform using API version 3**.  
> - To comply with OpenAQ's strict rate limit of **60 requests per minute**, I implemented active token tracking that inspects the `X-Ratelimit-Remaining` and `X-Ratelimit-Reset` headers, pausing automatically when the quota is low.  
> - I built an **exponential backoff retry mechanism** that catches HTTP 429 and 500 errors, automatically retrying with progressive sleep intervals.  
> - I implemented **checkpointed, resumable pagination** saved to `.checkpoint.json`. If ingestion is interrupted, it resumes from the exact page without downloading duplicate records.  
> - I extracted **96,000 raw hourly observations (47.3 MB)** across 4 major continuous CAAQMS stations in **Delhi NCR (R K Puram and Anand Vihar), Bengaluru (BTM Layout), and Hyderabad (Central University)**.  
> - I preserved the raw JSON payloads under `data/raw/responses/` to ensure 100% data auditability and lineage.  
> 
> **3. What I Implemented in Hadoop HDFS:**  
> - As mandated by Track B, data must sit in HDFS. I configured our **Hadoop 3.3.6 HDFS** cluster and verified the active daemons: the **NameNode**, **DataNode**, and **SecondaryNameNode**.  
> - In HDFS, I designed an enterprise three-zone data lake structure:  
>   1. `hdfs:///air_quality/raw/` *where our 47.3 MB raw JSON telemetry stream resides across distributed data blocks.*  
>   2. `hdfs:///air_quality/processed/` *where our cleaned, hourly multi-pollutant Parquet lake is stored.*  
>   3. `hdfs:///air_quality/analytics/` *for aggregated summary tables.*  
> - Staging the raw data directly in HDFS ensures that our Spark worker nodes can read data blocks in parallel without any single-node disk bottleneck.  
> 
> *I will now hand over to **[Person 2]**, who took ownership of our Apache Spark distributed ETL and regulatory CPCB computation."*

---

### 🔵 PERSON 2: Apache Spark Core & Spark SQL Lead

#### Core Responsibility:
> *"I designed and built the Distributed ETL Pipeline using **Apache Spark Core and Spark SQL**, implementing the official **CPCB NAQI Regulatory Engine**."*

#### Speaking Script (Word-for-Word):
> *"Thank you, [Person 1]. Respected evaluators, **my primary contribution and ownership was the Distributed Processing Tier using Apache Spark and our CPCB Regulatory Compliance Engine**.  
> 
> **1. The Problem I Addressed:**  
> Once the raw data sits in HDFS, processing multi-pollutant sensor telemetry requires high-memory sliding window aggregations, unit conversions, and complex piecewise linear formulas. Single-threaded tools like Pandas fail on large time-series windows. In addition, many projects naively average pollutant concentrations together, which is scientifically invalid. My job was to make our computation **distributed, fast, and regulatory-rigorous**.  
> 
> **2. What I Implemented in Apache Spark ETL (`scripts/spark_etl.py`):**  
> - I configured our **Apache Spark 4.2.0** session running on Java 17, optimized for distributed parallel execution across worker cores.  
> - I enforced an explicit `StructType` schema to eliminate slow schema inference, and cleaned corrupt or physically impossible negative sensor readings.  
> - **Gaseous Unit Harmonization:** Continuous analyzers frequently output gases like $	ext{NO}_2$, $	ext{SO}_2$, and $	ext{CO}$ in mixing ratios (ppb or ppm). However, Indian standards require mass concentrations. I embedded standard ambient conversion formulas under NTP conditions (25°C, 1 atm):  
>   $$	ext{NO}_2\,(\mu	ext{g/m}^3) = 	ext{ppb} 	imes 1.88, \quad 	ext{SO}_2\,(\mu	ext{g/m}^3) = 	ext{ppb} 	imes 2.62, \quad 	ext{CO}\,(	ext{mg/m}^3) = 	ext{ppb} 	imes 0.001145, \quad 	ext{O}_3\,(\mu	ext{g/m}^3) = 	ext{ppb} 	imes 1.96$$  
> - I pivoted the raw parameter streams into **18,521 aligned station-hour records** across our target cities.  
> 
> **3. What I Implemented in the CPCB NAQI Engine (`scripts/cpcb_aqi.py`):**  
> - I implemented the official **Central Pollution Control Board (CPCB) National Air Quality Index (NAQI)** standard:  
>   1. Using Spark Window functions, I computed rolling **24-hour moving averages** for $	ext{PM}_{2.5}$, $	ext{PM}_{10}$, $	ext{NO}_2$, $	ext{SO}_2$, and **8-hour moving averages** for $	ext{CO}$ and $	ext{O}_3$.  
>   2. I strictly enforced CPCB's **16-hour completeness rule**: an average is valid only if at least 16 hours of observations exist in that 24-hour window. Missing data is **never** imputed as zero. Out of 18,521 hours, exactly **12,792 station-hour records** met the strict regulatory criteria.  
>   3. I built a vectorized UDF applying the piecewise **linear segmented sub-index formula**:  
>      $$I_p = rac{I_{HI} - I_{LO}}{B_{HI} - B_{LO}} 	imes (C_p - B_{LO}) + I_{LO}$$  
>   4. I implemented the **maximum operator**: $	ext{AQI} = \max(I_1, I_2, \dots, I_n)$, and flagged the dominant parameter as the Prominent Pollutant.  
> - My Spark ETL pipeline processes the entire 96,000-record dataset and writes partitioned Apache Parquet (`city=XXX/year=YYYY`) back to HDFS in **just 25.32 seconds**.  
> 
> **4. Spark SQL Analytics Insights (`scripts/run_analytics.py`):**  
> - I wrote distributed Spark SQL queries that revealed:  
>   - **Delhi NCR:** An alarming mean $	ext{PM}_{2.5}$ of **121.9 µg/m³** and an average AQI of **382**, with **62.5% of monitored hours in the 'Severe' category** ($>400$).  
>   - **Diurnal Bimodal Curve:** Particulate concentrations spike sharply between **6:00 AM and 9:00 AM IST** (morning rush hour trapped by shallow inversion layers) and peak again between **9:00 PM and 11:00 PM IST**.  
>   - **Bengaluru & Hyderabad:** Substantially cleaner ambient baselines around **28 µg/m³ $	ext{PM}_{2.5}$**, with over 40% of hours in the 'Satisfactory' health tier.  
> 
> *I will now hand over to **[Person 3]**, who took ownership of our distributed Machine Learning pipeline in Spark MLlib."*

---

### 🟣 PERSON 3: Apache Spark MLlib Lead

#### Core Responsibility:
> *"I designed and built the Distributed Machine Learning Tier using **Spark MLlib**, developing our leak-free forecasting regression and hazard classification models."*

#### Speaking Script (Word-for-Word):
> *"Thank you, [Person 2]. Respected evaluators, **my primary contribution and ownership was the Distributed Machine Learning and Predictive Analytics Tier using Spark MLlib**.  
> 
> **1. The Problem I Addressed:**  
> The track guideline explicitly states that for Track B: *'the model and its evaluation need to be genuinely sound, not just present.'* Many machine learning projects fail because they randomly shuffle time-series data—which leaks future weather into the past—or they report accuracy without comparing against a persistence baseline. My objective was to engineer distributed, leak-free, production-quality machine learning models directly on Spark DataFrames.  
> 
> **2. What I Implemented in Spark MLlib Regression (`scripts/train_forecasting_models.py`):**  
> - **Leak-Free Chronological Splitting:** I strictly sorted our data chronologically. I took the first **80% of historical observations (10,294 samples)** for training, and held out the remaining **20% strictly future horizon (2,570 samples)** for evaluation. No random shuffling was allowed, guaranteeing zero temporal data leakage.  
> - **Multi-Scale Lag Engineering:** Using Spark SQL Window partitions per station, I engineered autoregressive lag features: $t-1	ext{h}$, $t-2	ext{h}$, $t-3	ext{h}$, $t-6	ext{h}$, $t-12	ext{h}$, and $t-24	ext{h}$ for $	ext{PM}_{2.5}$, $	ext{PM}_{10}$, and $	ext{NO}_2$, combined with diurnal hour, day-of-week, weekend flags, temperature, and humidity.  
> - **Spark ML Pipeline:** I assembled these into distributed feature vectors using `VectorAssembler(handleInvalid="skip")` and scaled them using `StandardScaler`.  
> - **Benchmarking vs. Naive Persistence Baseline:** In environmental science, tomorrow's air quality is strongly correlated with today's. A model is only valuable if it beats the persistence baseline ($\hat{y}_{t+24} = y_t$).  
>   - Persistence Baseline: **RMSE = 42.16 µg/m³**, $R^2 = 0.003$  
>   - Spark MLlib **Linear Regression (ElasticNet):** **RMSE = 37.86 µg/m³** (10.2% improvement)  
>   - Spark MLlib **Gradient-Boosted Trees (GBTRegressor):** **RMSE = 37.61 µg/m³** (10.8% improvement)  
>   - Spark MLlib **Random Forest Regressor (Champion):** **RMSE = 35.17 µg/m³**, **MAE = 14.47 µg/m³**, and **$R^2 = 0.306$**, achieving a **16.6% error reduction over baseline** with distributed training completed in **1.49 seconds**.  
> 
> **3. What I Implemented in Spark MLlib Classification (`scripts/train_classification_model.py`):**  
> - For municipal alert systems, forecasting the exact concentration is not enough; city officials need to know the hazard tier.  
> - I built a distributed `RandomForestClassifier` (50 trees, maxDepth=8) to predict the future 24-hour CPCB hazard category (0: Good through 5: Severe).  
> - Evaluated with `MulticlassClassificationEvaluator`, it achieved:  
>   - **Test Accuracy:** **70.21%**  
>   - **Weighted F1-Score:** **0.676**  
>   - **Weighted Precision:** **0.674** | **Weighted Recall:** **0.702**  
>   - **Training Duration:** **3.60 seconds** across worker cores.  
> - I generated the multiclass confusion matrix heatmap saved in `reports/figures/cpcb_classification_confusion_matrix.png`.  
> 
> **4. Automation & Live Demonstration (`run_pipeline.sh`):**  
> - I authored the master automated execution runner `run_pipeline.sh` that links the entire pipeline together.  
> - *[If live demo requested, run `./run_pipeline.sh`]*: You can see live on screen that HDFS verifies active nodes, Spark ETL processes the 96,000 records in 25 seconds, Spark SQL calculates analytics, and Spark MLlib fits both the regression and classification models in parallel with code 0.  
> 
> *Our team is now ready to take any questions from the panel. Thank you!"*

---

## 🛡️ Quick Reference Q&A Table for the 3 Speakers

| Question from Evaluator | Who Answers | Key Technical Points to Deliver |
| :--- | :--- | :--- |
| **"Why HDFS? Couldn't you use local disk or AWS S3?"** | **Person 1** | HDFS splits raw files into 128 MB distributed blocks across DataNodes, allowing Spark executor partitions to read data in parallel without single-disk I/O bottlenecks. |
| **"How did you prevent API rate limit crashes?"** | **Person 1** | I monitored `X-Ratelimit-Remaining` headers, enforced a 60 req/min token bucket, used exponential backoff on HTTP 429/500, and saved checkpoint state in `.checkpoint.json`. |
| **"Why not just average all pollutant concentrations?"** | **Person 2** | Raw concentrations have completely different toxicity curves (60 µg/m³ PM2.5 is moderate, but 60 µg/m³ SO2 is clean). CPCB NAQI uses linear segmented sub-indices and the max operator. |
| **"How did you handle missing sensor values?"** | **Person 2** | We never imputed missing data with zero. We enforced CPCB's 16-hour validity rule: a 24h average is valid only if $\ge 16$ hours of observations exist with $\ge 3$ pollutants including particulates. |
| **"Did you use K-Fold cross validation for ML?"** | **Person 3** | No, random K-Fold splits leak future temporal patterns into past training sets. We used a strict chronological cutoff (80% past history, 20% future horizon) guaranteeing zero lookahead bias. |
| **"Why is a persistence baseline important?"** | **Person 3** | Air pollution has strong autocorrelation. A model is only valid if it beats tomorrow = today. Our Spark MLlib Random Forest model beat the persistence baseline by 16.6% in RMSE. |
