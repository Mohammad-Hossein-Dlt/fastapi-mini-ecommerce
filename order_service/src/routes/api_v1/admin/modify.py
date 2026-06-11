from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.schemas.order.modify_order_input import ModifyOrderInput
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.routes.depends.repo_depend import admin_order_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.modify import ModifyOrder
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def modify(
    entity: ModifyOrderInput = Query(...),
    order_repo: IOrderRepo = Depends(admin_order_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        update_order_usecase = ModifyOrder(order_repo)
        output = await update_order_usecase.execute(entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
