from src.infra.context.app_context import AppContext

from src.gateway.internal.interface.Iauth_service import IAuthService
from src.gateway.internal.http.auth_service import AuthService

from src.gateway.internal.interface.Iproduct_service import IProductService
from src.gateway.internal.http.product_service import ProductService
    
def auth_service_depend() -> IAuthService:
    
    return AuthService(
        AppContext.http_client,
        AppContext.auth_base_url,
    )

def product_service_depend() -> IProductService:
    
    return ProductService(
        AppContext.http_client,
        AppContext.product_base_url + "/product",
    )