from jinja2 import FileSystemLoader, Environment
import config
import asyncio
from . import url

jinja2_env = Environment(loader=FileSystemLoader(config.VIEWS_ROOT))


def jinja2_render(view, args) -> bytes:
    return jinja2_env.get_template(view).render(args).encode("utf-8")


class Request:
    def __init__(self, scope, receive):
        self._scope = scope
        self._receive = receive
        pass

    async def form(self):
        pass

    @property
    def method(self):
        return self._scope['method']

    pass


class Response:
    def __init__(self, request, send):
        self._send = send
        self._content_type = b"text/html"
        self._header_sent = False
        self._body = b''
        self._request = request

        self.alert = None
        self.success = None
        self.title = None
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

    @property
    def body(self):
        return self._body

    async def send_header(self, status=200):
        await self._send({
            'type': 'http.response.start',
            'status': status,
            'headers': self._get_headers()
        })
        self._header_sent = True

    async def end(self, data: bytes):
        if not self._header_sent:
            await self.send_header()
        await self._send({
            "type": "http.response.body",
            "body": data
        })
        self._body = data

    async def render(self, view: str, **kwargs):
        kwargs['URL'] = url.URL
        kwargs['config'] = config
        kwargs['response'] = self
        kwargs['request'] = self._request
        data = await asyncio.get_running_loop().run_in_executor(None, jinja2_render, view, kwargs)
        await self.end(data)
