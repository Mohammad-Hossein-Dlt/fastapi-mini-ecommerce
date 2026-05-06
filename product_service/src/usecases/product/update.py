from src.repo.interface.Iproduct_repo import IProductRepo
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.models.schemas.product.update_product_input import UpdateProductInput
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
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
        entity: UpdateProductInput,
    ) -> ProductModel:
                
        try:
            
            if entity.category_id:
                await self.category_repo.get_by_id(entity.category_id)
            
            product_model = ProductModel.model_validate(entity, from_attributes=True)
            product: ProductModel = await self.product_repo.update(product_model)

            categories_list = []
            if product.category_id:
                category_filter = CategoryFilterInput(id=str(product.category_id), based_on="child-to-parent")
                categories_list: list[CategoryModel] = await self.category_repo.get_ancestors(category_filter)
            
            related_categories = []
            for category in categories_list:
                related_categories.append(
                    category.model_dump(include={"id", "parent_id", "name"}, mode="json"),
                )
            
            setattr(product, "related_categories", related_categories)
            return product
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")