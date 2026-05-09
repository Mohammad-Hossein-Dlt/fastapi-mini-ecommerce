from fastapi import APIRouter
from .self._router import router as user_router

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

router.include_router(user_router)