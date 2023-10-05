from fastapi import APIRouter

router: APIRouter = APIRouter(
    prefix="/users",
    tags=["Users"],
)
