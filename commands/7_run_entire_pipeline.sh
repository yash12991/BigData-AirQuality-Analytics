#!/usr/bin/env bash
# [STEP 7 - ALL] Execute Entire End-to-End Pipeline in One Go
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
cd "$DIR"
echo "====================================================================="
echo "  [STEP 7 - ALL] Executing Master End-to-End Pipeline Runner"
echo "====================================================================="
./run_pipeline.sh
