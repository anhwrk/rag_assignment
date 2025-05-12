from core.cache.cache_manager import Cache
from core.cache.cache_tag import CacheTag
from .models import RecommendationDTO
from fastapi import Request, Body
from core.decorators import Controller
from .recommendation_service import RecommendationService
from loguru import logger

@Controller(tags=["recommendation"], prefix="/recommendation")
class RecommendationController:
    def __init__(self):
        self.service = RecommendationService()

    def _register_routes(self):
        @Cache.cached(tag=CacheTag.GET_RECOMMENDATION, ttl=300)
        @self.router.post("")
        async def get_fitting_recommendation(req: Request, body: RecommendationDTO = Body(...)):
            return await self.service.get_recommendation(body)

        

