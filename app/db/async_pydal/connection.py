

from aiomysql.connection import Connection
from .cursor import PyDALCursor
from .table import Table


class PyDALConnection:
    """
    数据库连接对象
    """

    def __init__(self, pydal, aiomysql_conn: Connection) -> None:
        super().__init__()
        self._pydal = pydal
        self._aiomysql_conn = aiomysql_conn

    @property
    def aiomysql_conn(self) -> Connection:
        return self._aiomysql_conn

    async def commit(self):
        """
        提交数据
        :return:
        """
        await self.aiomysql_conn.commit()

    def close(self):
        """
        关闭该连接
        :return:
        """
        self.aiomysql_conn.close()

    async def autocommit(self, mode: bool):
        """
        设置该连接为自动提交数据
        :param mode:
        :return:
        """
        await self.aiomysql_conn.autocommit(mode)

    def autocommit_mode(self):
        """
        用于确定当前是否为自动提交状态
        :return:
        """
        return self.aiomysql_conn.autocommit_mode

    async def cursor(self) -> PyDALCursor:
        """
        Cursor对象用于操作数据库
        :return:
        """
        return PyDALCursor(
            self._pydal,
            self,
            await self.aiomysql_conn.cursor()
        )
