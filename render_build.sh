#!/bin/bash

# Script fail na ho agar warning aaye
set -e

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🚀 Starting Microservices..."

# 1. Start Auth Service (Port 8001 - Login ke liye zaroori)
# Background (&) mein chalayenge
if [ -d "services/auth_service" ]; then
    echo "🔐 Starting Auth Service..."
    python -m uvicorn services.auth_service.main:app --host 0.0.0.0 --port 8001 &
fi

# 2. Start API Gateway (Port 8000 - Main Entry Point)
# FIX: Folder ka naam 'api_gateway' hai, 'gateway' nahi.
if [ -d "services/api_gateway" ]; then
    echo "🌐 Starting API Gateway..."
    python -m uvicorn services.api_gateway.main:app --host 0.0.0.0 --port 8000 &
else
    echo "❌ ERROR: api_gateway folder nahi mila!"
    exit 1
fi

# 3. Start AI Engine (Optional - Agar memory bachi to chalega)
if [ -d "services/ai_engine" ]; then
    echo "🤖 Starting AI Engine..."
    python -m uvicorn services.ai_engine.main:app --host 0.0.0.0 --port 8006 &
fi

# Thoda wait karein taaki backend start ho jaye
sleep 5

# 4. Start Frontend (Main Process)
echo "💻 Starting Streamlit Frontend..."
streamlit run services/frontend/app.py --server.port $PORT --server.address 0.0.0.0