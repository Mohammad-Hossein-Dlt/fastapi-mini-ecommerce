from src.infra.context.app_context import AppContext

def broker_client_depend():
    client = AppContext.broker_client
    return client