from src.infra.external_api.interface.Iproduct_service import IProductService
from src.domain.schemas.product.product_model import ProductModel

class GetProduct:
    
    def __init__(
        self,
        product_service: IProductService,
    ):  
        self.product_service = product_service
    
    def execute(
        self,
        access_token: str,
        product_id: str,
    ) -> ProductModel:
        response = self.product_service.get_product(access_token, product_id)        
        return ProductModel.model_validate(response)