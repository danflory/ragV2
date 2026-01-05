#!/bin/bash
# Gravitas Resource Watcher
# Monitors GPU VRAM and Docker Container overhead in real-time.

clear
echo "🚀 Initializing Gravitas Resource Watcher..."
echo "Press CTRL+C to stop."
sleep 1

while true; do
    # 1. Gather all data into a buffer first
    GPU_DATA=$(nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits | \
    awk -F', ' '{printf "GPU %d: %-15s | VRAM (Used / Total): %4.1f / %4.1f GB | Real Load: %3s%%\n", $1, $2, $3/1024, $4/1024, $5}')
    
    DOCKER_DATA=$(docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | grep -v "gravitas_mcp")
    
    # Read heartbeat if it exists
    if [ -f /tmp/gravitas_heartbeat ]; then
        ACTIVE_FILE=$(cat /tmp/gravitas_heartbeat)
        # Only show last 50 chars of path
        DISPLAY_FILE="...${ACTIVE_FILE: -50}"
    else
        DISPLAY_FILE="IDLE"
    fi

    # 2. Now move cursor home and overwrite
    tput home
    echo "=========================================================================="
    echo "🧪 REFACTOR STATUS"
    echo "=========================================================================="
    echo "Active File: $DISPLAY_FILE"
    echo ""
    echo "=========================================================================="
    echo "📟 GPU TELEMETRY"
    echo "=========================================================================="
    echo "$GPU_DATA"
    
    echo ""
    echo "=========================================================================="
    echo "🐳 CONTAINER RESOURCE CONSUMPTION"
    echo "=========================================================================="
    echo "$DOCKER_DATA"
    
    echo ""
    echo "=========================================================================="
    echo "🕒 Last Updated: $(date '+%H:%M:%S')"
    echo "=========================================================================="
    
    # 3. Clear any leftover lines below
    tput ed
    
    sleep 1
done
