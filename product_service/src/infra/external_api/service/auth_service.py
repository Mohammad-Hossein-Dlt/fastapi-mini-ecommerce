import requests
from src.infra.external_api.interface.Iauth_service import IAuthService
from src.infra.exceptions.exceptions import AppBaseException


class AuthService(IAuthService):
    
    def __init__(
        self,
        base_url: str,
    ):
        
        self.base_url = base_url
        self.allowed_status_codes = [200, 201]
    
    def admin_get_self(
        self,
        access_token: str,
    ) -> dict:
        
        target_url = self.base_url + "/admin/self/get"
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(target_url, headers=headers)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    
    def admin_get_user(
        self,
        access_token: str,
        user_id: str | None = None,
        username: str | None = None,
    ) -> dict:
        
        target_url = self.base_url + "/admin/user/get"
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        data = {
            "user_id": user_id,
            "username": username,
        }
        
        response = requests.get(target_url, headers=headers, data=data)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    
    def user_get_self(
        self,
        access_token: str,
    ) -> dict:
        
        target_url = self.base_url + "/user/self/get"
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(target_url, headers=headers)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)