from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Generator

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from prisma import Prisma
from app import router

from core.cache import Cache, CustomKeyMaker, RedisBackend
from core.config import config
from core.exceptions import CustomException
from core.fastapi.exception_handlers import init_listeners
from core.fastapi.middlewares import (
    ResponseMiddleware,
    LoggingMiddleware,
    AuthenticationMiddleware,
)
from core.utils import get_allowed_origins

# Middleware configuration
middleware = [
    Middleware(LoggingMiddleware),
    Middleware(
        CORSMiddleware,
        allow_origins=get_allowed_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(AuthenticationMiddleware),
    Middleware(ResponseMiddleware),
]

# Initialize 
def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)

def init_cache() -> None:
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    try:
        # Init prisma
        db = Prisma(auto_register=True)
        await db.connect()
        
        init_cache()

        yield
    except Exception as exc:
        logger.exception("Unhandled exception during lifespan")
        raise CustomException(message="An internal server error occurred.") from exc
    finally:
        # Close db
        await db.disconnect()
        # Close cache
        await Cache.shutdown()

def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Test API",
        description="Test API by Duc Anh Le",
        version="0.1.0",
        docs_url=None if config.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if config.ENVIRONMENT == "production" else "/redoc",
        middleware=middleware,
        lifespan=lifespan,
    )

    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_

# Create the application instance
app = create_app()
