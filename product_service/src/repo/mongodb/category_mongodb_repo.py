from src.repo.interface.Icategory_repo import ICategoryRepo
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.db.mongodb.collections.task_collection import TaskCollection
from bson.objectid import ObjectId
from beanie.operators import And
from src.infra.exceptions.exceptions import EntityNotFoundError

class TaskMongodbRepo(ICategoryRepo):
        
    async def insert_task(
        self,
        task: CategoryModel,
    ) -> CategoryModel:
        new_task = await TaskCollection.insert(
            TaskCollection(**task.model_dump(exclude={"id"})),
        )
        
        return CategoryModel.model_validate(new_task, from_attributes=True)
    
    async def get_all_tasks(
        self,
        user_id: str,
    ) ->  list[CategoryModel]:
        
        try:
            tasks = await TaskCollection.find(
                TaskCollection.user_id == ObjectId(user_id),
            ).to_list()
            
            return [ CategoryModel.model_validate(t, from_attributes=True) for t in tasks ]
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def get_task_by_id(
        self,
        task_id: str,
        user_id: str,
    ) ->  CategoryModel:
        
        try:
            task = await TaskCollection.find_one(
                TaskCollection.id == ObjectId(task_id),
                TaskCollection.user_id == ObjectId(user_id),
            )
            return CategoryModel.model_validate(task, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User or task not found")
    
    async def update_task(
        self,
        task: CategoryModel,
    ) ->  CategoryModel:
        
        try:
            await TaskCollection.find_one(
                And(
                    TaskCollection.id == ObjectId(task.id),
                    TaskCollection.user_id == ObjectId(task.user_id),
                )
            ).update(
                {
                    "$set": task.model_dump(exclude_unset=True, exclude_none=True, exclude={"id", "user_id"}),
                },
            )
            
            return await self.get_task_by_id(task.id, task.user_id)
        except:
            raise EntityNotFoundError(status_code=404, message="User or task not found")
    
    async def delete_all_task(
        self,
        user_id: str,
    ) -> bool:
        
        try:
            tasks = TaskCollection.find(
                TaskCollection.user_id == ObjectId(user_id),
            )                
            
            delete_tasks = await tasks.delete()
            
            return bool(delete_tasks.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def delete_task(
        self,
        task_id: str,
        user_id: str,
    ) -> bool:
        
        try:
            task = TaskCollection.find(
                TaskCollection.id == ObjectId(task_id),
                TaskCollection.user_id == ObjectId(user_id),
            )                
            
            delete_task = await task.delete()
            
            return bool(delete_task.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="User or task not found")