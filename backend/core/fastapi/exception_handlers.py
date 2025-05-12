from loguru import logger
from fastapi.exceptions import RequestValidationError
from fastapi import Request, FastAPI
from http import HTTPStatus
from starlette.exceptions import HTTPException as StarletteHTTPException
from prisma.errors import PrismaError
from core.exceptions import CustomException
from core.utils import create_json_response

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
    
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"VALIDATION_ERROR: {exc.errors()}")
    return create_json_response(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
        message="Validation error.",
        error_code="VALIDATION_ERROR",
        data=exc.errors(),
    )

async def prisma_exception_handler(request: Request, exc: PrismaError):
    logger.warning(f"PrismaError: {exc}")
    return create_json_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        message=str(exc),
        error_code="INTERNAL_SERVER_ERROR",
    )


# Init listeners
def init_listeners(app_: FastAPI) -> None:
    app_.exception_handler(CustomException)(custom_exception_handler)
    app_.exception_handler(Exception)(generic_exception_handler)
    app_.exception_handler(StarletteHTTPException)(http_exception_handler)
    app_.exception_handler(RequestValidationError)(validation_exception_handler)
    app_.exception_handler(PrismaError)(prisma_exception_handler)
    
