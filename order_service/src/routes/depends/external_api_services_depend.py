from src.infra.fastapi_config.app import app
from src.infra.fastapi_config.app_state import AppStates, get_app_state

from src.infra.external_api.interface.Iauth_service import IAuthService
from src.infra.external_api.service.auth_service import AuthService

from src.infra.external_api.interface.Iproduct_service import IProductService
from src.infra.external_api.service.product_service import ProductService

def get_auth_service() -> IAuthService:
    base_url = get_app_state(app, AppStates.AUTH_BASE_URL)
    return AuthService(base_url)


def get_product_service() -> IProductService:
    base_url = get_app_state(app, AppStates.PRODUCT_BASE_URL)
    return ProductService(base_url)
    
    
