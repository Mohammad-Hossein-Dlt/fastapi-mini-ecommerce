from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.infra.external_api.interface.Iorder_service import IOrderService
from src.routes.depends.external_api_services_depend import get_order_service
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.get_all_orders import AdminGetAllOrders
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/get/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_all_orders(
    filter_order: FilterOrderInput = Query(None),
    order_service: IOrderService = Depends(get_order_service),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_all_orders_usecase = AdminGetAllOrders(order_service)
        outputs_list = await get_all_orders_usecase.execute(user.credentials, filter_order)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
