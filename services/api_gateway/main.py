from fastapi import FastAPI, Request, HTTPException
import httpx

app = FastAPI(title='EduNex API Gateway')

# Define Service URLs
AUTH_SERVICE_URL = 'http://127.0.0.1:8001'
ACADEMIC_SERVICE_URL = 'http://127.0.0.1:8002'

@app.get('/')
def health_check():
    return {'status': 'API Gateway Running', 'port': '8000'}

# --- PROXY TO AUTH SERVICE ---
@app.api_route('/auth/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def auth_proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        target_url = f'{AUTH_SERVICE_URL}/{path}'
        body = await request.body()
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=request.headers,
                content=body  # Fix: Forward Raw Content (Form or JSON)
            )
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail='Auth Service Unavailable')

# --- PROXY TO ACADEMIC SERVICE ---
@app.api_route('/academic/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def academic_proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        target_url = f'{ACADEMIC_SERVICE_URL}/{path}'
        body = await request.body()
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=request.headers,
                content=body
            )
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail='Academic Service Unavailable')

