from src.repo.interface.Icategory_repo import ICategoryRepo
from src.models.schemas.category.create_category_input import CreateCategoryInput
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateCategory:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
    ):        
        self.category_repo = category_repo
    
    async def execute(
        self,
        category: CreateCategoryInput,
    ) -> CategoryModel:
        try:
            category = CategoryModel.model_validate(category, from_attributes=True)
            return await self.category_repo.insert_category(category)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  