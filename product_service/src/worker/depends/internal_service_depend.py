from src.infra.context.app_context import AppContext

from src.gateway.internal.interface.Iauth_service import IAuthService
from src.gateway.internal.http.auth_service import AuthHttpService
from src.gateway.internal.grpc_client.auth_service import AuthGrpcService
from src.gateway.internal.nats.auth_service import AuthBrokerService

def auth_service_depend() -> IAuthService:
    
    if AppContext.auth_communication_type == 'http':    
        return AuthHttpService(
            AppContext.http_client,
            AppContext.auth_base_url,
        )
    
    elif AppContext.auth_communication_type == 'broker':
        return AuthBrokerService(
            AppContext.broker_client,
        )
    
    elif AppContext.auth_communication_type == 'grpc':
        return AuthGrpcService(
            AppContext.auth_grpc_channel.channel,
        )