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
        product: UpdateProductInput,
    ) -> ProductModel:
        
        categories_list = []
        if product.category_id:
            try:
                categories_list: list[CategoryModel] = await self.category_repo.get_child_to_parent(
                    CategoryFilterInput(
                        id=product.category_id,
                        based_on="child-to-parent",
                    ),
                )
            except AppBaseException:
                raise
        
        try:
            to_update = ProductModel.model_validate(product, from_attributes=True)
            product = await self.product_repo.update_product(to_update)
            
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