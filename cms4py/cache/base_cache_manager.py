


class CachedDataWrapper:
    """
    该类用于包装缓存的数据
    """

    def __init__(self, data, timestamp) -> None:
        super().__init__()
        # 记录数据缓存的时间戳
        self.timestamp = timestamp
        # 记录缓存的数据
        self.data = data


class BaseCacheManager:
    """
    缓存管理器抽象基类，该类仅实现缓存管理功能，至于何时
    更新缓存、缓存什么数据，交由子类实现
    """

    def __init__(self) -> None:
        super().__init__()
        # 建立一个字典用于缓存数据
        self._cache_map = {}
        # 实现包装数据的回调函数
        self._wrap_data_callback = None
        # 实现确定何时重新缓存数据的回调函数
        self._will_reload_callback = None

    async def wrap_data(self, key) -> CachedDataWrapper:
        """
        创建包装的数据，返回值将由缓存机制进行缓存，该函数应由子
        类实现
        :param key:
        :return:
        """
        raise NotImplementedError()

    async def retrieve_cache_data(self, key):
        """
        根据键名直接从缓存中取数据
        :param key:
        :return:
        """
        if not self._wrap_data_callback:
            self._wrap_data_callback = self.wrap_data

        wrapper = await self._wrap_data_callback(key)
        if wrapper:
            self._cache_map[key] = wrapper
        return wrapper.data if wrapper else None

    async def get_data(
            self, key,
            wrap_data_callback=None, will_reload_callback=None
    ):
        """
        获取数据。该函数将自动根据需要创建新数据或返回缓存的数据
        :param key: 缓存键
        :param wrap_data_callback: 包装数据的回调函数，置空将调用
                                    self.wrap_data 函数以创建数据
        :param will_reload_callback: 提示是否创建新数据的回调函数，置空
                                    将使用self.will_reload进行回调
        :return:
        """

        self._wrap_data_callback = wrap_data_callback or self.wrap_data
        self._will_reload_callback = will_reload_callback or self.will_reload

        if key in self._cache_map:
            wrapper: CachedDataWrapper = self._cache_map[key]
            result = wrapper.data
            if await self._will_reload_callback(wrapper, key):
                result = await self.retrieve_cache_data(key)
        else:
            result = await self.retrieve_cache_data(key)
        return result

    async def will_reload(self, wrapper: CachedDataWrapper, key: str) -> bool:
        """
        子类重写该函数以指示不否需要创建新数据
        :param wrapper:
        :param key:
        :return:
        """
        raise NotImplementedError()

    def clear(self):
        """
        清除所有缓存
        :return:
        """
        self._cache_map = {}

    @property
    def cache_map(self):
        return self._cache_map
