from core.config import config
from core.decorators import Controller

from .monitoring_model import Health


@Controller(tags=["monitoring"], prefix="/monitoring")
class MonitoringController:
    def __init__(self):
        pass

    def _register_routes(self):
        @self.router.get("/health", response_model=Health)
        async def check_health():
            return Health(version=config.RELEASE_VERSION, status="Healthy")
