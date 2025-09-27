from fastapi import APIRouter
from .order._router import router as order_router
from .user._router import router as user_router

router = APIRouter()

router.include_router(user_router)
router.include_router(order_router)