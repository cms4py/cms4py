import asyncio, uuid
import re, datetime

from jinja2 import FileSystemLoader, Environment

import config
from . import translator, cache_managers
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
        self._accept_languages = re.compile(b"[a-z]{2}-[A-Z]{2}").findall(
            self._raw_accept_languages
        ) if self._raw_accept_languages else []

        lang: bytes = config.LANGUAGE or (self._accept_languages[0] if len(self._accept_languages) > 0 else b'en-US')
        self._language = lang.decode("utf-8")

        self._query_vars = {}
        self._body_vars = {}

        self._content_type = None
        self._args = []
        self._parse_args()
        self._cookie = None
        self._cookie_map = None
        self._session_id: bytes = b''
        pass

    def _parse_args(self):
        tokens = self.path.split("/")
        if len(tokens) >= 4:
            self._args = tokens[3:]

    @property
    def args(self):
        return self._args

    def get_arg(self, index):
        return self._args[index] if len(self._args) > index else None

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
    def query_string(self) -> bytes:
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
    def cookie(self) -> bytes:
        if not self._cookie:
            self._cookie = self.get_header(b'cookie')
        return self._cookie

    def get_cookie(self, key: bytes, default_value=None) -> bytes:
        if not self._cookie_map:
            self._cookie_map = {}
            cookie = self.cookie
            if cookie:
                tokens = cookie.split(b"; ")
                for t in tokens:
                    kv = t.split(b"=")
                    if len(kv) == 2:
                        self._cookie_map[kv[0]] = kv[1]
        return self._cookie_map[key] if key in self._cookie_map else default_value

    @property
    def session_id(self) -> bytes:
        self._session_id = self.get_cookie(config.CMS4PY_SESSION_ID_KEY, None)
        if not self._session_id:
            self._session_id = uuid.uuid4().hex.encode(config.GLOBAL_CHARSET)
        return self._session_id

    async def session(self):
        return await cache_managers.SessionCacheManager.get_instance().get_data(self.session_id)

    async def get_session(self, key, default_value=None):
        session_dict = await cache_managers.SessionCacheManager.get_instance().get_data(self.session_id)
        return session_dict[key] if key in session_dict else default_value

    async def set_session(self, key, value):
        session_dict = await cache_managers.SessionCacheManager.get_instance().get_data(self.session_id)
        session_dict[key] = value

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
                    boundary_search_result = re.search(b"multipart/form-data; boundary=(.+)", self.content_type)
                    if boundary_search_result:
                        boundary = boundary_search_result.group(1)
                        if 'body' in data and data['body']:
                            body_results = re.compile(boundary + b"\r\n([\s\S]*?)\r\n\r\n([\s\S]*?)\r\n", re.M).findall(
                                data['body']
                            )
                            if body_results:
                                for body_result in body_results:
                                    head = body_result[0]
                                    content = body_result[1]
                                    name_result = re.search(b'Content-Disposition: form-data; name="([^"]+)"', head,
                                                            re.M)
                                    if name_result:
                                        name = name_result.group(1)
                                        if name not in self._body_vars:
                                            self._body_vars[name] = []
                                        file_name_result = re.search(b' filename="([^"]+)"', head, re.M)
                                        file_name = file_name_result.group(1) if file_name_result else None
                                        if not file_name:
                                            self._body_vars[name].append(content)
                                        else:
                                            file_object = {'name': name, 'filename': file_name, 'content': content}
                                            content_type_result = re.search(b'Content-Type: (.*)', head, re.M)
                                            if content_type_result:
                                                file_object['content-type'] = content_type_result.group(1)
                                            self._body_vars[name].append(file_object)
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
    def path(self) -> str:
        return self._path

    pass


class Response:
    def __init__(self, request: Request, send):
        self._send = send
        self._content_type = None
        self._header_sent = False
        self._body_sent = False
        self._body = b''
        self._request: Request = request
        self._language_dict = None

        self.alert = None
        self.success = None
        self.title = None
        self._headers_map = {}

        self.content_type = b'text/html'
        self.add_header(b'server', config.SERVER_NAME)
        self.add_set_cookie(config.CMS4PY_SESSION_ID_KEY, self._request.session_id)
        pass

    def _get_headers(self):
        result = []
        for key in self._headers_map:
            for v in self._headers_map[key]:
                result.append([key, v])
        return result

    def add_header(self, key: bytes, value: bytes):
        if key not in self._headers_map:
            self._headers_map[key] = []
        self._headers_map[key].append(value)

    def add_set_cookie(self, name: bytes, value: bytes, max_age: int = 604800, path: bytes = b'/'):
        self.add_header(b'set-cookie',
                        f"{name.decode(config.GLOBAL_CHARSET)}={value.decode(config.GLOBAL_CHARSET)}; max-age={max_age}; path={path.decode(config.GLOBAL_CHARSET)}".encode(
                            config.GLOBAL_CHARSET))

    @property
    def body_sent(self):
        return self._body_sent

    @property
    def content_type(self) -> bytes:
        return self._content_type

    @content_type.setter
    def content_type(self, value: bytes):
        self._content_type = value
        self._headers_map[b"content-type"] = [value]

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
            "body": data,
        })
        self._body = data
        self._body_sent = True

    async def translate_async(self, words):
        return await translator.translate(words, self._request.language)

    async def _load_language_dict(self):
        if not self._language_dict:
            self._language_dict = await translator.get_language_dict(self._request.language)

    def translate(self, words):
        if self._language_dict and words in self._language_dict:
            words = self._language_dict[words]
        return words

    async def redirect(self, target: str, primary=False):
        url = target.encode(config.GLOBAL_CHARSET)
        status = 302 if not primary else 301
        self.add_header(b'location', url)
        await self.send_header(status)
        await self.end(
            b"<html lang=\"en\">"
            b"  <head>"
            b"      <meta charset=\"UTF-8\">"
            b"      <title>Redirecting</title>"
            b"  </head>"
            b"  <body>"
            b"      Redirecting to <a href='" + url + b"'>" + url + b"</a>" +
            b"  </body>"
            b"</html>")
        pass

    async def render_string(self, view: str, **kwargs) -> bytes:
        kwargs['URL'] = url_helper.URL
        kwargs['config'] = config
        kwargs['response'] = self
        kwargs['request'] = self._request
        kwargs["_"] = self.translate
        kwargs["T"] = self.translate
        data = await asyncio.get_running_loop().run_in_executor(None, jinja2_render, view, kwargs)
        return data

    async def render(self, view: str, **kwargs):
        await self.end(await self.render_string(view, **kwargs))


def cache(expire=3600, key=None):
    """
    :param expire: In seconds
    :param key:
    :return:
    """

    def wrapper(f):

        async def inner(req: Request, res: Response):
            _key = key
            if not _key:
                _key = req.path
                if req.query_string:
                    _key += f"?{req.query_string.decode(config.GLOBAL_CHARSET)}"

            async def wrap_data_callback(cache_key) -> cache_managers.CachedDataWrapper:
                await f(req, res)
                log_helper.Cms4pyLog.get_instance().debug(f"Cache page {cache_key}")
                return cache_managers.CachedDataWrapper(res.body, datetime.datetime.now().timestamp() + expire)

            cached_data = await cache_managers.PageCacheManager.get_instance().get_data(_key, wrap_data_callback)
            if not res.body_sent:
                await res.end(cached_data)

        return inner

    return wrapper
