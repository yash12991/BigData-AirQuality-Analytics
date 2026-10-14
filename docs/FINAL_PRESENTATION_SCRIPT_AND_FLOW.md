# 🎙️ Master Video Call Presentation Script & Flow Guide
### Track B: Machine Learning at Scale — Hadoop HDFS ➔ Apache Spark ➔ Spark MLlib
**Project Title:** Distributed Urban Air Quality Analytics & AQI Forecasting  
**Team Structure:** 3 Presenters (Person 1: HDFS & Storage | Person 2: Spark ETL & Regulatory | Person 3: Spark MLlib & Forecasting)  
**Total Target Duration:** 8 to 10 Minutes + Q&A  

---

## 🧭 High-Level Call Flow & Stage Directions

| Time Window | Speaker & Role | Screen to Share | Visual Action / Demo Cue |
| :--- | :--- | :--- | :--- |
| **0:00 – 0:30** | **Speaker 1** (Opening) | Dashboard Header / Cover | Introduce team, project title, and Track B architecture. |
| **0:30 – 3:00** | **Speaker 1** (HDFS & Storage Lead) | **Tab 2: HDFS Lake Explorer** | Click `/raw/` (96k rows) ➔ `/processed/` (Parquet) ➔ Show 128MB block & 3x replication. |
| **3:00 – 3:15** | *Hand-off: Speaker 1 ➔ Speaker 2* | Transition to Tab 3 | Smooth spoken handoff to Speaker 2. |
| **3:15 – 5:45** | **Speaker 2** (Spark ETL & Analytics Lead) | **Tab 3: CPCB Calculator** & **Tab 4: Spark SQL** | Click *Delhi Severe* preset ➔ Show dominant pollutant ➔ Show diurnal inversion chart. |
| **5:45 – 6:00** | *Hand-off: Speaker 2 ➔ Speaker 3* | Transition to Tab 5 | Smooth spoken handoff to Speaker 3. |
| **6:00 – 8:30** | **Speaker 3** (Spark MLlib Lead) | **Tab 5: MLlib Predictor** & **Tab 6: Live Terminal** | Highlight 16.6% RMSE reduction over persistence ➔ Click *Forecast Next 24h* ➔ Show terminal log. |
| **8:30 – 10:00+**| **All 3 Speakers** | Dashboard / Live Terminal | Conclude, thank evaluators, and transition to Viva Q&A Defense. |

---

## 🚀 Pre-Call Setup Checklist (Do This 5 Minutes Before Joining)
1. **Launch the Demo Website:** Run `./start_demo.sh` in your terminal. Ensure `http://localhost:8080` is open in Chrome and fullscreen.
2. **Open a Backup Terminal Window:** Have a terminal ready at `/Users/yashsonawane/Desktop/BigData` in case the evaluators ask to see raw bash commands.
3. **Decide Who Shares Screen:**
   - *Option A (Recommended):* One person (e.g. Speaker 1 or Speaker 2) shares screen throughout the entire call and smoothly clicks the tabs as each teammate speaks.
   - *Option B:* Each speaker takes over screen sharing during their dedicated turn.
4. **Keep This Document Open:** Use it on a second screen, phone, or notebook as your teleprompter.

---

# 🗣️ Verbatim Word-for-Word Speaking Script

---

### 🟢 PART 1: Opening & Distributed Storage in Hadoop HDFS (0:00 – 3:00)
**Speaker:** Person 1 (Distributed Storage & Ingestion Lead)  
**Screen to Share:** Start on Dashboard Header, then click **`[Tab 2: HDFS Lake Explorer]`**.

#### [0:00 – 0:45] Formal Introduction & Problem Statement
> **(Say with confidence and warmth):**  
> *"Good morning / afternoon, respected professors and members of the evaluation committee. Today, our team is presenting our project: **Distributed Urban Air Quality Analytics and AQI Forecasting** under **Track B: Machine Learning at Scale**.  
> 
> Continuous Ambient Air Quality Monitoring Stations deployed across Indian metros generate massive, continuous multi-pollutant telemetry. Traditional single-node data tools like Pandas or Scikit-Learn collapse under memory exhaustion when processing multi-year high-frequency streams with sliding windows. Furthermore, naive implementations often make the mistake of averaging raw concentrations or leaking future data in random splits.  
> 
> To solve this with true big data engineering, our architecture implements an end-to-end distributed pipeline using **Hadoop 3.3.6 HDFS** for fault-tolerant distributed storage, **Apache Spark 4.2.0** for distributed ETL and regulatory compliance, and **Spark MLlib** for scalable distributed machine learning."*

