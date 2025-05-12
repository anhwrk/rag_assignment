from fastapi import APIRouter

from .auth import AuthController
from .monitoring import MonitoringController
from .recommendation import RecommendationController

v1_router = APIRouter()
v1_router.include_router(MonitoringController().router)
v1_router.include_router(RecommendationController().router)
v1_router.include_router(AuthController().router)
