from cms4py.cache.base_cache_manager import BaseCacheManager
from cms4py.cache.base_cache_manager import CachedDataWrapper
from cms4py.utils import aiofile
import importlib, config, os
from cms4py.utils.log import Cms4pyLog


class ModulesCacheManager(BaseCacheManager):
    __instance = None

    @staticmethod
    def get_instance() -> "ModulesCacheManager":
        if not ModulesCacheManager.__instance:
            ModulesCacheManager.__instance = ModulesCacheManager()
        return ModulesCacheManager.__instance

    def file_name_from_module_name(self, module_name):
        """
        将模块名转为文件路径
        :param module_name:
        :return:
        """
        file_path_tokens = module_name.split(".")
        return os.path.join(
            config.SERVER_ROOT,
            file_path_tokens[0],
            file_path_tokens[1],
            f"{file_path_tokens[2]}.py"
        )

    async def wrap_data(self, key) -> CachedDataWrapper:
        m = None
        t = 0
        try:
            # 导入模块
            m = importlib.import_module(key)
            m_file = self.file_name_from_module_name(key)
            # 获取文件时间戳
            t = await aiofile.getmtime(m_file)
        except ModuleNotFoundError:
            Cms4pyLog.get_instance().debug(f"Module {key} not found")
        return CachedDataWrapper(m, t) if m else None

    async def will_reload(self, wrapper: CachedDataWrapper, key: str) -> bool:
        return_value = False
        if key in self.cache_map:
            m_file = self.file_name_from_module_name(key)
            # 如果已缓存的文件时间戳和现有文件时间戳不一致，则重新加载模块
            if await aiofile.exists(m_file) and \
                    await aiofile.isfile(m_file) and \
                    (await aiofile.getmtime(m_file)) != wrapper.timestamp:
                importlib.reload(wrapper.data)
                return_value = True
        else:
            return_value = True
        return return_value
