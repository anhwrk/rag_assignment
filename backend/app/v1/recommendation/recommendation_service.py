from common.constants import (
    DEFAULT_RECOMMENDATION, DEFAULT_CONFIDENCE, DEFAULT_REASONING, DEFAULT_FIT_TIPS, 
    VECTOR_SEARCH_PATH, VECTOR_SEARCH_LIMIT, VECTOR_SEARCH_THRESHOLD, VECTOR_SEARCH_INDEX_NAME,
    DEFAULT_BEST_MATCH_SCORE_THRESHOLD
)
from core.exceptions.base import AlreadyExistedException, NotFoundException
from .models import RecommendationDTO, RecommendationResponse
from loguru import logger
from core.decorators import Service
from typing import Dict, Optional, List
from common.openai.embedding import Embedding
from common.mongodb.index import MongoDBIndex

@Service()
class RecommendationService:
    def __init__(self):
        self.embedding_client = Embedding()
        self.mongodb_index = MongoDBIndex()
        self.index_name = VECTOR_SEARCH_INDEX_NAME

    def _create_search_pipeline(self, query_embedding: List[float]) -> List[Dict]:
        return [
            {
                "$vectorSearch": {
                    "index": self.index_name,
                    "queryVector": query_embedding,
                    "path": VECTOR_SEARCH_PATH,
                    "limit": VECTOR_SEARCH_LIMIT,
                    "minScore": VECTOR_SEARCH_THRESHOLD,
                    "numCandidates": 100,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "recommendation": 1,
                    "reasoning": 1,
                    "fit_tips": 1,
                    "common_issues": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            },
            {
                "$sort": {
                    "score": -1
                }
            }
        ]

    def _execute_vector_search(self, pipeline: List[Dict]) -> List[Dict]:
        results = list(self.mongodb_index.collection.aggregate(pipeline))
        logger.info(f"Found {len(results)} matches")
        return results

    def _create_response(self, match: Dict) -> RecommendationResponse:
        return RecommendationResponse(
            recommendation=match["recommendation"],
            confidence=match["score"],
            reasoning=match["reasoning"],
            fit_tips=match["fit_tips"],
            identified_issues=match["common_issues"]
        )

    def _get_default_response(self) -> RecommendationResponse:
        return RecommendationResponse(
            recommendation=DEFAULT_RECOMMENDATION, 
            confidence=DEFAULT_CONFIDENCE,
            reasoning=DEFAULT_REASONING,
            fit_tips=DEFAULT_FIT_TIPS,
        )

    async def get_recommendation(self, query: RecommendationDTO) -> RecommendationResponse:
        try:
            # Generate embedding for query
            query_embedding = self.embedding_client.embedding_text(query.text)

            # Search for similar fittings
            pipeline = self._create_search_pipeline(query_embedding)
            results = self._execute_vector_search(pipeline)

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
