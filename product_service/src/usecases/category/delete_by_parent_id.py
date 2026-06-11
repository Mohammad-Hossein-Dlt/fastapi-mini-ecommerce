from src.repo.interface.Icategory_repo import ICategoryRepo
from src.schemas.operation.operation_output import OperationOutput
from src.dto.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteCategories:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
    ):        
        
        self.category_repo = category_repo   
    
    async def execute(
        self,
        parent_id: str,
    ) -> OperationOutput:
        
        try:
            categories: list[CategoryModel] = await self.category_repo.get_descendants(parent_id)
            status = True if categories else False
            for c in categories:
                result = await self.category_repo.delete_by_id(c.id)
                if not result:
                    status = False

            return OperationOutput(id=None, request="delete/categories-by-parent-id", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  