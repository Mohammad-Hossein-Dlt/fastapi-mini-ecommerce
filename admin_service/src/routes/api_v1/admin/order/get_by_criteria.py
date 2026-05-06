from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.gateway.internal.interface.Iorder_service import IOrderService
from src.routes.depends.internal_http_depend import order_service_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.get_by_criteria import GetOrders
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_criteria(
    criteria: FilterOrderInput = Query(...),
    order_service: IOrderService = Depends(order_service_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_all_orders_usecase = GetOrders(order_service)
        outputs_list = await get_all_orders_usecase.execute(user.credentials, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
