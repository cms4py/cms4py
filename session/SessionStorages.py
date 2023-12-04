import config
from cms4py.session import session_storages
from cms4py.session.ISessageStorage import ISessionStorage
from cms4py.session.impl.LocalMemorySessionStorage import LocalMemorySessionStorage
from cms4py.session.impl.RedisSessionStorage import RedisSessionStorage


class SessionStorages:
    __sessionStorages = {
        session_storages.REDIS: RedisSessionStorage,
        session_storages.LOCAL_MEMORY: LocalMemorySessionStorage
    }

    __current = None

    @staticmethod
    def get_current() -> ISessionStorage:
        if SessionStorages.__current is None:
            if config.SESSION_STORAGE not in SessionStorages.__sessionStorages:
                raise Exception(
                    f"Session storage name must be {session_storages.REDIS} or {session_storages.LOCAL_MEMORY}"
                )
            clazz = SessionStorages.__sessionStorages[config.SESSION_STORAGE]
            SessionStorages.__current = clazz()
        return SessionStorages.__current
