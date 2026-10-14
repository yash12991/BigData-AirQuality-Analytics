# 3-Person Video Call Presentation Script & Defense Guide

**Project Title:** Distributed Urban Air Quality Analytics and AQI Forecasting  
**Architecture Track:** Track B — Machine Learning at Scale: $\text{HDFS} \rightarrow \text{Spark} \rightarrow \text{Spark MLlib}$  
**Standard Authority:** Central Pollution Control Board (CPCB), Government of India  
**Target Audience:** Project Review Committee, Evaluators, Technical Interviewers  
**Total Duration:** ~9 to 10 Minutes (~3 minutes per speaker) + Live Demo & Q&A  

---

## 👥 Speaker Roles & Division of Responsibilities

| Role | Team Member | Primary Presentation Focus |
| :--- | :--- | :--- |
| **Speaker 1** | *Data Engineer / Systems Architect* | Introduction, Problem Statement, OpenAQ API v3 Ingestion, and Hadoop HDFS Data Lake Architecture. |
| **Speaker 2** | *Big Data ETL & Regulatory Engineer* | Spark Distributed ETL, Gaseous Unit Harmonization, CPCB NAQI Regulatory Engine, and Spark SQL Analytics. |
| **Speaker 3** | *Machine Learning & MLOps Engineer* | Spark MLlib Distributed Regression & Classification, Chronological Leak-Free Validation, Benchmarks, Live Demo & Future Scope. |

---

## 🎙️ Complete Speaking Script (Word-for-Word)

---

### 🟢 SPEAKER 1: Introduction, Ingestion & Hadoop HDFS Data Lake (0:00 – 3:00)

#### Slide / Screen Share: Title Slide & System Architecture Diagram

> **[SPEAKER 1]:**  
> *"Good morning / afternoon, respected professors and evaluators.  
> 
> Today, our team is presenting our project: **Distributed Urban Air Quality Analytics and AQI Forecasting**, implemented strictly under **Track B: Machine Learning at Scale ($	ext{HDFS} ightarrow 	ext{Spark} ightarrow 	ext{Spark MLlib}$)**.  
> 
> To begin with our motivation: Urban air pollution is a catastrophic public health crisis in India. Government Continuous Ambient Air Quality Monitoring Stations (CAAQMS) deployed across major metropolitan centers generate continuous, multi-pollutant IoT sensor streams every 15 minutes.  
> 
> However, traditional single-machine tools like standard Python Pandas and Scikit-learn hit strict memory and computational bottlenecks when scaling to multi-year, multi-station telemetry with high-frequency rolling windows. Moreover, naive implementations often commit two severe flaws: they treat raw concentration values as AQI, and they use random cross-validation folds that leak future data into the past.  
> 
> To solve this, our team engineered an end-to-end distributed big-data architecture.  
> 
> **First, Data Acquisition:** We interfaced directly with the official **OpenAQ Platform using API version 3**. Our custom ingestion client features rate-limit monitoring—staying strictly within the 60 requests-per-minute quota—automatic exponential backoff retry on HTTP errors, and checkpointed resumable pagination. We extracted **96,000 raw hourly observations** (47.3 MB) across 4 high-density CAAQMS stations in **Delhi NCR (R K Puram and Anand Vihar), Bengaluru (BTM Layout), and Hyderabad (Central University)**, covering six criteria pollutants: $	ext{PM}_{2.5}$, $	ext{PM}_{10}$, $	ext{NO}_2$, $	ext{SO}_2$, $	ext{CO}$, and $	ext{O}_3$, alongside temperature and humidity.  
> 
> **Second, Distributed Storage in Hadoop HDFS:** As mandated by Track B, all raw data is stored directly in **Hadoop HDFS 3.3.6**. We designed three dedicated storage zones:  
> 1. `hdfs:///air_quality/raw/` *where our 47.3 MB raw JSON telemetry resides.*  
> 2. `hdfs:///air_quality/processed/` *hosting our columnar Apache Parquet lake, partitioned by city and year.*  
> 3. `hdfs:///air_quality/analytics/` *for pre-aggregated summary tables.*  
> 
> By keeping raw and processed data in HDFS, our Spark workers can stream and process data blocks in parallel without disk I/O bottlenecks.  
> 
> I will now hand over to **[Speaker 2]**, who will explain how Apache Spark handles distributed ETL and enforces India's official CPCB AQI regulatory standards."*

