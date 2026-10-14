#!/usr/bin/env bash
# [STEP 2 - PERSON 1] Inspect Partitioned Parquet Lake in Hadoop HDFS
echo "====================================================================="
echo "  [STEP 2 - PERSON 1] Inspecting Partitioned Parquet Lake in Hadoop HDFS"
echo "====================================================================="
/Users/yashsonawane/bigdata/hadoop/current/bin/hdfs dfs -ls -h /air_quality/processed/hourly_aqi_parquet/
