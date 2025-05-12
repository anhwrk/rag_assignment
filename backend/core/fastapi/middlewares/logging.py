from loguru import logger
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.utils import setup_logger  

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        setup_logger()
        
    async def dispatch(self, request: Request, call_next):
        """Log the request and response."""
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