---

### 🔵 SPEAKER 2: Distributed Spark ETL & Regulatory Analytics (3:00 – 6:00)

#### Slide / Screen Share: ETL Pipeline, CPCB NAQI Formulas & Analytics Charts (`reports/figures/`)

> **[SPEAKER 2]:**  
> *"Thank you, [Speaker 1]. Respected evaluators, I will now explain our distributed processing tier and regulatory compliance engine.  
> 
> Once data sits in HDFS, **Apache Spark 4.2.0** handles distributed loading and feature preparation. In our Spark ETL job:  
> 
> **1. Schema Enforcement & Unit Harmonization:**  
> Raw continuous sensor analyzers often report gaseous pollutants in volume mixing ratios like parts-per-billion (ppb). However, official Indian regulatory formulas require mass concentrations in micrograms per cubic meter. Under NTP conditions (25°C and 1 atmosphere), our Spark pipeline converted all gases: $	ext{NO}_2$ was scaled by 1.88, $	ext{SO}_2$ by 2.62, $	ext{CO}$ to milligrams per cubic meter by 0.001145, and $	ext{O}_3$ by 1.96.  
> 
> **2. Multi-Pollutant Station-Hour Pivoting:**  
> We pivoted the raw parameter streams into **18,521 aligned station-hour observations** across our target metros.  
> 
> **3. Strict CPCB NAQI Regulatory Compliance:**  
> A core requirement from our rubric is that calculations must be **genuinely sound, not just present**. Many projects make the mistake of averaging raw concentrations. That is scientifically invalid because 60 µg/m³ of $	ext{PM}_{2.5}$ is moderate pollution, while 60 µg/m³ of $	ext{SO}_2$ is completely clean.  
> 
> We implemented the official **CPCB National Air Quality Index (NAQI)** methodology:  
> - Using Spark Window partitions, we computed sliding **24-hour moving averages** for $	ext{PM}_{2.5}$, $	ext{PM}_{10}$, $	ext{NO}_2$, and $	ext{SO}_2$, and **8-hour averages** for $	ext{CO}$ and $	ext{O}_3$.  
> - We strictly enforced CPCB's **16-hour validity rule**: an average is valid only if at least 16 hours of data exist in that 24-hour cycle. Missing values are **never** replaced with zeros.  
> - Out of 18,521 hours, **12,792 station-hour records** met the strict multi-pollutant validity criteria.  
> - We computed individual sub-indices using CPCB linear segmented interpolation, and applied the **maximum operator** to determine the overall composite AQI.  
> - This entire distributed ETL job runs across the cluster in **just 25 seconds**, persisting partitioned Parquet directly back into HDFS.  
> 
> **4. Spark SQL Analytics Insights:**  
> Querying the Parquet lake with Spark SQL revealed stark environmental realities:  
> - **Delhi NCR Particulate Burden:** Delhi stations recorded a mean $	ext{PM}_{2.5}$ of **121.9 µg/m³** and an average AQI of **382**, with **62.5% of all monitored hours falling in the 'Severe' category** ($>400$).  
> - **Diurnal Inversion Peak:** In our diurnal charts, particulate concentrations follow a pronounced bimodal cycle, peaking sharply between **6:00 AM and 9:00 AM IST** due to morning rush-hour traffic trapped by shallow morning inversion layers, and peaking again between **9:00 PM and 11:00 PM IST**.  
> - **Regional Baseline:** In contrast, Bengaluru and Hyderabad maintained average $	ext{PM}_{2.5}$ levels around **28 µg/m³**, with over 40% of hours in the 'Satisfactory' health bracket.  
> 
> Now, I will pass it to **[Speaker 3]**, who will walk you through our distributed machine learning models in Spark MLlib and demonstrate the live running pipeline."*

---

### 🟣 SPEAKER 3: Spark MLlib Distributed ML, Benchmarks & Live Demo (6:00 – 9:30)

#### Slide / Screen Share: Model Evaluation Tables, Forecast Plots & Terminal for Live Demo

