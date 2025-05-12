import json
from prisma import Prisma

async def main():
    db = Prisma()
    await db.connect()

    # Load and insert BraFittingRecommendation data
    with open('prisma/seed/data/bra_fitting_data.json', encoding='utf-8') as f:
        bra_data = json.load(f)
        for item in bra_data:
            await db.brafittingrecommendation.create(
                data={
                    "description": item["description"],
                    "recommendation": item["recommendation"],
                    "reasoning": item["reasoning"],
                    "common_issues": item["common_issues"],
                    "fit_tips": item["fit_tips"],
                }
            )

    # Load and insert SizeRecommendation data
    with open('prisma/seed/data/size_data.json', encoding='utf-8') as f:
        size_data = json.load(f)
        for item in size_data:
            measurements = item["measurements"]
            await db.sizerecommendation.create(
                 data={
                    "description": item["description"],
                    "size": item["size"],
                    "chest": float(measurements["chest"]),  # Ensure it's a float
                    "waist": float(measurements["waist"]),  # Ensure it's a float
                    "additional_context": item["additional_context"],
                }
            )

    await db.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
