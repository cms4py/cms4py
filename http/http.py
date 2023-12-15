"""
Created on 2020/04/06
"""
import json
import re
import uuid
from urllib.parse import unquote

import config
from .. import template_engine
from .. import translator
from ..helpers import url_helper, log_helper
from ..session.SessionStorages import SessionStorages


class Request:
    def __init__(self, scope, receive):
        self._session_id_str = None
        self._scope = scope
        self._receive = receive
        self._protocol = scope['scheme']

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
        self._body: bytes = b''
        self._uri = None
        self._host = self.get_header(b"host")
        self._x_forwarded_host = self.get_header(b"x-forwarded-host")
        self._client = self._scope['client']
        self._client_ip = self._client[0]
        self._client_port = self._client[1]
        self._controller = None
        self._action = None

    @property
    def controller(self):
        return self._controller

    @property
    def action(self):
        return self._action

    @property
    def host(self) -> bytes:
        return self._host

    @property
    def x_forwarded_host(self) -> bytes:
        return self._x_forwarded_host

    def get_real_host(self) -> bytes:
        """
        Get the real host between client and server, if cms4py runs on back of a proxy server,
        this function also returns the proxy server's host
        Returns:

        """
        return self.x_forwarded_host if self.x_forwarded_host else self.host

    def get_real_host_as_str(self, charset=config.GLOBAL_CHARSET) -> str:
        real_host = self.get_real_host()
        return real_host.decode(charset) if real_host else ''

    def host_as_str(self, charset=config.GLOBAL_CHARSET) -> str:
        return self.host.decode(charset) if self.host else ''

    @property
    def client_ip(self):
        return self._client_ip

    @property
    def protocol(self) -> str:
        return self._protocol

    @property
    def uri(self) -> str:
        if not self._uri:
            self._uri = self.path
            if self.query_string:
                self._uri += "?"
                self._uri += self.query_string.decode(config.GLOBAL_CHARSET)
        return self._uri

    def _parse_args(self):
        tokens = self.path.split("/")
        if len(tokens) >= 4:
            self._args = tokens[3:]

    @property
    def body(self) -> bytes:
        return self._body

    @property
    def args(self) -> list:
        return self._args

    def get_arg(self, index) -> str:
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

    def is_mobile(self):
        user_agent = self.get_header(b"user-agent")
        if user_agent:
            return user_agent.find(b"iPhone") != -1 or \
                user_agent.find(b"iPad") != -1 or \
                user_agent.find(b"Android") != -1
        return False

    def runs_in_wx(self):
        """
        是否在微信中运行
        :param request:
        :return:
        """
        user_agent = self.get_header(b"user-agent")
        if user_agent:
            return user_agent.find(b"MicroMessenger") != -1
        return False

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

    def get_header(self, key: bytes, default_value=None) -> bytes:
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
            self._session_id_str = f"cms4py:session:{uuid.uuid4().hex}"
            self._session_id = self._session_id_str.encode(config.GLOBAL_CHARSET)
        return self._session_id

    @property
    def session_id_str(self) -> str:
        if self._session_id_str is None:
            self._session_id_str = self.session_id.decode(config.GLOBAL_CHARSET)
        return self._session_id_str

    async def session(self):
        return await SessionStorages.get_current().get_session(self.session_id_str)

    async def get_session(self, key: str, default_value=None):
        return await SessionStorages.get_current().get_session_field(self.session_id_str, key, default_value)

    async def set_session(self, key: str, value):
        await SessionStorages.get_current().set_session_field(self.session_id_str, key, value)

    @property
    def query_vars(self):
        return self._query_vars

    def get_query_vars(self, key: bytes) -> list:
        return self.query_vars[key] if key in self.query_vars else None

    def get_query_var(self, key: bytes, default_value=b'') -> bytes:
        return self._get_first_value_of_array_map(self.query_vars, key) or default_value

    @property
    def body_vars(self):
        return self._body_vars

    def get_body_vars(self, key: bytes) -> list:
        return self._body_vars[key] if key in self._body_vars else None

    def get_body_var(self, key: bytes, default_value=b'') -> bytes:
        return self._get_first_value_of_array_map(self.body_vars, key) or default_value

    def get_var(self, key: bytes, default_value=b'') -> bytes:
        if self.method == "GET":
            return self.get_query_var(key, default_value)
        elif self.method == 'POST':
            return self.get_body_var(key, default_value) or self.get_query_var(key, default_value)
        else:
            return default_value

    def get_var_as_str(self, key: bytes, default_value='', charset=config.GLOBAL_CHARSET) -> str:
        var_bytes = self.get_var(key)
        if var_bytes:
            return unquote(var_bytes.decode(charset))
        else:
            return default_value

    async def parse_form(self):
        if self.query_string:
            self._query_vars = url_helper.parse_url_pairs(self.query_string)
        if self.method == "POST":
            while True:
                message = await self._receive()
                self._body += message["body"] if 'body' in message else b''
                if "more_body" not in message or not message["more_body"]:
                    break
            if self.content_type:
                if self.content_type.startswith(b'application/x-www-form-urlencoded'):
                    self._body_vars = url_helper.parse_url_pairs(self._body)
                elif self.content_type.startswith(b"multipart/form-data"):
                    boundary_search_result = re.search(b"multipart/form-data; boundary=(.+)", self.content_type)
                    if boundary_search_result:
                        boundary = boundary_search_result.group(1)
                        if self._body:
                            body_results = self.body.split(b'\r\n--' + boundary)
                            if body_results:
                                for body_result in body_results:
                                    split_index = body_result.find(b'\r\n\r\n')
                                    if split_index != -1:
                                        head = body_result[:split_index]
                                        content = body_result[split_index + 4:]
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
                                        pass
                                    else:
                                        break
                else:
                    log_helper.Cms4pyLog.get_instance().info(
                        f"Request content-type is {self.content_type}, we do not parse"
                    )
            else:
                log_helper.Cms4pyLog.get_instance().warning("content-type is None")
            pass
        pass

    @property
    def method(self) -> str:
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
        self._status_code = None

        self.alert = None
        self.success = None
        self.title = None
        self._headers_map = {}

        self.content_type = b'text/html'
        self.add_header(b'server', config.SERVER_NAME)
        self.add_set_cookie(config.CMS4PY_SESSION_ID_KEY, self._request.session_id)
        pass

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, value):
        self._status_code = value

    @property
    def header_sent(self):
        return self._header_sent

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
        self.add_header(
            b'set-cookie',
            "{}={}; max-age={}; path={}; SameSite=Lax".format(
                name.decode(config.GLOBAL_CHARSET),
                value.decode(config.GLOBAL_CHARSET),
                max_age,
                path.decode(config.GLOBAL_CHARSET)
            ).encode(
                config.GLOBAL_CHARSET
            )
        )

    @property
    def body_sent(self):
        """
        Indicates whether the body has been sent
        :return:
        """
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

    async def write(self, data: bytes):
        """
        This function is always used to support long-live connection, if you want to render a page at once, you should
        use function 'end' instead.
        :param data:
        :return:
        """
        if not self._header_sent:
            await self.send_header()
        await self._send({
            "type": "http.response.body",
            "body": data,
            'more_body': True
        })

    async def end(self, data: bytes):
        if self._body_sent:
            return
        if not self._header_sent:
            await self.send_header(self.status_code or 200)
        await self._send({
            "type": "http.response.body",
            "body": data,
            'more_body': False
        })
        self._body = data
        self._body_sent = True

    async def json(self, data):
        self.content_type = b"application/json"
        await self.end(json.dumps(data).encode(config.GLOBAL_CHARSET))

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
        kwargs['session'] = await self._request.session()
        data = await template_engine.TemplateEngine.get_instance().render(view, **kwargs)
        return data

    async def render(self, view: str, **kwargs):
        if self._body_sent:
            return
        await self.end(await self.render_string(view, **kwargs))
