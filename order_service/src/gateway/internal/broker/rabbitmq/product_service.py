from src.gateway.internal.interface.Iproduct_service import IProductService
from src.infra.schemas.broker.rabbitmq_params import RabbitParams
from faststream.rabbit import RabbitBroker, RabbitExchange, ExchangeType
from src.infra.exceptions.exceptions import AppBaseException

class ProductService(IProductService):
    
    def __init__(
        self,
        params: RabbitParams,
    ):
        self.broker = RabbitBroker(url=params.url)
        self.exchange = RabbitExchange(name=params.exchange,type=ExchangeType.TOPIC)
        
        self.allowed_status_codes = [200, 201]
    
    async def get_product(
        self,
        access_token: str,
        product_id: str,
    ) -> dict:
        
        response = await self.broker.request(
            message={
                "access_token": access_token,
                "product_id": product_id,
            },
            routing_key="product_service.product.get.one",
            exchange=self.exchange,
            timeout=10,
        )
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
        