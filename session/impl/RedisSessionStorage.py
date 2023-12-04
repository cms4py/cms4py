import json

from redis.asyncio import Redis

import config
from cms4py.session.ISessageStorage import ISessionStorage


class RedisSessionStorage(ISessionStorage):

    def __init__(self):
        super().__init__()
        self._redis = config.SESSION_STORAGE_REDIS

    @property
    def redis(self):
        return self._redis

    async def get_session(self, session_id: str) -> dict:
        data = await self.redis.hgetall(session_id)
        return_dict = {}
        for key in data:
            if isinstance(key, bytes):
                key_str = key.decode(config.GLOBAL_CHARSET)
            else:
                key_str = key
            return_dict[key_str] = json.loads(data[key])
        return return_dict

    async def get_session_field(self, session_id: str, field: str, default_value=None):
        result = await self.redis.hget(session_id, field)
        if result is None:
            return default_value
        return json.loads(result)

    async def set_session_field(self, session_id: str, field: str, value):
        return await self.redis.hset(session_id, field, json.dumps(value))