> **[SPEAKER 3]:**  
> *"Thank you, [Speaker 2]. Respected evaluators, I will now present our distributed machine learning implementation in **Spark MLlib** and conduct our live execution.  
> 
> To guarantee that our machine learning evaluation is scientifically sound and free from bias, we enforced three rigorous principles:  
> 
> **1. Leak-Free Chronological Splitting:**  
> Standard random K-Fold cross-validation is completely invalid for time-series data because it leaks future weather and seasonal trends into past training sets. We implemented a strict chronological timestamp cutoff: the first **80% of historical observations (10,294 samples)** was used exclusively for training, and the final **20% strictly future horizon (2,570 samples)** was held out for evaluation.  
> 
> **2. Multi-Scale Lag Feature Engineering:**  
> Using Spark Window functions, we engineered multi-scale temporal lags at $t-1	ext{h}$, $t-2	ext{h}$, $t-3	ext{h}$, $t-6	ext{h}$, $t-12	ext{h}$, and $t-24	ext{h}$, combined with diurnal indicators and meteorological covariates. Our Spark ML Pipeline assembled and normalized these into dense feature vectors using `VectorAssembler` and `StandardScaler`.  
> 
> **3. Honest Benchmarking against Persistence:**  
> In atmospheric science, tomorrow's air quality is strongly correlated with today's. A model is only valuable if it beats the standard **Naive Persistence Baseline** ($\hat{y}_{t+24} = y_t$).  
> - Our Naive Persistence Baseline yielded an **RMSE of 42.16 µg/m³**.  
> - Spark MLlib **Linear Regression with ElasticNet** reduced RMSE to **37.86 µg/m³** (+10.2% improvement).  
> - Spark MLlib **Gradient-Boosted Trees (GBTRegressor)** achieved an RMSE of **37.61 µg/m³** (+10.8% improvement).  
> - Our champion model, Spark MLlib **Random Forest Regressor**, achieved an **RMSE of 35.17 µg/m³ and MAE of 14.47 µg/m³**, delivering a **16.6% error reduction over the persistence baseline** with an $R^2$ of 0.306 in just 1.5 seconds of training.  
> 
> Furthermore, for smart city alert systems, we trained a second distributed model: a **Spark MLlib RandomForestClassifier** predicting future CPCB hazard categories (Good to Severe). It achieved a **test accuracy of 70.21%** and a **weighted F1-score of 0.676**.  
> 
> **Live Pipeline Demonstration:**  
> If you look at my terminal screen right now, I am running `./run_pipeline.sh`:  
> - *[Point to screen]* The script verifies Hadoop HDFS NameNode and DataNodes.  
> - Spark ETL ingests 96,000 records from HDFS, applies the 16-hour CPCB rules, and updates the partitioned Parquet lake in 25 seconds.  
> - Spark SQL executes the city analytics queries.  
> - Spark MLlib trains and benchmarks both regression and classification pipelines across our executor cores.  
> 
> **Future Scope:**  
> As future work, this pipeline can be extended to near-real-time streaming using **Spark Structured Streaming with Apache Kafka**, and spatial sensor network dispersion modeling using **Apache Spark GraphX**.  
> 
> All code, reports, and architecture specifications are committed to our GitHub repository. Our team is now ready to answer any questions. Thank you!"*

---

## 5. Q&A Defense Strategy for the Team

When questions are asked by the panel, divide the answers based on your roles:

* **If asked about HDFS, Data Storage, or Ingestion:** $ightarrow$ **[Speaker 1] answers**
  - *Key point to state:* "We stored 96,000 raw JSONL records in `hdfs:///air_quality/raw/` and partitioned processed Parquet by city and year to enable predicate pushdown and minimize executor I/O shuffle."
* **If asked about CPCB Formulas, AQI calculation, or ETL:** $ightarrow$ **[Speaker 2] answers**
  - *Key point to state:* "We implemented the official CPCB linear segmented sub-index formula and the maximum operator: $	ext{AQI} = \max(I_p)$. We enforced the 16-hour completeness rule and converted all gases from ppb to µg/m³ under NTP conditions."
* **If asked about Machine Learning, Splitting, or MLlib:** $ightarrow$ **[Speaker 3] answers**
  - *Key point to state:* "We used a chronological block split (80/20) to prevent future data leakage, and proved that our Random Forest model beat the persistence baseline by 16.6%, reducing RMSE from 42.16 to 35.17 µg/m³."
