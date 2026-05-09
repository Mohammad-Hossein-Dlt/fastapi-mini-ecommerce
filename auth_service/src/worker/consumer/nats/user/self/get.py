from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import user_auth_depend
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "auth_service.user.get.self"

@client.broker.subscriber(
    subject=routing_key,
)
async def get_self(
    user: UserModel = Depends(user_auth_depend),
):
    try:
        return user.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()
