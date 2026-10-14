# 🎙️ Live Presentation, Demo & Defense Script
## Distributed Urban Air Quality Analytics & AQI Forecasting (Track B)

> **Team Presentation Guide:**  
> This script is designed for a 10-15 minute live project demonstration. It tells you **who speaks**, **when the driver runs each command**, **what output appears on the terminal**, and **what to say naturally** while pointing at the screen.

---

## 👥 Presentation Roles & Strategy

* **Terminal / Screen Driver:** Shares screen, opens the `commands/` directory in terminal, and executes commands when cued.
* **Speaker 1 (HDFS & Ingestion Lead):** Explains the problem statement, data ingestion, and HDFS distributed storage.
* **Speaker 2 (Spark ETL & Analytics Lead):** Explains CPCB regulatory math, distributed Spark ETL, and SQL spatial-temporal insights.
* **Speaker 3 (Spark MLlib ML Lead):** Explains leak-free time-series modeling, 24h regression forecasting, and multi-tier classification.

*(Note: If only 1 or 2 people are presenting, the cues below remain identical—simply transition the speaking parts).*

---

## 🎬 Section 0: Project Introduction (1 Minute)

**Speaker 1:**
> "Good morning professors and evaluators. Today, our team is presenting our Big Data project: **Distributed Urban Air Quality Analytics and AQI Forecasting**.
> 
> We are strictly following **Track B: Machine Learning at Scale**, implementing the full distributed lifecycle: **HDFS distributed storage $\rightarrow$ Apache Spark distributed ETL $\rightarrow$ Spark MLlib at scale**.
> 
> Our problem addresses India's severe urban pollution crisis across three diverse metropolitan centers: **Delhi NCR**, **Bengaluru**, and **Hyderabad**. Instead of building toy single-node Pandas scripts, we implemented a production-grade distributed pipeline adhering to the official **Central Pollution Control Board (CPCB)** National Air Quality Index standards.
> 
> Let us begin by inspecting our raw distributed data lake in Hadoop HDFS."

---

## 🎬 Section 1: Raw Data in Hadoop HDFS (`./1_hdfs_show_raw.sh`)

### 🕹️ Terminal Action:
* **Speaker 1 says:** *"Driver, please show our raw telemetry dataset in HDFS."*
* **Driver runs:**
  ```bash
  ./1_hdfs_show_raw.sh
  ```

### 🖥️ What Appears on Terminal:
```text
$ hdfs dfs -ls -h /air_quality/raw/
Found 1 items
-rw-r--r--   1 yashsonawane supergroup     47.3 M 2026-10-14 23:13 /air_quality/raw/raw_hourly_measurements.jsonl
```

### 🗣️ What Speaker 1 Explains:
> "As you can see on the terminal, our raw sensor telemetry is stored directly inside Hadoop HDFS under the `/air_quality/raw/` path.
> 
> * **Data Scale:** This file is **47.3 Megabytes** containing **96,000 raw continuous hourly sensor records** extracted from the OpenAQ API v3.
> * **Ingestion Engineering:** Our ingestion engine in `scripts/ingest_openaq.py` implements a token-bucket rate limiter that respects OpenAQ's 60 requests/minute restriction, with automated pagination and state checkpoints.
> * **HDFS Architecture:** In a production multi-node cluster, HDFS splits this file into 128 MB blocks with 3x replication across DataNodes, ensuring fault tolerance against node failures.
> 
> Now, let us inspect how this raw JSON is transformed and structured into our processed Parquet lake."

---

## 🎬 Section 2: Processed Parquet Lake in HDFS (`./2_hdfs_show_parquet.sh`)

### 🕹️ Terminal Action:
* **Speaker 1 says:** *"Driver, please display the partitioned Parquet lake in HDFS."*
* **Driver runs:**
  ```bash
  ./2_hdfs_show_parquet.sh
  ```

### 🖥️ What Appears on Terminal:
```text
$ hdfs dfs -ls -h /air_quality/processed/hourly_aqi_parquet/
Found 4 items
-rw-r--r--   1 yashsonawane supergroup          0 2026-10-15 02:22 /air_quality/processed/hourly_aqi_parquet/_SUCCESS
drwxr-xr-x   - yashsonawane supergroup          0 2026-10-15 02:22 /air_quality/processed/hourly_aqi_parquet/city=Bengaluru
drwxr-xr-x   - yashsonawane supergroup          0 2026-10-15 02:22 /air_quality/processed/hourly_aqi_parquet/city=Delhi NCR
drwxr-xr-x   - yashsonawane supergroup          0 2026-10-15 02:22 /air_quality/processed/hourly_aqi_parquet/city=Hyderabad
```

