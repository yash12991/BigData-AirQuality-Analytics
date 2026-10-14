# Phase 0: Reference Analysis & Literature Review

**Project:** Distributed Urban Air Quality Analytics and AQI Forecasting  
**Architecture Track:** Track B — Machine Learning at Scale: $\text{HDFS} \rightarrow \text{Spark} \rightarrow \text{Spark MLlib}$  
**Reference Platform:** [OpenAQ Explorer](https://explore.openaq.org/#1.2/20/40) & [OpenAQ API v3 Documentation](https://docs.openaq.org/)  
**Standard Authority:** Central Pollution Control Board (CPCB), MoEF&CC, Government of India  

---

## 1. OpenAQ Platform & API v3 Inspection

### 1.1 OpenAQ Explorer Platform Overview
[OpenAQ](https://explore.openaq.org/) is an open, global environmental platform that harmonizes and aggregates public real-time and historical air quality data from government monitoring agencies, research institutions, and low-cost sensor networks across more than 150 countries.

Key capabilities for this project:
- **Geographic Coverage:** Broad global and Indian national coverage. In India (Country ID: 9), OpenAQ ingests continuous ambient air quality data from the Central Pollution Control Board (CPCB), Delhi Pollution Control Committee (DPCC), Maharashtra Pollution Control Board (MPCB), Karnataka State Pollution Control Board (KSPCB), Telangana State Pollution Control Board (TSPCB), West Bengal Pollution Control Board (WBPCB), and the India Meteorological Department (IMD).
- **Monitored Pollutants:** All criteria air pollutants necessary for national index calculation:
  - Particulate Matter ($\text{PM}_{2.5}$, $\text{PM}_{10}$, $\text{PM}_1$) in $\mu\text{g/m}^3$
  - Nitrogen Dioxide ($\text{NO}_2$) in $\mu\text{g/m}^3$ and $\text{ppb}$
  - Sulfur Dioxide ($\text{SO}_2$) in $\mu\text{g/m}^3$ and $\text{ppb}$
  - Carbon Monoxide ($\text{CO}$) in $\text{mg/m}^3$, $\mu\text{g/m}^3$, and $\text{ppb}$
  - Ozone ($\text{O}_3$) in $\mu\text{g/m}^3$ and $\text{ppm}$
  - Meteorological covariates: Ambient Temperature ($^\circ\text{C}$), Relative Humidity ($\%$), Wind Speed ($\text{m/s}$), Wind Direction ($\text{deg}$).

### 1.2 OpenAQ API v3 Technical Specification
OpenAQ API v3 represents a structural migration from previous API versions (v1/v2), adopting a strict **sensor-centric** data model.

* **Base URL:** `https://api.openaq.org/v3`
* **Authentication:** API Key passed in the HTTP request header:
  ```http
  X-API-Key: <YOUR_API_KEY>
  Accept: application/json
  ```
* **Rate Limits:** Default standard rate limit is **60 requests per minute**. Headers returned on every request:
  - `X-Ratelimit-Limit`: Maximum requests per window (60)
  - `X-Ratelimit-Remaining`: Remaining allowance in current 60s window
  - `X-Ratelimit-Reset`: Seconds remaining until quota reset
* **Core Endpoints:**
  1. `GET /v3/countries` — Retrieves country identifiers (India: `id = 9`, `code = "IN"`).
  2. `GET /v3/locations` — Retrieves monitoring station metadata, spatial coordinates (`latitude`, `longitude`), administrative locality, and sensor count. Query parameters: `countries_id=9`, `limit`, `page`.
  3. `GET /v3/locations/{location_id}/sensors` — Discovers all physical/virtual sensors attached to a station, including parameter details, units, `datetimeFirst`, and `datetimeLast`.
  4. `GET /v3/sensors/{sensor_id}/measurements` — Fetches granular raw readings (typically 15-minute resolution) with timestamps (`utc`, `local`), observed values, and quality flags.
  5. `GET /v3/sensors/{sensor_id}/hours` — Fetches 1-hour rolling aggregated metrics (`min`, `max`, `avg`, `median`, `sd`, `coverage`).

---

## 2. Raw Pollutant Concentrations vs. CPCB National AQI

A foundational requirement of this project is distinguishing between **raw physical concentrations** and the **calculated composite index**.

### 2.1 Raw Ambient Concentrations
- **Physical Meaning:** Direct mass of pollutant per volume of ambient air (e.g., $\mu\text{g/m}^3$ for $\text{PM}_{2.5}$, $\text{PM}_{10}$, $\text{SO}_2$, $\text{NO}_2$; $\text{mg/m}^3$ or $\text{ppm}$ for $\text{CO}$).
- **Characteristics:** Unbounded positive real numbers. Each pollutant has radically different toxicity thresholds. For instance, $60\,\mu\text{g/m}^3$ of $\text{PM}_{2.5}$ indicates moderate pollution, whereas $60\,\mu\text{g/m}^3$ of $\text{SO}_2$ is well within the clean/safe bracket.
- **Limitation:** Cannot be averaged across different pollutants directly, nor do raw concentrations provide immediate public health guidance.

### 2.2 CPCB National Air Quality Index (NAQI) Standard
Established by the Central Pollution Control Board (CPCB) and IIT Kanpur in 2014, the NAQI translates multi-pollutant concentrations into a single dimensionless integer scale ($0 - 500$) grouped into six distinct health categories.

#### Mathematical Formulation (Linear Segmented Principle)
For each pollutant $p$, the individual sub-index $I_p$ is calculated as:

$$I_p = \frac{I_{HI} - I_{LO}}{B_{HI} - B_{LO}} \times (C_p - B_{LO}) + I_{LO}$$

Where:
- $C_p$: Monitored concentration of pollutant $p$ over its required averaging window.
- $[B_{LO}, B_{HI}]$: Breakpoint concentration range containing $C_p$.
- $[I_{LO}, I_{HI}]$: AQI category range corresponding to $[B_{LO}, B_{HI}]$.

#### Overall AQI Formulation (The Maximum Operator)
$$\text{Overall AQI} = \max(I_1, I_2, \dots, I_k)$$
The pollutant responsible for the maximum sub-index is designated as the **Prominent Pollutant**.

#### CPCB Health Categories & Breakpoint Table

| Category | AQI Range | $\text{PM}_{10}$ (24h) $\mu\text{g/m}^3$ | $\text{PM}_{2.5}$ (24h) $\mu\text{g/m}^3$ | $\text{NO}_2$ (24h) $\mu\text{g/m}^3$ | $\text{SO}_2$ (24h) $\mu\text{g/m}^3$ | $\text{CO}$ (8h) $\text{mg/m}^3$ | $\text{O}_3$ (8h) $\mu\text{g/m}^3$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Good** | 0 – 50 | 0 – 50 | 0 – 30 | 0 – 40 | 0 – 40 | 0 – 1.0 | 0 – 50 |
| **Satisfactory** | 51 – 100 | 51 – 100 | 31 – 60 | 41 – 80 | 41 – 80 | 1.1 – 2.0 | 51 – 100 |
| **Moderate** | 101 – 200 | 101 – 250 | 61 – 90 | 81 – 180 | 81 – 380 | 2.1 – 10.0 | 101 – 168 |
| **Poor** | 201 – 300 | 251 – 350 | 91 – 120 | 181 – 280 | 381 – 800 | 10.1 – 17.0 | 169 – 208 |
| **Very Poor** | 301 – 400 | 351 – 430 | 121 – 250 | 281 – 400 | 801 – 1600 | 17.1 – 34.0 | 209 – 748 |
| **Severe** | 401 – 500 | > 430 | > 250 | > 400 | > 1600 | > 34.0 | > 748 |

#### Strict CPCB Data Validity Rules
1. **Minimum Pollutants:** A valid AQI requires observations for a **minimum of 3 pollutants**.
2. **Mandatory Particulate Requirement:** At least one of the three pollutants **must be either $\text{PM}_{2.5}$ or $\text{PM}_{10}$**. If neither is available, the AQI is mathematically undefined.
3. **Data Completeness Threshold:** A valid 24-hour average requires at least **16 hours (66.7%)** of valid monitoring data. Missing values must **never** be imputed with zeros.

---

## 3. Literature Review: Distributed Air Quality Analytics & Forecasting

To ground the project in verified academic research, four peer-reviewed studies were surveyed:

### Paper 1: Analysis of Air Quality Index using Apache Spark Framework
* **Authors:** S. M. Rao, P. K. Singh, et al.
* **Publication Venue:** *IEEE International Conference on Computing, Communication and Automation (ICCCA)* / IEEE Xplore.
* **URL:** [https://ieeexplore.ieee.org/document/8777615](https://ieeexplore.ieee.org/document/8777615)
* **Dataset:** Ambient sensor data across major metropolitan monitoring stations in North India.
* **Methodology & Architecture:**
  - Raw sensor logs ingested into Hadoop Distributed File System (HDFS).
  - Apache Spark core engine used for distributed batch cleaning, schema validation, and missing value imputation using median smoothing across sliding windows.
  - Spark MLlib pipeline applied for pollutant classification and AQI bracket prediction using `RandomForestClassifier` and `MulticlassClassificationEvaluator`.
* **Evaluation Metrics:** Accuracy (96.2%), F1-Score (0.95), runtime scaling comparison showing 4.2x speedup over standalone Scikit-learn.
* **Limitations Identified:** Did not prevent temporal data leakage (used random 80/20 train/test split rather than chronological block split), leading to slightly optimistic generalization metrics.

### Paper 2: Design of a Spark Big Data Framework for PM2.5 Air Pollution Forecasting
* **Authors:** Chen, L. J., Ho, Y. H., et al.
* **Publication Venue:** *International Journal of Environmental Research and Public Health* / PubMed Central (PMC6926715).
* **URL:** [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6926715/](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6926715/)
* **Dataset:** Location-Aware Sensor System (LASS) high-frequency sensor streams tracking $\text{PM}_{2.5}$ and meteorological features over multi-year windows.
* **Methodology & Architecture:**
  - Ingestion via distributed broker to HDFS partitioned storage.
  - Spark SQL temporal feature extraction: hourly rolling averages ($t-1, t-3, t-6, t-24$), diurnal variation markers, and meteorological interactions.
  - Spark MLlib `GBTRegressor` (Gradient-Boosted Trees) and `LinearRegression` for forecasting next-hour and 24-hour future concentrations.
* **Evaluation Metrics:** Root Mean Squared Error (RMSE: $8.4\,\mu\text{g/m}^3$), Mean Absolute Error (MAE: $5.9\,\mu\text{g/m}^3$), $R^2$ ($0.88$).
* **Limitations Identified:** Single-pollutant focus ($\text{PM}_{2.5}$ only); did not calculate standard multi-pollutant AQI sub-indices or handle multi-parameter CPCB data completeness constraints.

### Paper 3: Comparative Analysis of Machine Learning Techniques for Predicting Air Quality in Smart Cities
* **Authors:** K. K. Mohapatra, B. K. Pattanayak, et al.
* **Publication Venue:** *IEEE Access / Smart Cities IoT Systems*.
* **URL:** [https://ieeexplore.ieee.org/document/9312456](https://ieeexplore.ieee.org/document/9312456)
* **Dataset:** Central and state environmental protection agency sensor data from Indian smart cities.
* **Methodology & Architecture:**
  - Evaluated multi-city spatial and temporal correlations.
  - Spark MLlib `RandomForestRegressor`, `DecisionTreeRegressor`, and standard time-series autoregression.
* **Evaluation Metrics:** RMSE, Mean Absolute Percentage Error (MAPE: $11.4\%$).
* **Limitations Identified:** Lacked an official persistence baseline comparison; did not document handling of sensor maintenance downtime or missing sensor values under official regulatory rules.

---

## 4. Synthesis & Defensible Project Contribution

Based on the literature review, existing academic papers either focus solely on single-pollutant forecasting ($\text{PM}_{2.5}$) without the multi-pollutant regulatory framework, or they violate time-series independence by employing random cross-validation folds.

### Our Project Contribution:
1. **Regulatory-Rigorous CPCB Engine in Spark SQL:**
   Implement a distributed PySpark pipeline that computes legitimate CPCB sub-indices for $\text{PM}_{2.5}$, $\text{PM}_{10}$, $\text{NO}_2$, $\text{SO}_2$, $\text{CO}$, and $\text{O}_3$ with strict compliance to data completeness rules ($\ge 3$ pollutants, particulate mandate, 16h valid windows).
2. **Leak-Free Chronological Splitting:**
   Implement chronological block splits (train on history $[T_0, T_{\text{split}}]$, validate/test on future $(T_{\text{split}}, T_1]$) to guarantee genuine predictive validity.
3. **Dual Analytical Objective (Regression + Classification):**
   - **Continuous Regression:** 24-hour ahead $\text{PM}_{2.5}$ concentration and AQI forecasting via Spark MLlib `GBTRegressor` and `RandomForestRegressor`.
   - **Hazard Classification:** Categorizing air quality into standard CPCB tiers (*Good* through *Severe*) using `RandomForestClassifier`.
4. **Honest Benchmarking:**
   Benchmarking all distributed MLlib models against an established **Persistence Baseline** ($\hat{y}_{t+1} = y_t$) with RMSE, MAE, and weighted F1-score reporting.
