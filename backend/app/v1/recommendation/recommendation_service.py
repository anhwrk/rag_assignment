from common.mongodb.search import MongoDBVectorSearch
from common.constants import (
    DEFAULT_RECOMMENDATION, DEFAULT_CONFIDENCE, 
    DEFAULT_REASONING, DEFAULT_FIT_TIPS, 
    DEFAULT_BEST_MATCH_SCORE_THRESHOLD
)
from .models import RecommendationDTO, RecommendationResponse
from loguru import logger
from core.decorators import Service
from typing import Dict
from common.openai.embedding import Embedding

@Service()
class RecommendationService:
    def __init__(self):
        self.embedding_client = Embedding()
        self.vector_search = MongoDBVectorSearch()

    def _create_response(self, match: Dict) -> RecommendationResponse:
        common_issues = [issue.replace("_", " ").capitalize() for issue in match["common_issues"]]
        return RecommendationResponse(
            recommendation=match["recommendation"],
            confidence=match["score"],
            reasoning=match["reasoning"],
            fit_tips=match["fit_tips"],
            identified_issues=common_issues
        )

    def _get_default_response(self) -> RecommendationResponse:
        return RecommendationResponse(
            recommendation=DEFAULT_RECOMMENDATION,  
            confidence=DEFAULT_CONFIDENCE,
            reasoning=DEFAULT_REASONING,
            fit_tips=DEFAULT_FIT_TIPS,
            identified_issues=[]
        )

    async def get_recommendation(self, query: RecommendationDTO) -> RecommendationResponse:
        try:
            # Generate embedding for query
            query_embedding = self.embedding_client.embedding_text(query.text)

            # Search for similar fittings
            results = self.vector_search.execute_vector_search(query_embedding)

            # Return default response if no matches found
            if not results:
                logger.warning("No matches found, returning default recommendation")
                return self._get_default_response()

            # Check if best match has sufficient confidence
            best_match = results[0]
            if best_match["score"] < DEFAULT_BEST_MATCH_SCORE_THRESHOLD: 
                logger.warning("Match found but confidence too low, returning default recommendation")
                return self._get_default_response()

            # Return best match
            return self._create_response(best_match)

        except Exception as e:
            logger.error(f"Error getting recommendation: {str(e)}")
            raise 
