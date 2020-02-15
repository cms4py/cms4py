class Request:
    def __init__(self, scope, receive):
        self._scope = scope
        self._receive = receive
        pass
    pass


class Response:
    def __init__(self, send):
        self._send = send
        self._content_type = b"text/html"
        self._header_sent = False
        pass

    def _get_headers(self):
        result = [
            [b"content-type", self._content_type]
        ]
        return result

    @property
    def content_type(self) -> bytes:
        return self._content_type

    @content_type.setter
    def content_type(self, value: bytes):
        self._content_type = value

    async def send_header(self, status=200):
        await self._send({
            'type': 'http.response.start',
            'status': status,
            'headers': self._get_headers()
        })
        self._header_sent = True

    async def write(self, data: bytes):
        if not self._header_sent:
            await self.send_header()
        await self._send({
            "type": "http.response.body",
            "body": data
        })
