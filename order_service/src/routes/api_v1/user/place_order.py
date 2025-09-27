from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.order.place_order_input import PlaceOrderInput
from src.usecases.user.order.place_order import PlaceOrder
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.routes.depends.order_repo_depend import get_order_repo
from src.infra.external_api.interface.Iproduct_service import IProductService
from src.routes.depends.external_api_services_depend import get_product_service
from src.routes.depends.auth_depend import user_auth_depend
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/place-order",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create_order(
    order: PlaceOrderInput = Query(...),
    order_repo: IOrderRepo = Depends(get_order_repo),
    product_service: IProductService = Depends(get_product_service),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        place_order_usecase = PlaceOrder(order_repo, product_service)
        order = await place_order_usecase.execute(user.token, order, user.id)
        return order.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
