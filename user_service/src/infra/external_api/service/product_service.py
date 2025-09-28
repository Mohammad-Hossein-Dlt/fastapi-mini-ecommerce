import requests
from src.infra.external_api.interface.Iproduct_service import IProductService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.products_filter_input import ProductFilterInput
from src.infra.exceptions.exceptions import AppBaseException

class ProductService(IProductService):
    
    def __init__(
        self,
        base_url: str,
    ):
        self.base_url = base_url + "/product"
        self.allowed_status_codes = [200, 201]

    def get_all(
        self,
        credentials: AuthCredentials,
        product_filter: ProductFilterInput,
    ) -> dict:
        
        target_url = self.base_url + "/get/all"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        response = requests.get(target_url, headers=headers, params=product_filter.model_dump(mode="json"))
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
        
    def get_one(
        self,
        credentials: AuthCredentials,
        product_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/get/one"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        params = {
            "product_id": product_id,
        }
        
        response = requests.get(target_url, headers=headers, params=params)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)