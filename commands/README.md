# 🎯 Step-by-Step Execution Order for Project Demonstration

Run these numbered scripts sequentially during your presentation / video call recording:

| Step & Script | Speaker / Role | What It Does & What To Say |
| :--- | :--- | :--- |
| **`./commands/1_hdfs_show_raw.sh`** | **Person 1** (HDFS Lead) | Shows the 47.3 MB raw JSON telemetry file in Hadoop HDFS with 128 MB block size & 3x replication factor. |
| **`./commands/2_hdfs_show_parquet.sh`** | **Person 1** (HDFS Lead) | Shows the processed Parquet lake partitioned by `city=Bengaluru`, `city=Delhi NCR`, `city=Hyderabad`. |
| **`./commands/3_spark_run_etl.sh`** | **Person 2** (Spark ETL Lead) | Runs Apache Spark ETL: cleans units, enforces CPCB 16-hour validity rules, and computes composite NAQI in 25s. |
| **`./commands/4_spark_run_analytics.sh`** | **Person 2** (Spark ETL Lead) | Executes Spark SQL analytics: prints city averages (Delhi 62.5% Severe) and generates diurnal peak figures. |
| **`./commands/5_spark_mllib_forecasting.sh`** | **Person 3** (Spark MLlib Lead)| Trains Spark MLlib Random Forest model (RMSE 35.17, +16.6% better than baseline) using chronological split. |
| **`./commands/6_spark_mllib_classification.sh`** | **Person 3** (Spark MLlib Lead)| Trains Spark MLlib 6-tier CPCB hazard classifier (70.21% test accuracy). |
| **`./commands/7_run_entire_pipeline.sh`** | **Any / Master Runner** | Executes the entire end-to-end pipeline from start to finish in one automated command. |
