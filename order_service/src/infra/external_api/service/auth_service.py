import requests
from src.infra.external_api.interface.Iauth_service import IAuthService
from src.infra.exceptions.exceptions import InvalidRequestException, EntityNotFoundError, AuthenticationException, OperationFailureException, Error


class AuthService(IAuthService):
    
    def __init__(
        self,
        base_url: str,
    ):
        
        self.base_url = base_url
    
    def admin_get_self(
        self,
        access_token: str,
    ) -> dict:
        
        target_url = self.base_url + "/admin/self/get"
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(target_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()

        if response.status_code == 400:
            data = response.json()
            detail = data["detail"]
            raise InvalidRequestException(response.status_code, detail)

        if response.status_code == 401:
            data = response.json()
            detail = data["detail"]
            raise AuthenticationException(response.status_code, detail)

        if response.status_code == 404:
            data = response.json()
            detail = data["detail"]
            raise EntityNotFoundError(response.status_code, detail)

        if response.status_code == 500:
            data = response.json()
            detail = data["detail"]
            raise OperationFailureException(response.status_code, detail)
                
        raise Error(500, "An error occurred during get user")
    
    
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
        
        if response.status_code == 200:
            return response.json()

        if response.status_code == 400:
            data = response.json()
            detail = data["detail"]
            raise InvalidRequestException(response.status_code, detail)

        if response.status_code == 401:
            data = response.json()
            detail = data["detail"]
            raise AuthenticationException(response.status_code, detail)

        if response.status_code == 404:
            data = response.json()
            detail = data["detail"]
            raise EntityNotFoundError(response.status_code, detail)

        if response.status_code == 500:
            data = response.json()
            detail = data["detail"]
            raise OperationFailureException(response.status_code, detail)
                
        raise Error(500, "An error occurred during get user")
    
    
    def user_get_self(
        self,
        access_token: str,
    ) -> dict:
        
        target_url = self.base_url + "/user/self/get"
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(target_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()

        if response.status_code == 400:
            data = response.json()
            detail = data["detail"]
            raise InvalidRequestException(response.status_code, detail)

        if response.status_code == 401:
            data = response.json()
            detail = data["detail"]
            raise AuthenticationException(response.status_code, detail)

        if response.status_code == 404:
            data = response.json()
            detail = data["detail"]
            raise EntityNotFoundError(response.status_code, detail)

        if response.status_code == 500:
            data = response.json()
            detail = data["detail"]
            raise OperationFailureException(response.status_code, detail)
                
        raise Error(500, "An error occurred during get user")