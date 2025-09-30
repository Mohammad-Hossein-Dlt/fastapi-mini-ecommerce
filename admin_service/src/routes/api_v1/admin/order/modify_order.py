from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.order.modify_order_input import ModifyOrderInput
from src.infra.external_api.interface.Iorder_service import IOrderService
from src.routes.depends.external_api_services_depend import get_order_service
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.modify_order import AdminModifyOrder
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/modify/one",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def modify_one_order(
    order: ModifyOrderInput = Query(None),
    order_service: IOrderService = Depends(get_order_service),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        update_order_usecase = AdminModifyOrder(order_service)
        output = await update_order_usecase.execute(user.credentials, order)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
