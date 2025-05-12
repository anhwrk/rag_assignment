from loguru import logger
import pymongo
from core.config import config

class MongoDBIndex:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(config.DATABASE_URL)
        self.db = self.client[config.DB_NAME]
        self.collection = self.db[config.DB_COLLECTION]
    
    @staticmethod
    def create_vector_search_index_if_not_exists(self, index_name: str = "vector_index"):
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
                                "dimensions": 1536,
                                "similarity": "cosine",
                                "type": "knnVector"
                            }
                        }
                    }
                }
            }]
        })
        logger.info(f"Successfully created index {index_name}")
        