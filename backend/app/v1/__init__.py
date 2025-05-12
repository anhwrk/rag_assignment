from fastapi import APIRouter

from .auth import AuthController
from .monitoring import MonitoringController
from .recommendation import RecommendationController
from .bra_fitting import BraFittingController

v1_router = APIRouter()
v1_router.include_router(MonitoringController().router)
v1_router.include_router(RecommendationController().router)
v1_router.include_router(AuthController().router)
v1_router.include_router(BraFittingController().router)
