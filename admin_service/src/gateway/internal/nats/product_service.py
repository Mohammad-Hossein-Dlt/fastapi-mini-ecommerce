from src.gateway.internal.interface.Iproduct_service import IProductService
from src.infra.schemas.broker.nats import NatsClient
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.product.create_product_input import CreateProductInput
from src.schemas.product.update_product_input import UpdateProductInput
from src.schemas.filter.product_filter_input import ProductFilterInput
from src.infra.exceptions.exceptions import AppBaseException
import json

class ProductBrokerService(IProductService):
    
    def __init__(
        self,
        client: NatsClient,
    ):
        self.client = client
        self.check_point = "status_code"
    
    async def create(
        self,
        credentials: AuthCredentials,
        product: CreateProductInput,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=product.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            subject="product_service.product.create",
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

    async def get_by_id(
        self,
        credentials: AuthCredentials,
        product_id: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=product_id,
            headers={
                "token": credentials.access_token,
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
    
    async def update(
        self,
        credentials: AuthCredentials,
        product: UpdateProductInput,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=product.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            subject="product_service.product.update",
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

    async def delete_by_id(
        self,
        credentials: AuthCredentials,
        product_id: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=product_id,
            headers={
                "token": credentials.access_token,
            },
            subject="product_service.product.delete.by-id",
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
        criteria: ProductFilterInput,
    ) -> list:
        
        response = await self.client.broker.request(
            message=criteria.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            subject="product_service.product.get.by-criteria",
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
        
    async def delete_all(
        self,
        credentials: AuthCredentials,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=None,
            headers={
                "token": credentials.access_token,
            },
            subject="product_service.product.delete.all",
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