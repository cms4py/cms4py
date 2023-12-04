from typing import Any

from cms4py.cache_managers import ObjectCacheManager
from cms4py.session.ISessageStorage import ISessionStorage


class LocalMemorySessionStorage(ISessionStorage):

    def __init__(self):
        super().__init__()
        self._cache = ObjectCacheManager()

    async def get_session(self, session_id: str) -> dict:
        return await self._cache.get_data(session_id)

    async def get_session_field(self, session_id: str, field: str, default_value=None):
        session_dict = await self.get_session(session_id)
        return session_dict[field] if field in session_dict else default_value

    async def set_session_field(self, session_id: str, field: str, value):
        session_dict = await self.get_session(session_id)
        session_dict[field] = value
