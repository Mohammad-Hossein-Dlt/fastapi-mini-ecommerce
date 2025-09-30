from fastapi import FastAPI
from fastapi.middleware import Middleware
from src.infra.middlewares.logging_middleware import LoggingMiddleware
from src.infra.middlewares.prometheus_middleware import PrometheusMiddleware
from .app_lifespan import lifespan

middlewares = [
    Middleware(LoggingMiddleware),
    Middleware(PrometheusMiddleware),
]

app: FastAPI = FastAPI(
    root_path="/product",
    lifespan=lifespan,
    middleware=middlewares,
)