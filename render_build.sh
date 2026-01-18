#!/bin/bash

# 1. Debugging: Print File Structure (Logs mein dikhega)
echo "-----------------------------------"
echo "📂 DEBUG: Checking File Structure..."
ls -R
echo "-----------------------------------"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start AI Service (Check if exists first)
if [ -d "services/ai_engine" ]; then
    echo "✅ Starting AI Engine..."
    python -m uvicorn services.ai_engine.main:app --host 0.0.0.0 --port 8006 &
else
    echo "⚠️ AI Engine folder missing!"
fi

# 4. Start Gateway (Check if exists first)
if [ -d "services/gateway" ]; then
    echo "✅ Starting Gateway..."
    python -m uvicorn services.gateway.main:app --host 0.0.0.0 --port 8000 &
else
    echo "⚠️ Gateway folder missing! Skipping..."
fi

# 5. Start Frontend (Try to find the file)
if [ -f "dashboard/main.py" ]; then
    echo "✅ Starting Dashboard..."
    streamlit run dashboard/main.py --server.port $PORT --server.address 0.0.0.0
else
    echo "❌ ERROR: dashboard/main.py nahi mila!"
    echo "🔍 Searching for ANY python file..."
    find . -name "*.py"
    # Fallback to keep container alive for debugging
    sleep 1000
fi