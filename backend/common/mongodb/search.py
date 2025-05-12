from typing import Dict, List
from loguru import logger
import pymongo
from core.config import config
from common.constants import (
    VECTOR_SEARCH_PATH, VECTOR_SEARCH_LIMIT, VECTOR_SEARCH_THRESHOLD, 
    VECTOR_SEARCH_NUM_CANDIDATES, VECTOR_SEARCH_INDEX_NAME
)
from .exception import (
    MongoDBParameterException,
    MongoDBVectorSearchException
)

class MongoDBVectorSearch:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(config.DATABASE_URL)
        self.db = self.client[config.DB_NAME]
        self.collection = self.db[config.DB_COLLECTION]
        self.index_name = VECTOR_SEARCH_INDEX_NAME
    
    def _create_search_pipeline(self, query_embedding: List[float], index_name: str) -> List[Dict]:
        return [
            {
                "$vectorSearch": {
                    "index": index_name,
                    "queryVector": query_embedding,
                    "path": VECTOR_SEARCH_PATH,
                    "limit": VECTOR_SEARCH_LIMIT,
                    "minScore": VECTOR_SEARCH_THRESHOLD,
                    "numCandidates": VECTOR_SEARCH_NUM_CANDIDATES,
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

    def execute_vector_search(self, query_embedding: List[float], index_name: str = VECTOR_SEARCH_INDEX_NAME) -> List[Dict]:
        try:
            if not query_embedding or not isinstance(query_embedding, list):
                raise MongoDBParameterException("query_embedding must be a non-empty list of floats")

            pipeline = self._create_search_pipeline(query_embedding, index_name)
            
            try:
                results = list(self.collection.aggregate(pipeline))
                logger.info(f"Vector search found {len(results)} matches")
                return results
            except Exception as e:
                logger.error(f"Vector search operation failed: {str(e)}")
                raise MongoDBVectorSearchException(f"Vector search failed: {str(e)}")

        except MongoDBParameterException as e:
            logger.error(f"Parameter error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in vector search: {str(e)}")
            raise MongoDBVectorSearchException(str(e))
