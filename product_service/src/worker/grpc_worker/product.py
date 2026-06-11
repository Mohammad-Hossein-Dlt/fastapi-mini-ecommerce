from grpc import aio
from google.protobuf.empty_pb2 import Empty
from google.protobuf.json_format import MessageToDict

from sharedlib.grpc.service.product import product_service_pb2
from sharedlib.grpc.service.product import product_service_pb2_grpc

from src.worker.depends.depend import Depends, inject

from src.repo.interface.Iproduct_repo import IProductRepo
from src.worker.depends.repo_depend import product_repo_depend
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.worker.depends.repo_depend import category_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend, user_auth_depend

from src.schemas.product.create_product_input import CreateProductInput
from src.schemas.product.update_product_input import UpdateProductInput
from src.schemas.filter.product_filter_input import ProductFilterInput
from src.usecases.product.create import CreateProduct
from src.usecases.product.get_by_id import GetProduct
from src.usecases.product.update import UpdateProduct
from src.usecases.product.delete_by_id import DeleteProduct
from src.usecases.product.get_by_criteria import GetProducts
from src.usecases.product.delete_all import DeleteProducts

from src.infra.utils.grpc_status_code import rest_to_grpc_status
from src.infra.exceptions.exceptions import AppBaseException

class ProductServicer(product_service_pb2_grpc.IProductService):
    
    @inject(cast=False)
    async def create(
        self,
        request: product_service_pb2.CreateProductInput,
        context: aio.ServicerContext,
        product_repo: IProductRepo = Depends(product_repo_depend),
        category_repo: ICategoryRepo = Depends(category_repo_depend),
        user: UserModel = Depends(admin_auth_depend),
    ):
        try:
            entity = CreateProductInput.model_validate(MessageToDict(request, preserving_proto_field_name=True), from_attributes=True)
            create_product_usecase = CreateProduct(product_repo, category_repo)
            output = await create_product_usecase.execute(entity)
            response = output.model_dump(mode="json")
            return product_service_pb2.CreateResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
    
    @inject(cast=False)
    async def get_by_id(
        self,
        request: product_service_pb2.GetByIdRequest,
        context: aio.ServicerContext,
        product_repo: IProductRepo = Depends(product_repo_depend),
        category_repo: ICategoryRepo = Depends(category_repo_depend),
        user: UserModel = Depends(user_auth_depend),
    ):
        try:
            get_product_usecase = GetProduct(product_repo, category_repo)
            output = await get_product_usecase.execute(request.product_id)
            response = output.model_dump(mode="json")
            return product_service_pb2.GetByIdResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
    
    @inject(cast=False)
    async def update(
        self,
        request: product_service_pb2.UpdateProductInput,
        context: aio.ServicerContext,
        product_repo: IProductRepo = Depends(product_repo_depend),
        category_repo: ICategoryRepo = Depends(category_repo_depend),
        user: UserModel = Depends(admin_auth_depend),
    ):
        try:
            entity = UpdateProductInput.model_validate(MessageToDict(request, preserving_proto_field_name=True), from_attributes=True)
            update_product_usecase = UpdateProduct(product_repo, category_repo)
            output = await update_product_usecase.execute(entity)
            response = output.model_dump(mode="json")
            return product_service_pb2.UpdateResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
    
    @inject(cast=False)
    async def delete_by_id(
        self,
        request: product_service_pb2.DeleteByIdRequest,
        context: aio.ServicerContext,
        product_repo: IProductRepo = Depends(product_repo_depend),
        user: UserModel = Depends(admin_auth_depend),
    ):
        try:
            delete_product_usecase = DeleteProduct(product_repo)
            output = await delete_product_usecase.execute(request.product_id)
            response = output.model_dump(mode="json")
            return product_service_pb2.DeleteByIdResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
    
    @inject(cast=False)
    async def get_by_criteria(
        self,
        request: product_service_pb2.ProductFilterInput,
        context: aio.ServicerContext,
        product_repo: IProductRepo = Depends(product_repo_depend),
        category_repo: ICategoryRepo = Depends(category_repo_depend),
        user: UserModel = Depends(user_auth_depend),
    ):
        try:
            entity = ProductFilterInput.model_validate(MessageToDict(request, preserving_proto_field_name=True), from_attributes=True)
            get_all_user_products_usecase = GetProducts(product_repo, category_repo)
            outputs_list = await get_all_user_products_usecase.execute(entity)
            response = [ output.model_dump(mode="json") for output in outputs_list ]
            return product_service_pb2.GetByCriteriaResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
    
    @inject(cast=False)
    async def delete_all(
        self,
        request: Empty,
        context: aio.ServicerContext,
        product_repo: IProductRepo = Depends(product_repo_depend),
        user: UserModel = Depends(admin_auth_depend),
    ):
        try:
            delete_all_product_usecase = DeleteProducts(product_repo)
            output = await delete_all_product_usecase.execute()
            response = output.model_dump(mode="json")
            return product_service_pb2.DeleteAllResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
