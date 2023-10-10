from fastapi import APIRouter

router: APIRouter = APIRouter(
    prefix="/api/medias",
    tags=["media"],
)
