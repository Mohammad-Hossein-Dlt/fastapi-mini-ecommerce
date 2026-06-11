from grpc import aio
from google.protobuf.json_format import MessageToDict

from sharedlib.grpc.service.order import user_order_service_pb2, user_order_service_pb2_grpc

from src.worker.depends.depend import Depends, inject

from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.worker.depends.repo_depend import user_order_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import user_auth_depend

from src.schemas.order.place_order_input import PlaceOrderInput
from src.schemas.filter.order_filter_input import OrderFilterInput

from src.schemas.order.update_order_input import UpdateOrderInput
from src.usecases.user.order.place_order import PlaceOrder
from src.usecases.user.order.get_by_id import GetOrder
from src.usecases.user.order.update import UpdateOrder
from src.usecases.user.order.get_by_criteria import GetOrders

from src.infra.utils.grpc_status_code import rest_to_grpc_status
from src.infra.exceptions.exceptions import AppBaseException

class UserOrderServicer(user_order_service_pb2_grpc.IOrderService):
    
    @inject(cast=False)
    async def place_order(
        self,
        request: user_order_service_pb2.PlaceOrderInput,
        context: aio.ServicerContext,
        order_repo: IOrderRepo = Depends(user_order_repo_depend),
        user: UserModel = Depends(user_auth_depend),
    ):
        try:
            entity = PlaceOrderInput.model_validate(MessageToDict(request, preserving_proto_field_name=True), from_attributes=True)
            get_order_usecase = PlaceOrder(order_repo)
            output = await get_order_usecase.execute(user, entity)
            response = output.model_dump(mode="json")
            return user_order_service_pb2.PlaceOrderResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
    
    @inject(cast=False)
    async def get_by_id(
        self,
        request: user_order_service_pb2.GetByIdRequest,
        context: aio.ServicerContext,
        order_repo: IOrderRepo = Depends(user_order_repo_depend),
        user: UserModel = Depends(user_auth_depend),
    ):
        try:
            get_order_usecase = GetOrder(order_repo)
            output = await get_order_usecase.execute(user, request.order_id)
            response = output.model_dump(mode="json")
            return user_order_service_pb2.GetByIdResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
                
    @inject(cast=False)
    async def update(
        self,
        request: user_order_service_pb2.UpdateOrderInput,
        context: aio.ServicerContext,
        order_repo: IOrderRepo = Depends(user_order_repo_depend),
        user: UserModel = Depends(user_auth_depend),
    ):
        try:
            entity = UpdateOrderInput.model_validate(MessageToDict(request, preserving_proto_field_name=True), from_attributes=True)
            update_order_usecase = UpdateOrder(order_repo)
            output = await update_order_usecase.execute(user, entity)
            response = output.model_dump(mode="json")
            return user_order_service_pb2.UpdateResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
            
    @inject(cast=False)
    async def get_by_criteria(
        self,
        request: user_order_service_pb2.OrderFilterInput,
        context: aio.ServicerContext,
        order_repo: IOrderRepo = Depends(user_order_repo_depend),
        user: UserModel = Depends(user_auth_depend),
    ):
        try:
            criteria = OrderFilterInput.model_validate(MessageToDict(request, preserving_proto_field_name=True), from_attributes=True)
            get_all_orders_usecase = GetOrders(order_repo)
            outputs_list = await get_all_orders_usecase.execute(user, criteria)
            response = [ output.model_dump(mode="json") for output in outputs_list ]
            return user_order_service_pb2.GetByCriteriaResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)