from grpc import aio
from google.protobuf.json_format import MessageToDict

from sharedlib.grpc.service.order import admin_order_service_pb2, admin_order_service_pb2_grpc

from src.worker.depends.depend import Depends, inject

from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.worker.depends.repo_depend import admin_order_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend

from src.schemas.order.modify_order_input import ModifyOrderInput
from src.schemas.filter.order_filter_input import OrderFilterInput
from src.usecases.admin.order.get_by_id import GetOrder
from src.usecases.admin.order.modify import ModifyOrder
from src.usecases.admin.order.delete_by_id import DeleteOrder
from src.usecases.admin.order.get_by_criteria import GetOrders
from src.usecases.admin.order.delete_by_criteria import DeleteOrders

from src.infra.utils.grpc_status_code import rest_to_grpc_status
from src.infra.exceptions.exceptions import AppBaseException

class AdminOrderServicer(admin_order_service_pb2_grpc.IOrderService):
    
    @inject(cast=False)
    async def get_by_id(
        self,
        request: admin_order_service_pb2.GetByIdRequest,
        context: aio.ServicerContext,
        order_repo: IOrderRepo = Depends(admin_order_repo_depend),
        user: UserModel = Depends(admin_auth_depend),
    ):
        try:
            get_order_usecase = GetOrder(order_repo)
            output = await get_order_usecase.execute(request.order_id)
            response = output.model_dump(mode="json")
            return admin_order_service_pb2.GetByIdResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
    
    @inject(cast=False)
    async def modify(
        self,
        request: admin_order_service_pb2.ModifyOrderInput,
        context: aio.ServicerContext,
        order_repo: IOrderRepo = Depends(admin_order_repo_depend),
        user: UserModel = Depends(admin_auth_depend),
    ):
        try:
            entity = ModifyOrderInput.model_validate(MessageToDict(request, preserving_proto_field_name=True), from_attributes=True)
            update_order_usecase = ModifyOrder(order_repo)
            output = await update_order_usecase.execute(entity)
            response = output.model_dump(mode="json")
            return admin_order_service_pb2.ModifyResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
                
    @inject(cast=False)
    async def delete_by_id(
        self,
        request: admin_order_service_pb2.DeleteByIdRequest,
        context: aio.ServicerContext,
        order_repo: IOrderRepo = Depends(admin_order_repo_depend),
        user: UserModel = Depends(admin_auth_depend),
    ):
        try:
            delete_order_usecase = DeleteOrder(order_repo)
            output = await delete_order_usecase.execute(request.order_id)
            response = output.model_dump(mode="json")
            return admin_order_service_pb2.DeleteByIdResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
            
    @inject(cast=False)
    async def get_by_criteria(
        self,
        request: admin_order_service_pb2.OrderFilterInput,
        context: aio.ServicerContext,
        order_repo: IOrderRepo = Depends(admin_order_repo_depend),
        user: UserModel = Depends(admin_auth_depend),
    ):
        try:
            criteria = OrderFilterInput.model_validate(MessageToDict(request, preserving_proto_field_name=True), from_attributes=True)
            get_all_orders_usecase = GetOrders(order_repo)
            outputs_list = await get_all_orders_usecase.execute(criteria)
            response = [ output.model_dump(mode="json") for output in outputs_list ]
            return admin_order_service_pb2.GetByCriteriaResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
            
    @inject(cast=False)
    async def delete_by_criteria(
        self,
        request: admin_order_service_pb2.OrderFilterInput,
        context: aio.ServicerContext,
        order_repo: IOrderRepo = Depends(admin_order_repo_depend),
        user: UserModel = Depends(admin_auth_depend),
    ):
        try:
            criteria = OrderFilterInput.model_validate(MessageToDict(request, preserving_proto_field_name=True), from_attributes=True)
            delete_all_order_usecase = DeleteOrders(order_repo)
            output = await delete_all_order_usecase.execute(criteria)
            response = output.model_dump(mode="json")
            return admin_order_service_pb2.DeleteByCriteriaResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)