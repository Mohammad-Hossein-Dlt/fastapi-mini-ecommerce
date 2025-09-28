import requests
from src.infra.external_api.interface.Iorder_service import IOrderService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.filter_order_input import UserFilterOrderInput
from src.models.schemas.order.place_order_input import PlaceOrderInput
from src.models.schemas.order.update_order_input import UpdateOrderInput
from src.infra.exceptions.exceptions import AppBaseException

class OrderService(IOrderService):
        
    def __init__(
        self,
        base_url: str,
    ):
        self.base_url = base_url
        self.allowed_status_codes = [200, 201]
    
    def user_place_order(
        self,
        credentials: AuthCredentials,
        order: PlaceOrderInput,
    ) -> dict:
        
        target_url = self.base_url + "/user/place-order"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        print(target_url)
        
        response = requests.post(target_url, headers=headers, params=order.model_dump(mode="json"))
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    
    def user_get_one(
        self,
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/user/get/one"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        params = {
            "order_id": order_id,
        }
        
        response = requests.get(target_url, headers=headers, params=params)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    
    def user_get_all(
        self,
        credentials: AuthCredentials,
        order_filter: UserFilterOrderInput,
    ) -> dict:
        
        target_url = self.base_url + "/user/get/all"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        response = requests.get(target_url, headers=headers, params=order_filter.model_dump(mode="json"))
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    def user_update_one(
        self,
        credentials: AuthCredentials,
        order: UpdateOrderInput,
    ) -> dict:
       
        target_url = self.base_url + "/user/update/one"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
                
        response = requests.put(target_url, headers=headers, params=order.model_dump(mode="json"))
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)