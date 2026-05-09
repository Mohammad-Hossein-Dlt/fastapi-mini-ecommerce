from src.infra.schemas.broker.rabbitmq import RabbitParams, RabbitClient
from src.infra.schemas.broker.nats import NatsParams, NatsClient
from faststream.rabbit import RabbitBroker, RabbitQueue, RabbitExchange, ExchangeType
from faststream.nats import NatsBroker
from src.infra.middlewares.faststream.exception_middleware import exc_middleware

def init_rabbitmq(
    params: RabbitParams, 
) -> RabbitClient:
    
    broker = RabbitBroker(
        url=params.url,
        middlewares=[
            exc_middleware,
        ]
    )
        
    exchange = RabbitExchange(
        name=params.exchange,
        type=ExchangeType.FANOUT,
    )
    
    queue = RabbitQueue(
        name=params.queue,
        routing_key=params.routing_key,
    )
    
    return RabbitClient(
        params=params,
        broker=broker,
        exchange=exchange,
        queue=queue,
    )
    
def init_nats(
    params: NatsParams, 
) -> NatsClient:
    
    client = NatsBroker(
        servers=[params.url]
    )
    
    return NatsClient(
        params=params,
        broker=client
    )
    
def init_broker_client(
    params: RabbitParams | NatsParams,
) -> RabbitClient | NatsClient:
    
    if isinstance(params, RabbitParams):
        return init_rabbitmq(params)
    
    if isinstance(params, NatsParams):
        return init_nats(params)

async def terminate_broker_client(
    context: RabbitClient | None = None,
):
    
    if not context:
        return
    
    if isinstance(context, RabbitClient):
        await context.broker.stop()    
        
    if isinstance(context, NatsClient):
        await context.broker.stop()