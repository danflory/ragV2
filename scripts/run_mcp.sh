#!/bin/bash
# Gravitas MCP Server Startup Script

cd /app
exec python -m app.mcp_server
