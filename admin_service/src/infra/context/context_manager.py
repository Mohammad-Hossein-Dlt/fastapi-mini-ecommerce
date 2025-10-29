from .app_context import AppContext
from src.infra.settings.settings import settings
from aiohttp import ClientSession

class AppContextManager:
        
    @classmethod
    def init_context(cls):
                
        AppContext.auth_base_url = settings.AUTH_BASE_URL
        AppContext.product_base_url = settings.PRODUCT_BASE_URL
        AppContext.order_base_url = settings.ORDER_BASE_URL
        
    @classmethod
    async def lazy_init_context(cls):
        
        print("Starting up...")
        
        AppContext.http_client = ClientSession()
        
    @classmethod
    async def terminate_context(cls):
        
        print("Shutting down...")
        
        await AppContext.http_client.close()
        
AppContextManager.init_context()