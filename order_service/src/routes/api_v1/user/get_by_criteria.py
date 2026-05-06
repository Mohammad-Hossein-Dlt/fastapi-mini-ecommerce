from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.order_filter_input import OrderFilterInput
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.routes.depends.repo_depend import user_order_repo_depend
from src.domain.schemas.user.user_model import UserModel
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
    order_repo: IOrderRepo = Depends(user_order_repo_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_all_orders_usecase = GetOrders(order_repo)
        outputs_list = await get_all_orders_usecase.execute(user, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
