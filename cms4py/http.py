import asyncio
import re
from . import translator

from jinja2 import FileSystemLoader, Environment

import config
from .helpers import url_helper, log_helper

jinja2_env = Environment(loader=FileSystemLoader(config.VIEWS_ROOT))


def jinja2_render(view, args) -> bytes:
    return jinja2_env.get_template(view).render(args).encode("utf-8")


class Request:
    def __init__(self, scope, receive):
        self._scope = scope
        self._receive = receive

        self._method = self._scope['method']
        self._path = self._scope['path']
        self._query_string = self._scope['query_string']
        self._raw_headers = self._scope['headers'] if 'headers' in self._scope else []
        self._headers = {}
        self._copy_headers()
        self._raw_accept_languages = self.get_header(b'accept-language')
        self._accept_languages = re.compile(b"[a-z]{2}-[A-Z]{2}").findall(self._raw_accept_languages)

        lang: bytes = config.LANGUAGE or (self._accept_languages[0] if len(self._accept_languages) > 0 else 'en-US')
        self._language = lang.decode("utf-8")

        self._query_vars = {}
        self._body_vars = {}

        self._content_type = None
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

    @property
    def query_string(self):
        return self._query_string

    def _get_first_value_of_array_map(self, data, key):
        values = data[key] if (data and key in data) else None
        value = None
        if values and len(values) > 0:
            value = values[0]
        return value

    def get_headers(self, key: bytes):
        """
        Get all values by key
        :param key:
        :return:
        """
        return self.headers[key] if key in self.headers else None

    def get_header(self, key: bytes, default_value=None):
        """
        Get first value by key
        :param key:
        :param default_value:
        :return:
        """
        return self._get_first_value_of_array_map(self.headers, key) or default_value

    @property
    def content_type(self) -> bytes:
        if not self._content_type:
            self._content_type = self.get_header(b"content-type")
        return self._content_type

    @property
    def query_vars(self):
        return self._query_vars

    def get_query_vars(self, key: bytes) -> list:
        return self.query_vars[key] if key in self.query_vars else None

    def get_query_var(self, key: bytes, default_value=None) -> bytes:
        return self._get_first_value_of_array_map(self.query_vars, key) or default_value

    @property
    def body_vars(self):
        return self._body_vars

    def get_body_vars(self, key: bytes) -> list:
        return self._body_vars[key] if key in self._body_vars else None

    def get_body_var(self, key: bytes, default_value=None) -> bytes:
        return self._get_first_value_of_array_map(self.body_vars, key) or default_value

    async def parse_form(self):
        if self.query_string:
            self._query_vars = url_helper.parse_url_pairs(self.query_string)
        if self.method == "POST":
            data = await self._receive()
            if self.content_type:
                if self.content_type == b'application/x-www-form-urlencoded':
                    self._body_vars = url_helper.parse_url_pairs(data['body'])
                elif self.content_type.startswith(b"multipart/form-data"):
                    # TODO
                    pass
                else:
                    log_helper.Cms4pyLog.get_instance().warning(f"Unsupported content-type {self.content_type}")
            else:
                log_helper.Cms4pyLog.get_instance().warning("content-type is None")
            pass
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
        kwargs['URL'] = url_helper.URL
        kwargs['config'] = config
        kwargs['response'] = self
        kwargs['request'] = self._request
        kwargs["_"] = self.translate
        kwargs["T"] = self.translate
        data = await asyncio.get_running_loop().run_in_executor(None, jinja2_render, view, kwargs)
        await self.end(data)
