#!/bin/bash
# scripts/reset_gravitas.sh

# --- HOMING BEACON ---
cd "$(dirname "$0")/.." || exit

# --- PREFLIGHT CHECKS ---
echo "🔍 Running preflight checks..."

# Check for docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ ERROR: docker-compose not found!"
    echo "   Docker Desktop WSL integration may not be enabled."
    echo "   Please enable WSL integration in Docker Desktop settings:"
    echo "   Settings → Resources → WSL Integration"
    echo ""
    exit 1
fi

# Check for docker daemon
if ! docker info &> /dev/null; then
    echo "❌ ERROR: Docker daemon is not running!"
    echo "   Please start Docker Desktop."
    echo ""
    exit 1
fi

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo "❌ ERROR: Virtual environment not found at ./venv"
    echo "   Please create it with: python3 -m venv venv"
    echo ""
    exit 1
fi

# Check for requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "❌ ERROR: requirements.txt not found!"
    exit 1
fi

# Check for critical Python dependencies
VENV_PY="venv/bin/python3"
echo "   → Validating Python dependencies..."

# Create a temporary script to validate all dependencies
VALIDATE_SCRIPT=$(mktemp)
cat > "$VALIDATE_SCRIPT" << 'VALIDATION_EOF'
import sys
import importlib.util

# Critical modules that must be present for the app to start
CRITICAL_MODULES = [
    'yaml',        # uvicorn logging config
    'GPUtil',      # L1_local.py
    'fastapi',     # Core framework
    'uvicorn',     # Server
    'httpx',       # Networking
    'ollama',      # LLM driver
    'asyncpg',     # Database
    'google.genai', # L3_google.py (new SDK)
]

missing = []
for module in CRITICAL_MODULES:
    if importlib.util.find_spec(module) is None:
        missing.append(module)

if missing:
    print("MISSING:" + ",".join(missing))
    sys.exit(1)
else:
    print("OK")
    sys.exit(0)
VALIDATION_EOF

VALIDATION_RESULT=$($VENV_PY "$VALIDATE_SCRIPT" 2>&1)
VALIDATION_EXIT=$?
rm -f "$VALIDATE_SCRIPT"

if [ $VALIDATION_EXIT -ne 0 ]; then
    MISSING_MODULES=$(echo "$VALIDATION_RESULT" | grep "^MISSING:" | cut -d: -f2)
    echo ""
    echo "❌ DEPENDENCY CHECK FAILED!"
    echo "   Missing Python modules: $MISSING_MODULES"
    echo ""
    echo "   🔧 Auto-fixing: Installing all requirements..."
    $VENV_PY -m pip install -r requirements.txt -q
    
    if [ $? -ne 0 ]; then
        echo "   ❌ Installation failed!"
        echo "   Please run manually: source venv/bin/activate && pip install -r requirements.txt"
        echo ""
        echo "   📋 Filing incident report..."
        $VENV_PY scripts/log_entry.py "DEPENDENCY_FAILURE" "Reset_Script" "Missing modules: $MISSING_MODULES"
        exit 1
    fi
    
    echo "   ✅ Dependencies installed successfully"
    echo ""
fi

echo "✅ All preflight checks passed!"
echo ""

# --- HOST OVERRIDES (Running on Metal) ---
export QDRANT_HOST="localhost"
export MINIO_ENDPOINT="localhost:9000"
export DB_HOST="localhost"
export L1_URL="http://localhost:11434"

# --- PATH ENFORCEMENT ---
# Use the python executable from your consolidated virtual environment
VENV_PY="venv/bin/python3"
export PYTHONPATH=$PYTHONPATH:$(pwd)

START_TIME=$(date +%s)
echo "-----------------------------------------------------"
echo "🕒 Start Time: $(date '+%H:%M:%S')"
echo "🔄 Starting Robust Reset..."

# 0. SYSTEM MAINTENANCE (Purge old logs/journals)
echo "   [$(date '+%H:%M:%S')] 🧹 Running System Maintenance..."
$VENV_PY ANTIGRAVITY_Scripts/maintenance.py

# 1. LOG THE RESET
$VENV_PY scripts/log_entry.py "SYSTEM_RESET" "User_CLI" "Reset sequence initiated"

# 2. CLEAR PORTS (5050 & 8000)
echo "   [$(date '+%H:%M:%S')] 🚫 Clearing Ports 5050 & 8000..."

kill_port() {
  local port=$1
  for i in {1..3}; do
    if lsof -i :$port > /dev/null 2>&1; then
      fuser -k -TERM $port/tcp > /dev/null 2>&1 || echo "Skipping sudo kill for $port" # sudo fuser -k -TERM $port/tcp > /dev/null 2>&1
      sleep 0.5
      fuser -k -KILL $port/tcp > /dev/null 2>&1 || echo "Skipping sudo kill for $port" # sudo fuser -k -KILL $port/tcp > /dev/null 2>&1
      sleep 0.5
    else
      break
    fi
  done
}

kill_port 5050
kill_port 8000

sleep 1

# Final check
if lsof -i :5050 > /dev/null 2>&1 || lsof -i :8000 > /dev/null 2>&1; then
    echo "   [$(date '+%H:%M:%S')] ❌ ERROR: Ports still in use."
    lsof -i :5050
    lsof -i :8000
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
    # sudo systemctl restart ollama
    echo "   (Skipping sudo systemctl restart ollama for automated run)"
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

# 10. LAUNCH SUPERVISOR (Background)
echo "   [$(date '+%H:%M:%S')] 🛡️  Launching Supervisor Service (Port 8000)..."
$VENV_PY -m uvicorn app.services.supervisor.main:app --host 0.0.0.0 --port 8000 --log-config log_conf.yaml > supervisor.log 2>&1 &
SUPERVISOR_PID=$!
echo "   ✅ Supervisor running (PID: $SUPERVISOR_PID)"

# 11. LAUNCH SERVER (Foreground)
echo "   [$(date '+%H:%M:%S')] 🚀 Launching Gravitas Lobby (Port 5050)..."
echo "-----------------------------------------------------"

# Launch browser after a short delay to let server start
(sleep 3 && (xdg-open http://localhost:5050 2>/dev/null || sensible-browser http://localhost:5050 2>/dev/null)) &

$VENV_PY -u -m uvicorn app.main:app --host 0.0.0.0 --port 5050 --reload --reload-dir app --log-config log_conf.yaml