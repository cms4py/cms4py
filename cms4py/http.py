import asyncio
import re
from . import translator

from jinja2 import FileSystemLoader, Environment

import config
from . import url

jinja2_env = Environment(loader=FileSystemLoader(config.VIEWS_ROOT))


def jinja2_render(view, args) -> bytes:
    return jinja2_env.get_template(view).render(args).encode("utf-8")


class Request:
    def __init__(self, scope, receive):
        self._scope = scope
        self._receive = receive

        self._method = self._scope['method']
        self._path = self._scope['path']
        self._raw_headers = self._scope['headers'] if 'headers' in self._scope else []
        self._headers = {}
        self._copy_headers()
        self._raw_accept_languages = self.get_header(b'accept-language')
        self._accept_languages = re.compile(b"[a-z]{2}-[A-Z]{2}").findall(self._raw_accept_languages)

        lang: bytes = config.LANGUAGE or (self._accept_languages[0] if len(self._accept_languages) > 0 else 'en-US')
        self._language = lang.decode("utf-8")
        pass

    def _copy_headers(self):
        for pair in self._raw_headers:
            if len(pair) == 2:
                key = pair[0]
                if key not in self._headers:
                    self._headers[key] = []
                self._headers[key].append(pair[1])
        pass

    @property
    def language(self) -> str:
        return self._language

    @property
    def accept_languages(self):
        return self._accept_languages

    @property
    def headers(self):
        return self._headers

    def header(self, key):
        return self.headers[key] if key in self.headers else None

    def get_header(self, key, default_value=None):
        values = self.header(key)
        value = default_value
        if values and len(values) > 0:
            value = values[0]
        return value

    async def form(self):
        pass

    @property
    def method(self):
        return self._method

    @property
    def path(self):
        return self._path

    pass


class Response:
    def __init__(self, request: Request, send):
        self._send = send
        self._content_type = b"text/html"
        self._header_sent = False
        self._body = b''
        self._request: Request = request
        self._language_dict = None

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

    async def translate_async(self, words):
        return await translator.translate(words, self._request.language)

    async def _load_language_dict(self):
        if not self._language_dict:
            self._language_dict = await translator.get_language_dict(self._request.language)

    def translate(self, words):
        if self._language_dict and words in self._language_dict:
            words = self._language_dict[words]
        return words

    async def render(self, view: str, **kwargs):
        await self._load_language_dict()
        kwargs['URL'] = url.URL
        kwargs['config'] = config
        kwargs['response'] = self
        kwargs['request'] = self._request
        kwargs["_"] = self.translate
        kwargs["T"] = self.translate
        data = await asyncio.get_running_loop().run_in_executor(None, jinja2_render, view, kwargs)
        await self.end(data)
