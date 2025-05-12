from functools import wraps
from typing import Any, Dict, Type
import threading  
from loguru import logger

def Service():
    def decorator(cls):
        _instances: Dict[Type, Any] = {}
        _lock = threading.Lock()  

        original_init = cls.__init__

        @wraps(original_init)
        def new_init(self, *args, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
            original_init(self, *args, **kwargs)

        cls.__init__ = new_init

        @wraps(cls)
        def wrapper(*args, **kwargs):
            if cls not in _instances:  
                with _lock:  
                    if cls not in _instances:  
                        logger.debug(f"Creating a new instance of {cls.__name__}")
                        _instances[cls] = cls(*args, **kwargs)
            return _instances[cls]

        return wrapper

    return decorator
