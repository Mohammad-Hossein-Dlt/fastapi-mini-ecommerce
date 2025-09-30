from fastapi import APIRouter
from src.routes.api_v1.auth._router import router as auth_router
from src.routes.api_v1.admin._router import router as admin_router
from src.routes.api_v1.user._router import router as user_router
from src.routes.api_v1.metrics._router import router as metrics_router

ROUTE_PREFIX_VERSION_API = "/api/v1"

main_router_v1 = APIRouter()

main_router_v1.include_router(auth_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(admin_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(user_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(metrics_router, prefix=ROUTE_PREFIX_VERSION_API)

# from src.routes.depends.health_check_depend import health_check

# main_router_v1.add_api_route(
#     "/health",
#     endpoint=health_check,
#     methods=["GET"],
#     tags=["Check health"],
# )