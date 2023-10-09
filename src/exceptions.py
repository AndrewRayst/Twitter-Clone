from typing import Any


class APIException(Exception):
    def __init__(self, name: str, message: str, *args: Any) -> None:
        self._name: str = name
        self._message: str = message
        super().__init__(*args)

    def get_name(self) -> str:
        return self._name

    def get_message(self) -> str:
        return self._message


class ExistError(APIException):
    def __init__(self, message: str, *args: Any) -> None:
        super().__init__("ExistError", message, *args)


class ConflictError(APIException):
    def __init__(self, message: str, *args: Any) -> None:
        super().__init__("ConflictError", message, *args)
