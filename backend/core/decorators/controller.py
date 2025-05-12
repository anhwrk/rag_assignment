from functools import wraps
from typing import Any, Dict, List, Optional, Type, TypeVar
from loguru import logger
from core.controller.base import BaseController
import threading  

T = TypeVar("T")

def Controller(
    prefix: str = "",
    tags: Optional[List[str]] = None,
    responses: Optional[Dict[int, dict]] = None,
):
    def decorator(cls: Type[T]) -> Type[T]:
        _instances: Dict[Type, Any] = {}
        _lock = threading.Lock() 

        # Ensure the class inherits from BaseController
        new_cls = (
            cls
            if issubclass(cls, BaseController)
            else type(
                cls.__name__, (BaseController, *cls.__bases__), dict(cls.__dict__)
            )
        )

        original_init = new_cls.__init__

        @wraps(original_init)
        def new_init(self, *args, **kwargs):
            super(new_cls, self).__init__(prefix=prefix, tags=tags, responses=responses)
            for key, value in kwargs.items():
                setattr(self, key, value)

            try:
                if not hasattr(self, "_register_routes") or not callable(
                    self._register_routes
                ):
                    raise NotImplementedError(
                        f"{new_cls.__name__} must implement '_register_routes'"
                    )
            except NotImplementedError as e:
                logger.error(str(e))
                return

            original_init(self, *args, **kwargs)

        new_cls.__init__ = new_init

        # Singleton wrapper
        @wraps(new_cls)
        def wrapper(*args, **kwargs):
            if new_cls not in _instances: 
                with _lock:  # Thread-safe block
                    if new_cls not in _instances:  # Double-check inside the lock
                        try:
                            logger.debug(f"Creating a new instance of {new_cls.__name__}")
                            _instances[new_cls] = new_cls(*args, **kwargs)
                        except TypeError as e:
                            logger.error(
                                f"{new_cls.__name__} must implement '_register_routes'"
                            )
                            return None
            return _instances.get(new_cls)

        return wrapper

    return decorator
