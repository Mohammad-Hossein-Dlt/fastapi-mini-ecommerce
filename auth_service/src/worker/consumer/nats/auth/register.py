from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.models.schemas.user.create_user_input import CreateUserInput
from src.repo.interface.Iuser_repo import IUserRepo
from src.worker.depends.repo_depend import user_repo_depend
from src.usecases.auth.register import RegisterUser
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "auth_service.auth.register"

@client.broker.subscriber(
    subject=routing_key,
)
async def register(
    entity: CreateUserInput,
    user_repo: IUserRepo = Depends(user_repo_depend),
):
    try:
        create_user_usecase = RegisterUser(user_repo)
        output = await create_user_usecase.execute(entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()