#### [0:45 – 2:30] Data Ingestion & HDFS 3-Tier Storage Architecture
> **(Action: Click on Tab 2: HDFS Lake Explorer. Click on `/raw/measurements.jsonl` in the tree):**  
> *"I spearheaded the distributed ingestion and storage tier.  
> 
> First, for data acquisition, we developed a production client interfacing with **OpenAQ API v3**. We implemented a token-bucket rate limiter at 60 requests per minute with exponential backoff and JSON checkpointing. Across 4 government-grade CAAQMS stations in **Delhi NCR, Bengaluru, and Hyderabad**, we ingested **96,000 raw hourly observations** (47.3 MB) covering six criteria pollutants: PM2.5, PM10, NO2, SO2, CO, and O3, along with ambient temperature and relative humidity.  
> 
> **(Action: Point to the HDFS tree nodes on screen):**  
> Adhering to enterprise big data architecture, we structured our **Hadoop HDFS cluster** into three dedicated data zones:  
> 1. `hdfs:///air_quality/raw/`: Storing our 47.3 MB raw JSON telemetry across HDFS blocks with a **128 MB default block size** and a **3x replication factor** for zero data loss.  
> 2. `hdfs:///air_quality/processed/`: Storing our cleaned, multi-pollutant dataset in columnar **Apache Parquet with Snappy compression**, achieving a 92% compression ratio. Crucially, we partitioned this dataset by `city` and `year`. This enables **partition pruning**, so Spark workers read only relevant disk partitions without scanning the full dataset.  
> 3. `hdfs:///air_quality/analytics/`: Storing pre-aggregated city-hour analytics marts.  
> 
> This distributed storage layer guarantees high data availability and enables Spark executors to read local blocks in parallel."*

#### [2:30 – 3:00] Smooth Hand-Off to Speaker 2
> **(Action: Click on Tab 3: CPCB NAQI Live Calculator):**  
> *"Now, I hand over the mic to **[Speaker 2 Name]**, who engineered our distributed Spark ETL pipeline and India's official CPCB NAQI regulatory compliance engine."*

---

### 🔵 PART 2: Distributed Spark ETL, CPCB NAQI Engine & Analytics (3:00 – 6:00)
**Speaker:** Person 2 (Distributed Data & Regulatory Lead)  
**Screen to Share:** Start on **`[Tab 3: CPCB NAQI Live Calculator]`**, then switch to **`[Tab 4: Spark SQL Analytics]`**.

#### [3:00 – 4:45] Distributed Spark ETL & CPCB NAQI Regulatory Compliance
> **(Say clearly):**  
> *"Thank you, [Speaker 1 Name]. Respected evaluators, once raw data sits in HDFS, **Apache Spark 4.2.0** drives our distributed transformations and regulatory intelligence.  
> 
> A critical scientific contribution of our work is strict adherence to India's official **Central Pollution Control Board (CPCB) National Air Quality Index (NAQI)** standards.  
> 
> A common flaw in student projects is taking an arithmetic average of pollutant concentrations. That is scientifically invalid: 60 µg/m³ of PM2.5 represents moderate air pollution, whereas 60 µg/m³ of SO2 is completely safe.  
> 
> In our Spark ETL job:  
> 1. **Unit Harmonization:** Continuous analyzers report gases in parts-per-billion (ppb). Under NTP conditions (25°C, 1 atm), our Spark pipeline harmonized all gases to mass concentrations (µg/m³) using molecular weights: NO2 was scaled by 1.88, SO2 by 2.62, CO to mg/m³ by 0.001145, and O3 by 1.96.  
> 2. **Sliding Window Rolling Averages:** Using Spark Window partitions, we computed sliding 24-hour moving averages for particulates (PM2.5, PM10, NO2, SO2) and 8-hour averages for CO and O3.  
> 3. **The 16-Hour Data Completeness Rule:** We strictly enforced CPCB's statutory rule—a daily average is valid only if at least 16 hours of valid data exist in that 24-hour window. Missing values are **never** imputed with zero, as zero implies pristine air.  
> 
> Out of 18,521 total hourly records, **12,792 station-hour records** met the strict 16-hour and minimum 3-pollutant criteria.  
> 
> **(Action: On Tab 3, click '🚨 Delhi Winter Smog' preset):**  
> As you can see live on screen, our engine computes individual sub-indices using CPCB linear segmented interpolation:  
> `Ip = ((I_hi - I_lo) / (B_hi - B_lo)) * (Cp - B_lo) + I_lo`  
> and applies the **maximum operator** to determine the overall AQI. Here, PM2.5 reaches an index of 438, accurately categorizing the air as **Severe**."*

