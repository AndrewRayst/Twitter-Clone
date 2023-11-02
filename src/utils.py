import hashlib
import random
import string
import uuid
from typing import Annotated

from fastapi import Header
from loguru import logger
from starlette.responses import JSONResponse

from src.exceptions import APIException


def get_hash(input_value: str) -> str:
    return hashlib.sha256(input_value.encode()).hexdigest()


def get_random_string(length: int = 10) -> str:
    if length <= 0:
        raise ValueError("length must be grater then 0")

    return "".join(random.choices(population=string.ascii_letters, k=length))


def get_unique_filename(filetype: str | None = None) -> str:
    """
    util for creating unique filename
    :param filetype: jpg, png, html and etc...
    :return: filename
    """
    if filetype:
        return get_random_string() + str(uuid.uuid4()) + "." + filetype
    return get_random_string() + str(uuid.uuid4())


def api_key_param(api_key: Annotated[str | None, Header()] = None) -> str | None:
    return api_key


async def return_user_exception(
    exception: APIException, status_code: int = 400, message: str = ""
) -> JSONResponse:
    logger.info(
        f"error name: {exception.get_name()}, error message: {exception.get_message()}"
    )
    await logger.complete()
    return JSONResponse(
        status_code=status_code,
        content={
            "result": False,
            "error_type": exception.get_name(),
            "error_message": message if message else exception.get_message(),
        },
    )


async def return_custom_exception(
    exception: Exception,
    message: str,
    status_code: int = 400,
    error_type: str = "",
) -> JSONResponse:
    logger.info(
        f"string representation: {exception.__str__()}, "
        f"args: {str(exception.args)}, "
        f"message: {message}"
    )
    await logger.complete()

    return JSONResponse(
        status_code=status_code,
        content={
            "result": False,
            "error_type": error_type if error_type else "Exception",
            "error_message": message,
        },
    )


async def return_server_exception(
    exception: Exception, status_code: int = 500, message: str = ""
) -> JSONResponse:
    logger.warning(
        f"string representation: {exception.__str__()}, args: {exception.args}"
    )
    await logger.complete()

    if not message:
        message = "Oops, something went wrong :(\nTry again please"

    return JSONResponse(
        status_code=status_code,
        content={"result": False, "error_type": "Exception", "error_message": message},
    )
