from cms4py import http


class Controller:
    def __init__(self) -> None:
        super().__init__()
        self._pre_execute = self.pre_execute
        self._execute = self.execute
        self._post_execute = self.post_execute
        self._request = None
        self._response = None

    @property
    def request(self) -> http.Request:
        return self._request

    @property
    def response(self) -> http.Response:
        return self._response

    async def pre_execute(self, request, response):
        self._request = request
        self._response = response
        pass

    async def post_execute(self, request, response):
        pass

    async def execute(self, request, response):
        pass

    def set_pre_execute(self, callback):
        self._pre_execute = callback
        return self

    def set_post_execute(self, callback):
        self._post_execute = callback
        return self

    def set_execute(self, callback):
        self._execute = callback
        return self

    async def __call__(self, request, response):
        await self._pre_execute(request, response)
        await self._execute(request, response)
        await self._post_execute(request, response)
