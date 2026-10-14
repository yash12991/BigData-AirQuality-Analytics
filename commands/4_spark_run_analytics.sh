#!/usr/bin/env bash
# [STEP 4 - PERSON 2] Execute Spark SQL Analytics & Generate Visual Figures
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
cd "$DIR"
echo "====================================================================="
echo "  [STEP 4 - PERSON 2] Running Distributed Spark SQL Analytics"
echo "====================================================================="
export JAVA_HOME="/opt/homebrew/Cellar/openjdk@17/17.0.20.1/libexec/openjdk.jdk/Contents/Home"
.venv/bin/python3 scripts/run_analytics.py
