from src.repo.interface.Iproduct_repo import IProductRepo
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.models.schemas.filter.products_filter_input import ProductFilterInput
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.domain.schemas.product.product_model import ProductModel
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllProducts:
    
    def __init__(
        self,
        product_repo: IProductRepo,
        category_repo: ICategoryRepo,
    ):        
        self.product_repo = product_repo
        self.category_repo = category_repo
    
    async def execute(
        self,
        product_filter: ProductFilterInput,
    ) -> list[ProductModel]:
        
        try:
            products_list: list[ProductModel] = await self.product_repo.get_all_products(product_filter)
            
            for product in products_list:
                category_filter = CategoryFilterInput(id=product.category_id, based_on="child-to-parent")
                categories_list: list[CategoryModel] = await self.category_repo.get_child_to_parent(category_filter)
                
                related_categories = []
                for category in categories_list:
                    related_categories.append(
                        {
                            "id": category.id,
                            "parent_id": category.parent_id,
                            "name": category.name,
                        }
                    )
                
                setattr(product, "related_categories", related_categories)
                
            return products_list
        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  