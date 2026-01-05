#!/bin/bash
# Simple alias script to list all models in the Gravitas RAG system

echo "🤖 Gravitas RAG - Model Inventory"
echo "====================================="
python3 "$(dirname "$0")/list_all_models.py"
