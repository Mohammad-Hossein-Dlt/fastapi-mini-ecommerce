import grpc
from src.infra.schemas.grpc_schema.params import GrpcParams
from src.infra.schemas.grpc_schema.channel import GrpcChannel

def init_channel(
    params: GrpcParams, 
) -> GrpcChannel:
    
    channel = grpc.insecure_channel(params.url)
    
    return GrpcChannel(channel=channel)

def init_grpc_channel(
    params: GrpcParams,
) -> GrpcChannel:
    
    if isinstance(params, GrpcParams):
        return init_channel(params)

async def terminate_grpc_client(
    context: GrpcChannel | None = None,
):
    
    if not context:
        return
    
    if isinstance(context, GrpcChannel):
        await context.channel.close()