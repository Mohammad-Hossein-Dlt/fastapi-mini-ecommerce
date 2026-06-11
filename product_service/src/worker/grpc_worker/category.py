from grpc import aio
from google.protobuf.empty_pb2 import Empty
from google.protobuf.json_format import MessageToDict

from sharedlib.grpc.service.category import category_service_pb2
from sharedlib.grpc.service.category import category_service_pb2_grpc

from src.worker.depends.depend import Depends, inject

from src.repo.interface.Icategory_repo import ICategoryRepo
from src.worker.depends.repo_depend import category_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend, user_auth_depend

from src.schemas.category.create_category_input import CreateCategoryInput
from src.schemas.category.update_category_input import UpdateCategoryInput
from src.schemas.filter.category_filter_input import CategoryFilterInput
from src.usecases.category.create import CreateCategory
from src.usecases.category.get_by_id import GetCategory
from src.usecases.category.update import UpdateCategory
from src.usecases.category.delete_by_id import DeleteCategory
from src.usecases.category.get_by_criteria import GetCategories
from src.usecases.category.delete_all import DeleteCategories

from src.infra.utils.grpc_status_code import rest_to_grpc_status
from src.infra.exceptions.exceptions import AppBaseException

class CategoryServicer(category_service_pb2_grpc.ICategoryService):
    
    @inject(cast=False)
    async def create(
        self,
        request: category_service_pb2.CreateCategoryInput,
        context: aio.ServicerContext,
        category_repo: ICategoryRepo = Depends(category_repo_depend),
        user: UserModel = Depends(admin_auth_depend),
    ):
        try:
            entity = CreateCategoryInput.model_validate(MessageToDict(request, preserving_proto_field_name=True), from_attributes=True)
            create_category_usecase = CreateCategory(category_repo)
            output = await create_category_usecase.execute(entity)
            response = output.model_dump(mode="json")
            return category_service_pb2.CreateResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
    
    @inject(cast=False)
    async def get_by_id(
        self,
        request: category_service_pb2.GetByIdRequest,
        context: aio.ServicerContext,
        category_repo: ICategoryRepo = Depends(category_repo_depend),
        user: UserModel = Depends(user_auth_depend),
    ):
        try:
            get_category_usecase = GetCategory(category_repo)
            output = await get_category_usecase.execute(request.category_id)
            response = output.model_dump(mode="json")
            return category_service_pb2.GetByIdResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
    
    @inject(cast=False)
    async def update(
        self,
        request: category_service_pb2.UpdateCategoryInput,
        context: aio.ServicerContext,
        category_repo: ICategoryRepo = Depends(category_repo_depend),
        user: UserModel = Depends(admin_auth_depend),
    ):
        try:
            entity = UpdateCategoryInput.model_validate(MessageToDict(request, preserving_proto_field_name=True), from_attributes=True)
            update_category_usecase = UpdateCategory(category_repo)
            output = await update_category_usecase.execute(entity)
            response = output.model_dump(mode="json")
            return category_service_pb2.UpdateResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
    
    @inject(cast=False)
    async def delete_by_id(
        self,
        request: category_service_pb2.DeleteByIdRequest,
        context: aio.ServicerContext,
        category_repo: ICategoryRepo = Depends(category_repo_depend),
        user: UserModel = Depends(admin_auth_depend),
    ):
        try:
            delete_category_usecase = DeleteCategory(category_repo)
            output = await delete_category_usecase.execute(request.category_id)
            response = output.model_dump(mode="json")
            return category_service_pb2.DeleteByIdResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
    
    @inject(cast=False)
    async def get_by_criteria(
        self,
        request: category_service_pb2.CategoryFilterInput,
        context: aio.ServicerContext,
        category_repo: ICategoryRepo = Depends(category_repo_depend),
        user: UserModel = Depends(user_auth_depend),
    ):
        try:
            criteria = CategoryFilterInput.model_validate(MessageToDict(request, preserving_proto_field_name=True), from_attributes=True)
            get_all_user_categorys_usecase = GetCategories(category_repo)
            outputs_list = await get_all_user_categorys_usecase.execute(criteria)
            response = [ output.model_dump(mode="json") for output in outputs_list ]
            return category_service_pb2.GetByCriteriaResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
    
    @inject(cast=False)
    async def delete_all(
        self,
        request: Empty,
        context: aio.ServicerContext,
        category_repo: ICategoryRepo = Depends(category_repo_depend),
        user: UserModel = Depends(admin_auth_depend),
    ):
        try:
            delete_all_category_usecase = DeleteCategories(category_repo)
            output = await delete_all_category_usecase.execute()
            response = output.model_dump(mode="json")
            return category_service_pb2.DeleteAllResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
