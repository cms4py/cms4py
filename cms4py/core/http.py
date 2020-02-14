class Request:
    def __init__(self, aio_lib_request) -> None:
        super().__init__()
        self._aio_lib_request = aio_lib_request


class Response:
    def __init__(self) -> None:
        super().__init__()
        self._data = ""

    def append(self, content):
        self._data += content

    @property
    def data(self):
        return self._data
