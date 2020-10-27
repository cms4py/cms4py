

from aiomysql.cursors import Cursor
from .table import Table
from .query import AsyncQuery


class PyDALCursor:
    def __init__(self, pydal, pydal_connection, aiomysql_cursor: Cursor) -> None:
        super().__init__()
        self._aiomysql_cursor = aiomysql_cursor
        self._pydal = pydal
        self._pydal_connection = pydal_connection
        self._table_map = {}

    @property
    def aiomysql_cursor(self) -> Cursor:
        return self._aiomysql_cursor

    @property
    def pydal_connection(self):
        return self._pydal_connection

    @property
    def description(self):
        """
        获取描述信息
        :return:
        """
        return self._aiomysql_cursor.description

    async def execute(self, sql, args=None):
        """
        以异步方式执行一条SQL语句
        :param sql: SQL语句
        :param args: 与SQL语句对应的参数
        :return:
        """
        await self.aiomysql_cursor.execute(sql, args)

    async def executemany(self, sql, args=None):
        await self.aiomysql_cursor.executemany(sql, args)

    async def fetchall(self):
        """
        获取执行SQL后得到的所有结果数据
        :return:
        """
        return await self.aiomysql_cursor.fetchall()

    async def fetchone(self):
        """
        获取一条数据
        :return:
        """
        return await self.aiomysql_cursor.fetchone()

    async def fetchmany(self, size=None):
        return await self.aiomysql_cursor.fetchmany(size)

    async def close(self):
        """
        关闭该Cursor对象
        :return:
        """
        await self.aiomysql_cursor.close()

    @property
    def lastrowid(self):
        return self.aiomysql_cursor.lastrowid

    @property
    def rowcount(self) -> int:
        """
        获取SQL语句影响的行数
        :return:
        """
        return self.aiomysql_cursor.rowcount

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __getattr__(self, item):
        """
        重载获取成员的运算符，用于封装对pyDAL的操作
        :param item:
        :return:
        """
        pydal_table = self._pydal.__getattr__(item)
        if pydal_table in self._table_map:
            async_table = self._table_map[pydal_table]
        else:
            async_table = Table(self._pydal, self, pydal_table)
            self._table_map[pydal_table] = async_table
        return async_table

    def __call__(self, *args) -> AsyncQuery:
        """
        在pyDAL中，db()函数会生成语句，重载该函数调用操作
        用于封装对pyDAL对象的调用
        :param args:
        :return:
        """
        return AsyncQuery(self, self._pydal(*args))
