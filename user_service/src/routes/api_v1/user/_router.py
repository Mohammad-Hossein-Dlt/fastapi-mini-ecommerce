from fastapi import APIRouter
from .self._router import router as user_self_router
from .order._router import router as user_order_router

router = APIRouter(
    prefix="/user",
)

router.include_router(user_order_router)
router.include_router(user_self_router)