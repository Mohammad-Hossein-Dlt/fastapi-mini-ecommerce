import requests
from src.infra.external_api.interface.Icategory_service import ICategoryService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.infra.exceptions.exceptions import AppBaseException

class CategoryService(ICategoryService):
    
    def __init__(
        self,
        base_url: str,
    ):
        self.base_url = base_url + "/category"
        
        self.allowed_status_codes = [200, 201]
    
    def get_all(
        self,
        credentials: AuthCredentials,
        category_filter: CategoryFilterInput,
    ) -> dict:
        
        target_url = self.base_url + "/get/all"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        response = requests.get(target_url, headers=headers, params=category_filter.model_dump(mode="json"))
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
        
    def get_one(
        self,
        credentials: AuthCredentials,
        category_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/get/one"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        params = {
            "category_id": category_id,
        }
        
        response = requests.get(target_url, headers=headers, params=params)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)