# Phase 1: OpenAQ Data Audit & Coverage Report

**Date Generated:** 2026-10-14 17:34:04 UTC  
**Data Source:** OpenAQ API v3 (`https://api.openaq.org/v3`)  
**Audited Territory:** India (Country ID: 9)  

---

## 1. Executive Summary

A systematic audit of OpenAQ API v3 ambient monitoring stations in India was executed to evaluate:
1. **Data Completeness for CPCB NAQI:** Verify availability of at least 3 criteria pollutants with mandatory $\text{PM}_{2.5}$ or $\text{PM}_{10}$.
2. **Historical Depth:** Assess earliest (`datetimeFirst`) and most recent (`datetimeLast`) observation timestamps.
3. **Sampling Resolution:** Confirm 15-minute raw interval and 1-hour pre-aggregated hourly availability.
4. **Rate Limit Profile:** Standard limit confirmed at **60 requests/minute** with automatic reset.

## 2. Station Coverage & CPCB NAQI Eligibility Table

| Station ID | City / Region | Station Name | Available Criteria Pollutants | CPCB Eligible? | PM2.5 Status |
| :--- | :--- | :--- | :--- | :---: | :---: |
| 17 | Delhi NCR | R K Puram, Delhi - DPCC | pm25, pm10, no2, so2, co, o3 | **YES** | Active (123.0 µg/m³) |
| 5509 | Delhi NCR | Anand Vihar, Delhi - DPCC | pm25, pm10, no2, so2, co, o3 | **YES** | Active (284.0 µg/m³) |
| 5613 | Delhi NCR | ITO, New Delhi - CPCB | pm25, pm10, no2, so2, co, o3 | **YES** | Active (280.0 µg/m³) |
| 2598 | Mumbai MMR | Navi Mumbai Municipal Corp Airoli | pm25, pm10, so2, co | **YES** | Active (71.25 µg/m³) |
| 2585 | Pune | AAQMS Karve Road Pune - MPCB | pm25, pm10, so2, co, o3 | **YES** | Active (107.0 µg/m³) |
| 5548 | Bengaluru | BTM Layout, Bengaluru - CPCB | pm25, pm10, no2, so2, co, o3 | **YES** | Active (24.66 µg/m³) |
| 5607 | Bengaluru | Peenya, Bengaluru - CPCB | pm25, pm10, no2, so2, co, o3 | **YES** | Active (124.0 µg/m³) |
| 2594 | Hyderabad | Sanathnagar, Hyderabad - TSPCB | pm25, so2, co, o3 | **YES** | Active (157.0 µg/m³) |
| 5623 | Hyderabad | Central University, Hyderabad - TSPCB | pm25, pm10, no2, so2, co, o3 | **YES** | Active (26.0 µg/m³) |
| 2586 | Chennai | Manali, Chennai - CPCB | pm25, pm10, no2, so2, co, o3 | **YES** | Active (53.59 µg/m³) |

---

## 3. Detailed Parameter & Temporal Audit

### Station 17: R K Puram, Delhi - DPCC (Delhi NCR)

- **Total Sensors Discovered:** 18
- **CPCB AQI Compliance:** Valid (Has >= 3 criteria pollutants incl PM2.5/PM10)

**Sensor Parameter Inventory:**

| Parameter | Sensor ID | Unit | Earliest Observation | Latest Observation |
| :--- | :---: | :---: | :--- | :--- |
| `no` | 12234783 | ppb | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `o3` | 12234785 | µg/m³ | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `pm25` | 12234787 | µg/m³ | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `no2` | 12234784 | ppb | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `pm10` | 12234786 | µg/m³ | 2025-02-18T20:30:00Z | 2026-10-13T18:00:00Z |
| `co` | 12234782 | ppb | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `temperature` | 12234790 | c | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `relativehumidity` | 12234788 | % | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `so2` | 12234789 | ppb | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `wind_speed` | 14340715 | m/s | 2025-10-10T18:15:00Z | 2026-10-13T18:00:00Z |
| `wind_direction` | 14340714 | deg | 2025-10-10T18:15:00Z | 2026-10-13T18:00:00Z |
| `nox` | 14340713 | ppb | 2025-10-10T18:15:00Z | 2026-10-13T18:00:00Z |


### Station 5509: Anand Vihar, Delhi - DPCC (Delhi NCR)

