from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health Check"]
)
