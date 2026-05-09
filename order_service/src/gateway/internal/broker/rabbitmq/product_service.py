from src.gateway.internal.interface.Iproduct_service import IProductService
from src.infra.schemas.broker.rabbitmq import RabbitClient
from src.infra.exceptions.exceptions import AppBaseException

class ProductService(IProductService):
    
    def __init__(
        self,
        client: RabbitClient,
    ):
        self.client = client
            
    async def get_by_id(
        self,
        access_token: str,
        product_id: str,
    ) -> dict:
        
        try:
            return await self.client.broker.request(
                message={
                    "token": access_token,
                    "product_id": product_id,
                },
                routing_key="product_service.product.get.by-id",
                exchange=self.client.exchange,
                timeout=10,
            )
        except:
            raise