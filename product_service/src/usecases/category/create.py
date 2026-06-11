from src.repo.interface.Icategory_repo import ICategoryRepo
from src.schemas.category.create_category_input import CreateCategoryInput
from src.dto.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, EntityNotFoundError, OperationFailureException

class CreateCategory:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
    ):        
        self.category_repo = category_repo
    
    async def execute(
        self,
        entity: CreateCategoryInput,
    ) -> CategoryModel:
        
        try:    
            if entity.parent_id:
                try:
                    parent: CategoryModel = await self.category_repo.get_by_id(entity.parent_id)
                    entity.parent_id = parent.id
                except EntityNotFoundError as ex:
                    raise EntityNotFoundError(ex.status_code, "Parent not found")
            
            category_model = CategoryModel.model_validate(entity, from_attributes=True)
            return await self.category_repo.create(category_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  