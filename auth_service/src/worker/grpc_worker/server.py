from src.infra.context.context_manager import AppContextManager
from grpc import aio
import asyncio

from sharedlib.grpc.service.auth import auth_service_pb2_grpc
from sharedlib.grpc.service.auth import admin_service_pb2_grpc
from sharedlib.grpc.service.auth import user_service_pb2_grpc

from .auth import AuthServicer
from .admin import AdminServicer
from .user import UserServicer

async def init_server():
    
    server = aio.server()
    auth_service_pb2_grpc.add_IAuthServiceServicer_to_server(AuthServicer(), server)
    admin_service_pb2_grpc.add_IAdminServiceServicer_to_server(AdminServicer(), server)
    user_service_pb2_grpc.add_IUserServiceServicer_to_server(UserServicer(), server)
    
    AppContextManager.init_context()
    await AppContextManager.lazy_init_context()
    
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()
    
def run_server():
    asyncio.run(init_server())