from src.gateway.internal.interface.Iproduct_service import IProductService
from src.infra.schemas.broker.nats import NatsClient
from src.infra.exceptions.exceptions import AppBaseException
import json

class ProductBrokerService(IProductService):
    
    def __init__(
        self,
        client: NatsClient,
    ):
        self.client = client
        self.check_point = "status_code"
            
    async def get_by_id(
        self,
        access_token: str,
        product_id: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=product_id,
            headers={
                "token": access_token,
            },
            subject="product_service.product.get.by-id",
            timeout=10,
        )
        
        data = json.loads(response.body.decode())
        status = False
        if isinstance(data, dict):
            status = data.get(self.check_point, False)
            
        if status:
            message = data.get("message", None)
            raise AppBaseException(status, message)
        else:
            return data