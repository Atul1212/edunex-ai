from fastapi import FastAPI, Request, HTTPException, Response
import httpx
import os

app = FastAPI(title='EduNex API Gateway')

# --- DYNAMIC SERVICE URLs ---
AI_SERVICE_URL = os.getenv('AI_SERVICE_URL', 'http://127.0.0.1:8006')
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://127.0.0.1:8001')
ACADEMIC_SERVICE_URL = os.getenv('ACADEMIC_SERVICE_URL', 'http://127.0.0.1:8002')
FINANCE_SERVICE_URL = os.getenv('FINANCE_SERVICE_URL', 'http://127.0.0.1:8003')
EXAM_SERVICE_URL = os.getenv('EXAM_SERVICE_URL', 'http://127.0.0.1:8004')
COMM_SERVICE_URL = os.getenv('COMM_SERVICE_URL', 'http://127.0.0.1:8005')

@app.get('/')
def health_check():
    return {'status': 'API Gateway Running', 'port': '8000'}

async def proxy_request(service_url: str, path: str, request: Request):
    async with httpx.AsyncClient() as client:
        target_url = f'{service_url}/{path}'
        
        # 1. Clean Headers: Host aur Content-Length ko httpx recalculate karne do
        headers = dict(request.headers)
        headers.pop('host', None)
        headers.pop('content-length', None)

        try:
            # 2. Forward Request
            upstream_response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=await request.body()
            )
            
            # 3. Return ACTUAL Status Code & Content (Sach bolo!)
            return Response(
                content=upstream_response.content,
                status_code=upstream_response.status_code,
                media_type=upstream_response.headers.get('content-type')
            )
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail='Service Unavailable')

# --- PROXY ROUTES ---
@app.api_route('/auth/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def auth_proxy(path: str, request: Request):
    return await proxy_request(AUTH_SERVICE_URL, path, request)

@app.api_route('/academic/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def academic_proxy(path: str, request: Request):
    return await proxy_request(ACADEMIC_SERVICE_URL, path, request)

@app.api_route('/finance/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def finance_proxy(path: str, request: Request):
    return await proxy_request(FINANCE_SERVICE_URL, path, request)

@app.api_route('/exam/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def exam_proxy(path: str, request: Request):
    return await proxy_request(EXAM_SERVICE_URL, path, request)

@app.api_route('/communication/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def comm_proxy(path: str, request: Request):
    return await proxy_request(COMM_SERVICE_URL, path, request)

@app.api_route('/ai/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def ai_proxy(path: str, request: Request):
    return await proxy_request(AI_SERVICE_URL, path, request)