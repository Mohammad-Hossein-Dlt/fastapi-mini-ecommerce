from sqlalchemy.orm import Session
from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.infra.db.postgresql.models.user_db_model import UserDBModel
from src.infra.exceptions.exceptions import EntityNotFoundError, InvalidRequestException

class UserPgRepo(IUserRepo):
    
    def __init__(
        self,
        db: Session,
    ):
        
        self.db = db
            
    async def insert_user(
        self,
        user: UserModel,
    ) -> UserModel:
        
        try:
            await self.get_user_by_username(user.username)
            raise InvalidRequestException(409, f"User '{user.username}' already exist")
        except EntityNotFoundError:
            try:
                user = UserDBModel(**user.model_dump())
                self.db.add(user)
                self.db.commit()
                return UserModel.model_validate(user, from_attributes=True)
            except:
                # self.db.rollback()
                raise
    
    async def get_user_by_id(
        self,
        user_id: str,
    ) ->  UserModel:
        
        try:
            user = self.db.query(
                UserDBModel   
            ).where(
                UserDBModel.id == int(user_id),
            ).first()

            return UserModel.model_validate(user, from_attributes=True)
        except:
            # self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def get_user_by_username(
        self,
        username: str,
    ) -> UserModel:
        
        try:
            user = self.db.query(
                UserDBModel   
            ).where(
                UserDBModel.username == username.strip(),
            ).first()
            
            return UserModel.model_validate(user, from_attributes=True)
        except:
            # self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def delete_user_by_id(
        self,
        user_id: str,
    ) -> bool:
        
        try:
            user = await self.get_user_by_id(user_id)
            if user:
                user = self.db.merge(UserDBModel(**user.model_dump()))

            if isinstance(user, UserDBModel):
                self.db.delete(user)
                self.db.commit()
                return True
            
            return False
        except EntityNotFoundError:
            raise
        except:
            # self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def delete_user_by_username(
        self,
        username: str,
    ) -> bool:
        
        try:
            user = await self.get_user_by_username(username)
            if user:
                user = self.db.merge(UserDBModel(**user.model_dump()))

            if isinstance(user, UserDBModel):
                self.db.delete(user)
                self.db.commit()
                return True
            
            return False
        except EntityNotFoundError:
            raise
        except:
            # self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="User not found")
            