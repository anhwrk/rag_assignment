# 🚀 Project Setup Guide

## 🧰 Tech Stack

This project leverages the following technologies:

- **FastAPI** — High-performance web framework for Python.
- **Redis** — In-memory store used as a message broker and cache.
- **Loguru** — Modern logging library for streamlined logging.
- **Custom Cache** — Caching utility using Redis for flexible storage.

---

## ✅ Prerequisites

Make sure you have the following installed:

- **Python 3.10+**
- **Docker**
- **Poetry**
- **MacOS, Linux, or WSL (if on Windows)**

---

## 📦 Poetry Installation

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
# Add to path 
nano ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc

```

---

## 🚀 Starting the Project

### ▶️ Using Docker

```bash
# Build and start services
docker-compose up -d --build
```

### ▶️ Running Locally

```bash
# Install dependencies
poetry install
# Start project
make run

```

---

## 🔧 Common Commands

```bash
# View available Makefile commands
make help

# Add a package
poetry add <package-name>
```

---

## 📋 Logging with Loguru

```python
from loguru import logger

logger.info("This is an info message")
logger.error("This is an error message")
```

---

## 🧠 Caching with Redis

### In Routes:

```python
def _register_routes(self):
    @self.router.get("")
    @Cache.cached(tag=CacheTag.GET_USER_LIST, ttl=300)
    async def read_users():
        return await self.service.get_all_user()
```

### Define Cache Tag (`core/cache/cache_tag.py`):

```python
from enum import Enum

class CacheTag(Enum):
    GET_USER_LIST = "get_user_list"
```

### In Functions:

```python
await Cache.backend.set(key="test", response="value", ttl=3600)
cache_data = await Cache.backend.get(key="test")
```

---

## ➕ Adding a New Feature

### 1. **Create New Module**

- Create a folder in `app/v1/`, e.g., `app/v1/users/`.

### 2. **Controller Example**

```python
@Controller(tags=["users"], prefix="/users")
@Auth(permissions=["CREATE"])
class UserController:
    def __init__(self):
        self.service = UserService()

    def _register_routes(self):
        @self.router.get("")
        async def read_users(req: Request, queries: GetQueries = Depends(get_queries)) -> PaginatedResponse:
            return await self.service.get_all_users(queries)

        @self.router.get("/{id}")
        @Auth(permissions=["CREATE"])
        @Cache.cached(tag=CacheTag.GET_USER_LIST, ttl=180)
        async def get_by_id(req: Request, id: str) -> Optional[User]:
            return await self.service.get_by_id(id)

        @self.router.post("")
        async def create_user(req: Request, body: UserCreateDTO = Body(...)) -> Optional[User]:
            return await self.service.create_user(body)

        @self.router.put("/{id}")
        async def update_user(req: Request, id: str, body: UserUpdateDTO = Body(...)) -> Optional[User]:
            return await self.service.update_user(id, body)

        @self.router.delete("/{id}")
        async def delete_user(req: Request, id: str) -> Optional[User]:
            return await self.service.delete_user(id)
```

### 3. **Register the Controller**

In `app/v1/users/__init__.py`:

```python
from .user_controller import UserController
from .user_service import UserService

__all__ = ["UserController", "UserService", "CurrentUser"]
```

In `app/v1/__init__.py`:

```python
from fastapi import APIRouter
from .users import UserController

v1_router = APIRouter()
v1_router.include_router(UserController().router)
```

### 4. **Create a Service**

In `user_service.py`:

```python
from core.decorators import Service

@Service()
class UserService:
    def __init__(self):
        pass

    async def create_user(self, user_data):
        # Logic to create a user
        return {"message": "User created", "data": user_data}
```

---

## 🚨 Adding a Custom Exception

Create an exception in `core/exceptions/`:

```python
from http import HTTPStatus
from core.exceptions.base import CustomException

class BadRequestException(CustomException):
    error_code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description
```

---

## 📝 Notes

- Use `@Controller` to define API controllers.
- Use `@Auth` to manage permissions and authentication.
- Use `@Service` for business logic layers.
- Use `Loguru` for enhanced logging and debugging.
- Make sure to leverage Redis caching for performance optimization.