#### [4:45 – 5:45] Spark SQL Analytics & Diurnal Atmospheric Dynamics
> **(Action: Click on Tab 4: Spark SQL Analytics. Point to the Diurnal Trends chart):**  
> *"Next, we executed distributed Spark SQL queries across our Parquet lake. This revealed two profound atmospheric insights:  
> 
> 1. **Bimodal Diurnal Inversion Dynamics:** As seen in our diurnal chart, PM2.5 exhibits two sharp peaks. The first occurs between **07:00 and 09:00 AM IST** due to morning rush-hour traffic trapped by a shallow nocturnal boundary layer. The second peak occurs between **21:00 and 23:00 IST**, caused by nighttime radiative cooling trapping vehicular emissions.  
> 2. **Geographic Hazard Asymmetry:** In Delhi NCR, **62.5% of all valid hours fell in the 'Severe' category** (AQI > 400), with a mean PM2.5 of 118.4 µg/m³. In sharp contrast, southern plateau stations in Bengaluru and Hyderabad maintained average PM2.5 around 34 µg/m³, with over 70% of hours in the 'Satisfactory' and 'Moderate' tiers.  
> 
> The entire Spark ETL and analytics job executed in **just 25.32 seconds** across our cluster."*

#### [5:45 – 6:00] Smooth Hand-Off to Speaker 3
> **(Action: Click on Tab 5: Spark MLlib Live Predictor):**  
> *"Now, I pass the mic to **[Speaker 3 Name]**, who led our distributed machine learning pipelines in Spark MLlib and will demonstrate our live forecasting model."*

---

### 🟣 PART 3: Spark MLlib Distributed ML, Forecasting & Live Demo (6:00 – 9:00)
**Speaker:** Person 3 (Distributed Machine Learning & Forecasting Lead)  
**Screen to Share:** Start on **`[Tab 5: Spark MLlib Live Predictor]`**, then switch to **`[Tab 6: Terminal Runner]`**.

#### [6:00 – 7:45] Machine Learning Architecture, Chronological Split & Baselines
> **(Say with enthusiasm):**  
> *"Thank you, [Speaker 2 Name]. Respected evaluators, I will now present our distributed machine learning models developed in **Spark MLlib**.  
> 
> To ensure that our machine learning evaluation was genuinely sound and publication-grade, we enforced three critical safeguards:  
> 
> 1. **Zero Data Leakage via Chronological Splitting:** In time-series forecasting, standard random K-Fold cross-validation leaks future weather patterns into past training folds, resulting in artificially high but fraudulent accuracy. We enforced a strict **chronological 80/20 block split**: the first 80% of historical timestamps (**10,294 observations**) were used for training, and the final 20% strictly future horizon (**2,570 observations**) was held out for testing.  
> 2. **Honest Benchmarking against a Naive Persistence Baseline:** In atmospheric physics, tomorrow's pollution is strongly correlated with today's. A model is only worthwhile if it outperforms the **Naive Persistence Baseline** (ŷ_{t+24} = y_t). Our persistence baseline achieved an **RMSE of 42.16 µg/m³**.  
> 3. **Distributed Feature Engineering:** Using Spark Window functions and `VectorAssembler`, we engineered multi-scale temporal lag features at t-1h, t-2h, t-3h, t-6h, t-12h, and t-24h, combined with temperature, humidity, and diurnal cyclical indicators.  
> 
> **(Action: Point to the Benchmark Table on Tab 5):**  
> We trained three distributed models via Spark MLlib Pipelines:  
> - Spark MLlib **Linear Regression with ElasticNet** achieved an RMSE of 37.86 µg/m³ (+10.2% improvement).  
> - Spark MLlib **Gradient-Boosted Trees (GBTRegressor)** achieved an RMSE of 37.61 µg/m³ (+10.8% improvement).  
> - Our best model—Spark MLlib **Random Forest Regressor**—achieved an **RMSE of 35.17 µg/m³ and MAE of 14.47 µg/m³**, delivering a **16.6% error reduction over the persistence baseline** with an R² of 0.306 in just **1.49 seconds of training time**!  
> 
> In addition, for civic emergency alerts, we trained a **Spark MLlib RandomForestClassifier** to forecast the 6 CPCB hazard tiers. It achieved **70.21% test accuracy** and a **weighted F1-score of 0.676**."*

