from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.schemas.order.update_order_input import UpdateOrderInput
from src.usecases.user.order.update import UpdateOrder
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.routes.depends.repo_depend import user_order_repo_depend
from src.routes.depends.auth_depend import user_auth_depend
from src.dto.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update_one_order(
    entity: UpdateOrderInput = Query(...),
    order_repo: IOrderRepo = Depends(user_order_repo_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        update_order_usecase = UpdateOrder(order_repo)
        output = await update_order_usecase.execute(user, entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
