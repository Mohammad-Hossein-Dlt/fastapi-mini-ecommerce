from src.infra.context.context_manager import AppContextManager
from grpc import aio
import asyncio

from sharedlib.grpc.service.order import admin_order_service_pb2_grpc
from sharedlib.grpc.service.order import user_order_service_pb2_grpc

from .admin_order import AdminOrderServicer
from .user_order import UserOrderServicer

async def init_server():
    
    server = aio.server()
    admin_order_service_pb2_grpc.add_IOrderServiceServicer_to_server(AdminOrderServicer(), server)
    user_order_service_pb2_grpc.add_IOrderServiceServicer_to_server(UserOrderServicer(), server)
    
    AppContextManager.init_context()
    await AppContextManager.lazy_init_context()
    
    server.add_insecure_port("[::]:50053")
    await server.start()
    await server.wait_for_termination()
    
def run_server():
    asyncio.run(init_server())