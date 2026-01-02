#!/bin/bash
# scripts/start_mcp.sh
# Gravitas MCP Server Startup Script

set -e # Exit on error

echo "--- GRAVITAS MCP: INITIALIZING ---"

# 1. Wait for Critical Infrastructure
# We use a simple python one-liner or wait-for-it if installed. 
# Here we assume Docker depends_on handles most, but let's be safe.
echo "Waiting for Postgres (5432)..."
# (Optional: Add actual wait logic if depends_on fails frequently)

# 2. Python Path Setup
export PYTHONPATH=$PYTHONPATH:$(pwd)
echo "PYTHONPATH set to: $PYTHONPATH"

# 3. Launch the Server
# We run as a module to resolve relative imports correctly
echo "Starting MCP SSE Server on Port 8000..."
exec python3 -m app.mcp_server