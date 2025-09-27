import requests
from src.infra.external_api.interface.Iauth_service import IAuthService
from src.models.schemas.user.user_register_input import UserRegisterInput
from src.models.schemas.user.user_login_input import UserLoginInput
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException

class AuthService(IAuthService):
    
    def __init__(
        self,
        base_url: str,
    ):
        
        self.base_url = base_url
        self.allowed_status_codes = [200, 201]
    
    def register(
        self,
        user_data: UserRegisterInput,
    ) -> dict:
        
        target_url = self.base_url + "/register"
        
        user_data: dict = user_data.model_dump(mode="json")
        user_data["role"] = "admin"
                
        response = requests.post(target_url, json=user_data)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    def login(
        self,
        user_data: UserLoginInput,
    ) -> dict:
        
        target_url = self.base_url + "/login"
        
        response = requests.post(target_url, data=user_data.model_dump(mode="json"))
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    def refresh_token(
        self,
        credentials: AuthCredentials,
    ) -> dict:
                
        target_url = self.base_url + "/refresh-token"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.refresh_token}"
        }
        
        response = requests.get(target_url, headers=headers)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    def admin_get_self(
        self,
        credentials: AuthCredentials,
    ) -> dict:
        
        target_url = self.base_url + "/admin/self/get"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
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
        credentials: AuthCredentials,
        user_id: str | None = None,
        username: str | None = None,
    ) -> dict:
        
        target_url = self.base_url + "/admin/user/get"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        data = {
            "user_id": user_id,
            "username": username,
        }
        
        response = requests.get(target_url, headers=headers, params=data)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    def admin_delete_user(
        self,
        credentials: AuthCredentials,
        user_id: str | None = None,
        username: str | None = None,
    ) -> dict:
        
        target_url = self.base_url + "/admin/user/delete"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        data = {
            "user_id": user_id,
            "username": username,
        }
        
        response = requests.delete(target_url, headers=headers, params=data)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    def user_get_self(
        self,
        credentials: AuthCredentials,
    ) -> dict:
        
        target_url = self.base_url + "/user/self/get"
        
        headers = {
            "Authorization": f"{credentials.token_type.title()} {credentials.access_token}"
        }
        
        response = requests.get(target_url, headers=headers)
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    def user_delete_self(
        self,
        credentials: AuthCredentials,
    ) -> dict:
                
        target_url = self.base_url + "/user/self/delete"
        
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