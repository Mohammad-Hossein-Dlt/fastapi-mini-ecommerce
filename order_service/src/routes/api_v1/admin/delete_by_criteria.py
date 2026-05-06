from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.routes.depends.repo_depend import admin_order_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.delete_by_criteria import DeleteOrders
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_by_criteria(
    criteria: FilterOrderInput = Query(None),
    order_repo: IOrderRepo = Depends(admin_order_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        delete_all_order_usecase = DeleteOrders(order_repo)
        output = await delete_all_order_usecase.execute(criteria)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
