from .models import RecommendationDTO
from fastapi import Request, Body
from core.decorators import Controller

from .recommendation_service import RecommendationService

@Controller(tags=["recommendation"], prefix="/recommendation")
class RecommendationController:
    def __init__(self):
        self.service = RecommendationService()

    def _register_routes(self):
        @self.router.post("")
        async def get_fitting_recommendation(req: Request, body: RecommendationDTO = Body(...)):
            return await self.service.get_recommendation(body)

        

