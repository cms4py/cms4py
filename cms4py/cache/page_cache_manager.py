

from cms4py.cache.base_cache_manager import BaseCacheManager
from cms4py.cache.base_cache_manager import CachedDataWrapper
import datetime


class PageCacheManager(BaseCacheManager):
    __instance = None

    @staticmethod
    def get_instance():
        if not PageCacheManager.__instance:
            PageCacheManager.__instance = PageCacheManager()
        return PageCacheManager.__instance

    async def wrap_data(self, key) -> CachedDataWrapper:
        # 由于包装数据功能自定义程度较高，在该类内部难以获得所有必要数据，
        # 所以该函数功能将由回调函数实现
        raise NotImplementedError()

    async def will_reload(self, wrapper: CachedDataWrapper, key: str) -> bool:
        # 当缓存的数据过期时重新加载数据
        return datetime.datetime.now().timestamp() > wrapper.timestamp
