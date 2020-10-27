

from app.db.async_pydal.dal import AsyncDAL
from pydal import Field


class Db:
    __instance = None

    @staticmethod
    async def get_instance() -> "Db":
        if not Db.__instance:
            Db.__instance = Db()
            await Db.__instance._async_init()
        return Db.__instance

    async def _async_init(self):
        self._async_pydal = await AsyncDAL.create(
            "127.0.0.1", "root", "rootpw", "mydb"
        )
        self._async_pydal.define_table(
            "student",
            Field("name"),
            Field("age")
        )
        pass

    @property
    def async_pydal(self):
        return self._async_pydal

    pass
