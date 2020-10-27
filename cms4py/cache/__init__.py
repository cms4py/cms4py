

from cms4py.cache.base_cache_manager import CachedDataWrapper
from cms4py.cache.base_cache_manager import BaseCacheManager
from cms4py.cache.modules_cache_manager import ModulesCacheManager
from cms4py.cache.page_cache_manager import PageCacheManager
from cms4py.cache.session_cache_manager import SessionCacheManager

from cms4py.utils.log import Cms4pyLog
import datetime


def cache(expire=3600, key=None):
    """
    为期望被缓存的页面添加该装饰器
    :param expire: 缓存过期时长，以秒为单位
    :param key: 缓存键
    :return:
    """

    def wrapper(target):

        async def inner(*args):
            argc = len(args)
            # 如果参数个数为2个，则目标action是函数
            if argc == 2:
                req = args[0]
                res = args[1]
            # 如果参数个数为2个，则目标action是类实例
            elif argc == 3:
                req = args[1]
                res = args[2]
            else:
                raise TypeError("Require 2 or 3 arguments")

            _key = key
            # 如果没有指定键，将使用 uri 作为缓存键
            if not _key:
                _key = req.uri

                # 移动端单独缓存
                if req.is_mobile():
                    _key += ",mobile"

            async def wrap_data_callback(cache_key) -> CachedDataWrapper:
                await target(*args)

                Cms4pyLog.get_instance().debug(f"Cache page {cache_key}")
                return CachedDataWrapper(
                    res.body,
                    # 记录缓存过期时间，便于对比
                    datetime.datetime.now().timestamp() + expire
                )

            cached_data = await PageCacheManager.get_instance().get_data(
                _key, wrap_data_callback
            )
            if not res.body_sent:
                await res.end(cached_data)

        return inner

    return wrapper
