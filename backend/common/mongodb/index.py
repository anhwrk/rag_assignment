from loguru import logger
import pymongo
from core.config import config
from common.constants import VECTOR_SEARCH_INDEX_NAME, VECTOR_SEARCH_DIMENSIONS, VECTOR_SEARCH_SIMILARITY, VECTOR_SEARCH_TYPE

class MongoDBIndex:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(config.DATABASE_URL)
        self.db = self.client[config.DB_NAME]
        self.collection = self.db[config.DB_COLLECTION]
    
    @staticmethod
    def create_vector_search_index_if_not_exists(self, index_name: str = VECTOR_SEARCH_INDEX_NAME):
        existing_indexes = list(self.collection.list_search_indexes())
        if any(idx.get('name') == index_name for idx in existing_indexes):
            logger.info(f"Index {index_name} already exists")
            return

        self.collection.database.command({
            "createSearchIndexes": self.collection.name,
            "indexes": [{
                "name": index_name,
                "definition": {
                    "mappings": {
                        "dynamic": True,
                        "fields": {
                            "embedding": {
                                "dimensions": VECTOR_SEARCH_DIMENSIONS,
                                "similarity": VECTOR_SEARCH_SIMILARITY,
                                "type": VECTOR_SEARCH_TYPE
                            }
                        }
                    }
                }
            }]
        })
        logger.info(f"Successfully created index {index_name}")
        