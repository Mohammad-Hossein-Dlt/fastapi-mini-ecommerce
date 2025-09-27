import requests
from src.infra.external_api.interface.Iproduct_service import IProductService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.product.create_product_input import CreateProductInput
from src.models.schemas.product.update_product_input import UpdateProductInput
from src.models.schemas.filter.products_filter_input import ProductFilterInput
from src.infra.exceptions.exceptions import AppBaseException

class ProductService(IProductService):
    
    def __init__(
        self,
        base_url: str,
    ):
        self.base_url = base_url + "/product"
        self.allowed_status_codes = [200, 201]
    
    def create(
        self,
        credentials: AuthCredentials,
        product_data: CreateProductInput,
    ) -> dict:
        
        target_url = self.base_url + "/create"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        response = requests.post(target_url, headers=headers, params=product_data.model_dump(mode="json"))
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
                                        
    def delete_all(
        self,
        credentials: AuthCredentials,
    ) -> dict:
        
        target_url = self.base_url + "/delete/all"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        response = requests.delete(target_url, headers=headers)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    def delete_one(
        self,
        credentials: AuthCredentials,
        product_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/delete/one"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        params = {
            "product_id": product_id,
        }
        
        response = requests.delete(target_url, headers=headers, params=params)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
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
    
    def update_one(
        self,
        credentials: AuthCredentials,
        product_data: UpdateProductInput,
    ) -> dict:
        
        target_url = self.base_url + "/update/one"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        response = requests.put(target_url, headers=headers, params=product_data.model_dump(mode="json"))
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)