
from cms4py.cache.base_cache_manager import BaseCacheManager
from cms4py.cache.page_cache_manager import CachedDataWrapper
import datetime


class SessionCacheManager(BaseCacheManager):
    __instance = None

    @staticmethod
    def get_instance():
        if not SessionCacheManager.__instance:
            SessionCacheManager.__instance = SessionCacheManager()
        return SessionCacheManager.__instance

    async def will_reload(
            self,
            wrapper: CachedDataWrapper,
            key: str
    ) -> bool:
        # TODO 设计 Session 过期机制
        return False

    async def wrap_data(self, key) -> CachedDataWrapper:
        return CachedDataWrapper(
            {}, datetime.datetime.now().timestamp()
        )

    async def set_current_user(self, session_id: bytes, user):
        """
        设置当前登录的用户
        :param session_id:
        :param user:
        :return:
        """
        session = await self.get_data(session_id)
        session['current_user'] = user

    async def get_current_user(self, session_id: bytes):
        """
        获取当前登录的用户
        :param session_id:
        :return:
        """
        session = await self.get_data(session_id)
        return session['current_user'] \
            if 'current_user' in session else None
