from src.gateway.internal.interface.Iproduct_service import IProductService
from src.infra.schemas.broker.rabbitmq import RabbitClient
from src.infra.exceptions.exceptions import AppBaseException

class ProductService(IProductService):
    
    def __init__(
        self,
        client: RabbitClient,
    ):
        
        self.client = client
                
        self.allowed_status_codes = [200, 201]
    
    async def get_by_id(
        self,
        access_token: str,
        product_id: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message={
                "access_token": access_token,
                "product_id": product_id,
            },
            routing_key="product_service.product.get.one",
            exchange=self.client.exchange,
            timeout=10,
        )
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
        