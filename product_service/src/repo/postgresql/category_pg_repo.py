from sqlalchemy.orm import Session
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.database.postgresql.models.category_db_model import CategoryDBModel
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.infra.utils.convert_id import convert_database_id
from src.infra.exceptions.exceptions import EntityNotFoundError, DuplicateEntityError

class CategoryPgRepo(ICategoryRepo):
    
    def __init__(
        self,
        db: Session,
    ):
        
        self.db = db
        
    async def create(
        self,
        category: CategoryModel,
    ) -> CategoryModel:
        
        try:
            await self.check_unique(category)
            raise DuplicateEntityError(409, "Category already exist")
        except EntityNotFoundError:
            new_category = CategoryDBModel(**category.model_dump_for_db())
            self.db.add(new_category)
            self.db.commit()
            return CategoryModel.model_validate(new_category, from_attributes=True)
        
    async def check_unique(
        self,
        category: CategoryModel,
    ) -> CategoryModel:
        
        try:
            category = self.db.query(
                CategoryDBModel   
            ).where(
                CategoryDBModel.name == category.name,
                CategoryDBModel.slug == category.slug,
            ).first()
            return CategoryModel.model_validate(category, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")
        
    async def get_by_id(
        self,
        category_id: str,
    ) -> CategoryModel:
        
        try:
            category_id = convert_database_id(category_id)
            category = self.db.query(
                CategoryDBModel   
            ).where(
                CategoryDBModel.id == category_id,
            ).first()
            
            return CategoryModel.model_validate(category, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")
        
    async def update(
        self,
        category: CategoryModel,
    ) -> CategoryModel:
        
        try:
            
            to_update: dict = category.model_dump_for_db(
                exclude_none=True,
                exclude_unset=True,
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
            
            return await self.get_by_id(category.id)
        except EntityNotFoundError:
            raise
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")
        
    async def delete_by_id(
        self,
        category_id: str,
    ) -> bool:
        
        try:
            
            category_id = convert_database_id(category_id)
            category = await self.get_by_id(category_id)                
            to_delete = self.db.merge(CategoryDBModel(**category.model_dump()))
                
            if isinstance(to_delete, CategoryDBModel):
                self.db.delete(to_delete)
                self.db.commit()
                return True
            
            return False            
        
        except EntityNotFoundError:
            raise
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")
        
    async def get_all(
        self,
    ) -> list[CategoryModel]:
        
        try:
            categories_list = await self.db.query().all()
            return [ CategoryModel.model_validate(category, from_attributes=True) for category in categories_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="Categories not found")
        
    async def get_by_criteria(
        self,
        criteria: CategoryFilterInput,
    ) -> list[CategoryModel]:
        
        try:
            if criteria.based_on == "parent-id":
                return await self.get_tree_from_parent(criteria)
            elif criteria.based_on == "child-to-parent":
                return await self.get_ancestors(criteria)
        except EntityNotFoundError:
            raise
        except:
            raise EntityNotFoundError(status_code=404, message="Categories not found")
        
    async def get_tree_from_parent(
        self,
        criteria: CategoryFilterInput,
    ) -> list[CategoryModel]:
        
        parents_list: list[CategoryModel] = await self.get_by_parent_id(criteria.id, criteria.contains_danglings)
            
        for parent in parents_list:
            children = await self.get_by_parent_id(parent.id, criteria.contains_danglings)
            
            if children:
                setattr(parent, "children", children)
                
        return parents_list
    
    async def get_ancestors(
        self,
        criteria: CategoryFilterInput,
    ) -> list[CategoryModel]:
        
        async def _get_ancestors(
            p_id: str | None = None,
        ) -> list[CategoryModel]:
            
            
            result: list[CategoryModel] = []
            if not p_id:
                return result
                          
            p_id = convert_database_id(p_id)
            category = await self.get_by_id(p_id)
            result.append(category)
            if category.parent_id:
                parent = await _get_ancestors(category.parent_id)
                result.extend(parent)
            
            return result
                        
        categories = await _get_ancestors(criteria.id)
        categories.reverse()
        return categories
    
    async def get_by_parent_id(
        self,
        parent_id: str | None = None,
        contains_danglings: bool = False,
    ) -> list[CategoryModel]:
        
        try:
            parent_id = convert_database_id(parent_id)
            if not parent_id and contains_danglings:
                categories_list = self.db.query(
                    CategoryDBModel
                ).where(
                    CategoryDBModel.parent_id == parent_id,
                    CategoryDBModel.parent_id == None,
                ).order_by(
                    CategoryDBModel.id.asc(),
                ).all()
            else:
                categories_list = self.db.query(
                    CategoryDBModel
                ).where(
                    CategoryDBModel.parent_id == parent_id,
                ).order_by(
                    CategoryDBModel.id.asc(),
                ).all()
                    
            return [ CategoryModel.model_validate(category, from_attributes=True) for category in categories_list ]
        except:
            raise EntityNotFoundError(status_code=404, message="Categories not found")

    async def get_descendants(
        self,
        parent_id: str,
    ) -> list[CategoryModel]:
        
        async def _get_descendants(
            p_id: str | None = None,
        ) -> list[CategoryModel]:
            
            result: list[CategoryModel] = []
            p_id = convert_database_id(p_id)
            categories = await self.get_by_parent_id(p_id)
                        
            for c in categories:
                result.append(c)
                if c and c.parent_id:
                    result.extend(await _get_descendants(c.id))

            return result
                
        return await _get_descendants(parent_id)
    
    async def delete_by_parent_id(
        self,
        parent_id: str,
    ) -> bool:
        try:
            parent_id = convert_database_id(parent_id)
            categories: list[CategoryModel] = await self.get_by_parent_id(parent_id)
            if categories:
                for record in categories:
                    record = self.db.merge(CategoryDBModel(**record.model_dump()))
                    if isinstance(record, CategoryDBModel):
                        self.db.delete(record)
                
                self.db.commit()        
                return True 

            return False
        except:
            raise EntityNotFoundError(status_code=404, message="Categories not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            
            try:
                categories: list[CategoryModel] = await self.get_by_parent_id(None)
            except:
                return False
                        
            if categories:
                for record in categories:
                    record = self.db.merge(CategoryDBModel(**record.model_dump()))
                    if isinstance(record, CategoryDBModel):
                        self.db.delete(record)
                
                self.db.commit()        
                return True 

            return False

        except EntityNotFoundError:
            raise
        except:
            raise EntityNotFoundError(status_code=404, message="There are no categories")
