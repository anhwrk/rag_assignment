from core.exceptions.base import AlreadyExistedException, NotFoundException
from .models import BraFitting
from loguru import logger
from core.decorators import Service
from typing import Dict, Optional, List
import json

@Service()
class BraFittingService:
    def __init__(self):
        pass
    
    def create_bra_fitting(self, bra_fitting: BraFitting) -> BraFitting:
        pass
    
    