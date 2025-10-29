from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.order.update_order_input import UpdateOrderInput
from src.gateway.internal.interface.Iorder_service import IOrderService
from src.routes.depends.internal_http_depend import order_service_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.usecases.user.order.update_order import UpdateOrder
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/update/one",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update_one_order(
    order: UpdateOrderInput = Query(None),
    order_service: IOrderService = Depends(order_service_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        update_order_usecase = UpdateOrder(order_service)
        output = await update_order_usecase.execute(user.credentials, order)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
