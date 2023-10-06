from pydantic import BaseModel, fields


class SuccessResponseSchema(BaseModel):
    result: bool = fields.Field(examples=[True])


class ErrorResponseSchema(BaseModel):
    result: bool = fields.Field(examples=[False])
    error_type: str
    error_message: str
