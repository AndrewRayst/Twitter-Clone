from fastapi import APIRouter


router: APIRouter = APIRouter(
    prefix="/api/tweets",
    tags=["Tweets"]
)
