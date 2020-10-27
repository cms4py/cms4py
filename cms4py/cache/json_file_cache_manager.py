

from cms4py.cache.file_cache_manager import FileCacheManager
from cms4py.cache.base_cache_manager import CachedDataWrapper
from cms4py.utils.log import Cms4pyLog
import json


class JsonFileCacheManager(FileCacheManager):
    __instance = None

    @staticmethod
    def get_instance() -> "JsonFileCacheManager":
        if not JsonFileCacheManager.__instance:
            JsonFileCacheManager.__instance = JsonFileCacheManager()
        return JsonFileCacheManager.__instance

    async def wrap_data(self, key) -> CachedDataWrapper:
        wrapper = await super().wrap_data(key)
        if wrapper and wrapper.data:
            # 对数据进行重新包装，将文件内容换成 json 对象
            wrapper.data = json.loads(wrapper.data)
            Cms4pyLog.get_instance().debug(f"Load json file {key}")
        return wrapper
