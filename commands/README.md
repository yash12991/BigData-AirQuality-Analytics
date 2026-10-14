# 🎯 Step-by-Step Execution Order for Project Demonstration

Run these numbered scripts sequentially during your presentation / video call recording:

| Step & Script | Speaker / Role | What It Does & What To Say | Generated Figures / Images |
| :--- | :--- | :--- | :--- |
| **`./1_hdfs_show_raw.sh`** | **Person 1** (HDFS Lead) | Shows the 47.3 MB raw JSON telemetry file in Hadoop HDFS with 128 MB block size & 3x replication factor. | *(None)* |
| **`./2_hdfs_show_parquet.sh`** | **Person 1** (HDFS Lead) | Shows the processed Parquet lake partitioned by `city=Bengaluru`, `city=Delhi NCR`, `city=Hyderabad`. | *(None)* |
| **`./3_spark_run_etl.sh`** | **Person 2** (Spark ETL Lead) | Runs Apache Spark ETL: cleans units, enforces CPCB 16-hour validity rules, and computes composite NAQI in 20s. | *(Writes to HDFS Parquet)* |
| **`./4_spark_run_analytics.sh`** | **Person 2** (Spark ETL Lead) | Executes Spark SQL analytics: prints city averages (Delhi 62.5% Severe) and generates 3 diurnal/distribution figures. | **`cmd4_fig1_diurnal_pm25_trends.png`**<br>**`cmd4_fig2_cpcb_category_distribution.png`**<br>**`cmd4_fig3_city_aqi_boxplots.png`** |
| **`./5_spark_mllib_forecasting.sh`** | **Person 3** (Spark MLlib Lead)| Trains Spark MLlib Random Forest model (RMSE 35.17, +16.6% better than baseline) using chronological split. | **`cmd5_fig1_model_forecast_actual_vs_pred.png`** |
| **`./6_spark_mllib_classification.sh`** | **Person 3** (Spark MLlib Lead)| Trains Spark MLlib 6-tier CPCB hazard classifier (70.21% test accuracy). | **`cmd6_fig1_cpcb_classification_confusion_matrix.png`** |
| **`./7_run_entire_pipeline.sh`** | **Any / Master Runner** | Executes the entire end-to-end pipeline from start to finish in one automated command. | *Generates all reports & figures above* |

---

### 🖼️ Quick Image Reference Table

When explaining your results, find your images in `reports/figures/`:

| Command | Figure Name | What It Proves |
| :--- | :--- | :--- |
| **Command 4** | `cmd4_fig1_diurnal_pm25_trends.png` | Diurnal PM2.5 spike at 08:00 AM (winter inversion) and 08:00 PM (rush hour). |
| **Command 4** | `cmd4_fig2_cpcb_category_distribution.png` | Delhi has 62.5% Severe hours, while Bengaluru has 87.5% Satisfactory/Moderate hours. |
| **Command 4** | `cmd4_fig3_city_aqi_boxplots.png` | Statistical distribution of composite NAQI across all 3 cities. |
| **Command 5** | `cmd5_fig1_model_forecast_actual_vs_pred.png` | Spark MLlib Random Forest 24h prediction closely tracking ground truth PM2.5 (+16.6% better than persistence). |
| **Command 6** | `cmd6_fig1_cpcb_classification_confusion_matrix.png` | Multiclass classifier confusion matrix across all 6 CPCB hazard tiers (70.21% accuracy). |
