from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from src.infra.middlewares.logging_middleware import LoggingMiddleware
from src.infra.middlewares.prometheus_middleware import PrometheusMiddleware
from .app_lifespan import lifespan

middlewares = [
    Middleware(LoggingMiddleware),
    Middleware(PrometheusMiddleware),
    Middleware(
        SessionMiddleware,
        secret_key="dbf8e8b2960f4223baf0eb2a50c56c98",
        https_only=False,
        max_age=None,
    ),
]

app: FastAPI = FastAPI(
    root_path="/user",
    lifespan=lifespan,
    middleware=middlewares,
)