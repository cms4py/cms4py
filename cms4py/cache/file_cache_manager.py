

from cms4py.cache.base_cache_manager import BaseCacheManager
from cms4py.cache.base_cache_manager import CachedDataWrapper
from cms4py.utils import aiofile


class FileCacheManager(BaseCacheManager):
    __instance = None

    @staticmethod
    def get_instance() -> "FileCacheManager":
        if not FileCacheManager.__instance:
            FileCacheManager.__instance = FileCacheManager()
        return FileCacheManager.__instance

    def __init__(self) -> None:
        super().__init__()

    async def wrap_data(self, key) -> CachedDataWrapper:
        wrapper = None
        if await aiofile.exists(key) and await aiofile.isfile(key):
            content = await aiofile.read_file(key)
            # 将文件与对应的修改时间包装成缓存数据包装器
            wrapper = CachedDataWrapper(content, await aiofile.getmtime(key))
        return wrapper

    async def will_reload(self, wrapper: CachedDataWrapper, key: str) -> bool:
        """
        如果文件已修改，则重新加载文件
        :param wrapper: 已缓存的文件数据包装器
        :param key: 文件路径
        :return:
        """
        return await aiofile.exists(
            key
        ) and await aiofile.isfile(
            key
        ) and await aiofile.getmtime(
            key
        ) != wrapper.timestamp
