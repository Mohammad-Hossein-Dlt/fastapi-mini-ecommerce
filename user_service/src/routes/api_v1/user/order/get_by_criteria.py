from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.schemas.filter.order_filter_input import OrderFilterInput
from src.gateway.internal.interface.Iorder_service import IOrderService
from src.routes.depends.internal_service_depend import order_service_depend
from src.dto.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.usecases.user.order.get_by_criteria import GetOrders
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_criteria(
    criteria: OrderFilterInput = Query(...),
    order_service: IOrderService = Depends(order_service_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_orders_usecase = GetOrders(order_service)
        outputs_list = await get_orders_usecase.execute(user.credentials, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
