from typing import List

from core.config import EnvironmentType, config


def get_allowed_origins() -> List[str]:
    """
    Returns the list of allowed origins based on the environment.
    - In production: Uses ALLOWED_ORIGINS from the configuration.
    - In development or test: Allows all origins.
    """
    if config.ENVIRONMENT == EnvironmentType.PRODUCTION:
        return config.ALLOWED_ORIGINS.split(",") if config.ALLOWED_ORIGINS else []
    else:
        # Allow all origins in development or test environments
        return ["*"]
