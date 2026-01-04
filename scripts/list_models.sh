#!/bin/bash
# Simple alias script to list all models in the AntiGravity RAG system

echo "🤖 AntiGravity RAG - Model Inventory"
echo "====================================="
python3 "$(dirname "$0")/list_all_models.py"