#### [7:45 – 8:45] Live Interactive Prediction & Terminal Demonstration
> **(Action: On Tab 5, click '🔮 Forecast Next 24-Hours via Spark MLlib'):**  
> *"To demonstrate live inference, our interactive widget feeds lag features into our Spark MLlib model weights. In real-time, the model predicts tomorrow's PM2.5 level at 126.4 µg/m³, beating the baseline and flagging a 'Very Poor' hazard alert.  
> 
> **(Action: Switch to Tab 6: Terminal Runner & Shell. Click button '▶ 1. Run Complete Pipeline'):**  
> Furthermore, looking at our terminal console right now, I am triggering our master pipeline runner `./run_pipeline.sh`:  
> - In stage 1, it checks Hadoop HDFS NameNode and DataNodes.  
> - In stage 2, Spark ETL loads the 96,000 raw records from HDFS, applies the 16-hour validity filter, and writes Parquet in 25 seconds.  
> - In stage 3, Spark SQL executes the city analytics queries.  
> - In stages 4 and 5, Spark MLlib trains both regression and classification pipelines across our executor cores, completing the full end-to-end pipeline with exit code 0."*

#### [8:45 – 9:30] Conclusion & Project Hand-Over
> **(Say to wrap up):**  
> *"In conclusion, our project demonstrates a complete, reproducible big data solution: from raw API extraction into Hadoop HDFS, distributed cleaning and regulatory CPCB indexing via Spark SQL, to scalable forecasting with Spark MLlib.  
> 
> We have compiled our complete methodology, formulas, tables, and figures into a 1.3 MB Master PDF Report, and our code is fully synchronized on GitHub.  
> 
> Our team is now delighted to answer any questions from the panel. Thank you!"*

---

# 🛡️ Academic Viva Q&A Defense Strategy

Assign these specific questions to the team members so nobody speaks over each other during evaluation:

### Question 1: "Why did you use Hadoop HDFS and Apache Spark instead of Pandas and Scikit-Learn?"
- **Answered by:** **Speaker 1 (HDFS Lead)**
- **Say:** *"Single-node libraries like Pandas load the entire dataset into RAM on one machine. When scaling to multi-year telemetry across hundreds of stations and thousands of sensors, memory exhaustion occurs. In our Track B architecture, Hadoop HDFS distributes raw data blocks across DataNodes with 3x replication, and Apache Spark executes distributed transformations in-memory across parallel partitions. Our Spark MLlib pipeline distributes decision-tree node splits across executor cores simultaneously, training complex ensembles in under 2 seconds."*

### Question 2: "Can't we just calculate AQI by taking the average of all pollutant concentrations?"
- **Answered by:** **Speaker 2 (Spark ETL Lead)**
- **Say:** *"No, taking an arithmetic average of pollutant concentrations is scientifically invalid. Different air pollutants have completely different toxicities—for example, 60 µg/m³ of PM2.5 represents moderate air pollution, whereas 60 µg/m³ of SO2 is completely safe. We strictly implemented India's official CPCB NAQI standard: each pollutant's concentration is converted into an independent sub-index via linear segmented interpolation using official breakpoints, and the final AQI is determined by the maximum operator: AQI = max(I_1, I_2, ... I_n)."*

### Question 3: "Did you use K-Fold Cross-Validation for your machine learning models?"
- **Answered by:** **Speaker 3 (MLlib Lead)**
- **Say:** *"We specifically avoided random K-fold cross-validation because in time-series forecasting, random shuffling leaks future observations into past training sets, producing artificially inflated accuracy that collapses in real life. Instead, we implemented a strict chronological 80/20 block split: the first 80% of historical timestamps were used for training, and the final 20% strictly future horizon was held out for testing. This guarantees zero temporal data leakage."*

### Question 4: "Why did you benchmark against a Naive Persistence Baseline?"
- **Answered by:** **Speaker 3 (MLlib Lead)**
- **Say:** *"In atmospheric and environmental science, air pollution exhibits strong autocorrelation: tomorrow's pollution often resembles today's pollution. Simply reporting an R² or RMSE without a baseline is misleading. In Track B, evaluation must be genuinely sound. We established the persistence baseline (ŷ_{t+24} = y_t), which yielded an RMSE of 42.16 µg/m³. Our Spark MLlib Random Forest model beat this baseline by 16.6%, reducing RMSE to 35.17 µg/m³ and proving that our lag feature engineering extracted genuine meteorological and diurnal patterns."*

### Question 5: "How did you handle missing values in the sensor streams?"
- **Answered by:** **Speaker 2 (Spark ETL Lead)**
- **Say:** *"We never imputed missing sensor values with zero, because zero implies completely clean air and would catastrophically bias rolling averages downward. Instead, we enforced CPCB's statutory 16-hour completeness rule: if a 24-hour window had fewer than 16 valid readings, the AQI was flagged as invalid. In the ML feature pipeline, Spark's VectorAssembler dropped incomplete lag rows, ensuring only complete temporal histories entered the estimators."*

---
