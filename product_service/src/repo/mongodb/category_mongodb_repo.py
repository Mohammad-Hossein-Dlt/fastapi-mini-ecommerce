from src.repo.interface.Icategory_repo import ICategoryRepo
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.db.mongodb.collections.category_collection import CategoryCollection
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_id

class CategoryMongodbRepo(ICategoryRepo):
        
    async def insert_category(
        self,
        category: CategoryModel,
    ) -> CategoryModel:
        
        new_category = await CategoryCollection.insert(
            CategoryCollection(**category.model_dump(exclude={"id"})),
        )
        
        return CategoryModel.model_validate(new_category, from_attributes=True)
        
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
        
    async def get_child_to_parent(
        self,
        filter: CategoryFilterInput,
    ) ->  list[CategoryModel]:
        
        async def get_parent(
            parent_id: str | None = None,
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
        parent_id: str
    ) -> list[CategoryModel]:

        parent_id = convert_id(parent_id)
        
        categories_list = await CategoryCollection.find_many(
            CategoryCollection.parent_id == parent_id,
        ).to_list()
        
        return [ CategoryModel.model_validate(category, from_attributes=True) for category in categories_list ]
    
    async def get_category_by_id(
        self,
        category_id: str,
    ) ->  CategoryModel:
        
        try:
                                    
            category_id = convert_id(category_id)
            category = await CategoryCollection.find_one(
                CategoryCollection.id == category_id,
            )
            
            return CategoryModel.model_validate(category, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")
    
    async def update_category(
        self,
        category: CategoryModel,
    ) ->  CategoryModel:
        
        try:               
            
            to_update: dict = category.model_dump_to_update(exclude_unset=True, by_alias=True)     
            await CategoryCollection.find(
                CategoryCollection.id == category.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_category_by_id(category.id)
        except EntityNotFoundError:
            raise
    
    async def delete_all_categories(
        self,
    ) -> bool:
        try:
            delete_categories = await CategoryCollection.delete_all()
            return bool(delete_categories.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")
        
    async def delete_category(
        self,
        category_id: str,
    ) -> bool:
        
        try:
            category_id = convert_id(category_id)
            delete_category = await CategoryCollection.find(
                CategoryCollection.id == category_id,
            ).delete()                       
            return bool(delete_category.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")