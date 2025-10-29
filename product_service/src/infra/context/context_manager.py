from .app_context import AppContext
from src.infra.settings.settings import settings
from src.infra.schemas.broker.rabbitmq_params import RabbitParams
from src.infra.schemas.broker.kafka_params import KafkaParams
from src.infra.bootstrap.database import init_database_client, terminate_database_client
from aiohttp import ClientSession

class AppContextManager:
        
    @classmethod
    def init_context(cls):
                
        AppContext.auth_base_url = settings.AUTH_BASE_URL
        AppContext.broker_params = RabbitParams.model_validate(settings.RABBITMQ_PRODUCT)
        
    @classmethod
    async def lazy_init_context(cls):
        
        print("Starting up...")
        
        AppContext.db_client = await init_database_client()
        AppContext.http_client = ClientSession()

    @classmethod
    async def terminate_context(cls):
        
        print("Shutting down...")
        
        await terminate_database_client(AppContext.db_client)
        await AppContext.http_client.close()
        
AppContextManager.init_context()