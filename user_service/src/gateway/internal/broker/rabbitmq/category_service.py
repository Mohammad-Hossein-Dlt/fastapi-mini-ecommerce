from src.infra.schemas.broker.rabbitmq import RabbitClient
from src.gateway.internal.interface.Icategory_service import ICategoryService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.category_filter_input import CategoryFilterInput
from src.infra.exceptions.exceptions import AppBaseException
import json

class CategoryService(ICategoryService):
    
    def __init__(
        self,
        client: RabbitClient,
    ):
        self.client = client
        self.check_point = "status_code"

    async def get_by_id(
        self,
        credentials: AuthCredentials,
        category_id: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message={
                "category_id": category_id,
            },
            headers={
                "token": credentials.access_token,
            },
            routing_key="product_service.category.get.by-id",
            exchange=self.client.exchange,
            timeout=10,
        )
        _dict: dict = json.loads(response.body.decode())
        status = _dict.get(self.check_point, None)
        if status:
            message = _dict.get("message", None)
            raise AppBaseException(status, message)
        else:
            return _dict  
    
    async def get_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: CategoryFilterInput,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=criteria.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            routing_key="product_service.category.get.by-criteria",
            exchange=self.client.exchange,
            timeout=10,
        )
        _dict: dict = json.loads(response.body.decode())
        status = _dict.get(self.check_point, None)
        if status:
            message = _dict.get("message", None)
            raise AppBaseException(status, message)
        else:
            return _dict   
