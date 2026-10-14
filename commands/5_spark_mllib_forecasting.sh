#!/usr/bin/env bash
# [STEP 5 - PERSON 3] Train Spark MLlib 24-Hour Ahead Forecasting Models
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
cd "$DIR"
echo "====================================================================="
echo "  [STEP 5 - PERSON 3] Training Spark MLlib 24h Forecasting Models"
echo "====================================================================="
export JAVA_HOME="/opt/homebrew/Cellar/openjdk@17/17.0.20.1/libexec/openjdk.jdk/Contents/Home"
.venv/bin/python3 scripts/train_forecasting_models.py
