#!/usr/bin/env bash
# [STEP 1 - PERSON 1] Inspect Raw JSON Telemetry in Hadoop HDFS
echo "====================================================================="
echo "  [STEP 1 - PERSON 1] Inspecting Raw JSON Telemetry in Hadoop HDFS"
echo "====================================================================="
/Users/yashsonawane/bigdata/hadoop/current/bin/hdfs dfs -ls -h /air_quality/raw/
