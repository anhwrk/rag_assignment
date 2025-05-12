from core.decorators import Controller
from .auth_service import AuthService

@Controller(tags=["auth"], prefix="/auth")
class AuthController:
    def __init__(self):
        self.service = AuthService()

    def _register_routes(self):
        @self.router.post("/permanent-token")
        async def create_permanent_token():
            token = await self.service.create_permanent_token()
            return {"api_key": token}
