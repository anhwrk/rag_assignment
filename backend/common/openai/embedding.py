from typing import List
from common.mongodb.index import MongoDBIndex
from loguru import logger
from langchain_openai import OpenAIEmbeddings
from core.config import config

class Embedding:
    def __init__(self):
        self.mongodbIndex = MongoDBIndex()
        self.embedding_model = OpenAIEmbeddings(
            model=config.OPEN_AI_EMBEDDING_MODEL,
            openai_api_key=config.OPEN_AI_KEY
        )
        self.index_name = "test_vector_index"

    def embedding_text(self, embedding_text: str) -> List[float]:
        logger.info(f"Start embedding text... {embedding_text}")
        MongoDBIndex.create_vector_search_index_if_not_exists(self.mongodbIndex, index_name=self.index_name)
        embedding = self.embedding_model.embed_query(embedding_text)
        logger.info(f"Text embedded")
        return embedding
