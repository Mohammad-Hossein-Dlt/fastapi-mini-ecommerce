from src.repo.interface.Iproduct_repo import IProductRepo
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.schemas.filter.product_filter_input import ProductFilterInput
from src.schemas.filter.category_filter_input import CategoryFilterInput
from src.dto.schemas.product.product_model import ProductModel
from src.dto.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetProducts:
    
    def __init__(
        self,
        product_repo: IProductRepo,
        category_repo: ICategoryRepo,
    ):        
        self.product_repo = product_repo
        self.category_repo = category_repo
    
    async def execute(
        self,
        criteria: ProductFilterInput,
    ) -> list[ProductModel]:
        
        try:
            products_list: list[ProductModel] = await self.product_repo.get_by_criteria(criteria)
            
            for product in products_list:
                category_filter = CategoryFilterInput(id=str(product.category_id), based_on="child-to-parent")
                categories_list: list[CategoryModel] = await self.category_repo.get_ancestors(category_filter)
                
                related_categories = []
                for category in categories_list:
                    related_categories.append(
                        category.model_dump(include={"id", "parent_id", "name"}, mode="json"),
                    )
                
                setattr(product, "related_categories", related_categories)
                
            return products_list
        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  