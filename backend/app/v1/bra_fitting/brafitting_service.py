from .models.dto import BraFitting 
from loguru import logger
from core.decorators import Service
from typing import Dict, Optional, List
from prisma import Prisma
from common.openai.embedding import Embedding

@Service()
class BraFittingService:
    def __init__(self):
        self.db = Prisma()
        self.embedding_client = Embedding()
    
    async def create_bra_fitting(self, bra_fitting: BraFitting) -> BraFitting:
        await self.db.connect() 
        try:
            combined_text = (
                f"Description: {bra_fitting.description}\n"
                f"Recommendation: {bra_fitting.recommendation}\n"
                f"Reasoning: {bra_fitting.reasoning}\n"
                f"Common Issues: {', '.join(bra_fitting.common_issues)}\n" 
                f"Fit Tips: {bra_fitting.fit_tips}"
            )
            
            embedding_vector = self.embedding_client.embedding_text(combined_text)
            
            created_bra_fitting = await self.db.brafitting.create(
                data={
                    "description": bra_fitting.description,
                    "recommendation": bra_fitting.recommendation,
                    "reasoning": bra_fitting.reasoning,
                    "common_issues": bra_fitting.common_issues,
                    "fit_tips": bra_fitting.fit_tips,
                    "embedding": embedding_vector
                }
            )
            return created_bra_fitting
        except Exception as e:
            logger.error(f"Error creating bra fitting: {str(e)}")
            raise
        finally:
            await self.db.disconnect()