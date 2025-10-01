from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.infra.settings.settings import settings
from .app_state import AppStates, set_app_state

@asynccontextmanager
async def lifespan(app: FastAPI):
        
    # set_app_state(app, AppStates.EXTERNAL_FASTAPI_PORT, settings.EXTERNAL_FASTAPI_PORT)
    # set_app_state(app, AppStates.INTERNAL_FASTAPI_PORT, settings.INTERNAL_FASTAPI_PORT)
    
    # set_app_state(app, AppStates.AUTH_BASE_URL, settings.AUTH_BASE_URL)
    # set_app_state(app, AppStates.PRODUCT_BASE_URL, settings.PRODUCT_BASE_URL)
    # set_app_state(app, AppStates.ORDER_BASE_URL, settings.ORDER_BASE_URL)
            
    yield
    