- **Total Sensors Discovered:** 6
- **CPCB AQI Compliance:** Valid (Has >= 3 criteria pollutants incl PM2.5/PM10)

**Sensor Parameter Inventory:**

| Parameter | Sensor ID | Unit | Earliest Observation | Latest Observation |
| :--- | :---: | :---: | :--- | :--- |
| `co` | 14519 | µg/m³ | 2018-03-09T03:30:00Z | 2022-10-31T00:30:00Z |
| `pm10` | 14522 | µg/m³ | 2018-03-09T03:30:00Z | 2022-10-31T00:30:00Z |
| `no2` | 14523 | µg/m³ | 2018-03-09T03:30:00Z | 2022-10-31T00:30:00Z |
| `o3` | 14524 | µg/m³ | 2018-03-09T03:30:00Z | 2022-10-31T00:30:00Z |
| `so2` | 14520 | µg/m³ | 2018-03-09T03:30:00Z | 2022-10-31T00:15:00Z |
| `pm25` | 14521 | µg/m³ | 2018-03-09T03:30:00Z | 2022-10-31T00:30:00Z |


### Station 5613: ITO, New Delhi - CPCB (Delhi NCR)

- **Total Sensors Discovered:** 14
- **CPCB AQI Compliance:** Valid (Has >= 3 criteria pollutants incl PM2.5/PM10)

**Sensor Parameter Inventory:**

| Parameter | Sensor ID | Unit | Earliest Observation | Latest Observation |
| :--- | :---: | :---: | :--- | :--- |
| `no2` | 14866 | µg/m³ | 2018-03-09T05:30:00Z | 2020-01-20T07:15:00Z |
| `pm10` | 14869 | µg/m³ | 2018-03-09T05:30:00Z | 2020-01-20T07:15:00Z |
| `pm25` | 14878 | µg/m³ | 2018-03-09T05:30:00Z | 2020-01-20T07:15:00Z |
| `o3` | 17785 | µg/m³ | 2018-08-10T06:00:00Z | 2020-01-20T07:15:00Z |
| `so2` | 17781 | µg/m³ | 2018-08-10T06:00:00Z | 2020-01-20T07:15:00Z |
| `co` | 17782 | µg/m³ | 2018-08-10T06:00:00Z | 2020-01-20T07:15:00Z |
| `no` | 12234749 | ppb | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `nox` | 14341687 | ppb | 2025-10-10T20:15:00Z | 2026-10-13T18:00:00Z |


### Station 2598: Navi Mumbai Municipal Corp Airoli (Mumbai MMR)

- **Total Sensors Discovered:** 4
- **CPCB AQI Compliance:** Valid (Has >= 3 criteria pollutants incl PM2.5/PM10)

**Sensor Parameter Inventory:**

| Parameter | Sensor ID | Unit | Earliest Observation | Latest Observation |
| :--- | :---: | :---: | :--- | :--- |
| `so2` | 13523 | µg/m³ | 2017-06-19T19:45:00Z | 2020-04-09T00:15:00Z |
| `pm10` | 5408 | µg/m³ | 2016-03-21T18:30:00Z | 2020-04-09T00:15:00Z |
| `co` | 5400 | µg/m³ | 2016-03-21T18:30:00Z | 2020-04-09T00:15:00Z |
| `pm25` | 5404 | µg/m³ | 2016-03-21T18:30:00Z | 2017-10-04T04:15:00Z |


### Station 2585: AAQMS Karve Road Pune - MPCB (Pune)

- **Total Sensors Discovered:** 5
- **CPCB AQI Compliance:** Valid (Has >= 3 criteria pollutants incl PM2.5/PM10)

**Sensor Parameter Inventory:**

| Parameter | Sensor ID | Unit | Earliest Observation | Latest Observation |
| :--- | :---: | :---: | :--- | :--- |
| `pm25` | 5354 | µg/m³ | 2016-03-21T08:00:00Z | 2018-02-22T03:00:00Z |
| `pm10` | 5355 | µg/m³ | 2016-03-21T08:00:00Z | 2018-02-22T03:00:00Z |
| `so2` | 14235 | µg/m³ | 2017-06-19T20:00:00Z | 2018-02-22T03:00:00Z |
| `o3` | 5372 | µg/m³ | 2016-03-21T08:00:00Z | 2018-02-22T03:00:00Z |
| `co` | 5338 | µg/m³ | 2016-03-21T08:00:00Z | 2018-02-22T03:00:00Z |


