import config
import re, uuid
from cms4py.utils.log import Cms4pyLog
from cms4py.utils import url_helper
from urllib.parse import unquote
from cms4py.cache import SessionCacheManager


class Request:
    """
    将浏览器的请求封装为一个Request对象，便于操作
    """

    def __init__(self, scope, receive):
        self._scope = scope
        self._receive = receive
        # 记录协议类型， http 或者 https
        self._protocol = scope['scheme']
        # 记录请求方法
        self._method = self._scope['method']
        # 记录请求路径
        self._path = self._scope['path']
        # 记录请求路径中 ? 后面的字符串
        self._query_string = self._scope['query_string']
        # 记录 ASGI 发来的原始请求头数据
        self._raw_headers = self._scope['headers'] \
            if 'headers' in self._scope else []
        # 声明一个字典用于存放头数据
        self._headers = {}
        # 将原始请求头数据装进 self._headers，便于后续使用
        self._copy_headers()
        # 记录原始请求头中的可接受的语言列表数据
        self._raw_accept_languages = self.get_header(
            b'accept-language'
        )
        # 用正则表达将可接受的语言截取出来转成数组
        self._accept_languages = re.compile(
            b"[a-z]{2}-[A-Z]{2}"
        ).findall(
            self._raw_accept_languages
        ) if self._raw_accept_languages else []

        lang: bytes = config.LANGUAGE or (
            self._accept_languages[0] if len(
                self._accept_languages
            ) > 0 else b'en-US'
        )
        # 记录将要使用的语言种类
        self._language = lang.decode("utf-8")

        # 该变量用于记录 content_type
        self._content_type = None
        # 该变量用于记录请求的 uri
        self._uri = None
        # 记录请求的主机
        self._host = self.get_header(b"host")
        # 记录信息
        self._client = self._scope['client']
        # 记录客户端 ip 地址
        self._client_ip = self._client[0]
        # 记录客户端端口
        self._client_port = self._client[1]

        # 该变量用于记录请求的控制器名
        self._controller = None
        # 该变量用于记录请求的函数名
        self._action = None
        # 该变量用于记录路径参数
        self._args = None
        # 记录浏览器端发来的数据内容
        self._body = b''
        # 路径中的参数
        self._query_vars = {}
        # 协议内容中的参数
        self._body_vars = {}

        # 用于存放 Cookie 字符串
        self._cookie = None
        # 用于存放 Cookie 键值对
        self._cookie_map = {}
        # 用于记录 session_id
        self._session_id = b''
        pass

    @property
    def scope(self):
        return self._scope

    @property
    def receive(self):
        """
        Get the asgi receive function
        """
        return self._receive

    @property
    def controller(self):
        return self._controller

    @property
    def action(self):
        return self._action

    @property
    def host(self) -> bytes:
        return self._host

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
                self._uri += self.query_string.decode(
                    config.GLOBAL_CHARSET
                )
        return self._uri

    def _copy_headers(self):
        # 将原始请求头数据装进 self._headers
        # 在 HTTP 协议中，消息头可以支持多条同名的字段，所以字段名
        # 对应的是个列表对象
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
        return self._get_first_value_of_array_map(
            self.headers, key
        ) or default_value

    @property
    def content_type(self) -> bytes:
        if not self._content_type:
            self._content_type = self.get_header(b"content-type")
        return self._content_type

    @property
    def method(self) -> str:
        return self._method

    @property
    def path(self) -> str:
        return self._path

    @property
    def args(self):
        """
        获取所有的路径参数
        :return:
        """
        return self._args

    def arg(self, index):
        """
        返回指定位置的值或者 None
        :param index:
        :return:
        """
        return self.args[index] \
            if self.args and len(self.args) > index \
            else None

    @property
    def body(self) -> bytes:
        """
        获取前端发来的数据
        :return:
        """
        return self._body

    @property
    def query_vars(self):
        """
        获取所有URL中的参数对
        :return:
        """
        return self._query_vars

    def get_query_vars(self, key: bytes) -> list:
        """
        根据键名获得对应的所有的值
        :param key:
        :return:
        """
        return self.query_vars[key] if key in self.query_vars else None

    def get_query_var(self, key: bytes, default_value=b'') -> bytes:
        """
        根据键名获得与之匹配的第一个值
        :param key:
        :param default_value:
        :return:
        """
        return self._get_first_value_of_array_map(
            self.query_vars, key
        ) or default_value

    @property
    def body_vars(self):
        """
        获取通过HTTP消息体传来的参数
        :return:
        """
        return self._body_vars

    def get_body_vars(self, key: bytes) -> list:
        """
        根据键名获取对应的所有消息体参数
        :param key:
        :return:
        """
        return self._body_vars[key] if key in self._body_vars else None

    def get_body_var(self, key: bytes, default_value=b'') -> bytes:
        """
        根据键名获得对应的第一个消息体参数
        :param key:
        :param default_value:
        :return:
        """
        return self._get_first_value_of_array_map(
            self.body_vars, key
        ) or default_value

    def get_var(self, key: bytes, default_value=b'') -> bytes:
        """
        根据键名获取对应的第一个参数，该函数会自动从URL中和消息体中取参数
        :param key:
        :param default_value:
        :return:
        """
        if self.method == "GET":
            return self.get_query_var(
                key, default_value
            )
        elif self.method == 'POST':
            return self.get_body_var(
                key, default_value
            ) or self.get_query_var(
                key, default_value
            )
        else:
            return default_value

    def get_var_as_str(
            self, key: bytes,
            default_value='',
            charset=config.GLOBAL_CHARSET
    ) -> str:
        """
        以指定的编码方式获取参数
        :param key:
        :param default_value:
        :param charset:
        :return:
        """
        var_bytes = self.get_var(key)
        if var_bytes:
            return unquote(var_bytes.decode(charset))
        else:
            return default_value

    async def _parse_form(self):
        """
        解析表单，该函数由cms4py框架内部调用，应用层不应该调用此函数
        :return:
        """

        # TODO 目前实现仅支持GET方法与POST方法，需要逐步完善
        #  并支持所有的 HTTP 方法
        if self.query_string:
            # 尝试从 URL 中解析参数
            self._query_vars = url_helper.parse_url_pairs(
                self.query_string
            )
        if self.method == "POST":
            # 如果是 POST 方式，尝试读取消息体
            while True:
                message = await self._receive()
                # TODO 需要实现数据限制机制以防攻击
                self._body += message["body"] if 'body' in message else b''
                if "more_body" not in message or not message["more_body"]:
                    break
            if self.content_type:
                # 如果是 application/x-www-form-urlencoded 编码方式，
                # 则尝试以 URL 参数对的方式解析
                if self.content_type.startswith(b'application/x-www-form-urlencoded'):
                    self._body_vars = url_helper.parse_url_pairs(self._body)
                # 如果是 multipart/form-data 则当成表单数据解析，可用
                # 于处理文件上传请求
                elif self.content_type.startswith(b"multipart/form-data"):
                    # 该正则用于取出数据分割符
                    boundary_search_result = re.search(b"multipart/form-data; boundary=(.+)", self.content_type)
                    if boundary_search_result:
                        # 取出分割符
                        boundary = boundary_search_result.group(1)
                        if self._body:
                            # 用分割符分割表单数据
                            body_results = self.body.split(
                                b'\r\n--' + boundary
                            )
                            if body_results:
                                for body_result in body_results:
                                    # 分割后的每一条数据都有头部和内容，
                                    # 头部和内容以 \r\n\r\n 分开，
                                    # 头部是字符串，描述该数据的信息
                                    # 内容部分是二进制数据
                                    split_index = body_result.find(b'\r\n\r\n')
                                    if split_index != -1:
                                        # 获取头部信息字符串
                                        head = body_result[:split_index]
                                        # 获取内容
                                        content = body_result[split_index + 4:]
                                        # 取出该字段的名称
                                        name_result = re.search(
                                            b'Content-Disposition: form-data; name="([^"]+)"',
                                            head, re.M
                                        )
                                        if name_result:
                                            name = name_result.group(1)
                                            if name not in self._body_vars:
                                                self._body_vars[name] = []
                                            # 如果是文件，则取出该字段的文件名
                                            file_name_result = re.search(b' filename="([^"]+)"', head, re.M)
                                            file_name = file_name_result.group(1) if file_name_result else None
                                            if not file_name:
                                                # 如果不是文件，值为普通字符串
                                                self._body_vars[name].append(content)
                                            else:
                                                file_object = {
                                                    'name': name,
                                                    'filename': file_name,
                                                    'content': content
                                                }
                                                content_type_result = re.search(b'Content-Type: (.*)', head, re.M)
                                                if content_type_result:
                                                    file_object['content-type'] = content_type_result.group(1)
                                                # 如果是文件，则值为文件对象
                                                self._body_vars[name].append(file_object)
                                        pass
                                    else:
                                        break
                else:
                    Cms4pyLog.get_instance().info(f"Request content-type is {self.content_type}, we do not parse")
            else:
                Cms4pyLog.get_instance().warning("content-type is None")
            pass
        pass

    @property
    def cookie(self) -> bytes:
        """
        获取 Cookie 字符串
        :return:
        """
        if not self._cookie:
            # 从 header 里取出 Cookie
            self._cookie = self.get_header(b'cookie')
        return self._cookie

    def get_cookie(self, key: bytes, default_value=None) -> bytes:
        """
        根据键名获取 Cookie 值
        :param key:
        :param default_value:
        :return:
        """
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
        """
        获取 Session ID
        :return:
        """

        # 从 Cookie 中取得 Session ID 的值
        self._session_id = self.get_cookie(
            config.CMS4PY_SESSION_ID_KEY,
            None
        )
        # 如果不存在，生成新的 Session ID
        if not self._session_id:
            self._session_id = uuid.uuid4().hex.encode(config.GLOBAL_CHARSET)
        return self._session_id

    async def session(self):
        """
        根据 Session ID 获得对应的 Session 数据
        :return:
        """
        return await SessionCacheManager.get_instance().get_data(self.session_id)

    async def get_session(self, key: str, default_value=None):
        """
        从 Session 中根据键名获取对应的值
        :param key:
        :param default_value:
        :return:
        """
        session_dict = await SessionCacheManager.get_instance().get_data(self.session_id)
        return session_dict[key] if key in session_dict else default_value

    async def set_session(self, key: str, value):
        """
        将键值对写入到 Session 中
        :param key:
        :param value:
        :return:
        """
        session_dict = await SessionCacheManager.get_instance().get_data(self.session_id)
        session_dict[key] = value
