from src.repo.interface.Iproduct_repo import IProductRepo
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.models.schemas.product.update_product_input import UpdateProductInput
from src.domain.schemas.product.product_model import ProductModel
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateProduct:
    
    def __init__(
        self,
        product_repo: IProductRepo,
        category_repo: ICategoryRepo,
    ):        
        self.product_repo = product_repo
        self.category_repo = category_repo
    
    async def execute(
        self,
        product: UpdateProductInput,
    ) -> ProductModel:
        
        if product.category_id:
            try:
                category: CategoryModel = await self.category_repo.get_category_by_id(product.category_id)
                product.category_id = category.id
            except AppBaseException:
                raise
        
        try:
            product = ProductModel.model_validate(product, from_attributes=True)
            return await self.product_repo.update_product(product)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")