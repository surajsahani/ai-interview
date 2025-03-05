import time
from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 记录请求
        logger.info(f"Request: {request.method} {request.url}")
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # 记录响应
            logger.info(f"Response: {request.method} {request.url} completed in {process_time:.3f}s")
            return response
            
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise e 