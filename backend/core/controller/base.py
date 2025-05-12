from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from fastapi import APIRouter


class BaseController(ABC):
    DEFAULT_RESPONSES = {
        200: {"content": {"application/json": {}}},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
    }

    def __init__(
        self,
        prefix: str = "",
        tags: Optional[List[str]] = None,
        responses: Optional[Dict[int, dict]] = None,
    ):
        self.router = APIRouter(
            prefix=prefix,
            tags=tags or [],
            responses={**self.DEFAULT_RESPONSES, **(responses or {})},
        )
        self._register_routes()

    @abstractmethod
    def _register_routes(self):
        """
        Abstract method that must be implemented by subclasses to define routes.
        """
        pass
