from fastapi import APIRouter
from .self._router import router as admin_self_router
from .order._router import router as admin_order_router

router = APIRouter(
    prefix="/self",
)

router.include_router(admin_self_router)
router.include_router(admin_order_router)