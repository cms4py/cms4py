import json

from .helpers import file_helper
from cms4py.helpers.log_helper import Cms4pyLog


class CachedDataWrapper:
    def __init__(self, data, timestamp) -> None:
        super().__init__()
        self.timestamp = timestamp
        self.data = data


class BaseCacheManager:

    def __init__(self) -> None:
        super().__init__()
        self._cache_map = {}

    async def wrap_data(self, key) -> CachedDataWrapper:
        raise NotImplementedError()

    async def cache_data(self, key):
        wrapper = await self.wrap_data(key)
        if wrapper:
            self._cache_map[key] = wrapper
        return wrapper.data if wrapper else None

    async def get_data(self, key):
        if key in self._cache_map:
            wrapper: CachedDataWrapper = self._cache_map[key]
            result = wrapper.data
            if await self.will_reload(wrapper, key):
                result = await self.cache_data(key)
        else:
            result = await self.cache_data(key)
        return result

    async def will_reload(self, wrapper: CachedDataWrapper, key: str) -> bool:
        raise NotImplementedError()


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
        if await file_helper.file_exists(key) and await file_helper.isfile(key):
            content = await file_helper.read_file_async(key)
            wrapper = CachedDataWrapper(content, await file_helper.getmtime(key))
        return wrapper

    async def will_reload(self, wrapper: CachedDataWrapper, key: str) -> bool:
        return await file_helper.file_exists(key) and \
               await file_helper.isfile(key) and \
               await file_helper.getmtime(key) != wrapper.timestamp


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
            wrapper.data = json.loads(wrapper.data)
            Cms4pyLog.get_instance().debug(f"Load json file {key}")
        return wrapper


class PythonAstObjectCacheManager(FileCacheManager):
    __instance = None

    @staticmethod
    def get_instance() -> "PythonAstObjectCacheManager":
        if not PythonAstObjectCacheManager.__instance:
            PythonAstObjectCacheManager.__instance = PythonAstObjectCacheManager()
        return PythonAstObjectCacheManager.__instance

    async def wrap_data(self, key) -> CachedDataWrapper:
        wrapper = await super().wrap_data(key)
        if wrapper and wrapper.data:
            wrapper.data = compile(wrapper.data, key, "exec")
            Cms4pyLog.get_instance().debug(f"Compile source {key}")
        return wrapper