### 🗣️ What Speaker 1 Explains:
> "Here on the terminal, you can see our processed Parquet lake, partitioned at the directory level by `city=Bengaluru`, `city=Delhi NCR`, and `city=Hyderabad`.
> 
> * **Why Parquet?** Rather than using slow, unindexed CSV files, we chose columnar Apache Parquet with Snappy compression. This gives us high compression ratios and enables **Partition Pruning**.
> * **Query Optimization:** When our downstream queries filter by city, Spark skips scanning irrelevant directories entirely, minimizing disk I/O and network shuffle.
> 
> I now hand over to Speaker 2 to explain how Apache Spark processed and calculated these regulatory indices."

---

## 🎬 Section 3: Distributed Spark ETL & CPCB Math (`./3_spark_run_etl.sh`)

### 🕹️ Terminal Action:
* **Speaker 2 says:** *"Driver, let us execute the Apache Spark distributed ETL pipeline."*
* **Driver runs:**
  ```bash
  ./3_spark_run_etl.sh
  ```

### 🖥️ What Appears on Terminal (executes in ~20s):
```text
$ python3 scripts/spark_etl.py
================ STARTING DISTRIBUTED SPARK ETL ================
Apache Spark Version: 4.2.0
[1/6] Ingesting raw dataset from: hdfs://localhost:9000/air_quality/raw/raw_hourly_measurements.jsonl
  Ingested 96,000 raw records.
[2/6] Cleaning data and enforcing validity constraints...
[3/6] Normalizing timestamps to IST and harmonizing pollutant units...
[4/6] Reshaping and pivoting pollutants into hourly station records...
[5/6] Calculating rolling exposure windows and CPCB NAQI...
  Total Station-Hour Records Processed: 18,521
  Records Meeting Strict CPCB 16h NAQI Validity: 12,792
+---------+-----------------------+-------------------+------------------+------------------+--------+---------------+
|city     |station_name           |ts_ist             |pm25_24h          |pm10_24h          |cpcb_aqi|health_category|
+---------+-----------------------+-------------------+------------------+------------------+--------+---------------+
|Delhi NCR|R K Puram, Delhi - DPCC|2016-02-06 12:30:00|193.42857142857142|528.3125          |500.0   |Severe         |
+---------+-----------------------+-------------------+------------------+------------------+--------+---------------+
[6/6] Persisting partitioned Parquet dataset to storage...
Spark ETL Pipeline completed successfully in 20.71 seconds.
```

### 🗣️ What Speaker 2 Explains:
> "Our ETL pipeline was completed in just 20 seconds over Spark 4.2.0. Notice the key engineering achievements here:
> 
> 1. **Unit Harmonization:** Sensors in India report gaseous pollutants in varying units. We implemented dynamic molecular weight conversions to convert gases from parts-per-billion ($\text{ppb}$) into standard $\mu\text{g/m}^3$.
> 2. **Multi-Pollutant Reshaping:** We pivoted individual pollutant measurement streams into structured station-hour multi-pollutant vectors.
> 3. **The Strict CPCB 16-Hour Completeness Rule:** In official Indian CPCB guidelines, you cannot simply take the average of 2 or 3 random readings. A 24-hour window is only legally valid if it contains **at least 16 valid hourly readings**. Out of 18,521 station-hours, exactly 12,792 met this strict regulatory requirement.
> 4. **Piecewise Linear Sub-Index & Max Operator:** For each valid pollutant, Spark evaluates piecewise linear breakpoints, and computes the composite NAQI as the maximum sub-index across all monitored gases.
> 
> Now, let us run Spark SQL analytics to discover spatial and diurnal pollution patterns."

---

## 🎬 Section 4: Distributed Spark SQL Analytics & Visual Trends (`./4_spark_run_analytics.sh`)

### 🕹️ Terminal Action:
* **Speaker 2 says:** *"Driver, please run the distributed Spark SQL analytics."*
* **Driver runs:**
  ```bash
  ./4_spark_run_analytics.sh
  ```

