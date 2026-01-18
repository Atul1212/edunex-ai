#!/bin/bash

# 1. Install dependencies
pip install -r requirements.txt

# 2. Start AI Service (Background mein)
python -m uvicorn services.ai_engine.main:app --host 0.0.0.0 --port 8006 &

# 3. Start Gateway (Background mein)
# Note: Agar RAM kam pade to hum isse skip kar sakte hain, 
# lekin abhi try karte hain.
python -m uvicorn services.gateway.main:app --host 0.0.0.0 --port 8000 &

# 4. Start Streamlit Frontend (Main Process)
# Ye sabse last mein hona chahiye
streamlit run dashboard/main.py --server.port $PORT --server.address 0.0.0.0