from fastapi import APIRouter

router = APIRouter(
    prefix="/order",
    tags=["Self order"]
)