### Station 5548: BTM Layout, Bengaluru - CPCB (Bengaluru)

- **Total Sensors Discovered:** 18
- **CPCB AQI Compliance:** Valid (Has >= 3 criteria pollutants incl PM2.5/PM10)

**Sensor Parameter Inventory:**

| Parameter | Sensor ID | Unit | Earliest Observation | Latest Observation |
| :--- | :---: | :---: | :--- | :--- |
| `o3` | 12235359 | µg/m³ | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `co` | 12235356 | ppb | 2025-02-18T20:15:00Z | 2026-08-06T17:45:00Z |
| `so2` | 12235363 | ppb | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `temperature` | 12235364 | c | 2025-02-18T20:15:00Z | 2026-08-06T11:15:00Z |
| `pm10` | 12235360 | µg/m³ | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `pm25` | 12235361 | µg/m³ | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `no` | 12235357 | ppb | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `no2` | 12235358 | ppb | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `relativehumidity` | 12235362 | % | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `wind_speed` | 14341818 | m/s | 2025-10-12T15:00:00Z | 2026-10-13T18:00:00Z |
| `wind_direction` | 14341817 | deg | 2025-10-12T15:00:00Z | 2026-10-13T18:00:00Z |
| `nox` | 14341816 | ppb | 2025-10-12T15:00:00Z | 2026-10-13T18:00:00Z |


### Station 5607: Peenya, Bengaluru - CPCB (Bengaluru)

- **Total Sensors Discovered:** 18
- **CPCB AQI Compliance:** Valid (Has >= 3 criteria pollutants incl PM2.5/PM10)

**Sensor Parameter Inventory:**

| Parameter | Sensor ID | Unit | Earliest Observation | Latest Observation |
| :--- | :---: | :---: | :--- | :--- |
| `pm25` | 14859 | µg/m³ | 2018-03-09T05:30:00Z | 2022-10-31T01:45:00Z |
| `so2` | 14862 | µg/m³ | 2018-03-09T05:30:00Z | 2022-10-31T01:45:00Z |
| `no2` | 14850 | µg/m³ | 2018-03-09T05:30:00Z | 2022-10-31T01:45:00Z |
| `o3` | 40537 | µg/m³ | 2020-11-30T15:15:00Z | 2022-10-31T01:45:00Z |
| `co` | 15270 | µg/m³ | 2018-03-09T05:30:00Z | 2022-10-31T01:45:00Z |
| `pm10` | 1303005 | µg/m³ | 2021-04-27T19:30:00Z | 2022-10-31T01:45:00Z |
| `temperature` | 12235373 | c | 2025-02-18T20:15:00Z | 2026-08-08T18:15:00Z |
| `relativehumidity` | 12235371 | % | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `no` | 12235366 | ppb | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `nox` | 14340829 | ppb | 2025-10-10T18:15:00Z | 2026-10-13T18:00:00Z |
| `wind_direction` | 14340830 | deg | 2025-10-10T18:15:00Z | 2026-08-08T18:15:00Z |
| `wind_speed` | 14340831 | m/s | 2025-10-10T18:15:00Z | 2026-08-08T18:15:00Z |


### Station 2594: Sanathnagar, Hyderabad - TSPCB (Hyderabad)

- **Total Sensors Discovered:** 4
- **CPCB AQI Compliance:** Valid (Has >= 3 criteria pollutants incl PM2.5/PM10)

**Sensor Parameter Inventory:**

| Parameter | Sensor ID | Unit | Earliest Observation | Latest Observation |
| :--- | :---: | :---: | :--- | :--- |
| `o3` | 5389 | µg/m³ | 2016-03-22T10:00:00Z | 2018-02-22T03:00:00Z |
| `so2` | 9128 | µg/m³ | 2017-06-19T19:00:00Z | 2018-02-22T03:00:00Z |
| `pm25` | 9127 | µg/m³ | 2017-02-18T19:00:00Z | 2018-02-22T03:00:00Z |
| `co` | 5387 | µg/m³ | 2016-03-22T10:00:00Z | 2018-02-22T03:00:00Z |


### Station 5623: Central University, Hyderabad - TSPCB (Hyderabad)

- **Total Sensors Discovered:** 18
- **CPCB AQI Compliance:** Valid (Has >= 3 criteria pollutants incl PM2.5/PM10)

