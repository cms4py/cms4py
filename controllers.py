import datetime

from cms4py import cache_managers
import traceback

from cms4py.helpers.log_helper import Cms4pyLog
from cms4py.http import http


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
        try:
            await self._execute(request, response)
        except:
            print(traceback.format_exc())
        await self._post_execute(request, response)


def cache(expire=3600, key=None):
    """
    :param expire: In seconds
    :param key:
    :return:
    """

    def wrapper(f):

        async def inner(*args):
            len_of_args = len(args)
            if len_of_args == 3:
                req = args[1]
                res = args[2]
            elif len_of_args == 2:
                req = args[0]
                res = args[1]
            else:
                raise Exception("Wrong number of arguments")

            _key = key
            if not _key:
                _key = req.uri
                if req.is_mobile():
                    _key += ",mobile"
                if req.runs_in_wx():
                    _key += ",wx"

            async def wrap_data_callback(cache_key) -> cache_managers.CachedDataWrapper:
                await f(*args)
                Cms4pyLog.get_instance().debug(f"Cache page {cache_key}")
                return cache_managers.CachedDataWrapper(res.body, datetime.datetime.utcnow().timestamp() + expire)

            cached_data = await cache_managers.PageCacheManager.get_instance().get_data(_key, wrap_data_callback)
            if not res.body_sent:
                await res.end(cached_data)

        return inner

    return wrapper
