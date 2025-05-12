from core.security.jwt import JWTHandler
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        excluded_paths = ["/docs", "/redoc"]

        if request.url.path in excluded_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        user = None

        if auth_header:
            try:
                token_type, token = auth_header.split(" ")
                if token_type.lower() == "bearer":
                    user = JWTHandler.decode(auth_header.split(" ")[1])
            except Exception as e: 
                pass

        request.state.user = user

        response = await call_next(request)

        return response
    
    