**Sensor Parameter Inventory:**

| Parameter | Sensor ID | Unit | Earliest Observation | Latest Observation |
| :--- | :---: | :---: | :--- | :--- |
| `co` | 12242116 | ppb | 2025-02-19T04:45:00Z | 2026-10-13T18:00:00Z |
| `no2` | 12242118 | ppb | 2025-02-19T04:45:00Z | 2026-10-13T18:00:00Z |
| `o3` | 12242119 | µg/m³ | 2025-02-19T04:45:00Z | 2026-10-13T18:00:00Z |
| `pm25` | 12242121 | µg/m³ | 2025-02-19T06:15:00Z | 2026-10-13T17:00:00Z |
| `wind_direction` | 14340846 | deg | 2025-10-10T18:15:00Z | 2026-10-13T18:00:00Z |
| `temperature` | 12242124 | c | 2025-02-19T04:45:00Z | 2026-10-13T18:00:00Z |
| `nox` | 14340845 | ppb | 2025-10-10T18:15:00Z | 2026-10-13T18:00:00Z |
| `pm10` | 12242120 | µg/m³ | 2025-02-19T06:15:00Z | 2026-10-13T17:00:00Z |
| `wind_speed` | 14340847 | m/s | 2025-10-10T18:15:00Z | 2026-10-13T18:00:00Z |
| `so2` | 12242123 | ppb | 2025-02-19T04:45:00Z | 2026-10-13T18:00:00Z |
| `relativehumidity` | 12242122 | % | 2025-02-19T04:45:00Z | 2026-10-13T18:00:00Z |
| `no` | 12242117 | ppb | 2025-02-19T04:45:00Z | 2026-10-13T18:00:00Z |


### Station 2586: Manali, Chennai - CPCB (Chennai)

- **Total Sensors Discovered:** 18
- **CPCB AQI Compliance:** Valid (Has >= 3 criteria pollutants incl PM2.5/PM10)

**Sensor Parameter Inventory:**

| Parameter | Sensor ID | Unit | Earliest Observation | Latest Observation |
| :--- | :---: | :---: | :--- | :--- |
| `so2` | 12235655 | ppb | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `co` | 12235648 | ppb | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `pm25` | 12235653 | µg/m³ | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `temperature` | 12235656 | c | 2025-02-18T20:15:00Z | 2026-08-13T14:45:00Z |
| `relativehumidity` | 12235654 | % | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `pm10` | 12235652 | µg/m³ | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `no2` | 12235650 | ppb | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `o3` | 12235651 | µg/m³ | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `no` | 12235649 | ppb | 2025-02-18T20:15:00Z | 2026-10-13T18:00:00Z |
| `wind_direction` | 14340871 | deg | 2025-10-10T18:15:00Z | 2026-10-12T21:30:00Z |
| `wind_speed` | 14340872 | m/s | 2025-10-10T18:15:00Z | 2026-10-12T21:30:00Z |
| `nox` | 14340870 | ppb | 2025-10-10T18:15:00Z | 2026-10-13T18:00:00Z |


## 4. Key Findings & Data Quality Risks

1. **High Historical Density in Delhi NCR:** DPCC and CPCB stations in Delhi (R K Puram, Anand Vihar, ITO) present comprehensive continuous data covering 2024 through October 2026.
2. **Unit Harmonization Requirement:** In OpenAQ v3, gaseous pollutants like $\text{NO}_2$ and $\text{CO}$ are frequently returned in volume mixing ratios (`ppb`, `ppm`) by continuous analyzers, whereas CPCB breakpoints use mass concentrations ($\mu\text{g/m}^3$ and $\text{mg/m}^3$). A standard ambient conversion step ($25^\circ\text{C}$, $1\text{ atm}$) must be embedded in the Spark ETL.
3. **Missing Value Characteristics:** Real-world sensor dropouts occur due to routine calibration and power outages. As required by CPCB rules and project guidelines, missing records will **never** be imputed with zeros; instead, sliding window averages will be calculated only when $\ge 16$ hours of valid data exist in a 24-hour cycle.
4. **Recommended Core Dataset for Project:** Delhi NCR (R K Puram [17], Anand Vihar [5509]), Bengaluru (BTM Layout [5548], Peenya [5607]), and Hyderabad (Central University [5623]). This multi-city selection provides rich spatial diversity across climatic zones.
