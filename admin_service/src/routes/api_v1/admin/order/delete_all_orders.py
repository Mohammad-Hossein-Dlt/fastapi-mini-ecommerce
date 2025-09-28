from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.infra.external_api.interface.Iorder_service import IOrderService
from src.routes.depends.external_api_services_depend import get_order_service
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.delete_all_orders import AdminDeleteAllOrders
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/delete/all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_all_orders(
    filter_order: FilterOrderInput = Query(None),
    order_service: IOrderService = Depends(get_order_service),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        delete_all_order_usecase = AdminDeleteAllOrders(order_service)
        output = await delete_all_order_usecase.execute(user.credentials, filter_order)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
