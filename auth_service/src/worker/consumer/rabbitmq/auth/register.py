from faststream import Depends
from faststream.rabbit import RabbitMessage
from src.worker.consumer.rabbitmq.broker import subscriber
from src.worker.depends.rabbitmq_depend import target_routing_key
from src.models.schemas.user.create_user_input import CreateUserInput
from src.repo.interface.Iuser_repo import IUserRepo
from src.worker.depends.user_repo_depend import user_repo_depend
from src.usecases.auth.register import RegisterUser
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "auth_service.auth.register"

@subscriber(
    filter=target_routing_key(routing_key),
)
async def register(
    msg: RabbitMessage,
    user_data: CreateUserInput,
    user_repo: IUserRepo = Depends(user_repo_depend),
):
    try:
        create_user_usecase = RegisterUser(user_repo)
        output = await create_user_usecase.execute(user_data)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()
