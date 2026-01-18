from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI(title='EduNex AI Engine')

# --- CONFIG ---
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class AIRequest(BaseModel):
    prompt: str
    context: str = 'email'

@app.get('/')
def health():
    return {'status': 'AI Engine Ready', 'model': 'Gemini-2.5-Flash'}

@app.post('/generate')
async def generate_text(req: AIRequest):
    if not GEMINI_API_KEY:
        return {'response': 'Error: API Key not found. Please set GEMINI_API_KEY in .env file.'}
    
    try:
        # ✅ UPDATED MODEL: Using the latest available from your list
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        if req.context == 'email':
            full_prompt = f'Write a professional school email. Topic: {req.prompt}. Keep it concise.'
        else:
            full_prompt = f'Act as an academic assistant. {req.prompt}'
            
        response = model.generate_content(full_prompt)
        return {'response': response.text}
    except Exception as e:
        return {'response': f"AI Error: {str(e)}"}