### 🖥️ What Appears on Terminal:
```text
$ python3 scripts/run_analytics.py
================ RUNNING DISTRIBUTED ANALYTICS ================
[1/4] Calculating city-wise descriptive statistics...
     city  total_hours  valid_aqi_hours  avg_pm25  avg_pm10  avg_cpcb_aqi  max_cpcb_aqi
Delhi NCR         8131             5924     121.9     288.8         382.0         500.0
Bengaluru         6126             3378      28.8      68.9         293.9         500.0
Hyderabad         4264             3490      28.0      69.7         265.1         500.0

[2/4] Computing CPCB health category distribution by city...
     city health_category  pct_of_city
Delhi NCR          Severe        62.5%
Bengaluru    Satisfactory        36.6%
Hyderabad    Satisfactory        41.3%

[4/4] Rendering analytics visualizations...
  [COMMAND 4 - FIGURE 1] Saved: reports/figures/cmd4_fig1_diurnal_pm25_trends.png
  [COMMAND 4 - FIGURE 2] Saved: reports/figures/cmd4_fig2_cpcb_category_distribution.png
  [COMMAND 4 - FIGURE 3] Saved: reports/figures/cmd4_fig3_city_aqi_boxplots.png
```

### 🗣️ What Speaker 2 Explains (Point to output / figures):
> "The Spark SQL aggregation highlights stark environmental contrasts between Indian metros:
> 
> * **Delhi NCR vs. Southern Metros:** Delhi's average $\text{PM}_{2.5}$ is **121.9 $\mu\text{g/m}^3$**, which is more than four times higher than Bengaluru ($28.8$) and Hyderabad ($28.0$).
> * **Hazard Distribution:** A staggering **62.5% of monitored hours in Delhi fell into the Severe category** ($AQI > 400$).
> * **Figure 1 (Diurnal Inversion Trends):** In `cmd4_fig1_diurnal_pm25_trends.png`, we observe a massive morning peak at 08:00 AM caused by nocturnal thermal inversion trapping exhaust near ground level, followed by an evening traffic spike at 08:00 PM.
> 
> I now hand over to Speaker 3 to show how we forecast these hazards 24 hours in advance using Spark MLlib."

---

## 🎬 Section 5: Spark MLlib 24-Hour Forecasting (`./5_spark_mllib_forecasting.sh`)

### 🕹️ Terminal Action:
* **Speaker 3 says:** *"Driver, please train and benchmark our Spark MLlib 24-hour regression forecasting models."*
* **Driver runs:**
  ```bash
  ./5_spark_mllib_forecasting.sh
  ```

### 🖥️ What Appears on Terminal:
```text
$ python3 scripts/train_forecasting_models.py
================ STARTING SPARK MLLIB TRAINING PIPELINE ================
[1/5] Engineering multi-scale temporal lags and 24h forecasting target...
[2/5] Creating chronological block split (80% Train, 20% Held-Out Test)...
  Training observations (Past):     10,294 (80.0%)
  Test observations (Future):        2,570 (20.0%)
[3/5] Evaluating Naive Persistence Baseline (ŷ_{t+24} = y_t)...
  [BASELINE] Naive Persistence -> RMSE: 42.16 µg/m³ | MAE: 15.56 µg/m³ | R²: 0.003
[5/5] Training distributed models across Spark cluster...
  --- Training Linear Regression (ElasticNet) ---
    RMSE: 37.86 µg/m³ (vs Baseline: +10.2%) | Training Latency: 1.32s
  --- Training Random Forest Regressor ---
    RMSE: 35.17 µg/m³ (vs Baseline: +16.6%) | Training Latency: 1.38s
  --- Training Gradient-Boosted Trees (GBT) ---
    RMSE: 37.61 µg/m³ (vs Baseline: +10.8%) | Training Latency: 5.80s

Best Performing Model: Random Forest Regressor with RMSE = 35.17 µg/m³
  [COMMAND 5 - FIGURE 1] Saved forecast plot: reports/figures/cmd5_fig1_model_forecast_actual_vs_pred.png
```

### 🗣️ What Speaker 3 Explains:
> "In Section 5, we train machine learning models directly at scale using Spark MLlib. Here is what is mathematically critical:
> 
> 1. **Zero Data Leakage:** Most amateur data science projects perform a random `train_test_split()`, which leaks future data into the training set. We enforced a **strict chronological 80/20 block split**: the models train strictly on past historical records and are evaluated on unseen future horizons.
> 2. **Multi-Scale Lag Engineering:** We constructed features at lags $t-1, t-2, t-3, t-6, t-12, t-24$ alongside cyclical temporal sine/cosine features.
> 3. **The Persistence Baseline Comparison:** To prove real ML utility, we benchmarked against the standard Persistence Baseline ($\hat{y}_{t+24} = y_t$), which achieved an RMSE of $42.16\,\mu\text{g/m}^3$.
> 4. **Model Performance:** Our **Random Forest Regressor** outperformed all models, achieving an **RMSE of 35.17 $\mu\text{g/m}^3$—a 16.6% accuracy improvement over baseline**, with distributed training completed in just 1.38 seconds.
> 
> Finally, let us demonstrate our multi-tier hazard classification model."

