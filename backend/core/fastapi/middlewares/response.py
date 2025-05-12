import json
from typing import Union
from core.utils import create_json_response
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Skip middleware for documentation routes
            excluded_paths = ["/docs", "/redoc", "/openapi.json"]
            if request.url.path in excluded_paths:
                return await call_next(request)

            # Get the response
            response = await call_next(request)

            # Handle streaming responses
            if response.headers.get("content-type", "").startswith("text/event-stream"):
                return response

            # Read the original response body
            original_status = response.status_code
            original_body = b""
            async for chunk in response.body_iterator:
                original_body += chunk

            # Try to parse the response body
            try:
                parsed_content = json.loads(original_body.decode())
            except json.JSONDecodeError:
                parsed_content = original_body.decode()
            except Exception as e:
                logger.error(f"Error parsing response body: {str(e)}")
                parsed_content = str(original_body)

            # Handle error responses (non-200 status codes)
            if not (200 <= original_status < 300):
                error_message = parsed_content.get('message', 'Error occurred') if isinstance(parsed_content, dict) else str(parsed_content)
                error_code = parsed_content.get('error_code', 'ERROR') if isinstance(parsed_content, dict) else 'ERROR'
                return create_json_response(
                    status_code=original_status,
                    message=error_message,
                    error_code=error_code,
                    data=parsed_content if isinstance(parsed_content, dict) else None
                )

            # Handle successful responses
            return create_json_response(
                status_code=original_status,
                message="Success",
                data=parsed_content
            )

        except ValueError as ve:
            logger.error(f"ValueError in response middleware: {str(ve)}")
            return create_json_response(
                status_code=400,
                message=str(ve),
                error_code="VALUE_ERROR"
            )

        except TypeError as te:
            logger.error(f"TypeError in response middleware: {str(te)}")
            return create_json_response(
                status_code=400,
                message=str(te),
                error_code="TYPE_ERROR"
            )

        except Exception as e:
            logger.error(f"Unexpected error in response middleware: {str(e)}")
            return create_json_response(
                status_code=500,
                message=str(e),
                error_code="INTERNAL_SERVER_ERROR"
            )