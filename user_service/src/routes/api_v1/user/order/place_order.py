from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.order.place_order_input import PlaceOrderInput
from src.gateway.internal.interface.Iorder_service import IOrderService
from src.routes.depends.internal_http_depend import order_service_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.usecases.user.order.place_order import PlaceOrder
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/place-order",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def place_order(
    order: PlaceOrderInput = Depends(PlaceOrderInput),
    order_service: IOrderService = Depends(order_service_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        place_order_usecase = PlaceOrder(order_service)
        output = await place_order_usecase.execute(user.credentials, order)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
