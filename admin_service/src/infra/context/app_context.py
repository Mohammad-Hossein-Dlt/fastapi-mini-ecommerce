from typing import ClassVar
from aiohttp import ClientSession

class AppContext(type):
    
    auth_base_url: ClassVar[str] = None
    product_base_url: ClassVar[str] = None
    order_base_url: ClassVar[str] = None
    http_client: ClassVar[ClientSession] = None