from loguru import logger
from fastapi.exceptions import RequestValidationError
from fastapi import Request, FastAPI
from http import HTTPStatus
from starlette.exceptions import HTTPException as StarletteHTTPException
from prisma.errors import PrismaError
from core.exceptions import CustomException
from core.utils import create_json_response
from fastapi.responses import JSONResponse
from typing import Any, Dict
from pydantic import ValidationError

async def custom_exception_handler(request: Request, exc: CustomException):
    log_level = "error" if exc.error_code.value >= 500 else "warning"
    getattr(logger, log_level)(f"{exc.error_code.name}: {exc.message}")
    return create_json_response(
        status_code=exc.error_code.value,
        message=exc.message,
        error_code=exc.error_code.name,
    )
    
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"INTERNAL_SERVER_ERROR: {str(exc)}")
    return create_json_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        message="An unexpected error occurred.",
        error_code="INTERNAL_SERVER_ERROR",
    )
    
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP_EXCEPTION: {exc.detail}")
    return create_json_response(
        status_code=exc.status_code,
        message=exc.detail,
        error_code=HTTPStatus(exc.status_code).phrase.replace(" ", "_").upper(),
    )
    
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle Pydantic validation errors"""
    return create_json_response(
        status_code=400,
        message=str(exc.errors()[0].get('msg')) if exc.errors() else "Validation error",
        error_code="VALIDATION_ERROR"
    )

async def prisma_exception_handler(request: Request, exc: PrismaError):
    logger.warning(f"PrismaError: {exc}")
    return create_json_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        message=str(exc),
        error_code="INTERNAL_SERVER_ERROR",
    )

async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Handle ValueError exceptions"""
    return create_json_response(
        status_code=400,
        message=str(exc),
        error_code="VALIDATION_ERROR"
    )

async def type_error_handler(request: Request, exc: TypeError) -> JSONResponse:
    """Handle TypeError exceptions"""
    return create_json_response(
        status_code=400,
        message=str(exc),
        error_code="TYPE_ERROR"
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other exceptions"""
    error_message = str(exc)
    error_type = exc.__class__.__name__
    
    return create_json_response(
        status_code=500,
        message=error_message,
        data={"error_type": error_type},
        error_code="INTERNAL_SERVER_ERROR"
    )

# Init listeners
def init_listeners(app_: FastAPI) -> None:
    app_.exception_handler(CustomException)(custom_exception_handler)
    app_.exception_handler(Exception)(generic_exception_handler)
    app_.exception_handler(StarletteHTTPException)(http_exception_handler)
    app_.exception_handler(RequestValidationError)(validation_exception_handler)
    app_.exception_handler(PrismaError)(prisma_exception_handler)
    app_.exception_handler(ValueError)(value_error_handler)
    app_.exception_handler(TypeError)(type_error_handler)
    app_.exception_handler(Exception)(general_exception_handler)
    
