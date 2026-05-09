from .app_context import AppContext
from src.infra.settings.settings import settings
from src.infra.bootstrap.broker import init_broker_client, terminate_broker_client
from aiohttp import ClientSession

class AppContextManager:
        
    @classmethod
    def init_context(cls):
        
        print("Starting up...")
        
        AppContext.auth_base_url = settings.AUTH_BASE_URL
        AppContext.product_base_url = settings.PRODUCT_BASE_URL
        AppContext.order_base_url = settings.ORDER_BASE_URL
        
        AppContext.auth_communication_type = settings.AUTH_COMMUNICATION_TYPE
        AppContext.product_communication_type = settings.PRODUCT_COMMUNICATION_TYPE
        AppContext.order_communication_type = settings.ORDER_COMMUNICATION_TYPE
        
        AppContext.broker_client = init_broker_client(settings.NATS)
        
    @classmethod
    async def lazy_init_context(cls):
        
        print("Starting up...")
        
        await AppContext.broker_client.broker.connect()
        
        AppContext.http_client = ClientSession()
        
    @classmethod
    async def terminate_context(cls):
        
        print("Shutting down...")
        
        await terminate_broker_client(AppContext.broker_client)
        await AppContext.http_client.close()
        
AppContextManager.init_context()