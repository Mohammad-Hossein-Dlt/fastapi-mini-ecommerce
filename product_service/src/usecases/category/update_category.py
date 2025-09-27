from src.repo.interface.Icategory_repo import ICategoryRepo
from src.models.schemas.category.update_category_input import UpdateCategoryInput
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateCategory:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
    ):        
        self.category_repo = category_repo  
    
    async def execute(
        self,
        category: UpdateCategoryInput,
    ) -> CategoryModel:
        
        try:
            category = CategoryModel.model_validate(category, from_attributes=True)
            return await self.category_repo.update_category(category)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")