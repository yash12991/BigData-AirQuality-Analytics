#!/usr/bin/env bash
# ==============================================================================
# Master Pipeline Execution Script
# Distributed Urban Air Quality Analytics and AQI Forecasting
# Architecture: HDFS -> Spark -> Spark MLlib
# ==============================================================================

set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${WORKSPACE_DIR}"

echo "========================================================================"
echo " Starting Distributed Air Quality Analytics & Forecasting Pipeline"
echo " Workspace: ${WORKSPACE_DIR}"
echo "========================================================================"

# 1. Environment Configuration
export JAVA_HOME="/opt/homebrew/Cellar/openjdk@17/17.0.20.1/libexec/openjdk.jdk/Contents/Home"
VENV_PYTHON="${WORKSPACE_DIR}/.venv/bin/python3"
HADOOP_BIN="/Users/yashsonawane/bigdata/hadoop/current/bin/hadoop"
HDFS_BIN="/Users/yashsonawane/bigdata/hadoop/current/bin/hdfs"

if [[ ! -f "${VENV_PYTHON}" ]]; then
    echo "Error: Python virtual environment not found at ${VENV_PYTHON}"
    exit 1
fi

# 2. Check and Ensure HDFS Daemons are running
echo "[1/5] Checking Hadoop HDFS daemons..."
if ! jps | grep -q "NameNode"; then
    echo "  Starting HDFS daemons..."
    /Users/yashsonawane/bigdata/hadoop/current/sbin/start-dfs.sh
    sleep 3
    "${HDFS_BIN}" dfsadmin -safemode leave || true
fi
echo "  HDFS NameNode and DataNodes are active."

# 3. Distributed Spark ETL (Raw HDFS -> Cleaned Partitioned Parquet)
echo -e "\n[2/5] Running Distributed Spark ETL & CPCB AQI Engine..."
"${VENV_PYTHON}" "${WORKSPACE_DIR}/scripts/spark_etl.py"

# 4. Distributed Analytics and Visualization
echo -e "\n[3/5] Running Distributed Spark SQL Analytics & Visualizations..."
"${VENV_PYTHON}" "${WORKSPACE_DIR}/scripts/run_analytics.py"

# 5. Distributed MLlib Forecasting Models
echo -e "\n[4/5] Training Distributed Spark MLlib Regression Forecasting Pipeline..."
"${VENV_PYTHON}" "${WORKSPACE_DIR}/scripts/train_forecasting_models.py"

# 6. Distributed MLlib Classification Models
echo -e "\n[5/5] Training Distributed Spark MLlib CPCB Hazard Classification..."
"${VENV_PYTHON}" "${WORKSPACE_DIR}/scripts/train_classification_model.py"

echo -e "\n========================================================================"
echo " Pipeline execution completed successfully!"
echo " Reports available in: docs/"
echo " Figures generated in: reports/figures/"
echo " Partitioned Parquet: data/processed/hourly_aqi_parquet/"
echo "========================================================================"
