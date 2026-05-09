from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.models.schemas.user.login_user_input import LoginUserInput
from src.worker.depends.auth_depend import jwt_handler_depend, user_repo_depend
from src.infra.auth.jwt_handler import JWTHandler
from src.repo.interface.Iuser_repo import IUserRepo
from src.usecases.auth.login import LoginUser
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "auth_service.auth.login"

@client.broker.subscriber(
    subject=routing_key,
)
async def login(
    form_data: LoginUserInput,
    user_repo: IUserRepo = Depends(user_repo_depend),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
):
    try:
        login_user_usecase = LoginUser(user_repo, jwt_handler)
        output = await login_user_usecase.execute(form_data)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()
