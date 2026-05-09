from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.worker.depends.auth_depend import jwt_handler_depend, refresh_token_depend
from src.infra.auth.jwt_handler import JWTHandler
from src.domain.schemas.user.user_model import UserModel
from src.usecases.auth.refresh_token import RefreshToken
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "auth_service.auth.refresh-token"

@client.broker.subscriber(
    subject=routing_key,
)
async def refresh_token(
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user: UserModel = Depends(refresh_token_depend),
):
    try:        
        refresh_token_usecase = RefreshToken(jwt_handler)
        output = await refresh_token_usecase.execute(user)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()
