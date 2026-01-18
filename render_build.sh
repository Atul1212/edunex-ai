#!/bin/bash

# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Gateway (Optional check)
if [ -d "services/gateway" ]; then
    echo "✅ Starting Gateway..."
    python -m uvicorn services.gateway.main:app --host 0.0.0.0 --port 8000 &
fi

# 3. Start Frontend (CORRECT PATH: services/frontend/app.py)
echo "✅ Starting Streamlit App..."
# Dhyan dein: 'services/' add kiya gaya hai
streamlit run services/frontend/app.py --server.port $PORT --server.address 0.0.0.0