from src.gateway.internal.interface.Icategory_service import ICategoryService
from src.infra.schemas.broker.nats import NatsClient
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.filter.category_filter_input import CategoryFilterInput
from src.infra.exceptions.exceptions import AppBaseException
import json

class CategoryBrokerService(ICategoryService):
    
    def __init__(
        self,
        client: NatsClient,
    ):
        self.client = client
        self.check_point = "status_code"

    async def get_by_id(
        self,
        credentials: AuthCredentials,
        category_id: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=category_id,
            headers={
                "token": credentials.access_token,
            },
            subject="product_service.category.get.by-id",
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
    
    async def get_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: CategoryFilterInput,
    ) -> list:
        
        response = await self.client.broker.request(
            message=criteria.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            subject="product_service.category.get.by-criteria",
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
