import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))  

import json
from prisma import Prisma
from common.openai.embedding import Embedding
from loguru import logger

async def main():
    db = Prisma()
    await db.connect()
    embedding_client = Embedding()

    with open('prisma/seed/data/bra_fitting_data.json', encoding='utf-8') as f:
        bra_data = json.load(f)
        for item in bra_data:
            combined_text = (
                f"Description: {item['description']}\n"
                f"Recommendation: {item['recommendation']}\n"
                f"Reasoning: {item['reasoning']}\n"
                f"Common Issues: {', '.join(item['common_issues'])}\n" 
                f"Fit Tips: {item['fit_tips']}"
            )
            
            embedding_vector = embedding_client.embedding_text(combined_text)
            
            await db.brafitting.create(
                data={
                    "description": item["description"],
                    "recommendation": item["recommendation"],
                    "reasoning": item["reasoning"],
                    "common_issues": item["common_issues"],
                    "fit_tips": item["fit_tips"],
                    "embedding": embedding_vector
                }
            )
            logger.info("Stored bra fitting data with embedding")

    await db.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
