from src.repo.interface.Icategory_repo import ICategoryRepo
from src.schemas.filter.category_filter_input import CategoryFilterInput
from src.dto.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetCategories:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
    ):        
        self.category_repo = category_repo  
    
    async def execute(
        self,
        criteria: CategoryFilterInput,
    ) -> list[CategoryModel]:
        
        try:
            return await self.category_repo.get_by_criteria(criteria)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  