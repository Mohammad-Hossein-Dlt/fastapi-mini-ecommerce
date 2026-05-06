from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.order.place_order_input import PlaceOrderInput
from src.usecases.user.order.place_order import PlaceOrder
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.routes.depends.repo_depend import user_order_repo_depend
from src.gateway.internal.interface.Iproduct_service import IProductService
from src.routes.depends.internal_http_depend import product_service_depend
from src.routes.depends.auth_depend import user_auth_depend
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def place_order(
    entity: PlaceOrderInput = Query(...),
    order_repo: IOrderRepo = Depends(user_order_repo_depend),
    product_service: IProductService = Depends(product_service_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        place_order_usecase = PlaceOrder(order_repo, product_service)
        output = await place_order_usecase.execute(user, entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
