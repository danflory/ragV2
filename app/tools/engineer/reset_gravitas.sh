#!/bin/bash
# scripts/reset_gravitas.sh

# --- HOMING BEACON ---
cd "$(dirname "$0")/.." || exit

# --- HOST OVERRIDES (Running on Metal) ---
export QDRANT_HOST="localhost"
export MINIO_ENDPOINT="localhost:9000"
export DB_HOST="localhost"
export L1_URL="http://localhost:11434"

# --- PATH ENFORCEMENT ---
# Use the python executable from your virtual environment
VENV_PY="venv/bin/python3"

START_TIME=$(date +%s)
echo "-----------------------------------------------------"
echo "🕒 Start Time: $(date '+%H:%M:%S')"
echo "🔄 Starting Robust Reset..."

# 0. SYSTEM MAINTENANCE (Purge old logs/journals)
echo "   [$(date '+%H:%M:%S')] 🧹 Running System Maintenance..."
$VENV_PY ANTIGRAVITY_Scripts/maintenance.py

# 1. LOG THE RESET
$VENV_PY scripts/log_entry.py "SYSTEM_RESET" "User_CLI" "Reset sequence initiated"

# 2. CLEAR PORT
echo "   [$(date '+%H:%M:%S')] 🚫 Clearing Port 5050..."
# Try to kill anything on 5050 with multiple attempts
for i in {1..3}; do
  if lsof -i :5050 > /dev/null 2>&1; then
    # Try SIGTERM then SIGKILL
    fuser -k -TERM 5050/tcp > /dev/null 2>&1 || sudo fuser -k -TERM 5050/tcp > /dev/null 2>&1
    sleep 0.5
    fuser -k -KILL 5050/tcp > /dev/null 2>&1 || sudo fuser -k -KILL 5050/tcp > /dev/null 2>&1
    sleep 0.5
  else
    break
  fi
done
sleep 1 # Extra cushion for OS to release port

# Final check before proceeding
if lsof -i :5050 > /dev/null 2>&1; then
    echo "   [$(date '+%H:%M:%S')] ❌ ERROR: Port 5050 is still in use by:"
    lsof -i :5050
    echo "   Manual intervention required: 'sudo fuser -k 5050/tcp'"
    exit 1
fi

# 3. STOP ALL DOCKER SERVICES
echo "   [$(date '+%H:%M:%S')] 🛑 Stopping All Docker Services..."
docker-compose down 2>/dev/null || echo "   (No services to stop)"
sleep 2

# 4. START ALL DOCKER SERVICES
echo "   [$(date '+%H:%M:%S')] 🐳 Starting Docker Services..."
echo "     - Gravitas_postgres (Database)"
echo "     - Gravitas_qdrant (Vector Store)"
echo "     - Gravitas_minio (Object Storage)"
echo "     - Gravitas_ollama (GPU 0 - Titan RTX)"
echo "     - Gravitas_ollama_embed (GPU 1 - GTX 1060)"

docker-compose up -d Gravitas_postgres qdrant minio ollama ollama_embed

# Wait for services to be ready
echo "   [$(date '+%H:%M:%S')] ⏳ Waiting for services to initialize..."
sleep 5

# Check service health
echo "   [$(date '+%H:%M:%S')] 🏥 Service Health Check:"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "Gravitas|qdrant|minio" | \
    awk '{print "     "$0}'

# 5. RESTART OLLAMA (Host Service if exists)
if systemctl is-active --quiet ollama; then
    echo "   [$(date '+%H:%M:%S')] ♻️  Restarting Host Ollama Service..."
    sudo systemctl restart ollama
fi

# 6. SMART WARM-UP
echo "   [$(date '+%H:%M:%S')] 🔥 Warming up Neural Core (Max 60s)..."
$VENV_PY scripts/warmup.py

# 7. CHECK GPU
echo "   [$(date '+%H:%M:%S')] 📟 GPU Status:"
nvidia-smi --query-gpu=index,memory.used,memory.free --format=csv,noheader,nounits | \
awk -F', ' '{print "     GPU "$1": Used "$2" MB (Free "$3" MB)"}'

# 8. GENERATE SESSION CONTEXT
echo "   [$(date '+%H:%M:%S')] 📝 Generating Gravitas Session Context..."
$VENV_PY scripts/generate_context.py

# 9. LOG THE STARTUP
$VENV_PY scripts/log_entry.py "SERVER_START" "Boot_Script" "FastAPI launching..."

# 10. LAUNCH SERVER
echo "   [$(date '+%H:%M:%S')] 🚀 Launching FastAPI Server..."
echo "-----------------------------------------------------"

# Final sanity check for port 5050
if lsof -i :5050 > /dev/null 2>&1; then
    echo "❌ FATAL: Cannot start Gravitas because Port 5050 is occupied."
    echo "   Process using port 5050:"
    lsof -i :5050
    exit 1
fi

$VENV_PY -u -m uvicorn app.main:app --host 0.0.0.0 --port 5050 --reload --reload-dir app --log-config log_conf.yaml