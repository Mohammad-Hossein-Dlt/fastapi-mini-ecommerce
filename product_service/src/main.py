from src.infra.context.context_manager import AppContextManager
from src.infra.context.app_context import AppContext

AppContextManager.init_context()

if AppContext.product_communication_type == 'http':
    from src.infra.fastapi_config.app import app
    from src.routes.api_v1.main_router import main_router_v1

    app.include_router(main_router_v1)

elif AppContext.product_communication_type == 'broker':
    from src.worker.consumer.app import app

elif AppContext.product_communication_type == 'grpc':
    from src.worker.grpc_worker.server import run_server
    run_server()