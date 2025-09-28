from fastapi import APIRouter
from .self._router import router as user_self_router
from .order._router import router as user_self_order_router

router = APIRouter(
    prefix="/self",
)

router.include_router(user_self_order_router)
router.include_router(user_self_router)