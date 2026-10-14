#!/usr/bin/env bash
# ==============================================================================
# AirFlow360 - Live Video Call Demonstration Launcher
# Track B: HDFS -> Spark -> Spark MLlib
# ==============================================================================
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "====================================================================="
echo "  ⚡ AirFlow360 Live Video Call Demonstration Platform"
echo "  Track B: Hadoop HDFS -> Apache Spark -> Spark MLlib"
echo "====================================================================="

PORT=8080
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    PORT=8085
fi

echo "[1/2] Starting lightweight local web server on port $PORT..."
python3 -m http.server $PORT --directory web_demo > /dev/null 2>&1 &
SERVER_PID=$!

sleep 1

echo "[2/2] Launching interactive dashboard in your default browser..."
URL="http://localhost:$PORT"

if [[ "$OSTYPE" == "darwin"* ]]; then
    open "$URL"
elif which xdg-open > /dev/null; then
    xdg-open "$URL"
else
    echo "Please open $URL in your browser."
fi

echo "====================================================================="
echo "  Dashboard running at: $URL"
echo "  Press Ctrl+C to stop the server."
echo "====================================================================="

trap "kill $SERVER_PID 2>/dev/null || true; exit 0" INT TERM EXIT
wait $SERVER_PID
