import config
from cms4py.http.request import Request
from cms4py.utils import translator
from cms4py.template_engine import TemplateEngine


class Response:
    def __init__(self, request: Request, send):
        self._send = send
        # 该变量用于记录返回的 content_type 类型
        self._content_type = None
        # 该变量用于指示头部是否已发送
        self._header_sent = False
        # 该变量用户指示内容是否已发送
        self._body_sent = False
        self._body = b''
        # 记录Request对象
        self._request: Request = request

        # 返回的头部信息
        self._headers_map = {}

        # 指定默认的 content_type 是 text/html
        self.content_type = b'text/html'
        # 添加自定义的服务器名称信息
        self.add_header(b'server', config.SERVER_NAME)
        # 将 Session ID 写到 Cookie 中
        self.add_set_cookie(
            config.CMS4PY_SESSION_ID_KEY,
            self._request.session_id
        )

        # 用于存放语言表
        self._language_dict = None
        pass

    @property
    def send(self):
        """
        Get the asgi send function
        """
        return self._send

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
        """
        发送协议头
        :param status:
        :return:
        """
        await self._send({
            'type': 'http.response.start',
            'status': status,
            'headers': self._get_headers()
        })
        self._header_sent = True

    async def write(self, data: bytes):
        """
        向浏览器端写数据，但不关闭连接
        :param data:
        :return:
        """
        if not self._header_sent:
            await self.send_header()
        await self._send({
            "type": "http.response.body",
            "body": data,
            # 如果指定 more_body 为 True，则意味着还有待发
            # 数据，连接需要被继续保持
            'more_body': True
        })

    async def end(self, data: bytes):
        """
        该函数用于发送数据之后关闭连接
        :param data:
        :return:
        """
        if self._body_sent:
            return
        if not self._header_sent:
            await self.send_header()
        await self._send({
            "type": "http.response.body",
            "body": data,
            'more_body': False
        })
        self._body = data
        self._body_sent = True

    def add_set_cookie(
            self,
            name: bytes,
            value: bytes,
            max_age: int = 604800,
            path: bytes = b'/'
    ):
        """
        添加设置 Cookie 的协议头
        :param name: Cookie的名称
        :param value: Cookie的值
        :param max_age: Cookie的有效期
        :param path: 为该Cookie指定路径
        :return:
        """

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

    async def _load_language_dict(self):
        """
        加载语言表
        :return:
        """
        if not self._language_dict:
            self._language_dict = await translator \
                .get_language_dict(self._request.language)

    def translate(self, words):
        """
        在不使用异步IO的情况下进行翻译
        :param words:
        :return:
        """
        if self._language_dict and words in self._language_dict:
            words = self._language_dict[words]
        return words

    async def render_string(self, view: str, **kwargs) -> bytes:
        """
        渲染一段字符串
        :param view: 将被渲染的模板字符串
        :param kwargs: 向模板渲染过程传参数
        :return: 被渲染之后的数据
        """

        # 该参数用于在模板渲染过程中访问配置信息
        kwargs['config'] = config
        # 该参数用于在模板渲染过程中访问 Response 对象
        kwargs['response'] = self
        # 该参数用于在模板渲染过程中访问 Request 对象
        kwargs['request'] = self._request
        # 该参数用于在模板渲染过程中访问翻译工具对象
        kwargs["_"] = self.translate
        # 该参数用于在模板渲染过程中访问翻译工具对象
        kwargs["T"] = self.translate
        # 该参数用于在模板渲染过程中访问 Session
        kwargs['session'] = await self._request.session()
        data = await TemplateEngine.get_instance().render(
            view, **kwargs
        )
        return data

    async def render(self, view: str, **kwargs):
        """
        渲染模板文件，并返回给浏览器端
        :param view:
        :param kwargs:
        :return:
        """
        if self._body_sent:
            return
        await self.end(
            await self.render_string(view, **kwargs)
        )

    async def redirect(self, target: str, primary=False):
        """
        页面重定向
        :param target: 目标地址
        :param primary: 是否为永久重定向
        :return:
        """
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
            b"</html>"
        )
        pass
