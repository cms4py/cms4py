from cms4py.core.http import Response, Request


class Cms4pyRequestHandlerContext():

    def __init__(self) -> None:
        super().__init__()
        self._request = None
        self._response = None
        self._data = dict()

    @property
    def request(self) -> Request:
        return self._request

    @request.setter
    def request(self, value: Request):
        self._request = value

    @property
    def response(self) -> Response:
        return self._response

    @response.setter
    def response(self, value):
        self._response = value

    def data(self):
        return self._data


class Cms4pyRequestHandler:

    async def pre_execute(self, context: "Cms4pyRequestHandlerContext"):
        pass

    async def execute(self, context: "Cms4pyRequestHandlerContext"):
        pass

    async def post_execute(self, context: "Cms4pyRequestHandlerContext"):
        pass
