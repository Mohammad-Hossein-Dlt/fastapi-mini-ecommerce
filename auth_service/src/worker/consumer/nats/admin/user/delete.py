from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.repo.interface.Iuser_repo import IUserRepo
from src.worker.depends.repo_depend import user_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.admin.delete_user import DeleteUser
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "auth_service.admin.delete.user"

@client.broker.subscriber(
    subject=routing_key,
)
async def delete_user(
    user_id: str | None = None,
    username: str | None = None,
    user_repo: IUserRepo = Depends(user_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:        
        delete_user_usecase = DeleteUser(user_repo)
        output = await delete_user_usecase.execute(user_id, username)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()
