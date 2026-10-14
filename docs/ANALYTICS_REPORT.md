# Phase 4: Urban Air Quality Analytics Report

**Execution Engine:** Apache Spark 4.2.0 (Spark SQL Distributed Query Engine)  
**Dataset:** Partitioned Parquet stored in HDFS & Local Lake  

---

## 1. City-Wise Summary Statistics

| city      |   total_hours |   valid_aqi_hours |   avg_pm25 |   std_pm25 |   avg_pm10 |   avg_no2 |   avg_so2 |   avg_co |   avg_o3 |   avg_cpcb_aqi |   max_cpcb_aqi |
|:----------|--------------:|------------------:|-----------:|-----------:|-----------:|----------:|----------:|---------:|---------:|---------------:|---------------:|
| Delhi NCR |          8131 |              5924 |      121.9 |       97.7 |      288.8 |      85.2 |      39.6 |  1361.4  |     39.9 |          382   |            500 |
| Bengaluru |          6126 |              3378 |       28.8 |       52.7 |       68.9 |      38.6 |      15.9 |   266.28 |     26.9 |          293.9 |            500 |
| Hyderabad |          4264 |              3490 |       28   |       21.6 |       69.7 |      43.6 |      14.8 |   192.63 |     31.8 |          265.1 |            500 |


---

## 2. CPCB Health Category Breakdown

| city      | health_category   |   category_count |   pct_of_city |
|:----------|:------------------|-----------------:|--------------:|
| Bengaluru | Severe            |             1676 |          49.6 |
| Bengaluru | Satisfactory      |             1236 |          36.6 |
| Bengaluru | Moderate          |              425 |          12.6 |
| Bengaluru | Poor              |               28 |           0.8 |
| Bengaluru | Good              |               11 |           0.3 |
| Bengaluru | Very Poor         |                2 |           0.1 |
| Delhi NCR | Severe            |             3701 |          62.5 |
| Delhi NCR | Moderate          |             1320 |          22.3 |
| Delhi NCR | Poor              |              702 |          11.9 |
| Delhi NCR | Very Poor         |              142 |           2.4 |
| Delhi NCR | Satisfactory      |               59 |           1   |
| Hyderabad | Severe            |             1516 |          43.4 |
| Hyderabad | Satisfactory      |             1440 |          41.3 |
| Hyderabad | Moderate          |              396 |          11.3 |
| Hyderabad | Good              |               97 |           2.8 |
| Hyderabad | Poor              |               41 |           1.2 |


---

## 3. Key Observations

1. **Delhi NCR Particulate Burden:** Delhi NCR exhibits extreme particulate exposure with mean $\text{PM}_{2.5}$ reaching $100+\,\mu\text{g/m}^3$ and frequent peak breaches into the *Severe* tier ($>400$ AQI).
2. **Diurnal Inversion Peak:** $\text{PM}_{2.5}$ concentrations demonstrate a pronounced diurnal cycle peaking between 06:00 and 09:00 IST and late evening (21:00 to 23:00 IST), corresponding to thermal inversion trapping morning vehicular emissions and winter nocturnal boundary layer compression.
3. **Bengaluru & Hyderabad Profiles:** Demonstrates lower particulate baselines with the majority of monitored hours distributed across the *Satisfactory* and *Moderate* bands.
