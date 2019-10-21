from pydal import DAL
import config
from . import table_user, table_session, table_group, table_membership
from cms4py.aiomysql_pydal import AsyncDAL


class DbConnector:
    __instance = None

    @staticmethod
    def get_instance():
        if not DbConnector.__instance:
            DbConnector.__instance = DbConnector()
        return DbConnector.__instance

    def __init__(self) -> None:
        super().__init__()

    async def async_init(self):
        self._async_dal = await AsyncDAL.create(
            config.DB_HOST,
            config.DB_USER,
            config.DB_PASSWORD,
            config.DB_NAME,
            config.DB_PORT,
            config.DB_POOR_SIZE
        )
        table_session.define_table(self._async_dal)
        table_user.define_table(self._async_dal)
        table_group.define_table(self._async_dal)
        table_membership.define_table(self._async_dal)

    @property
    def async_dal(self):
        return self._async_dal
