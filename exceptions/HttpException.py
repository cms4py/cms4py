"""
Created on 2023/12/06
"""
from cms4py.exceptions.Cms4pyException import Cms4pyException


class HttpException(Cms4pyException):

    def __init__(self, status_code: int, body: bytes = b""):
        super().__init__("HttpException")

        self._status_code = status_code
        self._body = body

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def body(self) -> bytes:
        return self._body
