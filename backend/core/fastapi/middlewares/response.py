import json
from core.utils import create_json_response
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        excluded_paths = ["/docs", "/redoc", "/openapi.json"]
        if request.url.path in excluded_paths:
            return await call_next(request)

        response = await call_next(request)

        if not (200 <= response.status_code < 300) or response.headers.get(
            "content-type", ""
        ).startswith("text/event-stream"):
            return response

        if response.headers.get("content-type", "") == "text/event-stream":
            return response

        original_status = response.status_code
        original_body = b""
        async for chunk in response.body_iterator:
            original_body += chunk

        try:
            parsed_content = json.loads(original_body.decode())
        except json.JSONDecodeError:
            parsed_content = original_body.decode()

        return create_json_response(
            status_code=original_status,
            message="Success" if 200 <= original_status < 300 else "Error",
            data=parsed_content,
        )