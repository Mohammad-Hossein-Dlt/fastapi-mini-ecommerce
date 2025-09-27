from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.order.update_order_input import UpdateOrderInput
from src.usecases.user.order.update_order import UpdateOrder
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.routes.depends.order_repo_depend import get_order_repo
from src.routes.depends.auth_depend import user_auth_depend
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/update/one",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update_order(
    order: UpdateOrderInput = Query(...),
    order_repo: IOrderRepo = Depends(get_order_repo),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        update_order_usecase = UpdateOrder(order_repo)
        order = await update_order_usecase.execute(user.id, order)
        return order.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