---

## 🎬 Section 6: Spark MLlib Hazard Classification (`./6_spark_mllib_classification.sh`)

### 🕹️ Terminal Action:
* **Speaker 3 says:** *"Driver, please train the Spark MLlib 6-tier hazard classification model."*
* **Driver runs:**
  ```bash
  ./6_spark_mllib_classification.sh
  ```

### 🖥️ What Appears on Terminal:
```text
$ python3 scripts/train_classification_model.py
================ STARTING SPARK MLLIB CLASSIFICATION PIPELINE ================
Total usable classified samples: 11,074
Training distributed RandomForestClassifier...

--- Spark MLlib Classification Metrics ---
  Accuracy:           70.21%
  Weighted F1-Score:  0.676
  Weighted Precision: 0.674
  Weighted Recall:    0.702
  Training Duration:  3.48s
  [COMMAND 6 - FIGURE 1] Saved confusion matrix plot: reports/figures/cmd6_fig1_cpcb_classification_confusion_matrix.png
```

### 🗣️ What Speaker 3 Explains:
> "In addition to regression forecasting, public health authorities need discrete hazard warnings.
> 
> * **The Task:** Predicting which of the 6 official CPCB hazard tiers (Good, Satisfactory, Moderate, Poor, Very Poor, Severe) each station will experience 24 hours in advance.
> * **Results:** Our distributed `RandomForestClassifier` achieved **70.21% accuracy** and a **0.676 weighted F1-score**.
> * **Figure 1:** In `cmd6_fig1_cpcb_classification_confusion_matrix.png`, you can observe strong diagonal concentration, particularly for the critical Severe and Satisfactory categories.
> 
> If the evaluators wish to see the entire automated pipeline run from end-to-end, our driver can run `./7_run_entire_pipeline.sh`."

---

## 🎬 Section 7: Conclusion & Wrap-Up

**Speaker 1:**
> "To summarize our project:
> 1. We built a genuine distributed Track B architecture: **HDFS $\rightarrow$ Apache Spark $\rightarrow$ Spark MLlib**.
> 2. We enforced official government CPCB NAQI regulations with 16-hour validity windows and unit conversions.
> 3. We proved machine learning value with a 16.6% improvement over baseline and 70.2% hazard classification accuracy.
> 
> Thank you, professors. We are now open for your questions."

---

## 🛡️ Evaluator Viva Q&A Defense Cheat Sheet

| Likely Evaluator Question | Recommended Perfect Answer |
| :--- | :--- |
| **Q1: Why did you use Parquet instead of CSV in HDFS?** | "CSV is row-oriented, uncompressed, and has no schema. Parquet is a columnar format with Snappy compression that supports **Partition Pruning** and **Dictionary Encoding**. When Spark queries filter by city, it reads only the relevant partition directory without scanning the rest of the dataset." |
| **Q2: Why did you use an 80/20 chronological split instead of K-Fold Cross Validation?** | "Environmental air quality is time-series data with strong autocorrelation. If we used random splitting or standard K-Fold, future records would leak into the training set, causing severe data leakage and artificially inflated scores. Chronological block splitting is the only mathematically sound approach." |
| **Q3: What is the CPCB 16-hour completeness rule?** | "India's CPCB NAQI regulations mandate that a 24-hour moving average is valid only if at least 16 hourly sensor readings exist in that window. If fewer than 16 hours are recorded, the sub-index must be marked invalid (`null`) to prevent bias from incomplete data." |
| **Q4: Why did Random Forest perform better than Gradient-Boosted Trees (GBT)?** | "Air pollution telemetry contains sudden meteorological spikes (dust storms, Diwali fireworks, crop burning). GBT focuses heavily on optimizing residual errors, which makes it prone to overfitting noisy outliers. Random Forest's bagging and feature subsampling proved more robust across multi-station noise." |
| **Q5: Can this pipeline scale to all 500+ Indian monitoring stations?** | "Yes. Because every stage is implemented as a distributed Apache Spark job over HDFS, scaling from 3 cities to 500 stations requires zero code changes—only adding worker nodes to the Hadoop/Spark cluster." |
