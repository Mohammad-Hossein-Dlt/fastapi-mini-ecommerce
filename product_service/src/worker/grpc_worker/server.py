from src.infra.context.context_manager import AppContextManager
from grpc import aio
import asyncio

from sharedlib.grpc.service.category import category_service_pb2_grpc
from sharedlib.grpc.service.product import product_service_pb2_grpc

from .category import CategoryServicer
from .product import ProductServicer

async def init_server():
    
    server = aio.server()
    category_service_pb2_grpc.add_ICategoryServiceServicer_to_server(CategoryServicer(), server)
    product_service_pb2_grpc.add_IProductServiceServicer_to_server(ProductServicer(), server)
    
    AppContextManager.init_context()
    await AppContextManager.lazy_init_context()
    
    server.add_insecure_port("[::]:50052")
    await server.start()
    await server.wait_for_termination()
    
def run_server():
    asyncio.run(init_server())