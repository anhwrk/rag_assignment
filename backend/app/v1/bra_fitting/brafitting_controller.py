from .models.dto import BraFitting
from fastapi import Request, Body
from core.decorators import Controller

from .brafitting_service import BraFittingService

@Controller(tags=["bra-fitting"], prefix="/bra-fitting")
class BraFittingController:
    def __init__(self):
        self.service = BraFittingService()

    def _register_routes(self):
        @self.router.post("")
        async def create_bra_fitting_data(req: Request, body: BraFitting = Body(...)):
            return await self.service.create_bra_fitting(body)

        

