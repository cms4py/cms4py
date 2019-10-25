import inspect
import datetime


class CachedContentWrapper:

    def __init__(self, content, expire=3600) -> None:
        super().__init__()
        self._content = content
        self._timestamp = datetime.datetime.now()
        self._expire = expire

    @property
    def content(self):
        return self._content

    def is_expired(self):
        return (datetime.datetime.now() - self._timestamp).total_seconds() > self._expire


class CacheManager:
    __instance = None

    @staticmethod
    def get_instance():
        if not CacheManager.__instance:
            CacheManager.__instance = CacheManager()
        return CacheManager.__instance

    def __init__(self) -> None:
        super().__init__()
        self._cache_map = {}

    def has_cache(self, key):
        return key in self._cache_map

    def get_cache(self, key):
        return self._cache_map[key]

    def set_cache(self, key, value):
        self._cache_map[key] = value

    def clear(self):
        self._cache_map.clear()


def cache(expire=3600):
    def outer(func):
        async def inner(context, *args, **kwargs):
            key = context.get_request_uri()
            cm = CacheManager.get_instance()
            if cm.has_cache(key):
                wrapper: CachedContentWrapper = cm.get_cache(key)
                if not wrapper.is_expired():
                    context.finish(wrapper.content)
                    return

            func_result = func(context, *args, **kwargs)
            if inspect.isawaitable(func_result):
                await func_result
            if context.result_html:
                cm.set_cache(key, CachedContentWrapper(context.result_html, expire))
            pass

        return inner

    return outer
