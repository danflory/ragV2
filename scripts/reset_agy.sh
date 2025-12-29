#!/bin/bash
# scripts/reset_agy.sh

# --- HOMING BEACON ---
cd "$(dirname "$0")/.." || exit

# --- PATH ENFORCEMENT ---
# Use the python executable from your virtual environment
VENV_PY="venv/bin/python3"

START_TIME=$(date +%s)
echo "-----------------------------------------------------"
echo "🕒 Start Time: $(date '+%H:%M:%S')"
echo "🔄 Starting Robust Reset..."

# 1. LOG THE RESET
$VENV_PY scripts/log_entry.py "SYSTEM_RESET" "User_CLI" "Reset sequence initiated"

# 2. CLEAR PORT
echo "   [$(date '+%H:%M:%S')] 🚫 Clearing Port 5050..."
fuser -k 5050/tcp > /dev/null 2>&1

# 3. RESTART OLLAMA
echo "   [$(date '+%H:%M:%S')] ♻️  Restarting Ollama Service..."
sudo systemctl restart ollama

# 4. SMART WARM-UP
echo "   [$(date '+%H:%M:%S')] 🔥 Warming up Neural Core (Max 60s)..."
$VENV_PY scripts/warmup.py

# 5. CHECK GPU
echo "   [$(date '+%H:%M:%S')] 📟 GPU Status:"
nvidia-smi --query-gpu=index,memory.used,memory.free --format=csv,noheader,nounits | \
awk -F', ' '{print "     GPU "$1": Used "$2" MB (Free "$3" MB)"}'

# 6. LOG THE STARTUP
$VENV_PY scripts/log_entry.py "SERVER_START" "Boot_Script" "FastAPI launching..."

# 7. LAUNCH SERVER
echo "   [$(date '+%H:%M:%S')] 🚀 Launching FastAPI Server..."
echo "-----------------------------------------------------"

$VENV_PY -u -m uvicorn app.main:app --host 0.0.0.0 --port 5050 --reload --log-config log_conf.yaml