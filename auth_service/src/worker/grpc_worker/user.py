from grpc import aio
from google.protobuf.empty_pb2 import Empty

from sharedlib.grpc.service.auth import user_service_pb2, user_service_pb2_grpc

from src.worker.depends.depend import Depends, inject

from src.repo.interface.Iuser_repo import IUserRepo
from src.worker.depends.repo_depend import user_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import user_auth_depend

from src.usecases.user.delete import DeleteUser

from src.infra.utils.grpc_status_code import rest_to_grpc_status
from src.infra.exceptions.exceptions import AppBaseException

class UserServicer(user_service_pb2_grpc.IUserService):
    
    @inject(cast=False)
    async def get_self(
        self,
        request: Empty,
        context: aio.ServicerContext,
        user: UserModel = Depends(user_auth_depend),
    ):
        try:
            response = user.model_dump(mode="json")
            return user_service_pb2.GetSelfResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
            
    @inject(cast=False)
    async def delete_self(
        self,
        request: Empty,
        context: aio.ServicerContext,
        user_repo: IUserRepo = Depends(user_repo_depend),
        user: UserModel = Depends(user_auth_depend),
    ):
        
        try:
            delete_user_usecase = DeleteUser(user_repo)
            output = await delete_user_usecase.execute(user)
            response = output.model_dump(mode="json")
            return user_service_pb2.DeleteSelfResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)