
from cms4py.cache import cache


async def index(req, res):
    await res.end(b"Home page")
    pass


class hello:
    """
    如果 action 是类，则需要使用魔术函数 __call__ 重载函数调用
    运算符以接受调用操作
    """

    async def __call__(self, req, res):
        await res.end(b"Hello cms4py")


@cache(expire=5)
async def cached_page(req, res):
    await res.end(b"Cached page")


async def get_args(req, res):
    arg0 = req.arg(0)
    await res.write(b"Arg0 is ")
    await res.end(arg0.encode("utf-8") if arg0 else b"None")


async def login_handler(req, res):
    # 用于获取 URL 中的参数
    req.get_query_var(b"name")
    # 用于获取消息体中的参数
    req.get_body_var(b"name")
    # 自动从 URL 中和消息体中获取参数
    req.get_var(b"name")

    await res.end(b"Hello")
