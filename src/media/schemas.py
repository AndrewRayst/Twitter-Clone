from src.schemas import SuccessResponseSchema


class SuccessMediaResponseSchema(SuccessResponseSchema):
    media_id: int
