from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.infra.external_api.interface.Iorder_service import IOrderService
from src.routes.depends.external_api_services_depend import get_order_service
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.user.order.get_order import GetOrder
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/get/one",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_one_order(
    order_id: str,
    order_service: IOrderService = Depends(get_order_service),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_order_usecase = GetOrder(order_service)
        output = await get_order_usecase.execute(user.credentials, order_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
