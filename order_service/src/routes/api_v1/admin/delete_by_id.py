from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.routes.depends.repo_depend import admin_order_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.delete_by_id import DeleteOrder
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_by_id(
    order_id: str,
    order_repo: IOrderRepo = Depends(admin_order_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        delete_order_usecase = DeleteOrder(order_repo)
        output = await delete_order_usecase.execute(order_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
