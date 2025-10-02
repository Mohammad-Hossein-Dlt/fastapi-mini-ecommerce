from sqlalchemy.orm import Session
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.db.postgresql.models.category_db_model import CategoryDBModel
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.infra.exceptions.exceptions import EntityNotFoundError

class CategoryPgRepo(ICategoryRepo):
    
    def __init__(
        self,
        db: Session,
    ):
        
        self.db = db
        
    async def insert_category(
        self,
        category: CategoryModel,
    ) -> CategoryModel:
        try:
            new_category = CategoryDBModel(**category.model_dump(exclude_none=True))
            self.db.add(new_category)
            self.db.commit()

            return CategoryModel.model_validate(new_category, from_attributes=True)
        except:
            self.db.rollback()
            raise

    async def get_categories_with_filter(
        self,
        filter: CategoryFilterInput,
    ) ->  list[CategoryModel]:
        
        try:
            if filter.based_on == "parent-id":
                return await self.get_parent_to_child(filter)
            elif filter.based_on == "child-to-parent":
                return await self.get_child_to_parent(filter)
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no categories")
        except:
            self.db.rollback()
        
    async def get_child_to_parent(
        self,
        filter: CategoryFilterInput,
    ) ->  list[CategoryModel]:
        
        async def get_parent(
            parent_id: int | None = None,
        ) -> CategoryModel | None:
            try:
                return await self.get_category_by_id(parent_id)
            except:
                return None
        
        async def get_categories(
            category: CategoryModel = None,
        ) -> list[CategoryModel]:
                                 
            result: list[CategoryModel] = []
            
            if not category:
                category = await get_parent(filter.id)
            
            if not category:
                return result    
                        
            result.append(category)
                            
            parent = await get_parent(category.parent_id)

            if parent and parent.parent_id:
                result.extend( await get_categories(parent) )
                return result
            elif parent:
                result.append(parent)
                return result
            else:
                return result
                
        categories = await get_categories()
        categories.reverse()
        
        return categories
    
    async def get_parent_to_child(
        self,
        filter: CategoryFilterInput,
    ) -> list[CategoryModel]:
        
        parents_list = await self.get_categories_with_parent_id(filter.id)
            
        for parent in parents_list:
            children = await self.get_categories_with_parent_id(parent.id)
            
            if children:
                setattr(parent, "children", children)
                
        return parents_list
                    
    async def get_categories_with_parent_id(
        self,
        parent_id: int,
    ) -> list[CategoryModel]:
        
        try:
            categories_list = self.db.query(
                CategoryDBModel
            ).where(
                CategoryDBModel.parent_id == parent_id,
            ).order_by(
                CategoryDBModel.id.asc(),
            ).all()
            
            return [ CategoryModel.model_validate(category, from_attributes=True) for category in categories_list ]
        except:
            self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="There are no categories")
    
    async def get_category_by_id(
        self,
        category_id: int,
    ) ->  CategoryModel:
        
        try:
            category = self.db.query(
                CategoryDBModel   
            ).where(
                CategoryDBModel.id == category_id,
            ).first()
            
            return CategoryModel.model_validate(category, from_attributes=True)
        except:
            self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="Category not found")
    
    async def update_category(
        self,
        category: CategoryModel,
    ) ->  CategoryModel:
        
        try:
            
            to_update: dict = category.custom_model_dump(
                exclude_unset=True,
                exclude={
                    "id",
                },
                db_stack="sql",
            )
 
            self.db.query(
                CategoryDBModel   
            ).where(
                CategoryDBModel.id == category.id
            ).update(
                to_update,
                synchronize_session='fetch',
            )
            
            self.db.commit()
            
            return await self.get_category_by_id(category.id)
        except EntityNotFoundError:
            raise
        except:
            self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="Category not found")
    
    async def delete_all_categories(
        self,
    ) -> bool:
        try:
            categories: list[CategoryModel] = await self.get_categories_with_parent_id(parent_id=None)
            if categories:
                for record in categories:
                    record = self.db.merge(CategoryDBModel(**record.model_dump(exclude={"children"})))
                    if isinstance(record, CategoryDBModel):
                        self.db.delete(record)
                
                self.db.commit()        
                return True 
            else:
                return False
        except EntityNotFoundError:
            raise
        except:
            self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="There are no categories")
        
    async def delete_category(
        self,
        category_id: int,
    ) -> bool:
        
        try:
            category = await self.get_category_by_id(category_id)
            if category:
                category = self.db.merge(CategoryDBModel(**category.model_dump()))
                
            if isinstance(category, CategoryDBModel):
                self.db.delete(category)
                self.db.commit()
                return True
            else:
                return False
        except EntityNotFoundError:
            raise
        except:
            self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="Category not found")