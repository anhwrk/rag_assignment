from core.decorators import Service
from core.security.jwt import JWTHandler


@Service()
class AuthService:
    def __init__(self):
        pass

    async def create_permanent_token(self) -> str:
        payload = {
            "user_id": "test-api-bff", 
            "permissions": ["CREATE"]
        }
        return JWTHandler.encode(payload, expires=False)
