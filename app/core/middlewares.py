
from main import app
from fastapi import Request
from utils.logger import logger
import time, json

@app.middleware("http")
async def log_requests(request: Request, call_next):    
    body = await request.body()
    content_type = request.headers.get("content-type", "")

    if len(body) > 0:
        if "application/json" in content_type or "text/" in content_type:
            try:
                body = body.decode("utf-8")
            except UnicodeDecodeError:
                body = "<undecodable text>"
        else:
            body = "<binary content>"

    logger.info(f"⬇️ {request.method} {request.url}")
    
    if len(body) > 0:
        logger.info(f"📦 payload: {json.dumps(body, indent=2)}")
    
    try:
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        logger.info(f"⬆️ status: {response.status_code} - {duration:.3f}s")
                
        return response
    
    except Exception as e:
        logger.exception("🔥an error has occurred")
        raise e
