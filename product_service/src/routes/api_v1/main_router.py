from fastapi import APIRouter
from src.routes.api_v1.category._router import router as category_router
from src.routes.api_v1.product._router import router as product_router

ROUTE_PREFIX_VERSION_API = "/api/v1"

main_router_v1 = APIRouter()

main_router_v1.include_router(category_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(product_router, prefix=ROUTE_PREFIX_VERSION_API)
