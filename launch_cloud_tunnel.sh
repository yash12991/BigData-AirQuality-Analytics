#!/usr/bin/env bash
# ==============================================================================
# AirFlow360 - Instant Cloud Live Public URL Generator
# Generates a public HTTPS link you can paste into Zoom / Google Meet
# ==============================================================================
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

PORT=8080
if ! lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "[1/2] Starting local web server on port $PORT..."
    python3 -m http.server $PORT --directory web_demo > /dev/null 2>&1 &
    sleep 1
else
    echo "[1/2] Local web server already active on port $PORT."
fi

echo "[2/2] Generating instant public HTTPS cloud tunnel..."
echo "---------------------------------------------------------------------"
echo "  PASTE THIS URL INTO YOUR ZOOM / GOOGLE MEET CHAT FOR EVALUATORS:"
echo "---------------------------------------------------------------------"

npx -y localtunnel --port $PORT
