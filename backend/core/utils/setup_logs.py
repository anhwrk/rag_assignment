import os
from loguru import logger
from core.config import config

def setup_logger():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    try:
        if config.ENVIRONMENT == "production":
            logger.add(
                "logs/production.log",
                level="INFO",
                format="{time} {level} {message}",
                rotation="10 MB",
                retention="30 days",
                compression="zip",
            )
        else:
            logger.add(
                "logs/debug.log",
                level="DEBUG",
                format="{time} {level} {message}",
                rotation="1 MB",
                retention="7 days",
                compression="zip",
            )
    except Exception as e:
        logger.info(f"Failed to configure logger: {e}")
