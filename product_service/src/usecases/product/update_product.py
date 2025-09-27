from src.repo.interface.Iproduct_repo import IProductRepo
from src.models.schemas.product.update_product_input import UpdateProductInput
from src.domain.schemas.product.product_model import ProductModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateProduct:
    
    def __init__(
        self,
        product_repo: IProductRepo,
    ):        
        self.product_repo = product_repo  
    
    async def execute(
        self,
        product: UpdateProductInput,
    ) -> ProductModel:
        
        try:
            product = ProductModel.model_validate(product, from_attributes=True)
            return await self.product_repo.update_product(product)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")