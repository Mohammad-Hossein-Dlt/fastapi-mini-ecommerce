from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .collections.category_collection import CategoryCollection
from .collections.product_collection import ProductCollection


async def init_mongodb(
    host: str,
    port: int,
    username: str,
    password: str,
    db_name: str
) -> AsyncIOMotorClient:
    
    client = AsyncIOMotorClient(
        host=host,
        port=port,
        username=username,
        password=password
    )
    
    await init_beanie(
        database=client[db_name],
        document_models=[
            CategoryCollection,
            ProductCollection,    
        ],
    )
    
    return client