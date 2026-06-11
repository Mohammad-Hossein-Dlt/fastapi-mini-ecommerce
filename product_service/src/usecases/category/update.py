from src.repo.interface.Icategory_repo import ICategoryRepo
from src.schemas.category.update_category_input import UpdateCategoryInput
from src.dto.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, EntityNotFoundError, InvalidRequestException, OperationFailureException

class UpdateCategory:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
    ):        
        self.category_repo = category_repo  
    
    async def execute(
        self,
        entity: UpdateCategoryInput,
    ) -> CategoryModel:
                        
        try:
            if entity.parent_id and entity.parent_id != entity.id:
                try:
                    parent: CategoryModel = await self.category_repo.get_by_id(entity.parent_id)
                    entity.parent_id = parent.id
                except EntityNotFoundError as ex:
                    raise EntityNotFoundError(ex.status_code, "Parent not found")
            elif entity.parent_id == entity.id:
                    raise InvalidRequestException(400, "Parent-id cannot be equal to id")
            
            category_model = CategoryModel.model_validate(entity, from_attributes=True)
            return await self.category_repo.update(category_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")