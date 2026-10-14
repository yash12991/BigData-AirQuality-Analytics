#!/usr/bin/env bash
# [STEP 3 - PERSON 2] Execute Distributed Spark ETL & CPCB NAQI Engine
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
cd "$DIR"
echo "====================================================================="
echo "  [STEP 3 - PERSON 2] Executing Apache Spark Distributed ETL"
echo "====================================================================="
export JAVA_HOME="/opt/homebrew/Cellar/openjdk@17/17.0.20.1/libexec/openjdk.jdk/Contents/Home"
.venv/bin/python3 scripts/spark_etl.py
