import requests
from src.infra.external_api.interface.Iproduct_service import IProductService
from src.infra.exceptions.exceptions import AppBaseException


class ProductService(IProductService):
    
    def __init__(
        self,
        base_url: str,
    ):
        self.base_url = base_url + "/product"
        self.allowed_status_codes = [200, 201]
    
    def get_product(
        self,
        access_token: str,
        product_id: str,
    ) -> dict:
                
        target_url = self.base_url + "/get/one"
                
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        data = {
            "product_id": product_id,
        }
        
        response = requests.get(target_url, headers=headers, params=data)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
        