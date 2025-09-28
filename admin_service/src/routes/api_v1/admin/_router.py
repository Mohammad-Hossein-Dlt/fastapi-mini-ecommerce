from fastapi import APIRouter
from .order._router import router as admin_order_router
from .user._router import router as admin_user_router

router = APIRouter()

router.include_router(admin_order_router)
router.include_router(admin_user_router)