from fastapi import APIRouter

router = APIRouter(
    prefix="/self",
    tags=["Self management"],
)
