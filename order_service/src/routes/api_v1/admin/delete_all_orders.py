from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.usecases.admin.order.delete_all_orders import DeleteAllOrders
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.routes.depends.order_repo_depend import get_admin_order_repo
from src.routes.depends.auth_depend import admin_auth_depend
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/delete/all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_all_order(
    filter_order: FilterOrderInput = Query(None),
    order_repo: IOrderRepo = Depends(get_admin_order_repo),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        delete_all_order_usecase = DeleteAllOrders(order_repo)
        output = await delete_all_order_usecase.execute(filter_order)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
