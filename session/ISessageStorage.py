import abc
from abc import abstractmethod


class ISessionStorage(metaclass=abc.ABCMeta):

    @abstractmethod
    async def get_session(self, session_id: str) -> dict:
        pass

    @abstractmethod
    async def get_session_field(self, session_id: str, field: str, default_value=None):
        pass

    @abstractmethod
    async def set_session_field(self, session_id: str, field: str, value):
        pass

    async def set_current_user(self, session_id: str, user):
        await self.set_session_field(session_id, "current_user", user)

    async def get_current_user(self, session_id: str):
        return await self.get_session_field(session_id, "current_user")
