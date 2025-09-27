from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.admin.order.delete_order import DeleteOrder
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.routes.depends.order_repo_depend import get_admin_order_repo
from src.routes.depends.auth_depend import admin_auth_depend
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/delete/one",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_order(
    order_id: str,
    order_repo: IOrderRepo = Depends(get_admin_order_repo),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        delete_order_usecase = DeleteOrder(order_repo)
        output = await delete_order_usecase.execute(order_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
