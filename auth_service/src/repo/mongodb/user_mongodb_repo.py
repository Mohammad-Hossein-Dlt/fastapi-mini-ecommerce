from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.infra.db.mongodb.collections.user_collection import UserCollection
from bson.objectid import ObjectId
from src.infra.exceptions.exceptions import EntityNotFoundError, InvalidRequestException

class UserMongodbRepo(IUserRepo):
            
    async def insert_user(
        self,
        user: UserModel,
    ) -> UserModel:
        
        try:
            await self.get_user_by_username(user.username)
            raise InvalidRequestException(400, f"User '{user.username}' already exist")
        except EntityNotFoundError:
            new_user = await UserCollection.insert(
                UserCollection(**user.model_dump(exclude={"id", "_id"})),
            )
            return UserModel.model_validate(new_user, from_attributes=True)
    
    async def get_user_by_id(
        self,
        user_id: str,
    ) ->  UserModel:
        try:
            user = await UserCollection.get(user_id)
            return UserModel.model_validate(user, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def get_user_by_username(
        self,
        username: str,
    ) -> UserModel:
        
        try:
            user = await UserCollection.find_one(
                UserCollection.username == username.strip(),
            )
            return UserModel.model_validate(user, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def delete_user_by_id(
        self,
        user_id: str,
    ) -> bool:
        try:
            result = await UserCollection.find(
                UserCollection.id == ObjectId(user_id),
            ).delete()
            
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def delete_user_by_username(
        self,
        username: str,
    ) -> bool:
        try:
            result = await UserCollection.find(
                UserCollection.username == username.strip(),
            ).delete()
            
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")