#!/usr/bin/env bash
# [STEP 6 - PERSON 3] Train Spark MLlib 6-Tier CPCB Hazard Classifier
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
cd "$DIR"
echo "====================================================================="
echo "  [STEP 6 - PERSON 3] Training Spark MLlib 6-Tier Hazard Classifier"
echo "====================================================================="
export JAVA_HOME="/opt/homebrew/Cellar/openjdk@17/17.0.20.1/libexec/openjdk.jdk/Contents/Home"
.venv/bin/python3 scripts/train_classification_model.py
