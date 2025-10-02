from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.user.order.get_order import GetOrder
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.routes.depends.order_repo_depend import get_user_order_repo
from src.routes.depends.auth_depend import user_auth_depend
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/get/one",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_one_order(
    order_id: str = Query(...),
    order_repo: IOrderRepo = Depends(get_user_order_repo),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_order_usecase = GetOrder(order_repo)
        output = await get_order_usecase.execute(order_id, user.id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
